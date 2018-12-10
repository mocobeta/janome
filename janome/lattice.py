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

import sys, os
PY3 = sys.version_info[0] == 3

class NodeType:
    SYS_DICT = "SYS_DICT"
    USER_DICT = "USER_DICT"
    UNKNOWN = "UNKNOWN"


class Node(object):
    """
    Node class
    """
    __slots__ = [
        'pos', 'index', 'surface', 'left_id', 'right_id', 'cost',
        'part_of_speech', 'infl_type', 'infl_form',
        'base_form', 'reading', 'phonetic', 'node_type',
        'min_cost', 'back_pos', 'back_index'
    ]

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        self.pos = 0
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1

        self.surface, self.left_id, self.right_id, self.cost, self.part_of_speech, self.infl_type, self.infl_form, self.base_form, self.reading, self.phonetic = dict_entry

        self.node_type = node_type

    def __str__(self):
        return "(%s,%s,%s,%d,%s,%s,%s,%s,%s,%s) [back_pos=%d,back_index=%d]" % \
               (self.surface, self.left_id, self.right_id, self.cost, self.part_of_speech,
                self.infl_type, self.infl_form, self.base_form, self.reading, self.phonetic,
                self.back_pos, self.back_index)

    def node_label(self):
        return self.surface


class SurfaceNode(object):
    """
    Node class with surface form only.
    """
    __slots__ = ['pos', 'index', 'num', 'surface', 'left_id', 'right_id', 'cost', 'node_type', 'min_cost', 'back_pos', 'back_index']

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        self.pos = 0
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1

        self.num, self.surface, self.left_id, self.right_id, self.cost = dict_entry
        self.node_type = node_type

    def node_label(self):
        return self.surface


class BOS(object):
    """
    BOS node
    """
    def __init__(self):
        self.pos = 0
        self.index = 0
        self.right_id = 0
        self.cost = 0
        self.min_cost = 0
        self.back_pos = -1
        self.back_index = -1

    def __str__(self):
        return '__BOS__'

    def node_label(self):
        return 'BOS'


class EOS(object):
    """
    EOS node
    """
    def __init__(self, pos):
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.pos = pos
        self.cost = 0
        self.left_id = 0

    def __str__(self):
        return '__EOS__' + ' [back_pos=%d]' % self.back_pos

    def node_label(self):
        return 'EOS'

class Lattice:
    def __init__(self, size, dic):
        self.snodes = [[BOS()]] + [[] for i in range(0, size + 1)]
        self.enodes = [[], [BOS()]] + [[] for i in range(0, size + 1)]
        self.conn_costs = [[]]
        self.p = 1
        self.dic = dic

    def add(self, node):
        min_cost, best_node, node_left_id = node.min_cost - node.cost, None, node.left_id
        dic = self.dic
        for enode in self.enodes[self.p]:
            cost =  enode.min_cost + dic.get_trans_cost(enode.right_id, node_left_id)
            if cost < min_cost:
                min_cost, best_node = cost, enode
        node.min_cost = min_cost + node.cost
        node.back_index = best_node.index
        node.back_pos = best_node.pos
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

    # generate Graphviz dot file
    def generate_dotfile(self, filename='lattice.gv'):
        def is_unknown(node):
            return hasattr(node, 'node_type') and node.node_type == NodeType.UNKNOWN

        # traverse lattice and make nodes and edges
        node_ids = []
        edges = []
        path = self.backward()
        for pos in range(0, len(self.snodes) - 1):
            for i in range(0, len(self.snodes[pos])):
                node1 = self.snodes[pos][i]
                if is_unknown(node1) and node1 not in path:
                    continue
                node1_id = (pos, i)
                if node1_id not in node_ids:
                    node_ids.append(node1_id)
                node_len = len(node1.surface) if hasattr(node1, 'surface') else 1
                for j in range(0, len(self.snodes[pos + node_len])):
                    node2 = self.snodes[pos + node_len][j]
                    if is_unknown(node2) and node2 not in path:
                        continue
                    node2_id = (pos+node_len, j)
                    if node2_id not in node_ids:
                        node_ids.append(node1_id)
                    edges.append((node1_id, node2_id))

        # output dot file
        with self.__open_file(filename, mode='w', encoding='utf-8') as f:
            f.write(u'digraph G {\n')
            f.write(u'  rankdir=LR;\n')
            f.write(u'  ranksep=2.0;\n')
            for node_id in node_ids:
                (pos, idx) = node_id
                node = self.snodes[pos][idx]
                id_str = '%d.%d' % (pos, idx)
                label = '%s\\n%s' % (node.node_label(), str(node.cost))
                shape = 'ellipse' if isinstance(node, BOS) or isinstance(node, EOS) else 'box'
                color = 'lightblue' if isinstance(node, BOS) or isinstance(node, EOS) or node in path else 'lightgray'
                font = 'MS UI Gothic' if os.name == 'nt' else ''
                f.write(u'  %s [label="%s",shape=%s,style=filled,fillcolor=%s,fontname="%s"];\n' % (id_str, label, shape, color, font))
            for edge in edges:
                ((pos1, idx1), (pos2, idx2)) = edge
                node1 = self.snodes[pos1][idx1]
                node2 = self.snodes[pos2][idx2]
                id_str1 = '%d.%d' % (pos1, idx1)
                id_str2 = '%d.%d' % (pos2, idx2)
                label = str(self.dic.get_trans_cost(node1.right_id, node2.left_id))
                (color, style) = ('blue', 'bold') if node1 in path and node2 in path else ('black', 'solid')
                f.write(u'  %s -> %s [label="%s",color=%s,style=%s,fontcolor=red];\n' % (id_str1, id_str2, label, color, style))
            f.write('}\n')

    def __open_file(self, filename, mode, encoding):
        if PY3:
            return open(filename, mode=mode, encoding=encoding)
        else:
            import codecs
            return codecs.open(filename, mode, encoding)

    def __str__(self):
        return '\n'.join(','.join(str(node) for node in nodes) for nodes in self.snodes)
