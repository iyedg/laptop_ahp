from itertools import combinations_with_replacement
import pandas as pd

import ipywidgets as widgets
from IPython.display import display


class AHP:
    def __init__(self, df):
        self.df = df
        self.pairwise_df = pd.DataFrame()
        self.slider_pair = {}
        self.slider_caption = {}

    def _compare_sentence(self, i, j, q=None):
        """
        Given two words and a number `q`, create a sentence of comparison
        where i is the leftmost operand
        """
        i = " ".join([s.title() for s in i.split("_")])
        j = " ".join([s.title() for s in j.split("_")])
        return r"<b>{i}</b> is <b>{q}</b> times more important than <b>{j}</b>".format(
            i=i, j=j, q=q)

    def _on_change(self, change):
        """
        Fill the location of the pair specified by the corresponding slider
        with its value
        """
        if change["type"] == "change":
            owner = change["owner"]
            val = float(change["new"])
            i, j = self.slider_pair[owner]
            compare_sentence = self._compare_sentence(i, j, val)
            if val <= 0:
                # Account for -8 being the smallet value by adding 1 to its
                # absolute value
                val = round(1 / (abs(val) + 1), 1)
                i, j = j, i
                compare_sentence = self._compare_sentence(
                    i, j, round(1 / val, 1))
            self.pairwise_df.loc[i, j] = val
            self.pairwise_df.loc[j, i] = 1 / val
            self.slider_caption[owner].value = compare_sentence

    def display(self):
        cols = self.df.columns
        # TODO: fill all with 1
        self.pairwise_df = pd.DataFrame(columns=cols, index=cols)
        pairs = combinations_with_replacement(cols, 2)
        for i, j in pairs:
            if i == j:
                self.pairwise_df.loc[i, j] = 1
                continue
            # The scale ranges from 1 to 9 in both positive and negative
            # directions. A minimum of 8 is used, the value will be adjusted
            # for negative values when calculating
            slider = widgets.FloatSlider(value=1, min=-8, max=9, readout=False)
            caption = widgets.HTML(
                value=self._compare_sentence(i, j, slider.value))
            self.slider_caption[slider] = caption

            slider.observe(self._on_change, names="value")
            display(caption, slider)
            self.slider_pair[slider] = (i, j)
