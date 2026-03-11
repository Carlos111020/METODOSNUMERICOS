import math

# Datos
R = 3.0          # m
V_obj = 30.0     # m^3

def V(h):
    return (math.pi * h**2 * (3*R - h)) / 3.0

def f(h):
    return V(h) - V_obj

# Intervalo inicial
xl = 0.0
xu = R

print("PUNTO 3 - Tanque esferico (Falsa Posicion) - 3 iteraciones")
print("i\t xl\t\t xu\t\t xr\t\t f(xr)\t\t ea(%)")

xr_old = None

for i in range(1, 4):  # 3 iteraciones
    fl = f(xl)
    fu = f(xu)

    xr = xu - fu * (xl - xu) / (fl - fu)
    fr = f(xr)

    ea = None
    if xr_old is not None:
        ea = abs((xr - xr_old) / xr) * 100

    print(f"{i}\t {xl:.6f}\t {xu:.6f}\t {xr:.6f}\t {fr:.6f}\t {'' if ea is None else f'{ea:.6f}'}")

    # Actualizar intervalo
    if fl * fr < 0:
        xu = xr
    else:
        xl = xr

    xr_old = xr

print("\nAproximacion despues de 3 iteraciones:")
print(f"h ≈ {xr:.6f} m")
print(f"V(h) ≈ {V(xr):.6f} m^3")