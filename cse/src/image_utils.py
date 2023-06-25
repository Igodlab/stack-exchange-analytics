# image_utils.py

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import os
import datetime

# set plotting params
plt.rcParams["figure.figsize"] = [10,4]
plt.rc('font', family='serif')
plt.rc('xtick', labelsize=13)
plt.rc('ytick', labelsize=13)
plt.rcParams.update({'legend.fontsize': 11})
plt.rcParams.update({'axes.labelsize': 15})
plt.rcParams.update({'font.size': 15})

# barplot for tags in `Posts.csv`
def postsTagsBarplot(*, x=None, y=None, hue=None, data=None, order=None, hue_order=None, estimator=<function mean at 0x7ff320f315e0>, ci=95, n_boot=1000, units=None, seed=None, orient=None, color=None, palette=None, saturation=0.75, errcolor='.26', errwidth=None, capsize=None, dodge=True, ax=None, **kwargs):
    #fig, axes = plt.subplots(figsize=(14,6))
    sns.barplot(y=y, x=x, data=data)
    #plt.xticks(rotation=60)
    #plt.show()
