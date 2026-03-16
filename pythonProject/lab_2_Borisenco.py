import math
import time

A = [
    [3.738, 0.195, 0.275, 0.136],
    [0.519, 5.002, 0.405, 0.283],
    [0.306, 0.381, 4.812, 0.418],
    [0.272, 0.142, 0.314, 3.935]
]

b = [0.815, 0.191, 0.423, 0.352]
eps = 1e-6
maxIter = 1000


def checkDominateElement():

    numOfVariables = len(A)
    dominantColumns = set()

    for i in range(numOfVariables):

        row = A[i]
        maxElem = abs(max(row, key=abs))
        maxIndex = row.index(maxElem)

        sumOther = 0
        for j in range(numOfVariables):
            if j != maxIndex:
                sumOther += abs(row[j])

        if maxElem <= sumOther:
            print("В строке", i + 1, "нет доминантного элемента\nМетод Якоби не гарантирует сходимость.")
            return False

        dominantColumns.add(maxIndex)

    if len(dominantColumns) < numOfVariables:
        print("Доминантные элементы находятся в одинаковых колонках.\n Метод Якоби не сходится")
        return False

    print("Проверка на доминирующий элемент пройдена")
    return True


def iterJacobi(i, xOld):

    row = A[i]

    summ = 0
    for elem in range(len(row)):
        if elem != i:
            summ += row[elem] * xOld[elem]

    return (b[i] - summ) / row[i]


def jacobi():

    n = len(A)
    xOld = [0] * n

    startTime = time.perf_counter()

    for iteration in range(maxIter):

        xNew = [0] * n

        for i in range(n):
            xNew[i] = iterJacobi(i, xOld)

        maxDiff = 0

        for i in range(n):
            diff = abs(xNew[i] - xOld[i])
            if diff > maxDiff:
                maxDiff = diff

        if maxDiff < eps:

            endTime = time.perf_counter()
            workTime = endTime - startTime

            return xNew, iteration + 1, workTime

        xOld = xNew

    print("Метод Якоби не сошёлся")
    return None


if checkDominateElement():

    result = jacobi()

    if result:

        x, iterations, timeWork = result

        print("\nРезультат:")
        print("x1 =", x[0])
        print("x2 =", x[1])
        print("x3 =", x[2])
        print("x4 =", x[3])

        print("\nСтатистика работы метода:")
        print(f"\033[32mКоличество итераций:  {iterations}\033[0m  ")
        print(f"\033[32mВремя выполнения:{timeWork}секунд\033[0m ")