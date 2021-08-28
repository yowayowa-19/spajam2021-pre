import random
from collections import Counter

characters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
              'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']


def generate() -> str:
    result = random.choices(characters, k=5)
    while Counter(result).most_common(1)[0][1] == 5:
        # Counter('abracadabra').most_common(3)
        #     [('a', 5), ('b', 2), ('r', 2)]
        result = random.choices(characters, k=5)
    return ''.join(result)


# score
NYARN = 1000
FOURCARD = 700
FULLHOUSE = 600
THREECARD = 500
STRAIGHT = 400
TWOPAIR = 300
ONEPAIR = 200


def score(phrase: str) -> int:
    if phrase == 'NYARN':
        return NYARN
    # base score
    result = sum(map(ord, phrase)) - ord('A') * 5
    counts = [item[1] for item in Counter(phrase).most_common()]
    if len(counts) == 2:
        if counts[0] == 4:
            result += FOURCARD
        else:
            result += FULLHOUSE
    if counts[0] == 3:
        if max(counts) == 3:
            result += THREECARD
        else:
            result += TWOPAIR
    if len(counts) == 4:
        result += ONEPAIR
    if len(counts) == 5:
        if [ord(p)-ord(phrase[0]) for p in phrase] == [0, 1, 2, 3, 4]:
            result += STRAIGHT
    return result
