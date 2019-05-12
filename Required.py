import json

CRAFTING_SPEEDS = [0.5, 0.75, 1.25]
PATH_SPEEDS = [7.5, 15, 22.5]

TARGET = {
    'automation-science-pack': 100,
    "chemical-science-pack": 100,
    "logistic-science-pack": 100,
    "military-science-pack": 100,
    "production-science-pack": 100,
    "utility-science-pack": 100
}


def load_recipe_data():
    with open('recipe.json') as json_file:
        data = json.load(json_file)
        return(data)


RECIPE_DATA = load_recipe_data()


class resource():
    def __init__(self, resource, amount, resource_master):
        self.resource = resource
        self.amount = amount
        self.resource_master = resource_master
        self.resource_master.add_resource_amount(self.resource, self.amount)
        self.process_ingredients()
        pass

    def process_ingredients(self):
        if self.resource in RECIPE_DATA.keys():
            self.ingredients = RECIPE_DATA[self.resource]['ingredients']
            for key in self.ingredients:
                resource(key, self.amount *
                         int(self.ingredients[key]), self.resource_master)


class resource_master():
    def __init__(self):
        self.resources = {}
        pass

    def add_resource_amount(self, resource, amount):
        if resource in self.resources.keys():
            new_amount = self.resources[resource] + amount
        else:
            new_amount = amount
        self.resources[resource] = new_amount

    def print_all(self):
        print(self.resources)


def main():
    main_resource_master = resource_master()
    for key in TARGET:
        resource(key, TARGET[key], main_resource_master)
    pass
    main_resource_master.print_all()


main()
