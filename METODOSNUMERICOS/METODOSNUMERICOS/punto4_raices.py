import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return -12 - 21*x + 18*x**2 - 2.75*x**3

# -------------------------
# (a) Grafica para ubicar raices
# -------------------------
x = np.linspace(-5, 5, 2000)
y = f(x)

plt.figure()
plt.plot(x, y)
plt.axhline(0)
plt.grid(True)
plt.title("PUNTO 4a - Grafica de f(x)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.show()

# -------------------------
# (b) Biseccion: xl=-1, xu=0, es=1%
# -------------------------
xl, xu = -1.0, 0.0
es = 1.0

xr_old = None
print("\nPUNTO 4b - Biseccion (es=1%)")
print("i\t xl\t\t xu\t\t xr\t\t f(xr)\t\t ea(%)")

for i in range(1, 101):
    xr = (xl + xu) / 2.0
    fl = f(xl)
    fr = f(xr)

    ea = None
    if xr_old is not None:
        ea = abs((xr - xr_old) / xr) * 100

    print(f"{i}\t {xl:.6f}\t {xu:.6f}\t {xr:.6f}\t {fr:.6f}\t {'' if ea is None else f'{ea:.6f}'}")

    # Criterio de paro
    if ea is not None and ea < es:
        break

    # Actualizar intervalo
    if fl * fr < 0:
        xu = xr
    else:
        xl = xr

    xr_old = xr

print(f"\nRaiz por biseccion: xr ≈ {xr:.6f}")

# -------------------------
# (c) Falsa posicion: mismo intervalo, es=1%
# -------------------------
xl, xu = -1.0, 0.0
xr_old = None

print("\nPUNTO 4c - Falsa Posicion (es=1%)")
print("i\t xl\t\t xu\t\t xr\t\t f(xr)\t\t ea(%)")

for i in range(1, 101):
    fl = f(xl)
    fu = f(xu)

    xr = xu - fu * (xl - xu) / (fl - fu)
    fr = f(xr)

    ea = None
    if xr_old is not None:
        ea = abs((xr - xr_old) / xr) * 100

    print(f"{i}\t {xl:.6f}\t {xu:.6f}\t {xr:.6f}\t {fr:.6f}\t {'' if ea is None else f'{ea:.6f}'}")

    if ea is not None and ea < es:
        break

    if fl * fr < 0:
        xu = xr
    else:
        xl = xr

    xr_old = xr

print(f"\nRaiz por falsa posicion: xr ≈ {xr:.6f}")