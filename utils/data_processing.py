import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np

stemmer = LancasterStemmer()


def get_words(data):
    words = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)

    words = [stemmer.stem(w) for w in words if w != "?"]
    words = sorted(list(set(words)))
    return words


def get_labels(data):
    labels = []  # unique tags

    for intent in data["intents"]:
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    return labels


def get_docs(data):
    docs_x = []
    docs_y = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

    return docs_x, docs_y


def prepare_training_data(words, labels, docs_x, docs_y):
    training = []
    output = []

    out_empty = [0 for _ in range(len(labels))]

    for x, doc in enumerate(docs_x):
        bag = []

        wrds = [stemmer.stem(w.lower()) for w in doc]

        for w in words:
            if w in wrds:
                bag.append(1)
            else:
                bag.append(0)

        output_row = out_empty[:]
        output_row[labels.index(docs_y[x])] = 1

        training.append(bag)
        output.append(output_row)

    training = np.array(training)
    output = np.array(output)

    return training, output
