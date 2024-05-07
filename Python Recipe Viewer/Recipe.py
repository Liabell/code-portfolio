from isodate import parse_duration
from PIL import Image
import requests
import shutil
from colorama import init, Fore, Style
# from loading_bar import increment_loading_bar

init() # initialize colorama

class Recipe:
    def __init__(self, name, picture, prep, cook, yeild):
        self.name = name
        self.image = picture
        self.prep_time = prep
        self.cook_time = cook
        self.amount = yeild
    
    def get_name(self):
        return self.name
    
    def get_cook_time(self):
        if self.cook_time != "":
            time = parse_duration(self.cook_time)
            return("{:02d}:{:02d}".format((time.seconds // 3600), (time.seconds // 60) % 60)) # hours:minutes
        else:
            return '00:00' 
    
    def get_prep_time(self):
        if "PT" in self.prep_time:
            time = parse_duration(self.prep_time)
            return("{:02d}:{:02d}".format((time.seconds // 3600), (time.seconds // 60) % 60)) # hours:minutes
        else:
            return '00:00'
    
    def set_image(self, image_url, bar_input): # bar_input not specified in HW pdf

        image_request = requests.get(image_url, stream=True) # creates images as .gifs
        with open(self.get_image(), 'wb') as f:
            shutil.copyfileobj(image_request.raw, f)
        
        scaled_width = 200
        img = Image.open(self.get_image()) # stores .gif in object
        percent_width=(scaled_width / float (img.size[0]))
        h_size = int ((float(img.size[1]) * float (percent_width)))
        img = img.resize((scaled_width, h_size), Image.LANCZOS) # scales image correctly and applies AA
        img.save (self.get_image()) # save the resized image as a GIF for loading in ezgraphics

        if bar_input[1] <= bar_input[0]:
            bar_input = increment_loading_bar(bar_input) # increments bar after each image is "loaded" (resized and saved as .gif), bar_input is updated with new information by increment_loading_bar
            bar_input[1] = bar_input[1] + 1 # progress_step is incremented
        return bar_input
    
    def get_image(self):
        if ":" in self.name: # saving files on windows with ':' in the filename causes file to corrupt
            return self.name.replace(":", "") + '.gif'
        else:
            return self.name + '.gif' # images are named according to the recipe name
        
def create_loading_bar():
    new_bar_len = 20
    progress_step = 1
    progress =''
    green = f'\033[32m'
    remaining_bar = '░'
    remaining = ''
    bar_input = [new_bar_len, progress_step, progress, green, remaining_bar, remaining]
    return bar_input

def increment_loading_bar(bar_input): # green coloring doesnt work on default windows command prompt
    bar = '█'
    if bar_input is not None:
        new_bar_len = bar_input[0]
        progress_step = bar_input[1]
        progress = bar_input[2]
        green = bar_input[3]
        remaining_bar = bar_input[4]
        remaining = bar_input[5]
    else:
        return
    
    if progress_step < new_bar_len:
        progress = bar * progress_step
        progress_step += 1
        remaining = new_bar_len - progress_step
        print(f'{Fore.GREEN}{progress}{remaining * remaining_bar} {progress_step * 100 / new_bar_len}%{Style.RESET_ALL}', end="\r")
        bar_output = [new_bar_len, progress_step, progress, green, remaining_bar, remaining]
        return bar_output