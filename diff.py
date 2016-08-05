import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x] ** 2 for x in vec1.keys()])
     sum2 = sum([vec2[x] ** 2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
         return 0.0
     else:
        return float(numerator) / denominator


def text_to_vector(text):
    print (text)
    words = WORD.findall(text)
    return Counter(words)




def calculate_cosine(sen, senArray):
    similiar = 0
    vector1 = text_to_vector(sen)
    for sentence in senArray:
        vector2 = text_to_vector(str(sentence))
        cosine = get_cosine(vector1, vector2)
        if (cosine > similiar):
            similiar = cosine
        #print('Cosine:', cosine)
    return similiar

def calculate_cosine_for_song(song, lyrics):

    sum = 0

    for row in song:
        print (row)
        max = calculate_cosine(str(row), lyrics)
        print (row + " : " + str(max))
        sum += max

    return sum / len(song)





