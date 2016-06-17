import pandas as pd

titanic = pd.read_csv("titanic.csv")
print titanic.head()

tab = titanic.pivot_table('Survived', index='Sex', columns='Pclass',aggfunc='count')
print tab

