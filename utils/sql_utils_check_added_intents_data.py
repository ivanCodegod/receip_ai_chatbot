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
                "Can I getthe instructions for Baked Shrimp Scampi?",
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

# Выберем все данные из таблицы Recipes
mycursor.execute("SELECT * FROM Recipes")
recipes_result = mycursor.fetchall()
print(f"recipes_result: {recipes_result}")

# Выберем все данные из таблицы Patterns
mycursor.execute("SELECT * FROM Patterns")
patterns_result = mycursor.fetchall()
print(f"patterns_result: {patterns_result}")

# Выберем все данные из таблицы Responses
mycursor.execute("SELECT * FROM Responses")
responses_result = mycursor.fetchall()
print(f"responses_result: {responses_result}")

# Проверим совпадение данных
for intent in intents['intents']:
    recipe_name = intent['tag']
    # Проверим, совпадают ли данные в таблице Recipes
    for recipe_row in recipes_result:
        if recipe_name == recipe_row[1]:
            print(f"Данные в таблице Recipes для {recipe_name} совпадают")
            recipe_id = recipe_row[0]
            # Проверим, совпадают ли данные в таблице Patterns
            for pattern in intent['patterns']:
                for pattern_row in patterns_result:
                    if pattern == pattern_row[2] and recipe_id == pattern_row[1]:
                        print(f"...данные в таблице Patterns для {pattern} совпадают")
                    else:
                        print(f"...данные в таблице Patterns для {pattern} НЕ совпадают")
            # Проверим, совпадают ли данные в таблице Responses
            for response in intent['responses']:
                for response_row in responses_result:
                    if response == response_row[2] and recipe_id == response_row[1]:
                        print(f"...данные в таблице Responses для этого интента совпадают")
                    else:
                        print(f"...данные в таблице Responses для этого интента НЕ совпадают")
        else:
            print(f"Данные в таблице Recipes для {recipe_name} НЕ совпадают")