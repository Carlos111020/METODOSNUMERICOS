def f(x):
    return -0.1 * x**4 - 0.15 * x**3 - 0.5 * x**2 - 0.25 * x + 1.25


def f_prime_exact(x):
    return -0.4 * x**3 - 0.45 * x**2 - x - 0.25


def diferencias_aproximadas(func, x, h):
    if h == 0:
        raise ValueError("h no puede ser cero.")

    f_x = func(x)
    f_xh = func(x + h)
    f_xmh = func(x - h)

    adelante = (f_xh - f_x) / h
    atras = (f_x - f_xmh) / h
    centrada = (f_xh - f_xmh) / (2 * h)

    return adelante, atras, centrada


print("Aproximacion de derivadas usando diferencias finitas")
x0 = float(input("Ingrese el valor de x: "))
h1 = float(input("Ingrese el primer valor de h: "))
h2 = float(input("Ingrese el segundo valor de h: "))

valores_h = [h1, h2]
real = f_prime_exact(x0)

resultados = []
for h in valores_h:
    fa, fr, fc = diferencias_aproximadas(f, x0, h)

    if real != 0:
        ea = abs((fa - real) / real) * 100
        er = abs((fr - real) / real) * 100
        ec = abs((fc - real) / real) * 100
    else:
        ea = abs(fa - real) * 100
        er = abs(fr - real) * 100
        ec = abs(fc - real) * 100

    resultados.append((h, fa, ea, fr, er, fc, ec))

print(f"\nDerivada exacta en x = {x0} es f'(x) = {real:.6f}\n")
print(" h      f_adelante    Error %     f_atras       Error %     f_centrada    Error %")
print("-" * 79)
for h, fa, ea, fr, er, fc, ec in resultados:
    print(f"{h:<6.3f} {fa:>12.6f} {ea:>9.3f} {fr:>12.6f} {er:>9.3f} {fc:>12.6f} {ec:>9.3f}")
