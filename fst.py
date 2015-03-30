# -*- coding: utf-8 -*-

import copy
from struct import pack, unpack
from collections import OrderedDict
import logging
import time

# bit flags to represent class of arcs
# refer to Apache Lucene FST's implementation
FLAG_FINAL_ARC = 1 << 0             # 1
FLAG_LAST_ARC = 1 << 1              # 2
FLAG_TARGET_NEXT = 1 << 2           # 4  TODO: not used. can be removed?
FLAG_STOP_NODE = 1 << 3             # 8  TODO: not used. can be removed?
FLAG_ARC_HAS_OUTPUT = 1 << 4        # 16
FLAG_ARC_HAS_FINAL_OUTPUT = 1 << 5  # 32

# all characters
CHARS = set()


class State:
    """
    State Class
    """
    def __init__(self, id=None):
        self.id = id
        self.final = False
        self.trans_map = {}
        self.final_output = set()

    def is_final(self):
        return self.final

    def set_final(self, final):
        self.final = final

    def transition(self, char):
        if char in self.trans_map:
            return self.trans_map[char]['state']
        else:
            return None

    def set_transition(self, char, state):
        self.trans_map[char] = {'state': state,
                                'output': bytes() if char not in self.trans_map else self.trans_map[char]['output']}

    def state_output(self):
        return self.final_output

    def set_state_output(self, output):
        self.final_output = set([bytes(e) for e in output])

    def clear_state_output(self):
        self.final_output = set()

    def output(self, char):
        if char in self.trans_map:
            return self.trans_map[char]['output']
        else:
            return bytes()

    def set_output(self, char, out):
        if char in self.trans_map:
            self.trans_map[char]['output'] = bytes(out)

    def clear(self):
        self.final = False
        self.trans_map = {}
        self.final_output = set()

    def __eq__(self, other):
        if other is None or not isinstance(other, State):
            return False
        else:
            return \
                self.final == other.final and \
                self.trans_map == other.trans_map and \
                self.final_output == other.final_output

    def __hash__(self):
        return hash(str(self.final) + str(self.trans_map) + str(self.final_output))


def copy_state(src, id):
    state = State(id)
    state.final = src.final
    for c, t in src.trans_map.items():
        state.set_transition(c, copy.copy(t['state']))
        state.set_output(c, t['output'])
    state.final_output = copy.copy(src.final_output)
    return state


class FST:
    """
    FST (final dictionary) class
    """
    def __init__(self):
        # must preserve inserting order
        self.dictionary = OrderedDict()

    def size(self):
        return len(self.dictionary)

    def member(self, state):
        return self.dictionary.get(hash(state))

    def insert(self, state):
        self.dictionary[hash(state)] = state

    def print_dictionary(self):
        for s in self.dictionary.values():
            for (c, v) in s.trans_map.items():
                print(s.id, c, v['state'].id, v['output'], sep='\t')
            if s.is_final():
                print(s.id, 'final', s.final_output, sep='\t')


