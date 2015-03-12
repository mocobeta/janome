import copy
from struct import pack, unpack
import logging

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
            return bytes(self.trans_map[char]['output'])
        else:
            return bytes()

    def set_output(self, char, out):
        if char in self.trans_map:
            self.trans_map[char]['output'] = bytes(out)

    def deepcopy(self, id):
        state = State(id)
        state.final = self.final
        state.trans_map = copy.deepcopy(self.trans_map)
        state.final_output = copy.deepcopy(self.final_output)
        return state

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


class FST:
    """
    FST (final dictionary) class
    """
    def __init__(self):
        self.dictionary = []

    def size(self):
        return len(self.dictionary)

    def member(self, state):
        for s in self.dictionary:
            if s == state:
                return s
        return None

    def insert(self, state):
        self.dictionary.append(state)

    def print_dictionary(self):
        for s in reversed(self.dictionary):
            for (c, v) in s.trans_map.items():
                print(s.id, c, v['state'].id, v['output'], sep='\t')
            if s.is_final():
                print(s.id, 'final', s.final_output, sep='\t')


# naive implementation for building fst
# http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698
def create_minimum_transducer(inputs):
    fstDict = FST()
    buffer = []
    buffer.append(State())  # insert 'initial' state

    # previous word
    prev_word = bytes()

    def find_minimized(state):
        # if an equal state exists in the dictionary, use that
        s = fstDict.member(state)
        if s is None:
            # if no equal state exists, insert new one ant return it
            s = state.deepcopy(fstDict.size())
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
    # main loop
    for (current_word, current_output) in inputs:
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
                common_prefix += pack('b', output[k])
                k += 1
            word_suffix = output[len(common_prefix):]

            # re-set (j-1)'th state's output to prefix
            buffer[j - 1].set_output(current_word[j - 1], common_prefix)

            # re-set jth state's output to suffix or set final state output
            for c in CHARS:
                # FIXME: terrible loop...
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

    # minimize the last word
    for i in range(len(current_word), 0, -1):
        buffer[i - 1].set_transition(prev_word[i - 1], find_minimized(buffer[i]))

    find_minimized(buffer[0])

    return fstDict


def compileFST(fst):
    """
    convert FST to byte array
    """
    arcs = []
    address = {}
    cnt = 0
    for s in fst.dictionary:
        # print(address)
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
            target = cnt - next_addr + 1
            assert target > 0
            bary += pack('i', target)
            # add the arc represented in bytes
            arcs.append(bytes(bary))
            # address count up
            cnt += 1
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
        address[s.id] = cnt
    arcs.reverse()
    return arcs


def save(file, arcs):
    with open(file, 'bw') as f:
        f.write(b''.join(arcs))
        f.flush()


class Arc:
    """
    Arc class
    """
    def __init__(self, addr):
        self.addr = addr
        self.flag = 0
        self.label = 0
        self.output = bytes()
        self.final_output = [b'']
        self.target = 0

    def __str__(self):
        return "addr=%d, flag=%d, label=%s, target=%d, output=%s, final_output=%s" \
               % (self.addr, self.flag, self.label, self.target, str(self.output), str(self.final_output))


def loadCompiledFST(file):
    data = bytearray()
    with open(file, 'br') as f:
        buf = f.read(1024)
        if buf:
            data += buf
    data = bytes(data)
    arcs = []
    while data:
        arc = Arc(len(arcs))
        flag, data = unpack('b', data[:1])[0], data[1:]
        arc.flag = flag
        if flag & FLAG_FINAL_ARC:
            if flag & FLAG_ARC_HAS_FINAL_OUTPUT:
                output_size, data = unpack('i', data[:4])[0], data[4:]
                output, data = data[:output_size].split(b'\x1a'), data[output_size:]
                arc.final_output = output
        else:
            label, data = unpack('B', data[:1])[0], data[1:]
            arc.label = label
            if flag & FLAG_ARC_HAS_OUTPUT:
                output_size, data = unpack('i', data[:4])[0], data[4:]
                output, data = data[:output_size], data[output_size:]
                arc.output = output
            target, data = unpack('i', data[:4])[0], data[4:]
            arc.target = target
        logging.debug(arc)
        arcs.append(arc)
    return arcs


class Matcher:
    def __init__(self, arcs):
        self.arcs = arcs

    def run(self, word):
        logging.debug('word=' + str([c for c in word]))
        outputs = set()
        accept = False
        buf = bytearray()
        i = 0
        cnt = 0
        while cnt < len(self.arcs):
            logging.debug(str(i) + ", " + str(cnt))
            arc = self.arcs[cnt]
            if arc.flag & FLAG_FINAL_ARC > 0:
                # accepted
                accept = True
                for out in arc.final_output:
                    outputs.add(bytes(buf + out))
                if arc.flag & FLAG_LAST_ARC:
                    break
                cnt += 1
            elif arc.flag & FLAG_LAST_ARC:
                if i >= len(word):
                    break
                if word[i] == arc.label:
                    buf += arc.output
                    i += 1
                    cnt += arc.target
                else:
                    break
            else:
                if i >= len(word):
                    break
                if word[i] == arc.label:
                    buf += arc.output
                    i += 1
                    cnt += arc.target
                else:
                    cnt += 1
        return accept, outputs


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    inputs1 = [
        ('apr'.encode('utf-8'), '30'.encode('utf-8')),
        ('aug'.encode('utf-8'), '31'.encode('utf-8')),
        ('dec'.encode('utf-8'), '31'.encode('utf-8')),
        ('feb'.encode('utf-8'), '28'.encode('utf-8')),
        ('feb'.encode('utf-8'), '29'.encode('utf-8')),
        ('jan'.encode('utf-8'), '31'.encode('utf-8')),
        ('jul'.encode('utf-8'), '31'.encode('utf-8')),
        ('jun'.encode('utf-8'), '30'.encode('utf-8'))
    ]
    dict = create_minimum_transducer(inputs1)
    #dict.print_dictionary()
    arcs = compileFST(dict)
    save('dict1.dat', arcs)
    arcs = loadCompiledFST('dict1.dat')
    m = Matcher(arcs)
    print(m.run('apr'.encode('utf-8')))
    print(m.run('aug'.encode('utf-8')))
    print(m.run('dec'.encode('utf-8')))
    print(m.run('feb'.encode('utf-8')))
    print(m.run('jan'.encode('utf-8')))
    print(m.run('jul'.encode('utf-8')))
    print(m.run('jun'.encode('utf-8')))

    print("\n\n")

    inputs2 = [
        ('さくら'.encode('utf-8'), '10'.encode('utf-8')),
        ('さくらんぼ'.encode('utf-8'), '11'.encode('utf-8')),
        ('すもも'.encode('utf-8'), '20'.encode('utf-8')),
        ('なし'.encode('utf-8'), '10'.encode('utf-8')),
        ('もも'.encode('utf-8'), '20'.encode('utf-8')),
    ]
    dict = create_minimum_transducer(inputs2)
    #dict.print_dictionary()
    arcs = compileFST(dict)
    save('dict2.dat', arcs)
    arcs = loadCompiledFST('dict2.dat')
    m = Matcher(arcs)
    print(m.run('さくら'.encode('utf-8')))
    print(m.run('さくらんぼ'.encode('utf-8')))
    print(m.run('すもも'.encode('utf-8')))
    print(m.run('なし'.encode('utf-8')))
    print(m.run('もも'.encode('utf-8')))
