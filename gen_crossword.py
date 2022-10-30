import sys

from PyDictionary import PyDictionary
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
from random import randint as ri
from random import choice
from english_words import english_words_lower_alpha_set

words_dict = dict()

def gen_words_dict(min_size, max_size):
    for i in range(min_size, max_size + 1):
        words_dict[i] = [x for x in english_words_lower_alpha_set if len(x) == i]
    return words_dict


def synonyms(term):
    response = requests.get('https://www.thesaurus.com/browse/{}'.format(term))
    soup = BeautifulSoup(response.text, 'lxml')
    soup.find('section', {'class': 'css-17ofzyv e1ccqdb60'})
    return [span.text for span in soup.findAll('a', {'class': 'css-1kg1yv8 eh475bn0'})]


def get_blackout_ratio(df: pd.DataFrame):
    return df.apply(pd.value_counts).loc['X'].sum()/df.size

def word_select(word_len, index):
    try:
        dictionary = PyDictionary()
        if isinstance(word_len, int):
            word = words_dict[word_len][ri(0, len(words_dict[word_len]))]
        else:
            word = word_len
        length= len(word)
        print(f"Word is {word}")
        meaning_dict = dictionary.meaning(word)
        if not meaning_dict:
            return word_select(length, words_dict)
        mean_keys = list(meaning_dict)
        desc = f"{str(index)}.{choice(meaning_dict.get(choice(mean_keys)))}"
        syn_list = synonyms(word)
        if syn_list:
            desc += f",{choice(syn_list).strip()}"
        desc += f"({len(word)})"
        # print(desc)
        return desc
    except:
        print("Unable to select word with the specified length")


def create_cross_word(size: int, blackout_ratio: float, min_word_len=2):
    if size <= 4:
        print("Cannot create such a small crossword. Select a bigger size")
        sys.exit()

    cw = pd.DataFrame(columns=list(range(0, size)), index=list(range(0, size))).fillna('X')
    horizantal = dict()
    vertical = dict()
    words_dict = gen_words_dict(min_word_len, size)

    # print(cw.to_string(index=False, col_space=5))

    cw, selected, desc = add_word_to_index(cw, 0, [], 'H', size-2)
    cw, selected, desc = add_word_to_index(cw, 0, [], 'V', size - 2)


    print(cw)
    print(desc)
    print(get_blackout_ratio(cw))


def add_word_to_index(df, index, selected,direction,max_length):
    word = choice(words_dict[ri(2, max_length)])
    desc = word_select(word, 1)
    selected.append(word)
    for i, c in enumerate(word,start=index):
        if direction == 'H':
            df.iloc[index, i] = c
        else:
            df.iloc[i, index] = c

    return df, selected, desc



#
#

create_cross_word(8, 1, 1)
# print(english_words_lower_alpha_set)
