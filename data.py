# Work done by Sebastian and Lauren

import bs4
import requests
import glob


def get_ingredients_dict(food_path=None):
    if food_path is None:
        food_path = './data/food/'
    food_types = glob.glob(food_path + '*.txt')
    food_types = [food.replace(food_path, '').replace(
        '.txt', '') for food in food_types]
    food_dict = {}
    for food in food_types:
        food_dict[food] = get_info(food_path + food + '.txt')
    return food_dict


def get_ingredients_all():
    food_dict = get_ingredients_dict()
    ingredients = []
    for key in food_dict.keys():
        ingredients = ingredients + food_dict[key]
    return ingredients


def get_measurements():
    return get_info('./data/measurements.txt')


def get_descriptors():
    return get_info('./data/descriptors.txt')


def get_preparations():
    return get_info('./data/preparations.txt')


def get_tools():
    return get_info('./data/tools.txt')


def get_primary_cooking_methods():
    return get_info('./data/primary_cooking_methods.txt')


def get_secondary_cooking_methods():
    return get_info('./data/secondary_cooking_methods.txt')


def get_info(filename):
    text_file = open(filename, "r")
    lines = text_file.read().split('\n')
    if '' in lines:
        lines.remove('')
    for i in range(0, len(lines)):
        lines[i] = lines[i].lower()
    return lines


def get_recipe_online(url):
    response = requests.get(url)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    ingredients = [ingredient.text.lower() for ingredient in soup.find_all(
        'span', attrs={'itemprop': 'ingredients'})]

    steps = [step.text.lower() for step in soup.find_all(
        'span', {'class': 'recipe-directions__list--item'})]

    return ingredients, steps


def save_unk(ingredients_unk):
    filename = './data/food/unk.txt'
    with open(filename, "r+") as f:
        lines = f.read().split('\n')
        if '' in lines:
            lines.remove('')
        lines = lines + ingredients_unk
        f.seek(0)
        for line in lines:
            f.write("%s\n" % line)
        f.truncate()
