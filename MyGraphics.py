# -*- coding: utf-8 -*-

import numpy as np
from matplotlib import pyplot as plt



def plot_graph_smart():
    #Создание объекта Figure
    x = np.arange(0,4*np.pi,0.1)
    y = np.sin(x)
    z = np.cos(x)
    fig, axes = plt.subplots(nrows=2, ncols=1)
#    fig = plt.figure()
    #Тип объекта Figure
    print(type(fig))
    #scatter - метод для нанесения маркера в точке (1.0, 1.0)

    axes[0].plot(x, y, x,z)
#    plt.scatter(1.0, 1.0)
    axes[1].scatter(1.0, 5.0)
    print(fig.axes)
    #plt.show()
    #fig, axes = plt.subplots
    return fig

if __name__ == "__main__":
    plot_graph_smart()