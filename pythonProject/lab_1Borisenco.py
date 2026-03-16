
import math
import time


def f1(x):
    return 2**x + x**2 - 6*math.sin(2*x)


def f2(x):
    return (x**6 - 1.8*x**5 - 18.87*x**4 + 17.06*x**3 +117.533*x**2 - 14.2296*x - 182.613)


def df(func, x):
    h = 1e-6
    return (func(x + h) - func(x - h)) / (2 * h)


def findDiapazon(func, a, b):
    intervals = []
    step = 0.2
    x = a
    while x < b:
        if func(x) * func(x + step) < 0:
            intervals.append((x, x + step))
        x += step

    print("Найденные интервалы:", intervals)
    return intervals


def bisection(func, intervals, eps):
    results = []
    for (a, b) in intervals:
        start_time = time.perf_counter()
        iterations = 0

        while (b - a) / 2 > eps:
            iterations += 1
            c = (a + b) / 2

            if abs(func(c)) < eps:
                a = b = c
                break

            if func(a) * func(c) < 0:
                b = c
            else:
                a = c

        root = (a + b) / 2
        elapsed = time.perf_counter() - start_time
        results.append((root, iterations, elapsed))
    return results


def chord(func, intervals, eps):
    results = []
    for (a, b) in intervals:
        start_time = time.perf_counter()
        iterations = 0

        while True:
            iterations += 1
            xNew = a - func(a) * (b - a) / (func(b) - func(a))

            if abs(func(xNew)) < eps:
                break

            if func(a) * func(xNew) < 0:
                b = xNew
            else:
                a = xNew

        elapsed = time.perf_counter() - start_time
        results.append((xNew, iterations, elapsed))
    return results


def newton(func, intervals, eps, maxIter=1000):
    results = []
    for (a, b) in intervals:
        start_time = time.perf_counter()
        iterations = 0
        x = (a + b) / 2

        for _ in range(maxIter):
            iterations += 1
            fx = func(x)
            dfx = df(func, x)

            if abs(dfx) < 1e-12:
                break

            xNew = x - fx / dfx

            if xNew < a or xNew > b:
                break

            if abs(func(xNew)) < eps:
                x = xNew
                break

            x = xNew

        elapsed = time.perf_counter() - start_time
        results.append((x, iterations, elapsed))
    return results


def simpleIter(func, intervals, eps, maxIter=1000):
    results = []
    for (a, b) in intervals:
        start_time = time.perf_counter()
        iterations = 0

        maxDf = 0.0
        steps = 100

        for i in range(steps):
            xi = a + (b - a) * i / steps
            maxDf = max(maxDf, abs(df(func, xi)))

        if maxDf == 0:
            maxDf = 1.0

        lam = 1.0 / maxDf
        if df(func, a) < 0:
            lam = -lam

        x = (a + b) / 2

        for _ in range(maxIter):
            iterations += 1
            xNew = x - lam * func(x)

            if xNew < a or xNew > b:
                break

            if abs(xNew - x) < eps:
                x = xNew
                break

            x = xNew

        elapsed = time.perf_counter() - start_time
        results.append((x, iterations, elapsed))
    return results



def run_for_function(func, func_name, a, b, eps):
    print(f"Функция: {func_name}")

    intervals = findDiapazon(func, a, b)

    methods = [
        ("Метод дихотомии", bisection),
        ("Метод хорд", chord),
        ("Метод Ньютона", newton),
        ("Метод простой итерации", simpleIter)
    ]

    for name, method in methods:
        print("\n" + "=" * 50)
        print(name)

        results = method(func, intervals, eps)

        for i, (root, iterations, elapsed) in enumerate(results, 1):
            print(f"\nКорень {i}: \033[32m {root}\033[0m ")
            print(f"Итераций: {iterations}")
            print(f"Время: {elapsed:.8f} сек")



def main():

    eps = 1e-6

    print("\nВведите диапазон для функции 1")
    left1 = float(input("Левая граница: "))
    right1 = float(input("Правая граница: "))

    run_for_function(
        f1,
        "2^x + x^2 - 6*sin(2x)",
        left1,
        right1,
        eps
    )

    print("\nВведите диапазон для функции 2")
    left2 = float(input("Левая граница: "))
    right2 = float(input("Правая граница: "))

    run_for_function(
        f2,
        "Полином 6 степени",
        left2,
        right2,
        eps
    )


main()