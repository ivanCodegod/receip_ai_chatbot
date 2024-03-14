from helpers.intents_helper import load_intents_file
from utils.data_processing import prepare_training_data, get_words, get_labels, get_docs
from utils.model_handling import set_model
from utils.chat_handling import chat

# load intent data
data = load_intents_file()

words = get_words(data)
docs_x, docs_y = get_docs(data)
labels = get_labels(data)

training_data, output_data = prepare_training_data(words, labels, docs_x, docs_y)

# prepare model
model = set_model(training_data, output_data)

# start chat
chat(model, words=words, labels=labels)
