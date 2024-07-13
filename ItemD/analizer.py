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

    def set_processors(self, processors):
        self.processors = processors
    
    def set_problem_sizes(self, problem_sizes):
        self.problem_sizes = problem_sizes

    def speedup_analysis(self):
        print("Speedup analysis")
        
        theoretical_sums = np.zeros(len(self.processors))
        count = 0
        all_speedups = {p: [] for p in self.processors}

        for n in self.problem_sizes:
            with open(f"speedup_data_{n}k.txt", "r") as file:
                lines = file.readlines()
            lines = [lines[i - 1] for i in self.processors] 

            speedups = [float(line.split()[0]) for line in lines]
            theoretical = [float(line.split()[1]) for line in lines]

            for p, s in zip(self.processors, speedups):
                all_speedups[p].append(round(s, 2))

            plt.plot(self.processors, speedups, label=f"N = {n}k experimental")

            # Compute similarities
            # exp_data = np.array([[i + 1, val] for i, val in enumerate(speedups)])
            # ref_data = np.array([[i + 1, 1] for i in range(len(self.processors))])
            # pcm = similaritymeasures.pcm(exp_data, ref_data)
            # df = similaritymeasures.frechet_dist(exp_data, ref_data)
            # area = similaritymeasures.area_between_two_curves(exp_data, ref_data)
            # cl = similaritymeasures.curve_length_measure(exp_data, ref_data)
            # dtw, d = similaritymeasures.dtw(exp_data, ref_data)
            # mae = similaritymeasures.mae(exp_data, ref_data)  # mean absolute error
            # mse = similaritymeasures.mse(exp_data, ref_data)  # mean squared error
            
            # similarity_headers = ["pcm", "df", "area", "cl", "dtw", "mae", "mse"]
            # similarity_data = [[round(pcm, 2), round(df, 2), round(area, 2), round(cl, 2), round(dtw, 2), round(mae, 2), round(mse, 2)]]
            # print(tabulate(similarity_data, similarity_headers, tablefmt="pretty"))
            
            theoretical_sums += np.array(theoretical)
            count += 1

        theoretical_avg = theoretical_sums / count
        plt.plot(self.processors, theoretical_avg, label="Ideal speedup", linestyle='--')

        # Creating the table with headers
        headers = ["Processors"] + [f"Speedup (N = {n}k)" for n in self.problem_sizes]
        data_table = [[p] + all_speedups[p] for p in self.processors]
        
        print("Metrics")
        print(tabulate(data_table, headers, tablefmt="pretty"))

        plt.title("Speedup weak scaling analysis (N-Body algorithms)")
        plt.xlabel("Number of processors (p)")
        plt.ylabel("Speedup (S)")

        plt.legend()
        # plt.savefig('speedup_analysis.png')
        plt.show()

    def scalability_analysis(self):
        print("Scalability analysis")
        plt.plot(self.processors, len(self.processors) * [1], label="Ideal efficiency")

        weak_analysis_e = []
        weak_analysis_p = []
        all_efficiencies = {p: [] for p in self.processors}

        for n in self.problem_sizes:
            with open(f"speedup_data_{n}k.txt", "r") as file:
                lines = file.readlines()
            lines = [lines[i - 1] for i in self.processors] 

            # ideal speedup
            theoretical = float(lines[0].split()[1])

            # experimental speedups
            speedups = [float(line.split()[0]) for line in lines]

            # experimental efficiencies
            efficiencies = [speedups[p - 1] / (p * theoretical) for p in self.processors]

            for p, e in zip(self.processors, efficiencies):
                all_efficiencies[p].append(round(e, 2))

            plt.plot(self.processors, efficiencies, label=f"N = {n}k experimental")

            # Computing the optimal number of processors (p) for the size of the problem (n)
            # based on the scalability condition
            p_optimal = round(newton_raphson.newton_raphson(5, n))
            e_optimal = float(lines[p_optimal - 1].split()[0]) / (p_optimal * theoretical)
            weak_analysis_e.append(e_optimal)
            weak_analysis_p.append(p_optimal)

        # Creating the table with headers
        headers = ["Processors"] + [f"Efficiency (N = {n}k)" for n in self.problem_sizes]
        data_table = [[p] + all_efficiencies[p] for p in self.processors]
        
        print("Metrics")
        print(tabulate(data_table, headers, tablefmt="pretty"))

        # Analyzing the points weak_analysis_e and weak_analysis_p
        x = np.array(weak_analysis_p).reshape(-1, 1)
        y = np.array(weak_analysis_e).reshape(-1, 1)
        model = LinearRegression().fit(x, y)
        slope = model.coef_[0][0]
        intercept = model.intercept_[0]

        # Plotting the points and the regression line
        plt.plot(weak_analysis_p, weak_analysis_e, '--bo', label="Analysis points")
        plt.plot(weak_analysis_p, model.predict(x), 'r', linewidth=3, label="Regression line")

        plt.title("Efficiency weak scaling analysis (N-Body algorithms)")
        plt.xlabel("Number of processors (p)")
        plt.ylabel("Efficiency (E = S / p)")
        plt.legend()

        # Conclusions
        if abs(slope) < 0.02:  # Threshold to consider the slope close to zero
            print(f"The algorithm is scalable ", end="")
        else:
            print(f"The algorithm is NOT scalable ", end="")
        print(f"for problem sizes {self.problem_sizes}k. Algorithm evaluated with {self.processors} processors.")

        # plt.savefig('scalability_analysis.png')
        plt.show()

processors = range(1, 14)
problem_sizes = [8, 9, 12, 14, 16]
analizer = Analizer(processors, problem_sizes)
analizer.scalability_analysis()

problem_sizes = [1, 2, 3, 4]
analizer.set_problem_sizes(problem_sizes)
analizer.scalability_analysis()
