import itertools
import nltk
import numpy as np

from Crawler import get_lyrics

unknown_token = "UNKNOWN_TOKEN"
sentence_start_token = "SENTENCE_START"
song_start_token = "SONG_START"
song_end_token = "SONG_END"
sentence_end_token = "SENTENCE_END"



def insert_special_token(songs_lyric_list):
    song_with_special_token = []
    for song in songs_lyric_list:
        counter = 0
        first = True
        sentences_with_special_token = []
        for sentence in song:
            counter += 1
            last = counter == len(song)

            try:
                s = str(sentence)
                if "{" in s or "}" in s or "[" in s or "]" in s or "(" in s or ")" in s:
                    continue
                else:
                    if first:
                        sentences_with_special_token.append(song_start_token + " " + sentence_start_token +
                                                            " " + s + " " + sentence_end_token)
                        first = False
                    else:
                        if not last:
                            sentences_with_special_token.append(sentence_start_token +
                                                            " " + s + " " + sentence_end_token)
                        else:
                            sentences_with_special_token.append(sentence_start_token + " " + s + " " + sentence_end_token + " " + song_end_token)
            except ValueError:
                continue
        song_with_special_token.append(sentences_with_special_token)
    return song_with_special_token


def tokenize_song_to_word(songs):
    tokenized_sentences = []
    for song in songs:
        for sent in song:
            tokenized_sentences.append(nltk.word_tokenize(sent))
    return tokenized_sentences


def create_vocabulary(size, tokenized_sentences):
    word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    print "Found %d unique words tokens." % len(word_freq.items())
    vocab = word_freq.most_common(size - 1)
    return vocab

def map_index_to_word(vocabulary):
    index_to_word = [x[0] for x in vocabulary]
    return index_to_word

def map_word_to_index(index_to_word):
    index_to_word.append(unknown_token)
    word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])
    return word_to_index


def replace_word_not_in_vocabulary(word_to_index, songs):
    for i, sent in enumerate(songs):
        songs[i] = [w if w in word_to_index else unknown_token for w in sent]

def get_x_train (songs, word_to_index):
    X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in songs])
    return X_train

def get_y_train (songs, word_to_index):
    y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in songs])
    return y_train



