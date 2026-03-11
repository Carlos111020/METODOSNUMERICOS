import math


def biseccion_mejorada(f, xl, xu, es=0.01, max_iter=100):
    fl, fu = f(xl), f(xu)
    if fl * fu > 0:
        raise ValueError("No hay cambio de signo en el intervalo.")

    xr = xl
    ea = None

    for i in range(1, max_iter + 1):
        xrold = xr
        xr = (xl + xu) / 2
        fr = f(xr)

        if i > 1 and xr != 0:
            ea = abs((xr - xrold) / xr) * 100

        if fr == 0 or (ea is not None and ea < es):
            return xr, i, ea

        if fl * fr < 0:
            xu, fu = xr, fr
        else:
            xl, fl = xr, fr

    return xr, max_iter, ea


def build_function(expr):
    allowed_names = {name: getattr(math, name) for name in dir(math) if not name.startswith("_")}
    allowed_names["abs"] = abs
    return lambda x: eval(expr, {"__builtins__": {}}, {**allowed_names, "x": x})


print("=== METODO DE BISECCION MEJORADA ===")
expr = input("Ingrese la funcion en terminos de x (ej: x**3 - 4*x - 9): ")
f = build_function(expr)

try:
    xl = float(input("Ingrese el valor de xl: "))
    xu = float(input("Ingrese el valor de xu: "))
    es = float(input("Ingrese el error permitido (%): "))
    max_iter = int(input("Ingrese el maximo numero de iteraciones: "))

    raiz, iteraciones, error = biseccion_mejorada(f, xl, xu, es, max_iter)

    print("\n=== RESULTADOS ===")
    print(f"Raiz aproximada: {raiz}")
    print(f"Iteraciones: {iteraciones}")
    print(f"Error aproximado: {error}%")
except Exception as e:
    print("Error:", e)
