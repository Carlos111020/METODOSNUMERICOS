from falsa_posicion import build_function, falsa_posicion


def evaluar_seguro(func, x, etiqueta):
    try:
        return func(x)
    except ValueError as exc:
        raise ValueError(
            f"Error de dominio al evaluar {etiqueta} en x={x}. "
            "Pruebe otros valores iniciales dentro del dominio de la funcion."
        ) from exc


def secante(f, x_prev, x_curr, es=0.01, max_iter=100):
    if x_prev == x_curr:
        raise ValueError("En secante, x_-1 y x_0 deben ser distintos.")

    f_prev = evaluar_seguro(f, x_prev, "f(x_-1)")
    f_curr = evaluar_seguro(f, x_curr, "f(x_0)")
    if f_prev == f_curr:
        raise ValueError("En secante, f(x_-1) y f(x_0) no pueden ser iguales.")

    for i in range(1, max_iter + 1):
        denom = f_curr - f_prev
        if abs(denom) < 1e-15:
            raise ValueError("Secante indeterminada: f(x_i)-f(x_{i-1}) es cero.")

        x_new = x_curr - f_curr * (x_curr - x_prev) / denom
        ea = None if x_new == 0 else abs((x_new - x_curr) / x_new) * 100
        f_new = evaluar_seguro(f, x_new, f"f(x) en iteracion {i}")

        if f_new == 0:
            return x_new, i, 0.0
        if ea is not None and ea < es:
            return x_new, i, ea

        x_prev, x_curr = x_curr, x_new
        f_prev, f_curr = f_curr, f_new

    return x_new, max_iter, ea


def secante_historial(f, x_prev, x_curr, es=0.01, max_iter=100):
    historial = []

    if x_prev == x_curr:
        return {
            "estado": "invalido",
            "mensaje": "x_-1 y x_0 son iguales.",
            "historial": historial,
        }

    try:
        f_prev = evaluar_seguro(f, x_prev, "f(x_-1)")
        f_curr = evaluar_seguro(f, x_curr, "f(x_0)")
    except ValueError as exc:
        return {"estado": "dominio", "mensaje": str(exc), "historial": historial}

    if f_prev == f_curr:
        return {
            "estado": "invalido",
            "mensaje": "f(x_-1) y f(x_0) son iguales.",
            "historial": historial,
        }

    ea = None
    x_new = x_curr

    for i in range(1, max_iter + 1):
        denom = f_curr - f_prev
        if abs(denom) < 1e-15:
            return {
                "estado": "indeterminada",
                "mensaje": "f(x_i)-f(x_{i-1}) es cero o muy pequeno.",
                "iteraciones": i - 1,
                "raiz": x_curr,
                "error": ea,
                "historial": historial,
            }

        x_new = x_curr - f_curr * (x_curr - x_prev) / denom
        ea = None if x_new == 0 else abs((x_new - x_curr) / x_new) * 100

        try:
            f_new = evaluar_seguro(f, x_new, f"f(x) en iteracion {i}")
        except ValueError:
            return {
                "estado": "diverge_dominio",
                "iteraciones": i,
                "x_problematico": x_new,
                "historial": historial,
            }

        historial.append((i, x_new, ea))

        if f_new == 0:
            return {
                "estado": "convergio",
                "iteraciones": i,
                "raiz": x_new,
                "error": 0.0,
                "historial": historial,
            }
        if ea is not None and ea < es:
            return {
                "estado": "convergio",
                "iteraciones": i,
                "raiz": x_new,
                "error": ea,
                "historial": historial,
            }

        x_prev, x_curr = x_curr, x_new
        f_prev, f_curr = f_curr, f_new

    return {
        "estado": "max_iter",
        "iteraciones": max_iter,
        "raiz": x_new,
        "error": ea,
        "historial": historial,
    }


def derivada_numerica(f, x, h=1e-6):
    fxh = evaluar_seguro(f, x + h, f"f(x+h) con x={x}")
    fxmh = evaluar_seguro(f, x - h, f"f(x-h) con x={x}")
    return (fxh - fxmh) / (2 * h)


