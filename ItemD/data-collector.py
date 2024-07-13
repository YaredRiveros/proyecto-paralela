import os
import re

class DataCollector:
    def __init__(self, processors, problem_sizes):
        print('Data collector')
        print('For each n, the size of the problem will be N = n * np * (1024 / np)')
        self.problem_sizes = problem_sizes
        self.processors = processors

    # Real speedup and ideal speedup
    def collect_data(self):
        for n in self.problem_sizes:
            os.system(f"./gen-plum.exe {n} {1}")
            print(f"Collecting data for N = {n}k...")
            print(f"Running algorithm with 1 processor...")
            file = open(f"speedup_data_{n}k.txt", "w")

            lines = [line.strip('\n') for line in os.popen(f"mpirun -np {self.processors[0]} ./cpu-4th")]
            real_speed = float(re.search(r"(\d+\.\d+)", lines[-14]).group(1))
            ideal = real_speed

            file.write(f"{round(real_speed, 2)} {round(ideal, 2)}\n")

            for p in self.processors[1:]:
                print(f"Running algorithm with {p} processors...")
                lines = [line.strip('\n') for line in os.popen(f"mpirun -np {p} ./cpu-4th")]
                real_speed = float(re.search(r"(\d+\.\d+)", lines[-14]).group(1))
                ideal_speed = ideal * p
                file.write(f"{round(real_speed, 2)} {round(ideal_speed, 2)}\n")

            file.close()

processors = range(1, 14)
problem_sizes = [1, 2] # N = 1 * 1024, N = 2 * 1024
collector = DataCollector(processors, problem_sizes)
collector.collect_data()