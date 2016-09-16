def pgeo(a, r):
    t = a
    while True:
        yield t
        t = t * r

g = pgeo(10, 3)
