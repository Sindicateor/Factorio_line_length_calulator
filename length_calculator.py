import json
import tkinter as tk
from tkinter import ttk

CRAFTING_SPEEDS = [0.5, 0.75, 1.25]
PATH_SPEEDS = [7.5, 15, 22.5]


def load_recipe_data():
    with open('recipe.json') as json_file:
        data = json.load(json_file)
        return(data)


class recipe_select():
    def __init__(self, master, recipe_data, ingredients):
        self.master = master
        self.ingredients = ingredients
        self.recipe_keys = list(recipe_data.keys())
        self.recipe = tk.StringVar(self.master)
        self.recipe.set(self.recipe_keys[0])
        self.ingredients.update_ingredients(self.recipe.get())

        self.recipeLbl = tk.Label(self.master, text="Choose recipe:")
        self.recipeLbl.grid(row=0, column=0)
        self.recipeSelect = tk.OptionMenu(
            self.master, self.recipe, *self.recipe_keys)
        self.recipeSelect.grid(row=0, column=1)

        self.recipe.trace("w", self.dropdown_change)

    def dropdown_change(self, *args):
        self.ingredients.update_ingredients(self.recipe.get())


class crafting_speed_select():
    def __init__(self, master, output):
        self.master = master
        self.output = output
        self.c_speed = tk.DoubleVar(self.master)
        self.c_speed.set(CRAFTING_SPEEDS[0])
        self.output.update_c_speed(self.c_speed.get())

        self.c_speedLbl = tk.Label(self.master, text="Choose crafting speed:")
        self.c_speedLbl.grid(row=1, column=0)
        self.c_speedSelect = tk.OptionMenu(
            self.master, self.c_speed, *CRAFTING_SPEEDS)
        self.c_speedSelect.grid(row=1, column=1)

        self.c_speed.trace("w", self.dropdown_change)

    def dropdown_change(self, *args):
        self.output.update_c_speed(self.c_speed.get())


class path_speed_select:
    def __init__(self, master, output):
        self.master = master
        self.output = output
        self.p_speed = tk.DoubleVar(self.master)
        self.p_speed.set(PATH_SPEEDS[0])
        self.output.update_p_speed(self.p_speed.get())

        self.p_speedLbl = tk.Label(self.master, text="Choose path speed:")
        self.p_speedLbl.grid(row=2, column=0)
        self.p_speedSelect = tk.OptionMenu(
            self.master, self.p_speed, *PATH_SPEEDS)
        self.p_speedSelect.grid(row=2, column=1)

        self.p_speed.trace("w", self.dropdown_change)

    def dropdown_change(self, *args):
        self.output.update_p_speed(self.p_speed.get())


class manage_ingredients:
    def __init__(self, master, recipe_data, output):
        self.master = master
        self.output = output
        self.recipe_data = recipe_data

        self.label = tk.Label(self.master, text="Ingredients: ")
        self.label.grid(row=4, column=0)

        self.ingredients_list = []
        for i in range(0, 6):
            self.ingredients_list.append(
                manage_ingredient(self.master, output, 5+i))

    def update_ingredients(self, recipe_name):
        self.recipe = self.recipe_data[recipe_name]
        self.recipe_ingredients = self.recipe["ingredients"]
        self.recipe_time = self.recipe["time"]

        self.recipe_keys = list(self.recipe_ingredients.keys())

        for i in range(0, 6):
            if i < len(self.recipe_keys):
                self.ingredients_list[i].update(recipe_name,
                                                self.recipe_keys[i], self.recipe_ingredients[self.recipe_keys[i]], self.recipe_time)
            else:
                self.ingredients_list[i].update(
                    recipe_name, 'none', 0, self.recipe_time)


class manage_ingredient:
    def __init__(self, master, output, row):
        self.master = master
        self.output = output
        self.name = 'none'
        self.recipe_name = 'none'
        self.amount = 0
        self.recipe_time = 0.5
        self.paths = tk.IntVar(self.master)
        self.paths.set(1)

        self.label = tk.Label(
            self.master, text=self.name+': '+str(self.amount))
        self.label.grid(row=row, column=0)

        self.path_select = tk.OptionMenu(
            self.master, self.paths, *[1, 2])
        self.path_select.grid(row=row, column=1)

        self.paths.trace("w", self.dropdown_change)

    def dropdown_change(self, *args):
        self.output.update_recipe(
            self.recipe_name, self.amount, self.paths.get(), self.recipe_time)

    def update(self, recipe_name, name, amount, time):
        self.recipe_time = time
        self.recipe_name = recipe_name
        self.name = name
        self.amount = amount
        self.label.configure(text=self.name+': '+str(self.amount))
        self.output.update_recipe(
            self.recipe_name, self.amount, self.paths.get(), self.recipe_time)


class output_calculator:
    def __init__(self, master):
        self.master = master

        self.c_speed = 0
        self.p_speed = 0
        self.recipe_time = 0.5
        self.recipe_name = 'none'
        self.amount = 0

        self.label = tk.Label(self.master, text="Number: ")
        self.label.grid(row=3, column=0)

        self.out_label = tk.Label(self.master, text="Loading!")
        self.out_label.grid(row=3, column=1)
        # todo calulate the output! update the label

    def update_output(self):
        # print(self.c_speed)
        # print(self.p_speed)
        # print(self.recipe_time)
        pass

    def update_recipe(self, recipe_name, amount, paths, time):
        self.recipe_time = time
        if self.recipe_name == recipe_name:
            self.amount = max(float(self.amount), float(amount) * float(paths))
        else:
            self.amount = amount * paths
        print(self.amount)
        self.recipe_name = recipe_name
        self.update_output()

    def update_p_speed(self, new_speed):
        self.p_speed = new_speed
        self.update_output()

    def update_c_speed(self, new_speed):
        self.c_speed = new_speed
        self.update_output()


def main():
    recipe_data = load_recipe_data()

    window = tk.Tk()
    window.title("Row length calculator")
    # window.geometry('500x600')

    output = output_calculator(window)
    ingredients = manage_ingredients(window, recipe_data, output)
    recipe = recipe_select(window, recipe_data, ingredients)
    crafting_speed = crafting_speed_select(window, output)
    path_speed = path_speed_select(window, output)

    window.mainloop()


main()
