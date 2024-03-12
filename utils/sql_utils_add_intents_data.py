import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="test-user",
    password="password",
    database="ai_chat_bot_database"
)

mycursor = mydb.cursor()

intents = {
    "intents": [
        {
            "tag": "Baked Shrimp Scampi instructions",
            "patterns": [
                "Baked Shrimp Scampi",
                "Shrimp Scampi",
                "Scampi",
                "How to make Baked Shrimp Scampi?",
                "Give me the recipe for Baked Shrimp Scampi",
                "Baked Shrimp Scampi recipe",
                "Shrimp Scampi recipe",
                "Shrimp Scampi instructions",
                "Can I get the instructions for Baked Shrimp Scampi?",
                "Can you share the Baked Shrimp Scampi recipe from Ina Garten: Barefoot Contessa Back to Basics?",
                "I want to cook Baked Shrimp Scampi, can you guide me?",
            ],
            "responses": [
                "Preheat the oven to 425 degrees F.\r\n\r\nDefrost shrimp by putting in cold water, then drain and toss with wine, oil, salt, and pepper. Place in oven-safe dish and allow to sit at room temperature while you make the butter and garlic mixture.\r\n\r\nIn a small bowl, mash the softened butter with the rest of the ingredients and some salt and pepper.\r\n\r\nSpread the butter mixture evenly over the shrimp. Bake for 10 to 12 minutes until hot and bubbly. If you like the top browned, place under a broiler for 1-3 minutes (keep an eye on it). Serve with lemon wedges and French bread.\r\n\r\nNote: if using fresh shrimp, arrange for presentation. Starting from the outer edge of a 14-inch oval gratin dish, arrange the shrimp in a single layer cut side down with the tails curling up and towards the center of the dish. Pour the remaining marinade over the shrimp. "
            ],
            "source": "Ina Garten: Barefoot Contessa Back to Basics",
            "calories": 2565,
            "fat": 159,
            "sat-fat": 67,
            "carbs": 76,
            "fiber": 4,
            "sugar": 6,
            "protein": 200
        }
    ]
}

# Вставляем данные в таблицу "Recipes" для каждого интента
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

    insert_recipe_query = "INSERT INTO Recipes (RecipeName, Source, Calories, Fat, SatFat, Carbs, Fiber, Sugar, Protein, IsVegan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    recipe_values = (recipe_name, source, calories, fat, sat_fat, carbs, fiber, sugar, protein, False)

    mycursor.execute(insert_recipe_query, recipe_values)
    mydb.commit()

    # получаем ID только что добавленного рецепта
    recipe_id = mycursor.lastrowid

    # вставляем данные в таблицу "Patterns"
    insert_pattern_query = "INSERT INTO Patterns (RecipeID, PatternText) VALUES (%s, %s)"
    pattern_values = [(recipe_id, pattern_text) for pattern_text in intent['patterns']]

    mycursor.executemany(insert_pattern_query, pattern_values)
    mydb.commit()

    # вставляем данные в таблицу "Responses"
    insert_response_query = "INSERT INTO Responses (RecipeID, ResponseText) VALUES (%s, %s)"
    response_values = [(recipe_id, response_text) for response_text in intent['responses']]

    mycursor.executemany(insert_response_query, response_values)
    mydb.commit()
