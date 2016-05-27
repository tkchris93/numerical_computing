import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


titanic = pd.read_csv('titanic.csv')
def heading():
    heading = titanic.head()
    # save heading as heading.pdf

def gend_surv():
    tab = titanic.groupby('sex')[['survived']].mean()
    # save tab as gend_surv.pdf

def gend_class():
    tab = titanic.groupby(['sex', 'class'])[['survived']].aggregate('mean').unstack()
    # save tab as gend_class.pdf

def piv_gend_class():
    tab = titanic.pivot_table('survived', index='sex', columns='class')
    # save tab as piv_gend_class.pdf()
    
if __name__=='__main__':
    heading()
    gend_surv()
    gend_class()
    piv_gend_class()