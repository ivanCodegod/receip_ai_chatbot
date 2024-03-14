import numpy as np
import random
import json
import nltk
from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()


def bag_of_words(s, words):
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat(model, words, labels):
    print("Start talking with the bot (type quit to stop)!")

    while True:
        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict(bag_of_words(inp, words)[np.newaxis, :])[0]  # TODO: Educational: How it works?
        print(f"results: {results}")
        results_index = np.argmax(results)
        tag = labels[results_index]
        print(f"tag: {tag}")

        if results[results_index] > 0.5:
            with open("intents_2024-03-14T22-57-23.json") as file:
                data = json.load(file)
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    responses = tg['responses']
                    print(random.choice(responses))
        else:
            print("I didn't get that, try again.")
