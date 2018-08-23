import pandas as pd

import anytree
from anytree import Node


class AHP:
    def __init__(self,  goal, criteria, alternatives,
                 df=None, children_char="."):
        self.children_char = children_char
        if df:
            self.mx = df
        else:
            self.mx = pd.DataFrame(columns=criteria, index=alternatives)
        self.goal = goal
        self._build_tree()

    def _build_tree(self):
        goal = Node(self.goal)

        for col in self.mx.columns:
            levels = [Node(l) for l in col.split(".")]
            for i, l in enumerate(levels):
                def children_names(n): return [c.name for c in n.children]
                # The first element is a root node
                if i > 0:
                    parent = anytree.search.find_by_attr(
                        node=goal, value=levels[i - 1].name)
                else:
                    parent = goal
                if l.name not in children_names(parent):
                    l.parent = parent
        self.tree = goal
