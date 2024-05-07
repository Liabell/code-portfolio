from RecipeProcessor import RecipeProcessor
from RecipeUI import RecipeUI
from Recipe import create_loading_bar

def main():
    picture_number = 16 # represents number of recipes that will be printed
    recipes = RecipeProcessor()

    recipes.load_recipes('recipes.json') # stores all recipe data (more than 50 recipes) from json file into objects
    recipe = recipes.get_recipes() # organizes recipe data into individual recipes in a list

    bar_input = create_loading_bar() # creates the parameters of the loading bar
    print("Please wait, loading images.")

    for pics in range(picture_number):
        bar_input = recipe[pics].set_image(recipe[pics].image, bar_input) # loads images of the food in each recipe and displays a progress bar from loading_bar.py

    recipe_canvas = RecipeUI()
    recipe_canvas.layout_ui(recipe) # creates a canvas using ezgraphics where the recipe information is displayed in a separate window

    recipes.tabulate_recipes() # tabulates the recipe data after the canvas is closed

main()