import os
import re
import matplotlib
matplotlib.use('TkAgg') # delete it if Tkinter is NOT installed
import matplotlib.pyplot as plt
# import similaritymeasures
from tabulate import tabulate
import similaritymeasures
import numpy as np


class Analizer():

    def __init__(self):
        print('Performance analizer')
        print('Choose n and np. The size of the problem will be N = n * np * (1024 / np)')
        n = int(input('n: '))
        npp = int(input('np: '))
        os.system(f"./gen-plum.exe {n} {npp}")
    
    def collect_data(self):
        experimental = []
        theorical = []
        print("Collecting data...")
        print(f"Running algorithm with 1 processor...")
        data = [line.strip('\n') for line in os.popen(f"mpirun -np 1 ./cpu-4th")]
        real_speed = re.search(r"(\d+\.\d+)", data[-14])
        real_speed = float(real_speed.group(1))
        ideal_speed = re.search(r"(\d+\.\d+)", data[-1])
        ideal_speed = float(ideal_speed.group(1))
        experimental.append(real_speed)
        theorical.append(ideal_speed)
        for p in range(2, 14):
            print(f"Running algorithm with {p} processors...")
            data = [line.strip('\n') for line in os.popen(f"mpirun -np {p} ./cpu-4th")]
            real_speed = re.search(r"(\d+\.\d+)", data[-14])
            real_speed = float(real_speed.group(1))
            ideal_speed = theorical[0] * p
            experimental.append(real_speed)
            theorical.append(ideal_speed)
        self.experimental = experimental
        self.theorical = theorical

    def speedup_analysis(self):
        print("Speedup analysis")
        table_data = []

        for p in range(1, 14):
            table_data.append([p, round(self.experimental[p - 1], 2)])

        headers = ["Processors", "Speedup"]
        print(tabulate(table_data, headers, tablefmt="pretty"))

        plt.plot(range(1, 14), self.experimental)
        plt.plot(range(1, 14), self.theorical)
        plt.show()

        # Compute similarities
        exp_data = np.array([[i + 1, val] for i, val in enumerate(self.experimental)])
        ref_data = np.array([[i + 1, 1] for i in range(13)])

        pcm = similaritymeasures.pcm(exp_data, ref_data)
        df = similaritymeasures.frechet_dist(exp_data, ref_data)
        area = similaritymeasures.area_between_two_curves(exp_data, ref_data)
        cl = similaritymeasures.curve_length_measure(exp_data, ref_data)
        dtw, d = similaritymeasures.dtw(exp_data, ref_data)
        # mean absolute error
        mae = similaritymeasures.mae(exp_data, ref_data)
        # mean squared error
        mse = similaritymeasures.mse(exp_data, ref_data)
        headers = ["pcm", "df", "area", "cl", "dtw", "mae", "mse"]
        table_data = [[round(pcm, 2), round(df, 2), round(area, 2), round(cl, 2), round(dtw, 2), round(mae, 2), round(mse, 2)]]
        print(tabulate(table_data, headers, tablefmt="pretty"))

        # Write conclusions
        if pcm >= 10:
            print("The algorithm is scalable.")
        else:
            print("The algorithm is NOT scalable.")

    def scalability_analysis(self):
        print("Scalability analysis")
        
        table_data = []
        for p in range(1, 14):
            self.experimental[p - 1] /= (p * self.theorical[0])
            table_data.append([p, round(self.experimental[p - 1], 2)])
        
        headers = ["Processors", "Efficiency"]
        print(tabulate(table_data, headers, tablefmt="pretty"))
    
        plt.plot(range(1, 14), self.experimental)
        plt.plot(range(1, 14), 13 * [1])
        plt.show()

        exp_data = np.array([[i + 1, val] for i, val in enumerate(self.experimental)])
        ref_data = np.array([[i + 1, 1] for i in range(13)])

        # Compute similarities
        pcm = similaritymeasures.pcm(exp_data, ref_data)
        df = similaritymeasures.frechet_dist(exp_data, ref_data)
        area = similaritymeasures.area_between_two_curves(exp_data, ref_data)
        cl = similaritymeasures.curve_length_measure(exp_data, ref_data)
        dtw, d = similaritymeasures.dtw(exp_data, ref_data)
        # mean absolute error
        mae = similaritymeasures.mae(exp_data, ref_data)
        # mean squared error
        mse = similaritymeasures.mse(exp_data, ref_data)

        headers = ["pcm", "df", "area", "cl", "dtw", "mae", "mse"]
        table_data = [[round(pcm, 2), round(df, 2), round(area, 2), round(cl, 2), round(dtw, 2), round(mae, 2), round(mse, 2)]]
        print(tabulate(table_data, headers, tablefmt="pretty"))

        # Write conclusions
        if pcm >= 10:
            print("The algorithm is scalable.")
        else:
            print("The algorithm is NOT scalable.")


analizer = Analizer()
analizer.collect_data()
analizer.speedup_analysis()
analizer.scalability_analysis()





