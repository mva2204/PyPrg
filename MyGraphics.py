# -*- coding: utf-8 -*-

import matplotlib as mpl
import math
from matplotlib import pyplot as plt



def plot_graph_smart():
    #Создание объекта Figure
    fig = plt.figure()
    #Тип объекта Figure
    print(type(fig))
    #scatter - метод для нанесения маркера в точке (1.0, 1.0)
    plt.scatter(1.0, 1.0)
    print(fig.axes)
    #plt.show()
    #fig, axes = plt.subplots
    return fig

if __name__ == "__main__":
    plot_graph_smart()