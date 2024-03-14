import mysql.connector


def get_db_connection():
    db_connection = mysql.connector.connect(
        host="localhost",
        user="test-user",
        password="password",
        database="ai_chat_bot_database"
    )
    return db_connection


def get_pattern_texts():
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    # Query for fetching PatternText from Patterns table
    cursor.execute('SELECT PatternText FROM Patterns;')
    pattern_texts = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()

    return pattern_texts


def get_recipe_names():
    db_connection = get_db_connection()
    cursor = db_connection.cursor()

    # Query for fetching RecipeName from Recipes table
    cursor.execute('SELECT RecipeName FROM Recipes;')
    recipe_names = [row[0] for row in cursor.fetchall()]

    cursor.close()
    db_connection.close()

    return recipe_names


print(f'Pattern Texts: {get_pattern_texts()}')
print(f'Recipe Names: {get_recipe_names()}')
