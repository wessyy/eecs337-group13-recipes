# Work done by Sebastian and Lauren

import pandas as pd
import re

import data


def list_recipe(url, total_ingredients_used=None):
    allrecipes_ingredients, allrecipes_steps = data.get_recipe_online(
        url)

    measurements_all = data.get_measurements()
    ingredients_all = data.get_ingredients_all()
    tools_all = data.get_tools()
    primary_methods_all = data.get_primary_cooking_methods()
    secondary_methods_all = data.get_secondary_cooking_methods()

    if total_ingredients_used is None:
        total_ingredients_used = get_ingredient_info(
            allrecipes_ingredients, ingredients_all, measurements_all)
    tools_used = get_step_info(allrecipes_steps, tools_all)
    primary_methods_used = get_step_info(
        allrecipes_steps, primary_methods_all)
    secondary_methods_used = get_step_info(
        allrecipes_steps, secondary_methods_all)

    print('\n')
    print('Ingredients:')
    print(total_ingredients_used)
    print('\n')

    print('Equipment needed:')
    for tool in tools_used:
        print(tool)
    print('\n')

    print('Primary cooking methods:')
    for method in primary_methods_used:
        print(method)
    print('\n')

    print('Secondary cooking methods:')
    for method in secondary_methods_used:
        print(method)
    print('\n')


def get_keyword(unparsed_text, keyword_list):
    for keyword in keyword_list:
        key_regex = keyword + '(s|(es))?'
        key = re.search(key_regex, unparsed_text, re.IGNORECASE)
        if key is not None:
            return key.group()
    return None


def get_ingredient_info(unparsed_ingredients, ingredients_all, measurements_all):
    quantities_used = []
    measurements_used = []
    ingredients_used = []
    ingredients_unk = []

    for unparsed_ingredient in unparsed_ingredients:
        quantity = get_quantity(unparsed_ingredient)
        measurement = get_keyword(unparsed_ingredient, measurements_all)
        ingredient = get_keyword(unparsed_ingredient, ingredients_all)

        # if there is a more precise measurement in parenthesis, use that
        if quantity is not None:
            if '(' in quantity and ')' in quantity:
                measurement = get_keyword(quantity[1:-1], measurements_all)
                quantity = get_quantity(quantity[1:-1])
        else:
            quantity = 1

        # if the ingredient is not in the text file, use the whole unparsed string
        if ingredient is None:
            ingredient = unparsed_ingredient
            if measurement is None:
                measurement = ''
            if quantity is None:
                quantity = ''
            ingredient = ingredient.replace(quantity, '')
            ingredient = ingredient.replace(measurement, '')

        # if there is no measurement unit, use the ingredient as the unit
        # if measurement == None:
        #    measurement = ingredient

        quantities_used.append(quantity)
        measurements_used.append(measurement)
        ingredients_used.append(ingredient)

    return pd.DataFrame({'ingredients': ingredients_used, 'measurement': measurements_used, 'quantity': quantities_used})


def get_quantity(unparsed_ingredient):
    paren_regex = '\(.+\)'
    fraction_regex = '[0-9]+((/|\.)[0-9]+)?'
    found_quantity = re.search(paren_regex, unparsed_ingredient, re.IGNORECASE)
    if found_quantity is None:
        found_quantity = re.search(
            fraction_regex, unparsed_ingredient, re.IGNORECASE)
    if found_quantity is not None:
        return found_quantity.group()
    return None


def get_step_info(unparsed_steps, keyword_list):
    info_list = []
    for unparsed_step in unparsed_steps:
        while(get_keyword(unparsed_step, keyword_list) is not None):
            info = get_keyword(unparsed_step, keyword_list)
            unparsed_step = unparsed_step.replace(info, '')
            info_list.append(info)
    info_list = list(set(info_list))

    return info_list
