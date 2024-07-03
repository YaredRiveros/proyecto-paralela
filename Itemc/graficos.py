import numpy as np
import matplotlib.pyplot as plt

# Datos experimentales
p = np.array([1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

# Tiempos experimentales
tiempos_8k = np.array([9.314, 17.06066667, 25.22633333, 28.95166667, 29.70033333, 32.91066667, 35.09833333, 38.197, 41.32633333, 42.96266667, 44.763, 48.16])
tiempos_9k = np.array([9.274666667, 16.81566667, 25.787, 27.50266667, 30.022, 33.35166667, 35.583, 38.42066667, 40.49166667, 42.436, 46.625, 46.73533333])
tiempos_16k = np.array([9.163, 16.536, 24.24533333, 27.29033333, 29.336, 32.76666667, 35.089, 37.805, 39.199, 41.61866667, 44.12966667, 45.911])

# Crear el gráfico
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_8k, 'o-', label='n=8k', color='blue')
plt.plot(p, tiempos_9k, 's-', label='n=9k', color='green')
plt.plot(p, tiempos_16k, 'd-', label='n=16k', color='red')

# Curva ideal S = p
plt.plot(p, p, 'k--', label='Curva Ideal S=p', color='purple')

plt.xlabel('p')
plt.ylabel('Velocidad (Flops/s)')
#escala logaritmica
# plt.yscale('log')
plt.title('Comparación de Velocidad para Diferentes Valores de n')
plt.legend()
plt.grid(True)
plt.savefig('comparacion.png')
plt.show()
