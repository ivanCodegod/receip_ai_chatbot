"""
This script is responsible for preparing data for the intents used in the AI chatbot application. It parses data from
 the database, organizes it into the appropriate format, and then writes it to a JSON file.

The script imports functions to fetch data from several tables in the database. It structures the data into a list of
 intent dictionaries, with each dictionary containing details for a single intent, including the intent name, patterns,
  and associated metadata.

The script produces a JSON file in the project's root directory. The name of the JSON file is generated by
 combining 'intents_' with the current date and time.

Steps:
1. Import necessary libraries and functions
2. Define the generate_intents_file function
3. Inside this function, call the imported DB functions to fetch data
4. Loop through the fetched data and organize it into a list of dictionaries
5. Write the list of dictionaries to a JSON file
6. Return the name of the generated file
7. Call the generate_intents_file function to execute the script
"""

import json
import os
from datetime import datetime

from utils.sql_base_utils import get_recipes_data, get_pattern_text_data, get_ingredient_data


def generate_intents_file():
    recipes_data = get_recipes_data()
    patterns_data = get_pattern_text_data()
    ingredients_data = get_ingredient_data()

    intents = {
        "intents": []
    }

    for recipe in recipes_data:
        print(f"recipe: {recipe}")
        # Each recipe is a tuple with RecipeID at 0 index, RecipeName at 1 index and so on.
        recipe_id, recipe_name, source, calories, fat, sat_fat, carbs, fiber, sugar, protein, is_vegan, instructions = recipe

        matched_patterns = [pattern[1] for pattern in patterns_data if pattern[0] == recipe_id]

        matched_ingredients = [ingredient[1] for ingredient in ingredients_data if ingredient[0] == recipe_id]

        intent = {
            "tag": recipe_name,
            "patterns": matched_patterns,
            "instructions": [instructions],
            "ingredients": matched_ingredients,
            "source": source,
            "calories": calories,
            "fat": fat,
            "sat-fat": sat_fat,
            "carbs": carbs,
            "fiber": fiber,
            "sugar": sugar,
            "protein": protein,
            "is-vegan": bool(is_vegan)
        }

        intents["intents"].append(intent)

    parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    current_datetime = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")

    intents_filename = f"intents_{current_datetime}.json"
    with open(f'{parent_dir}/{intents_filename}', 'w') as outfile:
        json.dump(intents, outfile)


def main():
    if __name__ == '__main__':
        generate_intents_file()


main()