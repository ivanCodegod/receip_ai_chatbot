import nltk
from nltk.stem.lancaster import LancasterStemmer
import numpy as np
import random
import json
from tensorflow import keras

from utils.sql_utils_parce_data import get_pattern_texts, get_recipe_names

stemmer = LancasterStemmer()

with open("intents.json") as file:  # TODO: Use database for storing intents instead
    data = json.load(file)

words = []  # all words (patterns) tokenized
labels = []  # unique tags
docs_x = []  # list that contains lists with tokenized patterns for each pattern listed
docs_y = []  # tags for each word

training = []
output = []

recipe_names = get_recipe_names()
pattern_texts = get_pattern_texts()
for tag in recipe_names:
    for pattern in pattern_texts:
        wrds: list = nltk.word_tokenize(
            pattern)  # tokenized patterns in format like ['Shrimp', 'Scampi'] for "Shrimp Scampi" pattern
        words.extend(wrds)  # appending tokenized patterns to general list with all words tokenized
        docs_x.append(wrds)
        docs_y.append(tag)  # appending with tag aka. recipie name

    if tag not in labels:
        labels.append(tag)

# stemmer.stem(…) applies the "stemming" process to the converted lowercase word. Stemming is a sort of normalization
# for words. It removes suffixes (like "ing" or "ed") from words based on a set of heuristic rules. This allows the
# model to treat different forms of the same word as the identical word, which can be useful in many language
# processing tasks.
words = [stemmer.stem(w) for w in words if
         w != "?"]  # and applies the stemming process (reducing the word to its root form
words = sorted(list(set(words)))

out_empty = [0 for _ in range(len(labels))]
for x, doc in enumerate(docs_x):  # TODO: rename x and doc to better naming
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
        if w in wrds:
            bag.append(1)
        else:
            bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1  # creating the output for your training data using one-hot encoding

    training.append(bag)
    output.append(output_row)

training = np.array(training)
output = np.array(output)

model = keras.Sequential([  # TODO: Educational: How it works?
    keras.layers.Dense(8, activation='relu', input_shape=(len(training[0]),)),
    keras.layers.Dense(8, activation='relu'),
    keras.layers.Dense(len(output[0]), activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])  # TODO: Educational: How it works?

try:
    model = keras.models.load_model("ai_chat_bot_model.keras")
    print(f"model: {model}")
except:  # TODO: Use specific exceptions instead
    model.fit(training, output, epochs=1000, batch_size=8)
    model.save("ai_chat_bot_model.keras")


def bag_of_words(s, words):  # TODO: Educational: How it works?
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def chat():
    print("Start talking with the bot (type quit to stop)!")  # TODO: Make it more beautiful
    while True:  # TODO: We can create logic for vegans and for non vegans
        inp = input("You: ")
        if inp.lower() == "quit":
            # TODO: Make it more beautiful
            break
        results = model.predict(bag_of_words(inp, words)[np.newaxis, :])[0]  # TODO: Educational: How it works?
        print(f"results: {results}")
        results_index = np.argmax(results)
        tag = labels[results_index]
        print(f"tag: {tag}")

        # if results[results_index] >= 0.5:  # TODO: Should be a constant
        #     for tg in data["intents"]:
        #         if tg['tag'] == tag:
        #             responses = tg['responses']
        #             print(random.choice(responses))
        # else:
        #     print("I didn't get that, try again.")  # TODO: Make it more beautiful


chat()
