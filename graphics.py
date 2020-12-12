# -*- coding: utf-8 -*-

import matplotlib as mpl
import math
from matplotlib import pyplot as plt
import numpy as np

plt.ioff()

# put your python code here
n=int(input())
p="программист"
q=["ов","а"]
if n>=0 and n <=1000:
    if n==0:
        print("{} {}{}".format(n, p, q[0]))
    elif (str(n)[-1] == "1"):
        print("{} {}".format(n, p))
    elif int(str(n)[-1])>=2 and int(str(n)[-1])<=4:
        print("{} {}{}".format(n, p, q[1]))
    elif ((int(str(n)[-1])>=5 and int(str(n)[-1])<=9) or int(str(n)[-1])==0):
        print("{} {}{}".format(n, p, q[0]))
