USE Pic2Cook;
GO

IF OBJECT_ID('CookBook.RecipeIngredients') IS NOT NULL
	DROP TABLE CookBook.RecipeIngredients;
GO

IF OBJECT_ID('CookBook.Recipes') IS NOT NULL
	DROP TABLE CookBook.Recipes;
GO

IF OBJECT_ID('CookBook.Ingredients') IS NOT NULL
	DROP TABLE CookBook.Ingredients;
GO