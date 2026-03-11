import math


def cos_maclaurin_aprox(x, tolerancia_percent, max_iter=200):
    if tolerancia_percent <= 0:
        raise ValueError("La tolerancia debe ser mayor que cero.")

    valor_real = math.cos(x)
    suma = 0.0
    n = 0
    errores = []

    while n <= max_iter:
        signo = (-1) ** n
        termino = signo * (x ** (2 * n)) / math.factorial(2 * n)
        suma_nueva = suma + termino

        if valor_real != 0:
            et = abs((valor_real - suma_nueva) / valor_real) * 100
        else:
            et = abs(valor_real - suma_nueva) * 100

        if n == 0:
            ea = None
        elif suma_nueva != 0:
            ea = abs(termino / suma_nueva) * 100
        else:
            ea = float("inf")

        errores.append((n, termino, suma_nueva, ea, et))

        if ea is not None and ea < tolerancia_percent:
            break

        suma = suma_nueva
        n += 1

    return errores


print("Aproximacion de cos(x) usando la serie de Maclaurin")
x_raw = input("Ingrese x en radianes (puede usar pi, ej: pi/3): ")
x = eval(x_raw, {"__builtins__": {}}, {"pi": math.pi})
tol = float(input("Ingrese la tolerancia de error relativo (%) (ej: 5): "))

resultados = cos_maclaurin_aprox(x, tol)

print("\nResultados:")
print(" n  Termino        Aproximacion        Ea(%)        Et(%)")
print("-" * 65)

for n, term, aprox, ea, et in resultados:
    ea_str = "---" if ea is None else f"{ea:10.5f}"
    print(f"{n:<2} {term:12.6f} {aprox:15.6f} {ea_str:>12} {et:10.5f}")
