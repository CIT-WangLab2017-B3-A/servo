import numpy as np
L2=55
L3=85
LL2=L2*L2
LL3=L3*L3
LLLL2=LL2*LL2
LLLL3=LL3*LL3

X=70
Z=30
XX = X*X
ZZ = Z*Z
k = np.sqrt(np.square(XX + ZZ + LL2 + LL3) - (2*(np.square(XX+ZZ) + LLLL2 + LLLL3)))
theta2 = np.arctan2(Z,X)
theta2 -= np.arctan2(k, XX + ZZ + LL2 - LL3)
theta3 = np.arctan2(k, XX + ZZ - LL2 - LL3)
print np.degrees(theta2)
print np.degrees(theta3)
