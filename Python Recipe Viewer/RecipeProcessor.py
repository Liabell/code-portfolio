import json
from Recipe import Recipe

class RecipeProcessor():
    def __init__(self):
        self.recipe_list = []
        self.recipes = None

    def load_recipes(self, file):
        recipe_file = open(file, encoding='utf-8')
        self.recipes = json.load(recipe_file)

    def get_recipes(self):
        for recipe in self.recipes:
            recipe_row = Recipe(recipe['name'], recipe['image'], recipe['prepTime'], recipe['cookTime'], recipe['recipeYield'])
            self.recipe_list.append(recipe_row)
        return self.recipe_list
    
    def tabulate_recipes(self): # this is wrong and smells of cody
        print("-"*190)
        print("{:<90}{:<15}{:<15}{:<50}".format("Name", "Prep Time", "Cook Time", "recipeYield"))
        print('-'*190)

        for i in range(len(self.recipe_list)):
            print("{:<90}{:<15}{:<15}{:<50}".format(self.recipe_list[i].get_name(), self.recipe_list[i].get_prep_time(), self.recipe_list[i].get_cook_time(), self.recipe_list[i].amount))
