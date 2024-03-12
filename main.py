import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import json
from tensorflow import keras
import pickle

stemmer = LancasterStemmer()

with open("intents.json") as file:
    data = json.load(file)

try:
    with open("data.pickle", "rb") as f:
        words, labels, training, output = pickle.load(f)
except:
    words = []  # all words tokenized
    labels = []  # unique tags
    docs_x = []
    docs_y = []  # tags for each word

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            wrds = nltk.word_tokenize(pattern)
            words.extend(wrds)
            docs_x.append(wrds)
            docs_y.append(intent["tag"])

        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    words = [stemmer.stem(w.lower()) for w in words if w != "?"]

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

    with open("data.pickle", "wb") as f:
        pickle.dump((words, labels, training, output), f)

model = keras.Sequential([
    keras.layers.Dense(8, activation='relu', input_shape=(len(training[0]),)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

try:
    model = keras.models.load_model("my_model.keras")
    print(f"model: {model}")
except:
    model.fit(training, output, epochs=1000, batch_size=8)
    model.save("my_model.keras")


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")
    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break
        # results = model.predict([bag_of_words(inp, words)])
        results = model.predict(bag_of_words(inp, words)[np.newaxis, :])[0]
        print(f"results: {results}")
        results_index = np.argmax(results)
        tag = labels[results_index]
        print(f"tag: {tag}")

        if results[results_index] >= 0.5:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    print(random.choice(responses))
        else:
            print("I didn't get that, try again.")


chat()
