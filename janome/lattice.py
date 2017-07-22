# -*- coding: utf-8 -*-

# Copyright 2015 moco_beta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class NodeType:
    SYS_DICT = "SYS_DICT"
    USER_DICT = "USER_DICT"
    UNKNOWN = "UNKNOWN"


class BaseNode(object):
    """
    Base node class
    """
    def __init__(self):
        # position in the lattice of this node
        self.pos = 0
        # index of this node
        self.index = 0
        # left context ID of this node
        self.left_id = 0
        # right context ID of this node
        self.right_id = 0
        # cost of this node
        self.cost = 0
        # minimum cost to this node from BOS
        self.min_cost = int(pow(2,31)-1)
        # position and index info for Lattice#backward() method
        self.back_pos = -1
        self.back_index = -1
        # node type
        self.node_type = NodeType.SYS_DICT


class Node(BaseNode):
    """
    Node class
    """
    __slots__ = [
        'surface', 'left_id', 'right_id', 'cost'
        'part_of_speech', 'infl_type', 'infl_form',
        'base_form', 'reading', 'phonetic', 'node_type'
    ]

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        super(Node, self).__init__()
        surface, left_id, right_id, cost, part_of_speech, infl_type, infl_form, base_form, reading, phonetic = dict_entry
        self.surface = surface
        self.left_id = left_id
        self.right_id = right_id
        self.cost = cost
        self.part_of_speech = part_of_speech
        self.infl_type = infl_type
        self.infl_form = infl_form
        self.base_form = base_form
        self.reading = reading
        self.phonetic = phonetic
        self.node_type = node_type

    def __str__(self):
        return "(%s,%s,%s,%d,%s,%s,%s,%s,%s,%s) [back_pos=%d,back_index=%d]" % \
               (self.surface, self.left_id, self.right_id, self.cost, self.part_of_speech,
                self.infl_type, self.infl_form, self.base_form, self.reading, self.phonetic,
                self.back_pos, self.back_index)


class SurfaceNode(BaseNode):
    """
    Node class with surface form only.
    """
    __slots__ = ['surface']

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        super(SurfaceNode, self).__init__()
        self.num = dict_entry[0]
        self.surface = dict_entry[1]
        self.left_id = dict_entry[2]
        self.right_id = dict_entry[3]
        self.cost = dict_entry[4]
        self.node_type = node_type


class BOS(BaseNode):
    """
    BOS node
    """
    def __init__(self):
        super(BOS, self).__init__()
        self.cost = 0
        self.min_cost = 0

    def __str__(self):
        return '__BOS__'


class EOS(BaseNode):
    """
    EOS node
    """
    def __init__(self, pos):
        super(EOS, self).__init__()
        self.pos = pos
        self.cost = 0

    def __str__(self):
        return '__EOS__' + ' [back_pos=%d]' % self.back_pos


class Lattice:
    def __init__(self, size, dic):
        self.snodes = [[BOS()]] + [[] for i in range(0, size + 1)]
        self.enodes = [[], [BOS()]] + [[] for i in range(0, size + 2)]
        self.conn_costs = [[]]
        self.p = 1
        self.dic = dic

    def add(self, node):
        for enode in self.enodes[self.p]:
            cost = self.dic.get_trans_cost(enode.right_id, node.left_id) + node.cost
            if enode.min_cost + cost < node.min_cost:
                node.min_cost = enode.min_cost + cost
                node.back_index = enode.index
                node.back_pos = enode.pos
        node.pos = self.p
        node.index = len(self.snodes[self.p])
        self.snodes[self.p].append(node)
        node_len = len(node.surface) if hasattr(node, 'surface') else 1
        self.enodes[self.p + node_len].append(node)

    def forward(self):
        old_p = self.p
        self.p += 1
        while not self.enodes[self.p]:
            self.p += 1
        return self.p - old_p

    def end(self):
        eos = EOS(self.p)
        self.add(eos)
        # truncate snodes
        self.snodes = self.snodes[:self.p+1]

    def backward(self):
        assert isinstance(self.snodes[len(self.snodes)-1][0], EOS)
        path = []
        pos = len(self.snodes) - 1
        index = 0
        while pos >= 0:
            node = self.snodes[pos][index]
            path.append(node)
            index = node.back_index
            pos = node.back_pos
        path.reverse()
        return path

    def __str__(self):
        return '\n'.join(','.join(str(node) for node in nodes) for nodes in self.snodes)
