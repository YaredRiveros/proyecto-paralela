import os
import re
import matplotlib
matplotlib.use('TkAgg') # delete it if Tkinter is NOT installed
import matplotlib.pyplot as plt

class Analizer():

    def __init__(self):
        print('Performance analizer')
        print('Choose n and np. The size of the problem will be N = n * np * (1024 / np)')
        n = int(input('n: '))
        np = int(input('np: '))
        os.system(f"./gen-plum.exe {n} {np}")

    @staticmethod
    def get_speed(string):
        match = re.search(r"(\d+\.\d+)", string)
        return float(match.group(1))
    
    def get_data(self):
        experimental = []
        theorical = []
        print("Collecting data...")
        for p in range(1, 14):
            print(f"Running algorithm with {p} processors...")
            data = [line.strip('\n') for line in os.popen(f"mpirun -np {p} ./cpu-4th")]
            real_speed = Analizer.get_speed(data[-14])
            ideal_speed = Analizer.get_speed(data[-1])
            experimental.append(real_speed)
            theorical.append(ideal_speed)
        
        self.experimental = experimental
        self.theorical = theorical

    def scalability_analysis(self):
        print("Scalability analysis")
        for p in range(1, 14):
            self.experimental[p - 1] /= p
            self.theorical[p - 1] /= p
            print(f"{p} processors: real efficiency = {self.experimental[p - 1]}, ideal efficiency = {self.theorical[p - 1]}")
        plt.plot(range(1, 14), self.experimental)
        plt.plot(range(1, 14), self.theorical)
        plt.show()

    def speedup_analysis(self):
        print("Speedup analysis")
        for p in range(1, 14):
            print(f"{p} processors: real speedup = {self.experimental[p - 1]}, ideal speedup = {self.theorical[p - 1]}")
        plt.plot(range(1, 14), self.experimental)
        plt.plot(range(1, 14), self.theorical)
        plt.show()

analizer = Analizer()
analizer.get_data()
# analizer.speedup_analysis()
analizer.scalability_analysis()





