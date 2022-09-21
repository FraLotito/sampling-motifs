from scipy.stats import weightedtau

def mean_absolute_error(a, b):
    s = 0
    for i in range(len(a)):
        a_i = a[i]
        b_i = b[i]
        s += abs(a_i - b_i)
    return s / len(a)

def max_absolute_error(a, b):
    m = 0
    for i in range(len(a)):
        a_i = a[i]
        b_i = b[i]
        e = abs(a_i - b_i)
        if e > m:
            m = e
    return m

def mean_relative_error(a, b):
    s = 0
    for i in range(len(a)):
        a_i = a[i]
        b_i = b[i]
        s += (abs(a_i - b_i) / (a_i+1))
    return s / len(a)

def max_relative_error(a, b):
    m = 0
    for i in range(len(a)):
        a_i = a[i]
        b_i = b[i]
        e = (abs(a_i[1] - b_i[1]) / (a_i[1]+1))
        if e > m:
            m = e
    return m

def kendall(a, b):
    a = [i[1] for i in a]
    b = [i[1] for i in b]
    A = []
    B = []
    for i in range(len(a)):
        if a[i] > 0:
            A.append(a[i])
            B.append(b[i])
    res, _ = weightedtau(A, B)
    return res