# naive implementation for building fst
# http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698
def create_minimum_transducer(inputs):
    _start = time.time()
    _last_printed = 0
    inputs_size = len(inputs)
    logging.info('input size: %d' % inputs_size)

    fstDict = FST()
    buffer = []
    buffer.append(State())  # insert 'initial' state

    # previous word
    prev_word = bytes()

    def find_minimized(state):
        # if an equivalent state exists in the dictionary, use that
        s = fstDict.member(state)
        if s is None:
            # if no equivalent state exists, insert new one and return it
            s = copy_state(state, fstDict.size())
            fstDict.insert(s)
        return s

    def prefix_len(s1, s2):
        # calculate max common prefix length for s1 and s2
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return i

    current_word = bytes()
    current_output = bytes()
    processed = 0
    # main loop
    for (current_word, current_output) in inputs:
        logging.debug('current word: ' + str(current_word))
        logging.debug('current_output: ' + str(current_output))

        assert(current_word >= prev_word)

        for c in current_word:
            CHARS.add(c)

        pref_len = prefix_len(prev_word, current_word)

        # expand buffer to current word length
        while len(buffer) <= len(current_word):
            buffer.append(State())

        # set state transitions
        for i in range(len(prev_word), pref_len, -1):
            buffer[i - 1].set_transition(prev_word[i - 1], find_minimized(buffer[i]))
        for i in range(pref_len + 1, len(current_word) + 1):
            buffer[i].clear()
            buffer[i - 1].set_transition(current_word[i - 1], buffer[i])
        if current_word != prev_word:
            buffer[len(current_word)].set_final(True)
            buffer[len(current_word)].set_state_output(set([bytes()]))

        # set state outputs
        for j in range(1, pref_len + 1):
            # divide (j-1)th state's output to (common) prefix and suffix
            common_prefix = bytearray()
            output = buffer[j - 1].output(current_word[j - 1])
            k = 0
            while k < len(output) and k < len(current_output) and output[k] == current_output[k]:
                common_prefix += pack('B', output[k])
                k += 1
            word_suffix = output[len(common_prefix):]

            # re-set (j-1)'th state's output to prefix
            buffer[j - 1].set_output(current_word[j - 1], common_prefix)

            # re-set jth state's output to suffix or set final state output
            for c in CHARS:
                # TODO: optimize this
                if buffer[j].transition(c) is not None:
                    new_output = buffer[j].output(c) + word_suffix
                    buffer[j].set_output(c, new_output)
            # or, set final state output if it's a final state
            if buffer[j].is_final():
                tmp_set = set()
                for tmp_str in buffer[j].state_output():
                    tmp_set.add(tmp_str + word_suffix)
                buffer[j].set_state_output(tmp_set)

            # update current output (subtract prefix)
            current_output = current_output[len(common_prefix):]

        if current_word == prev_word:
            buffer[len(current_word)].state_output().add(current_output)
        else:
            buffer[pref_len].set_output(current_word[pref_len], current_output)

        # preserve current word for next loop
        prev_word = current_word

        # progress
        processed += 1
        _elapsed = round(time.time() - _start)
        if _elapsed % 30 == 0 and _elapsed > _last_printed:
            progress = processed / inputs_size * 100
            logging.info('elapsed=%dsec, progress: %f %%' % (_elapsed, progress))
            _last_printed = _elapsed

    # minimize the last word
    for i in range(len(current_word), 0, -1):
        buffer[i - 1].set_transition(prev_word[i - 1], find_minimized(buffer[i]))

    find_minimized(buffer[0])
    logging.info('num of state: %d' % fstDict.size())

    return fstDict


def compileFST(fst):
    """
    convert FST to byte array representing arcs
    """
    arcs = []
    address = {}
    cnt = 0
    pos = 0
    for s in fst.dictionary.values():
        for i, (c, v) in enumerate(sorted(s.trans_map.items(), reverse=True)):
            bary = bytearray()
            flag = 0
            output_size, output = 0, bytes()
            if i == 0:
                flag += FLAG_LAST_ARC
            if v['output']:
                flag += FLAG_ARC_HAS_OUTPUT
                output_size = len(v['output'])
                output = v['output']
            # encode flag, label, output_size, output, relative target address
            bary += pack('b', flag)
            bary += pack('B', c)
            if output_size > 0:
                bary += pack('i', output_size)
                bary += output
            next_addr = address.get(v['state'].id)
            assert next_addr is not None
            target = (pos + len(bary) + 4) - next_addr
            assert target > 0
            bary += pack('i', target)
            # add the arc represented in bytes
            arcs.append(bytes(bary))
            # address count up
            cnt += 1
            pos += len(bary)
        if s.is_final():
            bary = bytearray()
            # final state
            flag = FLAG_FINAL_ARC
            output_size, output = 0, bytes()
            if s.final_output and any(len(e) > 0 for e in s.final_output):
                # the arc has final output
                flag += FLAG_ARC_HAS_FINAL_OUTPUT
                output_size = sum(len(e) for e in s.final_output) + len(s.final_output) - 1
                output = b'\x1a'.join(s.final_output)
            if not s.trans_map:
                flag += FLAG_LAST_ARC
            # encode flag, output size, output
            bary += pack('b', flag)
            if output_size > 0:
                bary += pack('i', output_size)
                bary += output
            # add the arc represented in bytes
            arcs.append(bytes(bary))
            # address count up
            cnt += 1
            pos += len(bary)
        address[s.id] = pos

    logging.debug(address)
    logging.info('compiled arcs size: %d' % len(arcs))
    arcs.reverse()
    return b''.join(arcs)


class Arc:
    """
    Arc class
    """
    def __init__(self):
        self.flag = 0
        self.label = 0
        self.output = bytes()
        self.final_output = [b'']
        self.target = 0

    def __str__(self):
        return "flag=%d, label=%s, target=%d, output=%s, final_output=%s" \
               % (self.flag, self.label, self.target, str(self.output), str(self.final_output))