def newton_raphson(f, x0, es=0.01, max_iter=100, df=None):
    xr = x0

    for i in range(1, max_iter + 1):
        fx = evaluar_seguro(f, xr, f"f(x) en iteracion {i}")
        if df is not None:
            dfx = evaluar_seguro(df, xr, f"f'(x) en iteracion {i}")
        else:
            dfx = derivada_numerica(f, xr)

        if dfx == 0:
            raise ValueError("Derivada cero en Newton-Raphson.")

        x_new = xr - fx / dfx
        ea = None if x_new == 0 else abs((x_new - xr) / x_new) * 100
        fx_new = evaluar_seguro(f, x_new, f"f(x) en iteracion {i}")

        if fx_new == 0:
            return x_new, i, 0.0
        if ea is not None and ea < es:
            return x_new, i, ea

        xr = x_new

    return xr, max_iter, ea


def falsa_posicion_historial(f, xl, xu, es=0.01, max_iter=100):
    fl = evaluar_seguro(f, xl, "f(xl)")
    fu = evaluar_seguro(f, xu, "f(xu)")

    if fl * fu > 0:
        raise ValueError("No hay cambio de signo para Falsa Posicion en [xl, xu].")

    historial = []
    xr = xl
    ea = None

    for i in range(1, max_iter + 1):
        denom = fl - fu
        if abs(denom) < 1e-15:
            return {
                "estado": "indeterminada",
                "iteraciones": i - 1,
                "raiz": xr,
                "error": ea,
                "historial": historial,
            }

        xrold = xr
        xr = xu - fu * (xl - xu) / denom
        fr = evaluar_seguro(f, xr, f"f(xr) en iteracion {i}")

        if i > 1 and xr != 0:
            ea = abs((xr - xrold) / xr) * 100

        historial.append((i, xr, ea))

        if fr == 0:
            return {
                "estado": "convergio",
                "iteraciones": i,
                "raiz": xr,
                "error": 0.0,
                "historial": historial,
            }
        if ea is not None and ea < es:
            return {
                "estado": "convergio",
                "iteraciones": i,
                "raiz": xr,
                "error": ea,
                "historial": historial,
            }

        if fl * fr < 0:
            xu, fu = xr, fr
        else:
            xl, fl = xr, fr

    return {
        "estado": "max_iter",
        "iteraciones": max_iter,
        "raiz": xr,
        "error": ea,
        "historial": historial,
    }


def pedir_funcion(mensaje):
    expr = input(mensaje)
    return expr, build_function(expr)


def mostrar_comparacion(expr, f, x_prev, x_curr, es, imax):
    xl = min(x_prev, x_curr)
    xu = max(x_prev, x_curr)

    res_fp = falsa_posicion_historial(f, xl, xu, es, imax)
    res_sec = secante_historial(f, x_prev, x_curr, es, imax)

    print("\n=== COMPARACION DE METODOS ===")
    print(f"Funcion: f(x) = {expr}")
    print(f"Valores iniciales: x_-1 = {x_prev}, x_0 = {x_curr}")

    print("\nFalsa Posicion:")
    for i, xr, _ in res_fp["historial"]:
        print(f" - Iteracion {i}: xr = {xr:.6f}")
    if res_fp["estado"] == "convergio":
        print(f" - Converge a x ~ {res_fp['raiz']:.6f}")
    elif res_fp["estado"] == "max_iter":
        print(" - No convergio dentro del maximo de iteraciones.")
    else:
        print(" - Se detuvo por condicion numerica.")

    print("\nSecante:")
    for i, xk, _ in res_sec.get("historial", []):
        print(f" - Iteracion {i}: x{i} = {xk:.6f}")
    if res_sec["estado"] == "convergio":
        print(f" - Converge a x ~ {res_sec['raiz']:.6f}")
    elif res_sec["estado"] == "diverge_dominio":
        i = res_sec["iteraciones"]
        x_bad = res_sec["x_problematico"]
        print(f" - Iteracion {i}: x{i} = {x_bad:.6f} (diverge por dominio)")
    elif res_sec["estado"] == "max_iter":
        print(" - No convergio dentro del maximo de iteraciones.")
    else:
        print(f" - Se detuvo: {res_sec.get('mensaje', 'condicion numerica')}")

    print("\nConclusion:")
    if res_fp["estado"] == "convergio" and res_sec["estado"] == "convergio":
        if res_sec["iteraciones"] < res_fp["iteraciones"]:
            print("La secante convergio mas rapido en este caso.")
        elif res_sec["iteraciones"] > res_fp["iteraciones"]:
            print("Falsa Posicion convergio con menos iteraciones en este caso.")
        else:
            print("Ambos metodos convergieron con el mismo numero de iteraciones.")
    elif res_fp["estado"] == "convergio" and res_sec["estado"] != "convergio":
        print("La secante puede divergir; falsa posicion es mas robusta pero suele ser mas lenta.")
    elif res_fp["estado"] != "convergio" and res_sec["estado"] == "convergio":
        print("La secante convergio y falsa posicion no convergio en el limite dado.")
    else:
        print("Ninguno convergio con los datos y limites actuales.")


