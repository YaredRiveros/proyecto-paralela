import os
import numpy as np
import matplotlib.pyplot as plt

# Executing
# n = 8k
os.system('make cpu-4th')

data = []

for p in range(1, 14):
    # read timestamp
    os.system('mpirun -np 4 ./cpu-4th')


# change the size of problem (n)
os.system('./gen-plum.exe')

# n = 9k



# n = 16k


# Comparar con teorica