class Matcher:
    BUF_SIZE = 1024

    def __init__(self, dict_data=None, file=None):
        if dict_data:
            self.data = dict_data
        elif file:
            data = bytearray()
            with open(file, 'br') as f:
                buf = f.read(Matcher.BUF_SIZE)
                while buf:
                    data += buf
                    buf = f.read(Matcher.BUF_SIZE)
            self.data = bytes(data)

    def run(self, word):
        # logging.debug('word=' + str([c for c in word]))
        outputs = set()
        accept = False
        buf = bytearray()
        i = 0
        pos = 0
        while pos < len(self.data):
            arc, incr = self.next_arc(pos)
            if arc.flag & FLAG_FINAL_ARC:
                # accepted
                accept = True
                for out in arc.final_output:
                    outputs.add(bytes(buf + out))
                if arc.flag & FLAG_LAST_ARC or i >= len(word):
                    break
                pos += incr
            elif arc.flag & FLAG_LAST_ARC:
                if i >= len(word):
                    break
                if word[i] == arc.label:
                    buf += arc.output
                    i += 1
                    pos += arc.target
                else:
                    break
            else:
                if i >= len(word):
                    break
                if word[i] == arc.label:
                    buf += arc.output
                    i += 1
                    pos += arc.target
                else:
                    pos += incr
        return accept, outputs

    def next_arc(self, addr=0):
        assert addr >= 0
        # arc address
        pos = addr
        # create the arc
        arc = Arc()
        # read flag
        flag = unpack('b', self.data[pos:pos+1])[0]
        arc.flag = flag
        pos += 1
        if flag & FLAG_FINAL_ARC:
            if flag & FLAG_ARC_HAS_FINAL_OUTPUT:
                # read final outputs
                final_output_size = unpack('i', self.data[pos:pos+4])[0]
                pos += 4
                final_output = self.data[pos:pos+final_output_size]
                arc.final_output = final_output.split(b'\x1a')
                pos += final_output_size
        else:
            # read label
            label = unpack('B', self.data[pos:pos+1])[0]
            arc.label = label
            pos += 1
            if flag & FLAG_ARC_HAS_OUTPUT:
                # read output
                output_size = unpack('i', self.data[pos:pos+4])[0]
                pos += 4
                output = self.data[pos:pos+output_size]
                arc.output = output
                pos += output_size
            # read target's (relative) address
            target = unpack('i', self.data[pos:pos+4])[0]
            arc.target = target
            pos += 4
        incr = pos - addr
        # logging.debug(arc)
        return arc, incr



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    inputs1 = [
        ('apr'.encode('utf8'), '30'.encode('utf8')),
        ('aug'.encode('utf8'), '31'.encode('utf8')),
        ('dec'.encode('utf8'), '31'.encode('utf8')),
        ('feb'.encode('utf8'), '28'.encode('utf8')),
        ('feb'.encode('utf8'), '29'.encode('utf8')),
        ('jan'.encode('utf8'), '31'.encode('utf8')),
        ('jul'.encode('utf8'), '31'.encode('utf8')),
        ('jun'.encode('utf8'), '30'.encode('utf8'))
    ]
    dict = create_minimum_transducer(inputs1)
    data = compileFST(dict)

    m = Matcher(data)
    print(m.run('apr'.encode('utf8')))
    print(m.run('aug'.encode('utf8')))
    print(m.run('dec'.encode('utf8')))
    print(m.run('feb'.encode('utf8')))
    print(m.run('jan'.encode('utf8')))
    print(m.run('jul'.encode('utf8')))
    print(m.run('jun'.encode('utf8')))
    print(m.run('mar'.encode('utf8')))

    print("\n\n")


    inputs2 = [
        ('さくら'.encode('utf8'), '10'.encode('utf8')),
        ('さくらんぼ'.encode('utf8'), '11'.encode('utf8')),
        ('すもも'.encode('utf8'), '20'.encode('utf8')),
        ('なし'.encode('utf8'), '10'.encode('utf8')),
        ('もも'.encode('utf8'), '20'.encode('utf8')),
    ]
    dict = create_minimum_transducer(inputs2)
    #dict.print_dictionary()
    data = compileFST(dict)
    m = Matcher(data)
    print(m.run('さくら'.encode('utf8')))
    print(m.run('さくらんぼ'.encode('utf8')))
    print(m.run('すもも'.encode('utf8')))
    print(m.run('なし'.encode('utf8')))
    print(m.run('もも'.encode('utf8')))
