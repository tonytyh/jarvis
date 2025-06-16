import matplotlib.pyplot as plt
import pandas


class Plotter:

    def __init__(self, title):
        self.title = title
        self.figure = plt.plot()

    def plot_line(self, df_line:pandas.DataFrame, label :str):
        plt.plot(df_line, linewidth=1)

    def plot_scatter(self, df_scatter:pandas.DataFrame, label:str, marker:str):
        plt.scatter(df_scatter.index, df_scatter.value, marker=marker)


def plot(lines=None, scatters=None):

    if lines is not None:
        for l in lines:
            plt.plot(l, linewidth=1)

    if scatters is not None:
        for s in scatters:
            plt.scatter(s.index, s.value)
    plt.show()
