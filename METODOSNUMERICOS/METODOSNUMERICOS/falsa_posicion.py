import math
import re


def falsa_posicion(f, xl, xu, es=0.001, max_iter=100):
    fl, fu = f(xl), f(xu)
    if fl * fu > 0:
        raise ValueError("No hay cambio de signo en el intervalo.")

    xr = xl
    ea = None

    for i in range(1, max_iter + 1):
        xrold = xr
        xr = xu - fu * (xl - xu) / (fl - fu)
        fr = f(xr)

        if i > 1 and xr != 0:
            ea = abs((xr - xrold) / xr) * 100

        if fr == 0:
            ea = 0.0
            return xr, i, ea

        if ea is not None and ea < es:
            return xr, i, ea

        if fl * fr < 0:
            xu, fu = xr, fr
        else:
            xl, fl = xr, fr

    return xr, max_iter, ea


def falsa_pos_mod(f, xl, xu, es=0.01, imax=50):
    if imax <= 0:
        raise ValueError("imax debe ser mayor que cero.")

    iteraciones = 0
    fl, fu = f(xl), f(xu)
    if fl * fu > 0:
        raise ValueError("No hay cambio de signo en el intervalo.")

    il, iu = 0, 0
    xr = xl
    ea = None

    while True:
        xrold = xr
        xr = xu - fu * (xl - xu) / (fl - fu)
        fr = f(xr)
        iteraciones += 1

        if xr != 0:
            ea = abs((xr - xrold) / xr) * 100

        test = fl * fr

        if test < 0:
            xu, fu = xr, fr
            iu = 0
            il += 1
            if il >= 2:
                fl /= 2
        elif test > 0:
            xl, fl = xr, fr
            il = 0
            iu += 1
            if iu >= 2:
                fu /= 2
        else:
            ea = 0.0

        if (ea is not None and ea < es) or iteraciones >= imax:
            break

    return xr, iteraciones, ea


def normalizar_expresion(expr):
    expr = expr.strip().replace("^", "**")
    expr = expr.replace("sen", "sin")

    atajos = {
        "logx": "log(x)",
        "lnx": "log(x)",
        "sinx": "sin(x)",
        "cosx": "cos(x)",
        "tanx": "tan(x)",
        "sqrtx": "sqrt(x)",
        "expx": "exp(x)",
    }
    for viejo, nuevo in atajos.items():
        expr = re.sub(rf"\b{viejo}\b", nuevo, expr, flags=re.IGNORECASE)

    # Multiplicaciones implicitas comunes: 2x, )x, x(, 2(
    expr = re.sub(r"(?<=\d)(?=x\b)", "*", expr)
    expr = re.sub(r"(?<=\))(?=x\b)", "*", expr)
    expr = re.sub(r"(?<=x)(?=\()", "*", expr)
    expr = re.sub(r"(?<=\d)(?=\()", "*", expr)

    return expr


def build_function(expr):
    expr = normalizar_expresion(expr)
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    allowed_names["abs"] = abs

    def f(x):
        try:
            return eval(expr, {"__builtins__": {}}, {**allowed_names, "x": x})
        except NameError as exc:
            raise ValueError(
                "Funcion invalida. Usa notacion como log(x), sin(x), x**2 + 3*x - 1."
            ) from exc

    return f


def main():
    print("=== METODO DE FALSA POSICION ===")
    expr = input("Ingrese la funcion en terminos de x (ej: x**3 - 4*x - 9): ")
    f = build_function(expr)

    xl = float(input("Ingrese el valor de xl: "))
    xu = float(input("Ingrese el valor de xu: "))
    es = float(input("Ingrese el error permitido (%): "))
    imax = int(input("Ingrese el maximo numero de iteraciones: "))

    print("\nSeleccione metodo:")
    print("1. Falsa Posicion Normal")
    print("2. Falsa Posicion Modificada")
    op = int(input("Opcion: "))

    try:
        if op == 1:
            raiz, iteraciones, error = falsa_posicion(f, xl, xu, es, imax)
        elif op == 2:
            raiz, iteraciones, error = falsa_pos_mod(f, xl, xu, es, imax)
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
