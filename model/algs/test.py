import numpy as np
x = np.random.normal(loc=0.0, scale=20)
x = int(x + 1.5) if x > 0 else int(x - 1.5)
print(x)
