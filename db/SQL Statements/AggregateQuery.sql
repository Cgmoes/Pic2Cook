DECLARE @Ingredients VARCHAR(MAX) = 'Milk, eggs';

SELECT 
  R.RecipeID,
  R.RecipeName,
  R.RecipeURL,
  CAST(R.RecipeDirections AS VARCHAR(MAX)) AS RecipeDirections
FROM CookBook.Recipes R
JOIN CookBook.RecipeIngredients RI ON R.RecipeID = RI.RecipeID
JOIN CookBook.Ingredients I ON RI.IngredientID = I.IngredientID
JOIN STRING_SPLIT(@Ingredients, ',') AS S ON I.IngredientName = TRIM(S.value)
GROUP BY 
  R.RecipeID, 
  R.RecipeName, 
  R.RecipeURL, 
  CAST(R.RecipeDirections AS VARCHAR(MAX))
HAVING COUNT(DISTINCT I.IngredientName) = (
  SELECT COUNT(*) FROM STRING_SPLIT(@Ingredients, ',')
);
