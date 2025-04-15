USE Pic2Cook;
GO

IF OBJECT_ID(N'CookBook.Ingredients', 'U') IS NULL
CREATE TABLE CookBook.Ingredients(
	IngredientID INT PRIMARY KEY,
	IngredientName VARCHAR(64),
);
GO

IF OBJECT_ID(N'CookBook.Recipes', 'U') IS NULL
CREATE TABLE CookBook.Recipes(
	RecipeID Int PRIMARY KEY,
	IngredientId INT,
	RecipeName VARCHAR(128),
	RecipeURL VARCHAR(128),
	RecipeDirections TEXT
);
GO

IF OBJECT_ID(N'CookBook.RecipeIngredients', 'U') IS NULL
CREATE TABLE CookBook.RecipeIngredients(
	IngredientID INT,
	RecipeID INT,

	FOREIGN KEY(IngredientID) REFERENCES CookBook.Ingredients(IngredientID),
	FOREIGN KEY(RecipeID) REFERENCES CookBook.Recipes(RecipeID)
);
GO