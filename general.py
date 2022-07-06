import random
import string


def random_num(rng):
    rang_number = ''.join(random.SystemRandom().choice(string.digits) for _ in range(rng))
    return rang_number