def main():
    print("=== METODOS ABIERTOS ===")
    print("Nota: Falsa Posicion es un metodo cerrado; se incluye para comparar.")

    expr, f = pedir_funcion("Ingrese la funcion f(x) (ej: x**3 - 4*x - 9, logx): ")
    es = float(input("Ingrese el error permitido (%): "))
    imax = int(input("Ingrese el maximo numero de iteraciones: "))

    print("\nSeleccione metodo:")
    print("1. Secante (abierto)")
    print("2. Newton-Raphson con derivada numerica (abierto)")
    print("3. Newton-Raphson con derivada ingresada (abierto)")
    print("4. Falsa Posicion (cerrado, comparacion)")
    print("5. Comparacion Falsa Posicion vs Secante (estilo ejercicio)")
    op = int(input("Opcion: "))

    try:
        if op == 1:
            while True:
                x_prev = float(input("Ingrese x_-1: "))
                x_curr = float(input("Ingrese x_0: "))
                if x_prev == x_curr:
                    print("x_-1 y x_0 no pueden ser iguales. Ingreselos de nuevo.")
                    continue
                f_prev = evaluar_seguro(f, x_prev, "f(x_-1)")
                f_curr = evaluar_seguro(f, x_curr, "f(x_0)")
                if f_prev == f_curr:
                    print("f(x_-1) y f(x_0) son iguales. Ingrese otros valores.")
                    continue
                break
            raiz, iteraciones, error = secante(f, x_prev, x_curr, es, imax)
        elif op == 2:
            x0 = float(input("Ingrese x0: "))
            raiz, iteraciones, error = newton_raphson(f, x0, es, imax)
        elif op == 3:
            x0 = float(input("Ingrese x0: "))
            _, df = pedir_funcion("Ingrese la derivada f'(x): ")
            raiz, iteraciones, error = newton_raphson(f, x0, es, imax, df=df)
        elif op == 4:
            xl = float(input("Ingrese xl: "))
            xu = float(input("Ingrese xu: "))
            raiz, iteraciones, error = falsa_posicion(f, xl, xu, es, imax)
        elif op == 5:
            x_prev = float(input("Ingrese x_-1: "))
            x_curr = float(input("Ingrese x_0: "))
            mostrar_comparacion(expr, f, x_prev, x_curr, es, imax)
            return
        else:
            raise ValueError("Opcion invalida.")

        print("\n=== RESULTADOS ===")
        print(f"Raiz aproximada: {raiz}")
        print(f"Iteraciones: {iteraciones}")
        if error is None:
            print("Error aproximado: N/A")
        else:
            print(f"Error aproximado: {error}%")
    except Exception as e:
        print("Error:", e)


if __name__ == "__main__":
    main()
