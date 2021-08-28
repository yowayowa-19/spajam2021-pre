import random
from collections import Counter

characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def generate_phrase() -> str:
    result = random.choices(characters, k=5)
    while Counter(result).most_common(1)[0][1] == 5:
        # Counter('abracadabra').most_common(3)
        #     [('a', 5), ('b', 2), ('r', 2)]
        result = random.choices(characters, k=5)
    return ''.join(result)
