import numpy as np
import pandas as pd
from matplotlib import pyplot as plt


titanic = pd.read_csv('titanic.csv')

def problem_1():
    # Problem 1a
    titanic.groupby('embark_town')[['survived']].mean() 
    # Problem 1b
    titanic.pivot_table('survived', index='embark_town', columns='sex')
    # Problem 1c
    # We look at the number of data points in each category of the above pivot table
    titanic.pivot_table('survived', index='embark_town', columns='sex', aggfunc='count')
    print 'It seems that the place of embarkment isnt as important as the class and gender are. If someone embarked from Queenstown, it was more likely that they were 3rd class, affecting the probability of them surviving.'
    titanic.pivot_table('survived', index='sex', columns='class')

