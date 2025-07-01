import numpy as np


original = [True, True, False, True, True, True, None, True, True, False, False, False, None, False, True, True, None, True, True, True, True, False, True, None, False, None, None, None, False, None, False, True, True, True, True, False, False, False, False, False, None, True, True, None, None, False, None, None, False, True, True, False, None, None, None, None, False, False, False, False, False, False, None, None, True, None, True, None, True, False, None, True, False, False, None, None, True, None, True, None, None, True, None, False, None, True, False, True, None, True, None, False, False, False, True, False, False, True, False, False, None, True, False, False, False, True, None, False, True, None, False, None, False, True, True, None, False, True, True, False, None, None, True, True, False, True, None, True, True, True, True, True, False, None, True, None, None, None, None, None, True, None, True, True, True, False, None, False, True, True, True, False, None, True, None, True, True, False, None, None, False, False, False, False, False, None, False, True, None, None, True, True, True, False, False, True, None, None, True, False, True, False, None, True, True, False, False, True, None, True, True, False, None, True, True, True, None, True, True, False, False, True, False, False, None, True, None, False, True, False, False, True, False, False, None, False, True, False, None, None, True, None, True, False, True, None, None, True, None, False, True, True, None, True, False, None, False, False, None]

# Convert to GF(3) encoding
gf3_array = [0 if x is None else 1 if x is False else 2 for x in original]

print(gf3_array)

np.save('gf3_array.npy', gf3_array)