import sys
import os

from RNN import RNN
from Tokenizer import *

_VOCABULARY_SIZE = int(os.environ.get('VOCABULARY_SIZE', '8000'))
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
        if epoch % evaluate_loss_after == 0:
            loss = model.calculate_loss(X_train, y_train)
            losses.append((num_examples_seen, loss))
            # Adjust the learning rate if loss increases
            if len(losses) > 1 and losses[-1][1] > losses[-2][1]:
                learning_rate *= 0.5
            sys.stdout.flush()

        # For each training example...
        for i in range(len(y_train)):
            # One SGD step
            model.sgd_step(X_train[i], y_train[i], learning_rate)
            num_examples_seen += 1
        print (epoch)


def getModel(tokenized_sentences, word_to_index):
    x_train = get_x_train(tokenized_sentences, word_to_index)
    y_train = get_y_train(tokenized_sentences, word_to_index)

    model = RNN(_VOCABULARY_SIZE, hidden_dim=_HIDDEN_DIM)
    train_with_sgd(model, x_train, y_train, nepoch=_NEPOCH, learning_rate=_LEARNING_RATE)
    return model


def generate_sentence(model, word_to_index, index_to_word, start, end):
    # We start the sentence with the start token
    new_sentence = [word_to_index[start]]
    # Repeat until we get an end token
    while not new_sentence[-1] == word_to_index[end]:
        next_word_probs = model.forward_propagation(new_sentence)

        sampled_word = word_to_index[unknown_token]
        # We don't want to sample unknown words
        while sampled_word == word_to_index[unknown_token]:
            samples = np.random.multinomial(1, next_word_probs[-1])
            sampled_word = np.argmax(samples)
        new_sentence.append(sampled_word)
    sentence_str = []
    for x in new_sentence:
        sentence_str.append(index_to_word[x])
    return sentence_str


def softmax(x):
    xt = np.exp(x - np.max(x))
    return xt / np.sum(xt)