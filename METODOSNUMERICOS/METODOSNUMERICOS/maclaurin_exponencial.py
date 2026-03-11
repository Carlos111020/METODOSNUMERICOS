import math


def estimar_exponencial(x, tolerancia_percent, max_iter=200):
    if tolerancia_percent <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    valor_real = math.exp(x)
    estimacion = 1.0
    termino = 1.0
    n = 1
    errores = []

    et = abs((valor_real - estimacion) / valor_real) * 100
    errores.append((0, estimacion, None, et))

    while n <= max_iter:
        termino *= x / n
        nueva_estimacion = estimacion + termino

        if nueva_estimacion != 0:
            ea = abs((termino / nueva_estimacion) * 100)
        else:
            ea = float("inf")

        et = abs((valor_real - nueva_estimacion) / valor_real) * 100
        errores.append((n, nueva_estimacion, ea, et))

        if ea < tolerancia_percent:
            return nueva_estimacion, errores, valor_real

        estimacion = nueva_estimacion
        n += 1

    return nueva_estimacion, errores, valor_real


print("Estimacion de e^x usando la serie de Maclaurin")
x = float(input("Ingrese el valor de x: "))
tol = float(input("Ingrese la tolerancia de error relativo (%) (ej: 0.05): "))

aprox_final, pasos, real = estimar_exponencial(x, tol)

print(f"\nValor real: e^{x} = {real:.8f}")
print(f"Aproximacion final: {aprox_final:.8f}")
print("\nIteraciones:")
print(" n  estimacion        Ea(%)       Et(%)")
print("-" * 45)
for n, val, ea, et in pasos:
    ea_str = "---" if ea is None else f"{ea:10.5f}"
    print(f"{n:2d}  {val:12.8f}  {ea_str:>10}  {et:10.5f}")
