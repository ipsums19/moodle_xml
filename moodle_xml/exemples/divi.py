def f(a, b):
    if a >= b:
        (q, r) = f(a - b, b)
        r = (q + 1, r)
    else:
        r = (0, a)
    return r
