import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
from tabulate import tabulate
import similaritymeasures
newton_raphson = __import__('newton-raphson')
from sklearn.linear_model import LinearRegression

# Weak scalability analizer
class Analizer:
    def __init__(self, processors, problem_sizes):
        print('Performance analizer')
        print('For each n, the size of the problem will be N = n * np * (1024 / np)')
        self.problem_sizes = problem_sizes
        self.processors = processors

    def speedup_analysis(self):
        print("Speedup analysis")
        
        theoretical_sums = np.zeros(len(self.processors))
        count = 0

        for n in self.problem_sizes:
            file = open(f"speedup_data_{n}k.txt", "r")
            lines = file.readlines()
            lines = [lines[i - 1] for i in self.processors] 

            speedups = [float(line.split()[0]) for line in lines]
            theorical = [float(line.split()[1]) for line in lines]

            table_data = [[p, speedups[p - 1]] for p in self.processors]

            headers = ["Processors", "Speedup"]
            print(f"Metrics N = {n}k")
            print(tabulate(table_data, headers, tablefmt="pretty"))

            plt.plot(self.processors, speedups, label=f"N = {n}k experimental")

            # Compute similarities
            exp_data = np.array([[i + 1, val] for i, val in enumerate(speedups)])
            ref_data = np.array([[i + 1, 1] for i in range(len(self.processors))])
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
            theoretical_sums += np.array(theorical)
            count += 1

        theoretical_avg = theoretical_sums / count
        plt.plot(self.processors, theoretical_avg, label="Ideal speedup", linestyle='--')

        plt.title("Speedup weak scaling analysis (N-Body algorithms)")
        plt.xlabel("Number of processors (p)")
        plt.ylabel("Efficiency (E = S / p)")

        plt.legend()
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
            print(f"Metrics N = {n}k")
            print(tabulate(data_table, headers, tablefmt="pretty"))
            plt.plot(self.processors, efficiencies, label=f"N = {n}k experimental")

            # Computing the optimal number of processors (p) for the size of the problem (n)
            # based on the scalabity condition
            p_optimal = round(newton_raphson.newton_raphson(5, n))
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

        plt.title("Efficiency weak scaling analysis (N-Body algorithms)")
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
analizer = Analizer(processors, problem_sizes)

analizer.speedup_analysis()
analizer.scalability_analysis()





