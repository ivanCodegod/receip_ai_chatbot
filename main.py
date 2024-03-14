from utils.data_processing import prepare_training_data, get_words, get_labels, get_docs
from utils.model_handling import initialize_model, train_model, load_model
from utils.chat_handling import chat

import json

with open("intents_2024-03-14T19-10-06.json") as file:  # name of the intents data file should be passed here
    data = json.load(file)

docs_x, docs_y = get_docs(data)
words = get_words(data)
labels = get_labels(data)

training_data, output_data = prepare_training_data(words, labels, docs_x, docs_y)

# initialize and train model
model = initialize_model(input_shape=len(training_data[0]), output_shape=len(output_data[0]))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

try:
    model = load_model()
    print(f"model: {model}")
except:
    train_model(model, training_data, output_data)

# Start chat
chat(model, words=words, labels=labels)
