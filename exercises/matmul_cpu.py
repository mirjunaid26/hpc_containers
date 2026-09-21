import numpy as np
import time

a = np.random.rand(4000, 4000)
b = np.random.rand(4000, 4000)

start = time.time()
c = a @ b
elapsed = time.time() - start

print(f"4000x4000 matrix multiply took {elapsed:.3f} s")
