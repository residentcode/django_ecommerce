import random
import string


def random_num(rng):
    random_number = ''.join(random.SystemRandom().choice(string.digits) for _ in range(rng))
    return random_number
