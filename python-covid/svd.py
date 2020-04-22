# -*- coding
import numpy as np

# A is 5x4
A = np.array([
	[1, 0, 0, 0],
	[0, 0, 0, 4],
	[0, 3, 0, 0],
	[0, 0, 0, 0]
	])

u, s, vh = np.linalg.svd(A)

#print(u)
print(s)
#print(vh)
print( np.diag(s) )

sigma = np.zeros(A.shape, s.dtype)
np.fill_diagonal(sigma, s)

u, s, vh = np.linalg.svd(A, full_matrices=False)
