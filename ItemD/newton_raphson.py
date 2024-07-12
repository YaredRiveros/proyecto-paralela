import math

def f(p, n):
    return 1105 * p * math.log(p, 10) - (n * 1024)

def f_prime(p):
    return 1105 * (math.log(p, 10) + 1 / math.log(10))

def newton_raphson(initial_guess, n, tol=1e-7, max_iter=1000):
    p = initial_guess
    for _ in range(max_iter):
        if p <= 0:
            raise ValueError("p es menor o igual a cero, lo que no es válido para el logaritmo.")
        p_new = p - f(p, n) / f_prime(p)
        if abs(p_new - p) < tol:
            return p_new
        p = p_new
    raise ValueError("No convergence")

# # Valor inicial
# initial_guess = 5

# # Encontrar la solución
# p_solution = newton_raphson(initial_guess)

# print(f"La solución aproximada para p es: {round(p_solution)}")
