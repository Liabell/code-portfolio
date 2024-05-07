from ezgraphics import GraphicsImage, GraphicsWindow
from Recipe import Recipe

class RecipeUI:
    def __init__(self):
        self.canvas = None
        self.window = None
        self.spacing = 60
        self.length = 1080
        self.width = 1080
        self.setup_window()

    def setup_window(self):
        self.window = GraphicsWindow(self.width, self.length)
        self.window.setTitle("Recipe Book")
        self.canvas = self.window.canvas()

    def layout_ui(self, pictures):
        x = 0
        y = 0
        max_height = 0
        picture_number = 16

        current_image = GraphicsImage(pictures[0].get_image())
        self.canvas.drawImage(x, y, current_image)
        self.show_recipe_desc(pictures[0], x, y + current_image.height())

        for i in range(1, picture_number): # next 15 images
            max_height = max(max_height, current_image.height())

            previous_image = current_image
            current_image = GraphicsImage(pictures[i].get_image()) # picture filename
            x = x + previous_image.width() + self.spacing
            if x + current_image.width() < self.width:
                self.canvas.drawImage(x, y, current_image) # draws image on canvas
                self.show_recipe_desc(pictures[i], x, y + current_image.height()) # draws recipe info on canvas

            else: # new line of images
                x = 0
                y = y + max_height + self.spacing
                self.canvas.drawImage(x, y, current_image)
                self.show_recipe_desc(pictures[i], x, y + current_image.height())

        self.window.wait()

    def show_recipe_desc(self, recipe, x, y):
        name = recipe.get_name()
        cook_time = recipe.get_cook_time()
        prep_time = recipe.get_prep_time()

        self.canvas.drawText(x, y, "Name: " + name[:25]) # cuts text at 25 characters long based on the image in the assignment pdf
        self.canvas.drawText(x, y + 15, "Prep Time: " + prep_time)
        self.canvas.drawText(x, y + 30, "Cook Time: " + cook_time)