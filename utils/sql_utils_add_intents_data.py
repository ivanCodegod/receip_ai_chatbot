import json
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="test-user",
    password="password",
    database="ai_chat_bot_database"
)

mycursor = mydb.cursor()

# Open the intents.json file and load it into a dictionary
with open('intents.json') as f:
    intents = json.load(f)

# Insert data into the "Recipes" table for each intent
for intent in intents['intents']:
    recipe_name = intent['tag']
    source = intent['source']
    calories = intent['calories']
    fat = intent['fat']
    sat_fat = intent['sat-fat']
    carbs = intent['carbs']
    fiber = intent['fiber']
    sugar = intent['sugar']
    protein = intent['protein']
    is_vegan = intent['is-vegan']
    instructions = intent['instructions']

    insert_recipe_query = "INSERT INTO Recipes (RecipeName, Source, Calories, Fat, SatFat, Carbs, Fiber, Sugar, Protein, IsVegan, Instructions) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    recipe_values = (recipe_name, source, calories, fat, sat_fat, carbs, fiber, sugar, protein, is_vegan, instructions)

    mycursor.execute(insert_recipe_query, recipe_values)
    mydb.commit()

    # get the ID of the newly added recipe
    recipe_id = mycursor.lastrowid

    # insert data into the "Patterns" table
    insert_pattern_query = "INSERT INTO Patterns (RecipeID, PatternText) VALUES (%s, %s)"
    pattern_values = [(recipe_id, pattern_text) for pattern_text in intent['patterns']]

    mycursor.executemany(insert_pattern_query, pattern_values)
    mydb.commit()

    # insert data into the "Responses" table
    insert_ingredients_query = "INSERT INTO Ingredients (RecipeID, Ingredient) VALUES (%s, %s)"
    response_values = [(recipe_id, response_text) for response_text in intent['ingredients']]

    mycursor.executemany(insert_ingredients_query, response_values)
    mydb.commit()
