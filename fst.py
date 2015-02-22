import copy
import re
from enum import Enum


class State:
    """
    State Class
    """
    def __init__(self, id=''):
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
                                'output': '' if char not in self.trans_map else self.trans_map[char]['output']}

    def state_output(self):
        return self.final_output

    def set_state_output(self, output):
        self.final_output = output

    def add_state_output(self, output):
        self.final_output.add(output)

    def clear_state_output(self):
        self.final_output = set()

    def output(self, char):
        if char in self.trans_map:
            return self.trans_map[char]['output']
        else:
            return ''

    def set_output(self, char, str):
        if char in self.trans_map:
            self.trans_map[char]['output'] = str

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

# all characters
CHARS = set()


# naive implementation for building fst
# http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.24.3698
def create_minimum_transducer(inputs):
    fstDict = FST()
    buffer = []
    buffer.append(State())  # insert 'initial' state

    # previous word
    prev_word = ''

    def find_minimized(state):
        # if an equal state exists in the dictionary, use that
        s = fstDict.member(state)
        if s is None:
            # if no equal state exists, insert new one ant return it
            s = state.deepcopy("S" + str(fstDict.size()))
            fstDict.insert(s)
        return s

    def prefix_len(s1, s2):
        # calculate max common prefix length for s1 and s2
        i = 0
        while i < len(s1) and i < len(s2) and s1[i] == s2[i]:
            i += 1
        return i

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
            buffer[len(current_word)].set_state_output(set(['']))

        # set state outputs
        for j in range(1, pref_len + 1):
            # divide (j-1)th state's output to (common) prefix and suffix
            common_prefix = ''
            output = buffer[j - 1].output(current_word[j - 1])
            k = 0
            while k < len(output) and k < len(current_output) and output[k] == current_output[k]:
                common_prefix += output[k]
                k += 1
            word_suffix = re.sub("^" + common_prefix, "", output)

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
            current_output = re.sub("^" + common_prefix, "", current_output)

        if current_word == prev_word:
            buffer[len(current_word)].set_state_output(buffer[len(current_word)].state_output() | set(current_output))
        else:
            buffer[pref_len].set_output(current_word[pref_len], current_output)

        # preserve current word for next loop
        prev_word = current_word

    # minimize the last word
    for i in range(len(current_word), 0, -1):
        buffer[i - 1].set_transition(prev_word[i - 1], find_minimized(buffer[i]))

    find_minimized(buffer[0])

    return fstDict


class OP(Enum):
    MINC = 1  # Match or INCrement
    MBRK = 2  # Match or BReaK
    AINC = 3  # Accept and INCrement
    ACCP = 5  # ACCePt


class INST:
    def __init__(self, num, op, ch=None, jump=None, output=None):
        self.num = num
        self.op = op
        self.ch = ch
        self.jump = jump
        self.output = output

    def __str__(self):
        return '%d\t%s\t%s\t%s\t%s' % (
            self.num,
            self.op.name,
            self.ch if self.ch else '',
            str(self.jump) if self.jump else '',
            self.output if self.output else ''
        )


def fst2instructions(fst):
    arcs = []
    state_range = {}
    for s in reversed(fst.dictionary):
        state_range[s.id] = {'first': len(arcs), 'last': len(arcs)}
        if s.is_final():
            arc = {'state': s, 'ch': None, 'next': None, 'output': s.final_output}
            arcs.append(arc)
            state_range[s.id]['last'] += 1
        for (c, v) in s.trans_map.items():
            arc = {'state': s, 'ch': c, 'next': v['state'], 'output': v['output'] if v['output'] else ''}
            arcs.append(arc)
        state_range[s.id]['last'] += len(s.trans_map) - 1

    instructions = []
    for (i, arc) in enumerate(arcs):
        num = i
        ch = arc['ch']
        jump = state_range[arc['next'].id]['first'] - i if arc['next'] else None
        output = arc['output'] if arc['output'] else None
        op = None
        if arc['state'].is_final():
            if not arc['state'].trans_map:
                op = OP.ACCP
            elif num != state_range[arc['state'].id]['last']:
                op = OP.AINC
            else:
                op = OP.MBRK
        else:
            if num != state_range[arc['state'].id]['last']:
                op = OP.MINC
            else:
                op = OP.MBRK

        instructions.append(INST(num, op, ch, jump, output))

    return instructions


class VM:
    def __init__(self, instructions):
        self.insts = instructions

    def run(self, word):
        outputs = set()
        accept = False
        buf = ''
        i = 0
        cnt = 0
        while cnt < len(self.insts):
            #print(str(cnt), buf)
            inst = self.insts[cnt]
            if inst.op == OP.MINC:
                if i >= len(word):
                    break
                if word[i] == inst.ch:
                    if inst.output:
                        buf += inst.output
                    i += 1
                    cnt += inst.jump
                else:
                    cnt += 1
            elif inst.op == OP.MBRK:
                if i >= len(word):
                    break
                if word[i] == inst.ch:
                    if inst.output:
                        buf += inst.output
                    i += 1
                    cnt += inst.jump
                else:
                    break
            elif inst.op == OP.AINC:
                for out in inst.output:
                    outputs.add(buf + out)
                    accept = True
                cnt += 1
            elif inst.op == OP.ACCP:
                for out in inst.output:
                    outputs.add(buf + out)
                    accept = True
                break
            else:
                break
        return accept, outputs


if __name__ == '__main__':
    inputs1 = [
        ('apr', '30'),
        ('aug', '31'),
        ('dec', '31'),
        ('feb', '28'),
        ('feb', '29'),
        ('jan', '31'),
        ('jul', '31'),
        ('jun', '30')
    ]
    print('-- state transitions --')
    dict = create_minimum_transducer(inputs1)
    dict.print_dictionary()
    print('-- instructions --')
    insts = fst2instructions(dict)
    for inst in insts:
        print(inst)

    print("\n\n")

    inputs2 = [
        ('さくら', '10'),
        ('さくらんぼ', '11'),
        ('すもも', '20'),
        ('なし', '10'),
        ('もも', '20'),
    ]
    print('-- state transitions --')
    dict = create_minimum_transducer(inputs2)
    dict.print_dictionary()
    print('-- instructions --')
    insts = fst2instructions(dict)
    for inst in insts:
        print(inst)
