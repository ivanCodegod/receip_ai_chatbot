import mysql.connector


def create_sql_connection():
    sql_connection = mysql.connector.connect(
        host="localhost",
        user="test-user",
        password="password",
        database="ai_chat_bot_database"
    )
    return sql_connection


def get_recipes_data():
    connection = create_sql_connection()
    cursor = connection.cursor()

    # Query for fetching RecipeName from Recipes table
    cursor.execute('SELECT * FROM Recipes;')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_pattern_text_data():
    connection = create_sql_connection()
    cursor = connection.cursor()

    # Query for fetching RecipeName from Recipes table
    cursor.execute('SELECT RecipeID, PatternText FROM Patterns ORDER BY RecipeID;')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result


def get_ingredient_data():
    connection = create_sql_connection()
    cursor = connection.cursor()

    # Query for fetching RecipeName from Recipes table
    cursor.execute('SELECT RecipeID, Ingredient FROM Ingredients ORDER BY RecipeID;')
    result = cursor.fetchall()

    cursor.close()
    connection.close()

    return result
