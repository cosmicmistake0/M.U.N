print(__file__)
import numpy as np
x = np.array([-1, +1, +1, -27])
y = np.array([-1, -1, +1, +4])
print((270-(np.degrees(np.arctan2(y, x))))%360)
# print(np.degrees(np.arctan2(y, x)) )
#  * 180 / np.pi