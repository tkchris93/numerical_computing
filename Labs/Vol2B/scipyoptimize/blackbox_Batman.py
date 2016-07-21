# blackbox_Batman.py
"""Print the topologies to be used in the blackbox function."""

import numpy as np
from matplotlib import pyplot as plt

# Draw the top of Batman
top = np.array([29.]*91)+27
top_minus = -.5*np.array([13,13.3,13.6,13.85,14,14,14,14,14,14,14,0,7,7,7,7,7,
								7,0,14,14,14,14,14,14,14,13.85,13.6,13.3,13])
for i,item in enumerate(top_minus):
    top[31+i] += item

# Draw the bottem left (outer portion) of Batman
outer = np.array([29.]*15)+27
out_minus = -1*np.array([0,.5,1,1.5,2,2.5,3,3.5,4,4.5,5,7,8.6,10,14])
outer += out_minus

# Draw the bottem left (inner portion) of Batman
inner = np.array([8.]*30)+27
in_minus = []
for i,item in enumerate(out_minus):
    in_minus.append(item)
    if i < len(out_minus)-1:
        in_minus.append(sum([item,out_minus[i+1]])/2.)
in_minus = (8./14)*np.array([0]+in_minus)
inner += in_minus

# Mirror the left side to get the right side of Batman, combine
left = np.hstack((outer,inner))
right = np.array([i for i in reversed(left)])
bottom = np.hstack((left,np.array([22]),right))
bottom = .8*(bottom)+.2*56

plt.plot(top)
plt.plot(bottom)
plt.plot([0,0]) # So Batman's in the air.
plt.show()

# Save top, bottom to be used as topologies in Blackbox problem (no endpoints)
np.save("topologies.npy", np.column_stack((top[1:-1], bottom[1:-1])))