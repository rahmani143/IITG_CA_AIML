import numpy as np
A = np.arange(12).reshape(3, 4)
print(A)
C = A[:,::2]
print(C)
B = np.array([1, 2,3])
D = B[:,None] * C
print(D)