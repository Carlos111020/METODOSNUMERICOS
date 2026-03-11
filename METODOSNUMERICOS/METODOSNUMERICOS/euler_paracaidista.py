import numpy as np
import matplotlib.pyplot as plt


def euler_parachutist(m, c, g, dt, v0, t_final):
    if m == 0:
        raise ValueError("La masa m no puede ser cero.")
    if dt <= 0:
        raise ValueError("El paso dt debe ser mayor que cero.")
    if t_final < 0:
        raise ValueError("El tiempo final debe ser mayor o igual a cero.")

    n_steps = int(np.ceil(t_final / dt))
    t = np.linspace(0, n_steps * dt, n_steps + 1)
    v = np.zeros_like(t, dtype=float)
    v[0] = v0

    for i in range(n_steps):
        dvdt = g - (c / m) * v[i]
        v[i + 1] = v[i] + dvdt * dt

    return t, v


def main():
    m = float(input("Masa m [kg]: "))
    c = float(input("Coeficiente de arrastre c [kg/s]: "))
    g_in = input("Gravedad g [m/s^2] (Enter = 9.81): ")
    g = float(g_in) if g_in else 9.81
    dt = float(input("Paso de tiempo dt [s]: "))
    v0 = float(input("Velocidad inicial v0 [m/s]: "))
    t_final = float(input("Tiempo final [s]: "))

    t, v = euler_parachutist(m, c, g, dt, v0, t_final)

    print("\n t (s)   v (m/s)")
    print("-" * 22)
    for ti, vi in zip(t, v):
        print(f"{ti:7.2f} {vi:8.2f}")

    plt.plot(t, v, marker="o")
    plt.title("Velocidad del paracaidista (Metodo de Euler)")
    plt.xlabel("t (s)")
    plt.ylabel("v (m/s)")
    plt.grid()
    plt.show()


if __name__ == "__main__":
    main()
