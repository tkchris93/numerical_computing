from pydataset import data

msleep = data("msleep")
vore_cons = msleep.groupby(["vore", "conservation"])
tab = msleep.pivot_table('sleep_total', index='conservation', columns='vore',aggfunc='count')
print tab