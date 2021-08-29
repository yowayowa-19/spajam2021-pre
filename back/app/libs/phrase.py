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
NYARN = (1000, "にゃーん")
FOURCARD = (700, "フォーカード")
FULLHOUSE = (600, "フルハウス")
THREECARD = (500, "スリーカード")
STRAIGHT = (400, "ストレート")
TWOPAIR = (300, "ツーペア")
ONEPAIR = (200, "ワンペア")


def score(phrase: str) -> tuple[int, str]:
    if phrase == 'NYARN':
        return NYARN
    # base score
    result = (sum(map(ord, phrase)) - (ord('A')-1) * 5, "ノーペア")
    counts = [item[1] for item in Counter(phrase).most_common()]
    if len(counts) == 2:
        if counts[0] == 4:
            result = result[0] + FOURCARD[0], FOURCARD[1]
        else:
            result = result[0] + FULLHOUSE[0], FULLHOUSE[1]
    if counts[0] == 3:
        if max(counts) == 3:
            result = result[0] + THREECARD[0], THREECARD[1]
        else:
            result = result[0] + TWOPAIR[0], TWOPAIR[1]
    if len(counts) == 4:
        result = result[0] + ONEPAIR[0], ONEPAIR[1]
    if len(counts) == 5:
        if [ord(p)-ord(phrase[0]) for p in phrase] == [0, 1, 2, 3, 4]:
            result = result[0] + STRAIGHT[0], STRAIGHT[1]
    return result
