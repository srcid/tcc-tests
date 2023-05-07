from numpy.random import randint, shuffle


def gen_random_mcsp_instance(n: int):
    S1 = randint(1,5,n)
    S2 = S1.copy()
    shuffle(S2)

    return ''.join(map(str, S1)), ''.join(map(str,S2))
