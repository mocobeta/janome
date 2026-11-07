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

import os


class NodeType:
    SYS_DICT = "SYS_DICT"
    USER_DICT = "USER_DICT"
    UNKNOWN = "UNKNOWN"


class Node(object):
    """
    Standard Node class
    """

    __slots__ = [
        "pos",
        "index",
        "surface",
        "left_id",
        "right_id",
        "cost",
        "part_of_speech",
        "infl_type",
        "infl_form",
        "base_form",
        "reading",
        "phonetic",
        "node_type",
        "min_cost",
        "back_pos",
        "back_index",
    ]

    def __init__(self, dict_entry, node_type=NodeType.SYS_DICT):
        self.pos = 0
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1
        (
            self.surface,
            self.left_id,
            self.right_id,
            self.cost,
            self.part_of_speech,
            self.infl_type,
            self.infl_form,
            self.base_form,
            self.reading,
            self.phonetic,
        ) = dict_entry
        self.node_type = node_type

    def __str__(self):
        return f"({self.surface}, {self.left_id}, {self.right_id}, {self.cost}, {self.part_of_speech}, \
                  {self.infl_type}, {self.infl_form}, {self.base_form}, {self.reading}, {self.phonetic}) \
                      [back_pos = {self.back_pos}, back_index = {self.back_index}]"

    def node_label(self):
        return self.surface


class SurfaceNode(object):
    """
    Node class with surface form only.
    """

    __slots__ = [
        "pos",
        "index",
        "min_cost",
        "back_pos",
        "back_index",
        "num",
        "surface",
        "left_id",
        "right_id",
        "cost",
        "node_type",
    ]

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

    __slots__ = ["pos", "index", "min_cost", "back_pos", "back_index", "right_id", "cost"]

    def __init__(self):
        self.pos = 0
        self.index = 0
        self.min_cost = 0
        self.back_pos = -1
        self.back_index = -1
        self.right_id = 0
        self.cost = 0

    def __str__(self):
        return "__BOS__"

    def node_label(self):
        return "BOS"


class EOS(object):
    """
    EOS node
    """

    __slots__ = ["pos", "index", "min_cost", "back_pos", "back_index", "left_id", "cost"]

    def __init__(self, pos):
        self.pos = pos
        self.index = 0
        self.min_cost = 2147483647  # int(pow(2,31)-1)
        self.back_pos = -1
        self.back_index = -1
        self.cost = 0
        self.left_id = 0

    def __str__(self):
        return f"__EOS__ [back_pos={self.back_pos}]"

    def node_label(self):
        return "EOS"


class Lattice(object):
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
            cost = enode.min_cost + dic.get_trans_cost(enode.right_id, node_left_id)
            if cost < min_cost:
                min_cost, best_node = cost, enode
            elif (
                cost == min_cost
                and isinstance(best_node, SurfaceNode)
                and isinstance(enode, SurfaceNode)
                and enode.num < best_node.num
            ):
                min_cost, best_node = cost, enode
        assert best_node is not None
        node.min_cost = min_cost + node.cost
        node.back_index = best_node.index
        node.back_pos = best_node.pos
        node.pos = self.p
        node.index = len(self.snodes[self.p])
        self.snodes[self.p].append(node)
        node_len = len(node.surface) if hasattr(node, "surface") else 1
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
        self.snodes = self.snodes[: self.p + 1]

    def backward(self):
        assert isinstance(self.snodes[len(self.snodes) - 1][0], EOS)
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
    def generate_dotfile(self, filename="lattice.gv"):
        def is_unknown(node):
            return hasattr(node, "node_type") and node.node_type == NodeType.UNKNOWN

        # traverse lattice and make node lines and edge lines
        snodes = self.snodes
        on_path = {id(node) for node in self.backward()}
        font = "MS UI Gothic" if os.name == "nt" else ""
        get_trans_cost = self.dic.get_trans_cost
        # visible (dot id, node, on best path) triples per position; unknown nodes are shown only on the best path
        visible = [
            [
                (f"{pos}.{i}", node, id(node) in on_path)
                for i, node in enumerate(nodes)
                if not is_unknown(node) or id(node) in on_path
            ]
            for pos, nodes in enumerate(snodes)
        ]
        lines = ["digraph G {\n", "  rankdir=LR;\n", "  ranksep=2.0;\n"]
        edge_lines = []
        seen_ids = set()
        for pos in range(0, len(snodes) - 1):
            for id1, node1, on_path1 in visible[pos]:
                is_terminal = isinstance(node1, (BOS, EOS))
                shape = "ellipse" if is_terminal else "box"
                color = "lightblue" if is_terminal or on_path1 else "lightgray"
                node_line = (
                    f'  {id1} [label="{node1.node_label()}\\n{node1.cost}",shape={shape},'
                    f'style=filled,fillcolor={color},fontname="{font}"];\n'
                )
                if id1 not in seen_ids:
                    seen_ids.add(id1)
                    lines.append(node_line)
                edge_prefix = f"  {id1} -> "
                right_id = node1.right_id
                pos2 = pos + (len(node1.surface) if hasattr(node1, "surface") else 1)
                for id2, node2, on_path2 in visible[pos2]:
                    if id2 not in seen_ids:
                        lines.append(node_line)
                    style = "color=blue,style=bold" if on_path1 and on_path2 else "color=black,style=solid"
                    edge_lines.append(
                        f'{edge_prefix}{id2} [label="{get_trans_cost(right_id, node2.left_id)}",{style},fontcolor=red];\n'
                    )
        lines += edge_lines
        lines.append("}\n")

        # output dot file
        with self.__open_file(filename, mode="w", encoding="utf-8") as f:
            f.write("".join(lines))

    def __open_file(self, filename, mode, encoding):
        return open(filename, mode=mode, encoding=encoding)

    def __str__(self):
        return "\n".join(",".join(str(node) for node in nodes) for nodes in self.snodes)
