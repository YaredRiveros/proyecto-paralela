import os
import re
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import similaritymeasures
import numpy as np
from tabulate import tabulate
from newton_raphson import newton_raphson
from sklearn.linear_model import LinearRegression

class DataCollector:
    def __init__(self, problem_sizes):  # size of problems
        print('Data collector')
        print('For each n, the size of the problem will be N = n * np * (1024 / np)')
        self.problem_sizes = problem_sizes

    # Real speedup and ideal speedup
    def collect_data(self):
        for n in self.problem_sizes:
            os.system(f"./gen-plum.exe {n} {1}")
            print(f"Collecting data for N = {n}k...")
            print(f"Running algorithm with 1 processor...")
            file = open(f"speedup_data_{n}k.txt", "w")

            lines = [line.strip('\n') for line in os.popen(f"mpirun -np 1 ./cpu-4th")]
            real_speed = float(re.search(r"(\d+\.\d+)", lines[-14]).group(1))
            ideal = real_speed

            file.write(f"{round(real_speed, 2)} {round(ideal, 2)}\n")

            for p in range(2, 14):
                print(f"Running algorithm with {p} processors...")
                lines = [line.strip('\n') for line in os.popen(f"mpirun -np {p} ./cpu-4th")]
                real_speed = float(re.search(r"(\d+\.\d+)", lines[-14]).group(1))
                ideal_speed = ideal * p
                file.write(f"{round(real_speed, 2)} {round(ideal_speed, 2)}\n")

            file.close()

# Weak scalability analizer
class Analizer:
    def __init__(self, processors, problem_sizes):  # size of problems
        print('Performance analizer')
        print('For each n, the size of the problem will be N = n * np * (1024 / np)')
        self.problem_sizes = problem_sizes
        self.processors = processors

    def speedup_analysis(self):
        print("Speedup analysis")

        for n in problem_sizes:
            file = open(f"speedup_data_{n}k.txt", "r")
            lines = file.readlines()

            # push into an array
            experimental = []
            theorical = []
            for line in lines:
                line = line.split()
                experimental.append(float(line[0]))
                theorical.append(float(line[1]))

            table_data = []
            for p in range(1, 14):
                table_data.append([p, experimental[p - 1]])

            headers = ["Processors", "Speedup"]
            print(f"Metrics N = {n}k")
            print(tabulate(table_data, headers, tablefmt="pretty"))

            plt.plot(range(1, 14), theorical, label=f"N = {n}k theorical")
            plt.plot(range(1, 14), experimental, label=f"N = {n}k experimental")

            # Compute similarities
            exp_data = np.array([[i + 1, val] for i, val in enumerate(experimental)])
            ref_data = np.array([[i + 1, 1] for i in range(13)])
            pcm = similaritymeasures.pcm(exp_data, ref_data)
            df = similaritymeasures.frechet_dist(exp_data, ref_data)
            area = similaritymeasures.area_between_two_curves(exp_data, ref_data)
            cl = similaritymeasures.curve_length_measure(exp_data, ref_data)
            dtw, d = similaritymeasures.dtw(exp_data, ref_data)
            mae = similaritymeasures.mae(exp_data, ref_data) # mean absolute error
            mse = similaritymeasures.mse(exp_data, ref_data) # mean squared error
            headers = ["pcm", "df", "area", "cl", "dtw", "mae", "mse"]
            table_data = [[round(pcm, 2), round(df, 2), round(area, 2), round(cl, 2), round(dtw, 2), round(mae, 2), round(mse, 2)]]
            print(tabulate(table_data, headers, tablefmt="pretty"))

        plt.legend()
        plt.plot(4, 4000, 'o')
        plt.show()

    def scalability_analysis(self):

        print("Scalability analysis")
        plt.plot(self.processors, 13 * [1], label="Ideal efficiency")

        weak_analysis_e = []
        weak_analysis_p = []

        for n in self.problem_sizes:
            file = open(f"speedup_data_{n}k.txt", "r")
            lines = file.readlines()
            lines = [lines[i - 1] for i in self.processors] 

            # ideal speedup
            theorical = float(lines[0].split()[1])

            # experimental speedups
            speedups = [float(line.split()[0]) for line in lines]

            # experimental efficiencies
            efficiencies = [speedups[p - 1] / (p * theorical) for p in self.processors]

            # show data / results
            data_table = [[p, round(efficiencies[p - 1], 2)] for p in self.processors]
            headers = ["Processors", "Efficiency"]
            print(f"N = {n}k")
            print(tabulate(data_table, headers, tablefmt="pretty"))
            plt.plot(self.processors, efficiencies, label=f"N = {n}k experimental")

            # Computing the optimal number of processors (p) for the size of the problem (n)
            # based on the scalabity condition
            p_optimal = round(newton_raphson(5, n))
            e_optimal = float(lines[p_optimal - 1].split()[0]) / (p_optimal * theorical)
            weak_analysis_e.append(e_optimal)
            weak_analysis_p.append(p_optimal)

        # Analizar los puntos weak_analysis_e y weak_analysis_p
        x = np.array(weak_analysis_p).reshape(-1, 1)
        y = np.array(weak_analysis_e).reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        slope = model.coef_[0][0]
        intercept = model.intercept_[0]
        # print(f"Pendiente de la regresión lineal: {slope}")
        # print(f"Intersección con el eje y: {intercept}")

        # Graficar los puntos y la línea de regresión
        plt.plot(weak_analysis_p, weak_analysis_e, '--bo', label="Analysis points")
        plt.plot(weak_analysis_p, model.predict(x), 'r', linewidth=3, label="Regression line")

        plt.title("Weak scaling analysis (N-Body algorithms)")
        plt.xlabel("Number of processors (p)")
        plt.ylabel("Efficiency (E = S / p)")

        plt.legend()
        plt.show()

        # Conclusiones
        if abs(slope) < 0.02:  # Umbral para considerar la pendiente cercana a cero
            print(f"El algoritmo es escalable para problemas de tamaño {self.problem_sizes} con procesadores {self.processors}")
        else:
            print(f"El algoritmo NO es escalable para problemas de tamaño {self.problem_sizes} con procesadores {self.processors}")

# Number of processors
processors = range(1, 14)
# Sizes of the problems
problem_sizes = [8, 9, 12, 14, 16]
# problem_sizes = [1, 2, 3, 4, 5]
analizer = Analizer(processors, problem_sizes)
analizer.scalability_analysis()





