import pandas as pd
import time
from datetime import datetime

from selenium import webdriver   #used to automate web browser interaction
from selenium.webdriver.chrome.service import Service   #This class helps in managing the ChromeDriver service that Selenium uses to interact with the Chrome browser.
from webdriver_manager.chrome import ChromeDriverManager  #This class automatically downloads and sets up the latest version of ChromeDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By   #The By class is used to locate elements on a web page


#Get Chrome driver
driver = webdriver.Chrome()

# driver wait 10 seconds until the page loaded
driver.implicitly_wait(10)

# Enter to the site
driver.get('https://www.allrecipes.com/recipes-a-z-6735880');
time.sleep(5)

# Dictionary to hold scraped recipe data
dish_info = {
    'Name': [],
    'Ingredients': [],
    'Directions': []
}

# Get all alphabetical category groups on the A–Z page
group_elements = driver.find_elements(By.CLASS_NAME, "mntl-alphabetical-list__group")

# Loop through each group (e.g., A, B, C...)
for group_index in range(len(group_elements)):
    group_elements = driver.find_elements(By.CLASS_NAME, "mntl-alphabetical-list__group")  # Re-fetch to avoid stale reference
    row = group_elements[group_index]

    # Find all recipe category links under this group
    links = row.find_elements(By.XPATH, ".//ul/li/a")

    # Loop through each category link
    for link_index in range(len(links)):
        group_elements = driver.find_elements(By.CLASS_NAME, "mntl-alphabetical-list__group")
        row = group_elements[group_index]
        links = row.find_elements(By.XPATH, ".//ul/li/a")
        link = links[link_index]

        link_text = link.text.strip()
        href = link.get_attribute("href")
        print(f"Clicking: {link_text} ({href})")

        link.click()
        time.sleep(3)  # Give the page a chance to load

        # Try to find the section that contains recipe links
        try:
            WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "mntl-three-post__inner_1-0"))
            )
            div_for_recipes = driver.find_element(By.ID, "mntl-three-post__inner_1-0")
            recipe_links = div_for_recipes.find_elements(By.TAG_NAME, "a")[:3]  # Limit to 3 for now
        except:
            print("Recipe section not found — skipping.")
            driver.back()
            time.sleep(2)
            continue

        # Get top 3 recipe links
        three_recipes = div_for_recipes.find_elements(By.TAG_NAME, "a")[:3]

        for recipe_link in three_recipes:
            try:
                # Open each recipe link in a new tab
                recipe_href = recipe_link.get_attribute("href")
                print(f" - Opening recipe: {recipe_href}")
                driver.execute_script("window.open(arguments[0]);", recipe_href)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(2)

                # Skip if ingredients container is not found
                if not driver.find_elements(By.ID, "mm-recipes-structured-ingredients_1-0"):
                    print("❌ No ingredients — skipping")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

                # Get the recipe title
                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                    dish_info['Name'].append(title)
                    print(f"    Title: {title}")
                except:
                    print("    No title found.")

                # Scrape ingredients
                try:
                    ingredient_texts = []
                    ingredient_holder = driver.find_element(By.ID, "mm-recipes-structured-ingredients_1-0")
                    ingredients_elements = ingredient_holder.find_elements(By.TAG_NAME, "li")

                    for el in ingredients_elements:
                        full_ingredient = el.text.strip()
                        if full_ingredient:
                            ingredient_texts.append(full_ingredient)

                    dish_info['Ingredients'].append(ingredient_texts)
                    print(f"    Ingredients: {ingredient_texts}")
                except:
                    dish_info['Ingredients'].append([])
                    print("    No ingredients found.")

                # Scrape directions/steps
                try:
                    direction_elements = driver.find_elements(By.CLASS_NAME, "mntl-sc-block-group--LI")
                    direction_texts = []
                    step_number = 1

                    for el in direction_elements:
                        step = el.text.strip()
                        if step:
                            direction_texts.append(f"Step {step_number}: {step}")
                            step_number += 1

                    dish_info['Directions'].append(direction_texts)
                    print(f"    Directions: {direction_texts}")
                except Exception as e:
                    dish_info['Directions'].append([])
                    print(f"    No Directions found. Error: {e}")

                # Close recipe tab and return to previous page
                driver.close()
                driver.switch_to.window(driver.window_handles[0])

            except Exception as e:
                print(f"    Error clicking recipe link: {e}")

        # Go back to the category page
        driver.back()
        time.sleep(3)

# Convert to DataFrame and export to JSON
dishInfoDF = pd.DataFrame(dish_info)
dishInfoDF.to_json("recipes.json", orient="records", indent=2)


"""
This code is to open the json file into a pandas
dataframe and show top 5 data blocks


# Load the JSON file into a DataFrame
df = pd.read_json("recipes.json")

# View the first few rows
df.head()
"""