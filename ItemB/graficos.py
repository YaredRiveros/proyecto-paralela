import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

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
plt.savefig('sinConstante/comparacion_8k.png')
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
plt.savefig('sinConstante/comparacion_9k.png')
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
plt.savefig('sinConstante/comparacion_16k.png')
plt.show()

## Gráficos con constante que ajusta la curva teórica a la experimental con mínimos cuadrados

# Función para calcular el error cuadrático medio
def error(c, y_exp, y_teor):
    return np.sum((y_exp - c * y_teor)**2)

# Encontrar la constante de ajuste para n=8k
res_8k = minimize(error, x0=1, args=(tiempos_8k, curva_teorica_8k))
const_8k = res_8k.x[0]

# Gráfico para n = 8k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_8k, 'o-', label='Experimental n=8k')
plt.plot(p, const_8k * curva_teorica_8k, 's--', label=f'Teórica n=8k ajustada (const={const_8k:.8f})')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica Ajustada para n=8k')
plt.legend()
plt.grid(True)
plt.savefig('conConstante/comparacion_8k.png')
plt.show()

# Encontrar la constante de ajuste para n=9k
res_9k = minimize(error, x0=1, args=(tiempos_9k, curva_teorica_9k))
const_9k = res_9k.x[0]

# Gráfico para n = 9k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_9k, 'o-', label='Experimental n=9k')
plt.plot(p, const_9k * curva_teorica_9k, 's--', label=f'Teórica n=9k ajustada (const={const_9k:.8f})')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica Ajustada para n=9k')
plt.legend()
plt.grid(True)
plt.savefig('conConstante/comparacion_9k.png')
plt.show()

# Encontrar la constante de ajuste para n=16k
res_16k = minimize(error, x0=1, args=(tiempos_16k, curva_teorica_16k))
const_16k = res_16k.x[0]

# Gráfico para n = 16k
plt.figure(figsize=(10, 6))
plt.plot(p, tiempos_16k, 'o-', label='Experimental n=16k')
plt.plot(p, const_16k * curva_teorica_16k, 's--', label=f'Teórica n=16k ajustada (const={const_16k:.8f})')
plt.xlabel('p')
plt.ylabel('Tiempo (s)')
plt.yscale('log')
plt.title('Comparación Curva Experimental y Teórica Ajustada para n=16k')
plt.legend()
plt.grid(True)
plt.savefig('conConstante/comparacion_16k.png')
plt.show()