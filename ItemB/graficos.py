import numpy as np
import matplotlib.pyplot as plt

# Datos experimentales
p = np.array([1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
n_8k = 8000
n_9k = 9000
n_16k = 16000

# Tiempos experimentales
tiempos_8k = np.array([107.15, 62.959, 41.20966667, 39.52833333, 35.45, 31.69266667, 29.455, 27.083, 26.61066667, 23.74066667, 22.99666667, 23.37266667])
tiempos_9k = np.array([140.7766667, 74.45933333, 48.19866667, 45.02666667, 42.00666667, 39.379, 36.19933333, 34.91833333, 32.077, 29.92366667, 27.68733333, 27.618])
tiempos_16k = np.array([488.0366667, 268.3033333, 179.3266667, 164.3333333, 150.5, 136.9633333, 123.9033333, 116.8533333, 105.17, 98.84533333, 94.56266667, 96.21733333])

# Curvas teóricas
curva_teorica_8k = (n_8k**2 / p) + (n_8k * np.log(p))
curva_teorica_9k = (n_9k**2 / p) + (n_9k * np.log(p))
curva_teorica_16k = (n_16k**2 / p) + (n_16k * np.log(p))

# Gráfico para n = 8k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_8k, 'o-', label='Experimental n=8k')
plt.plot(p, curva_teorica_8k, 's--', label='Teórica n=8k')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
# escala log
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica para n=8k')
plt.legend()
plt.grid(True)
plt.savefig('comparacion_8k.png')
plt.show()

# Gráfico para n = 9k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_9k, 'o-', label='Experimental n=9k')
plt.plot(p, curva_teorica_9k, 's--', label='Teórica n=9k')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
# escala log
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica para n=9k')
plt.legend()
plt.grid(True)
plt.savefig('comparacion_9k.png')
plt.show()

# Gráfico para n = 16k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_16k, 'o-', label='Experimental n=16k')
plt.plot(p, curva_teorica_16k, 's--', label='Teórica n=16k')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
# escala log
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica para n=16k')
plt.legend()
plt.grid(True)
plt.savefig('comparacion_16k.png')
plt.show()
