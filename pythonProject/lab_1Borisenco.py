import math

def f1(x):
    return 2**x + x**2 - 6*math.sin(2*x)

def f2(x):
    return (x**6 - 1.8*x**5 - 18.87*x**4 +17.06*x**3 + 117.533*x**2 -14.2296*x - 182.613)


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
    print(intervals)
    return intervals

def bisection(func, intervals, eps):
    roots = []
    for (a, b) in intervals:
        while (b - a) / 2 > eps:
            c = (a + b) / 2
            if abs(func(c)) < eps:
                break
            if func(a) * func(c) < 0:
                b = c
            else:
                a = c
        roots.append((a + b) / 2)
    return roots


def chord(func, intervals, eps):
    roots = []
    for (a, b) in intervals:
        while True:
            xNew = a - func(a)*(b - a)/(func(b) - func(a))
            if abs(func(xNew)) < eps:
                break
            if func(a) * func(xNew) < 0:
                b = xNew
            else:
                a = xNew
        roots.append(xNew)

    return roots

def newton(func, intervals, eps, maxIter=1000):
    roots = []

    for (a, b) in intervals:
        x = (a + b) / 2
        for i in range(maxIter):
            fx = func(x)
            dfx = df(func, x)
            if abs(dfx) < 1e-12:
                break
            xNew = x - fx / dfx
            if xNew < a or xNew > b:
                break
            if abs(func(xNew)) < eps:
                roots.append(xNew)
                break
            x = xNew
    return roots


def simpleIter(func, intervals, eps, maxIter=1000):
    roots = []
    for (a, b) in intervals:
        maxDf = 0.0
        steps = 100
        for i in range(steps):
            xi = a + (b - a) * i / steps
            dfValue = abs(df(func, xi))
            if dfValue > maxDf:
                maxDf = dfValue
        if maxDf == 0:
            maxDf = 1.0
        lam = 1.0 / maxDf
        if df(func, a) < 0:
            lam = -lam
        x = (a + b) / 2
        for i in range(maxIter):
            xNew = x - lam * func(x)
            if xNew < a or xNew > b:
                break
            if abs(xNew - x) < eps:
                roots.append(xNew)
                break
            x = xNew
    return roots

def main():

    while True:
        funcChoice = input("Выберите функцию:\n1 - 2^x + x^2 - 6*sin(2x)\n2 - x**6 - 1.8*x**5 - 18.87*x**4 +17.06*x**3 + 117.533*x**2 -14.2296*x - 182.613\n Ваш выбор: ")

        if funcChoice == "1":
            func = f1
        elif funcChoice == "2":
            func = f2
        else:
            print("Неверный выбор")
            continue

        leftLimit = float(input("Введите левую границу: "))
        rightLimit = float(input("Введите правую границу: "))
        eps = 10e-6

        intervals = findDiapazon(func, leftLimit, rightLimit)

        while True:
            method = input("введите номер метода для счета.\nВыберите метод:\n1 – дихотомия (половинное деление)\n2 – метод хорд\n3 – метод Ньютона\n4 – метод простой итерации\n5 - Выйти из программы ")

            if method == "1":
                roots = bisection(func, intervals, eps)
                print("Метод дихотомии (половинное деление)")
            elif method == "2":
                roots = chord(func, intervals, eps)
                print("Метод хорд")
            elif method == "3":
                roots = newton(func, intervals, eps)
                print("Метод Ньютона")
            elif method == "4":
                roots = simpleIter(func, intervals, eps)
                print("Метод простой итерации")
            elif method == "5":

                print("Возвращается в меню")
                break
            else:
                print("Неверный метод")
                continue

            print("\nНайденные корни:")
            for r in roots:
                print(r)

main()
