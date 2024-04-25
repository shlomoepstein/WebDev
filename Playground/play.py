def test_1():
    def factorials():
        n, f = 0, 1
        while True:
            yield f
            n, f = n + 1, f * (n + 1)

    'INFINITE POWAHH!!'
    for n in factorials():
        print(n)

def test_2():
    def infinite_sequence():
        num = 0
        while True:
            yield num
            num += 1

    for i in infinite_sequence():
        print(i)

test_2()
