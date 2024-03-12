import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="test-user",
    password="password",
    database="ai_chat_bot_database"
)

mycursor = mydb.cursor()

# Создаём таблицу Recipes
# mycursor.execute(
#     "CREATE TABLE Recipes (RecipeID INT AUTO_INCREMENT PRIMARY KEY, RecipeName VARCHAR(255), Source VARCHAR(255), Calories INT, Fat INT, SatFat INT, Carbs INT, Fiber INT, Sugar INT, Protein INT, IsVegan BOOLEAN)")
#
# # Создаём таблицу Patterns
# mycursor.execute(
#     "CREATE TABLE Patterns (ID INT AUTO_INCREMENT PRIMARY KEY, RecipeID INT, PatternText VARCHAR(255), FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID))")
#
# # Создаём таблицу Responses
# mycursor.execute(
#     "CREATE TABLE Responses (ID INT AUTO_INCREMENT PRIMARY KEY, RecipeID INT, ResponseText VARCHAR(255), FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID))")
#
# # Создаём таблицу Ingredients
# mycursor.execute(
#     "CREATE TABLE Ingredients (ID INT AUTO_INCREMENT PRIMARY KEY, RecipeID INT, Ingredient VARCHAR(255), FOREIGN KEY (RecipeID) REFERENCES Recipes(RecipeID))")
