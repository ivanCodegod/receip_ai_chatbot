import numpy as np

import nltk
from nltk.stem.lancaster import LancasterStemmer

from art import tprint

from helpers.intents_helper import load_intents_file


def bag_of_words(s, words):
    stemmer = LancasterStemmer()
    bag = [0 for _ in range(len(words))]

    s_words = nltk.word_tokenize(s)
    s_words = [stemmer.stem(word.lower()) for word in s_words]

    for se in s_words:
        for i, w in enumerate(words):
            if w == se:
                bag[i] = 1

    return np.array(bag)


def print_recipe_name_found(tag, data):
    print(f"|| {(len(tag) + 21 + len(data['source'])) * '='} ||")
    print(f"|| '{tag}' Recipe found by '{data['source']}' ||")
    print(f"|| {(len(tag) + 21 + len(data['source'])) * '='} ||")


def print_recipe_instructions_info(recipe_name, instructions):
    print(f"\nHere are the instructions for '{recipe_name}':")
    print(f"\t{instructions[0]}\n")


def print_recipe_ingredients_info(recipe_name, ingredients):
    print(f"Here are the ingredients for '{recipe_name}':")
    for ingredient in ingredients:
        print(f"\t- {ingredient}")
    else:
        print("\n")


def print_recipe_nutritional_info(recipe_name, recipe_data):
    print(f"Here are the nutritional information for '{recipe_name}':")

    calories = f"Total number of calories in a serving of the recipe - '{recipe_data['calories']}'."
    fat = f"Total amount of fat (in grams) per serving - '{recipe_data['fat']}'."
    sat_fat = (f"Amount of saturated fat (in grams) per serving - '{recipe_data['sat-fat']}'. "
               f"\n\t\tAbout: Saturated fat is a type of fat that can raise LDL ('bad') cholesterol levels.")
    carbs = (f"Total amount of carbohydrates (in grams) per serving - '{recipe_data['carbs']}'. "
             f"\n\t\tAbout: Carbohydrates are a source of energy for the body.")
    fiber = (f"Amount of dietary fiber (in grams) per serving - '{recipe_data['fiber']}'. "
             f"\n\t\tAbout: Fiber promotes digestive health and can help you feel fuller for longer.")
    sugar = (f"Amount of sugar (in grams) per serving - '{recipe_data['sugar']}'. "
             f"\n\t\tAbout: This includes both naturally occurring sugars and added sugars.")
    protein = (f"Total amount of protein (in grams) per serving - '{recipe_data['protein']}'. "
               f"\n\t\tAbout: Protein is essential for building and repairing tissues.")
    is_vegan = (f"Suitable for a vegan diet - '{'Yes' if recipe_data['is-vegan'] else 'No'}'. "
                f"\n\t\tAbout: A vegan diet excludes all animal products, including meat, dairy, and eggs.")

    for item in [calories, fat, sat_fat, carbs, fiber, sugar, protein, is_vegan]:
        print(f"\t- {item}")


def start_chat(model, words, labels):
    tprint("Recipe AI ChatBot", space=1, decoration='5')
    help_text = """
        📄 Welcome to the Recipe AI ChatBot! 📄

        🍽️ Looking for a delicious and speedy meal recipie? You're in the right place! Our chatbot is here to provide you with a variety of quick and easy recipes for any occasion.

        🔍 How to Use:
            1. Type in your query with info about dish name.
            2. Follow the step-by-step instructions for a tasty meal in no time.

        📌 Pro Tip: Save your favorite recipes by sending them to yourself or sharing them with friends.

        Cooking made fun and simple with Recipe AI ChatBot. Get ready to create culinary delights!
    """
    print(help_text)
    print("Type 'quit' to exit the chat.\n")

    while True:
        data = load_intents_file()

        inp = input("You: ")
        if inp.lower() == "quit":
            break

        results = model.predict(bag_of_words(inp, words)[np.newaxis, :])[0]  # TODO: Educational: How it works?
        results_index = np.argmax(results)
        tag = labels[results_index]

        if results[results_index] > 0.5:
            for tg in data["intents"]:
                if tg['tag'] == tag:
                    print_recipe_name_found(tag, tg)

                    print_recipe_instructions_info(tag, tg['instructions'])
                    print_recipe_ingredients_info(tag, tg['ingredients'])
                    print_recipe_nutritional_info(tag, tg)
        else:
            print("I didn't get that, try again please.")
