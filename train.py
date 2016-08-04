import csv
import itertools
import operator
import numpy as np
import nltk
import sys
import os
import time
from datetime import datetime
from model_manager import *
from RNN import RNN
from Tokenizer import *

_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '2000'))
_HIDDEN_DIM = int(os.environ.get('HIDDEN_DIM', '80'))
_LEARNING_RATE = float(os.environ.get('LEARNING_RATE', '0.005'))
_NEPOCH = int(os.environ.get('NEPOCH', '20'))
_MODEL_FILE = os.environ.get('MODEL_FILE')


def train_with_sgd(model, X_train, y_train, learning_rate=0.005, nepoch=1, evaluate_loss_after=5):
    # We keep track of the losses so we can plot them later
    losses = []
    # we not train the data yet
    num_examples_seen = 0
    # start to train the model, each time we want to minimize the error more
    for epoch in range(nepoch):
        # Optionally evaluate the loss, every evaluate_loss_after
        if (epoch % evaluate_loss_after == 0):
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
            print "%s: Loss after num_examples_seen=%d epoch=%d: %f" % (time, num_examples_seen, epoch, loss)
            # Adjust the learning rate if loss increases
            if (len(losses) > 1 and losses[-1][1] > losses[-2][1]):
                learning_rate = learning_rate * 0.5
                print "Setting learning rate to %f" % learning_rate
            sys.stdout.flush()
            # ADDED! Saving model oarameters
            save_model_parameters_theano("./data/rnn-theano-%d-%d-%s.npz" % (model.hidden_dim, model.word_dim, time),
                                         model)
        # For each training example...
        for i in range(len(y_train)):
            # One SGD step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1
            print (i)

        print (epoch)




def getModel (tokenized_sentences,word_to_index):


    x_train = get_x_train(tokenized_sentences, word_to_index)
    y_train = get_y_train(tokenized_sentences, word_to_index)

    model = RNN(_VOCABULARY_SIZE, hidden_dim=_HIDDEN_DIM)
    t1 = time.time()
    model.sgd_step(x_train[10], y_train[10], _LEARNING_RATE)
    t2 = time.time()
    print "SGD Step time: %f milliseconds" % ((t2 - t1) * 1000.)

    if _MODEL_FILE != None:
        load_model_parameters_theano(_MODEL_FILE, model)

    train_with_sgd(model, x_train, y_train, nepoch=_NEPOCH, learning_rate=_LEARNING_RATE)
    return model


def generate_sentence(model,word_to_index, index_to_word):
    # We start the sentence with the start token
    new_sentence = [word_to_index[sentence_start_token]]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[sentence_end_token]:
        next_word_probs = model.forward_propagation(new_sentence)
        sampled_word = word_to_index[unknown_token]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[unknown_token]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
    sentence_str = [index_to_word[x] for x in new_sentence[1:-1]]
    return sentence_str



