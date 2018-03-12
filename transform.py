# Work done by Wesley

import random

import data
import recipe
import instructions


def transform(url, type, to_from, list_tag=False, parse_tag=False):
    path = './data/food/' + type + '/'
    allrecipes_ingredients, allrecipes_steps = data.get_recipe_online(
        url)

    measurements_all = data.get_measurements()
    ingredients_all = data.get_ingredients_all()
    ingredients_dict_type = data.get_ingredients_dict(path + 'type/')
    ingredients_dict_nontype = data.get_ingredients_dict(path + 'nontype/')
    tools_all = data.get_tools()
    primary_methods_all = data.get_primary_cooking_methods()
    secondary_methods_all = data.get_secondary_cooking_methods()

    ingredient_list = recipe.get_ingredient_info(
        allrecipes_ingredients, ingredients_all, measurements_all)
    if to_from == 'to':
        ingredient_list = transform_ingredient_list(
            ingredient_list, ingredients_dict_nontype, ingredients_dict_type)
    elif to_from == 'from':
        ingredient_list = transform_ingredient_list(
            ingredient_list, ingredients_dict_type, ingredients_dict_nontype)

    if list_tag:
        recipe.list_recipe(url, get_new_ingredient_list(ingredient_list))

    if parse_tag:
        print(instructions.create_database(
            url, new_steps=get_new_steps(allrecipes_steps, ingredient_list), total_ingredients_used=get_new_ingredient_list(ingredient_list)))
    if not (list_tag or parse_tag):
        transform_unedited_recipe(ingredient_list, allrecipes_steps)


def transform_ingredient_list(ingredient_list, source_ingredients, target_ingredients):
    # for every section of food
    for key in source_ingredients.keys():
        if key in target_ingredients.keys():
            # for every ingredient in the list, check if its in the specific section of food
            for ingredient in ingredient_list['ingredients']:
                if ingredient in source_ingredients[key]:
                    chosen_substitute = random.sample(
                        target_ingredients[key], 1)[0]
                    ingredient_transformation = ingredient + ':' + chosen_substitute
                    ingredient_list['ingredients'] = ingredient_list['ingredients'].replace(
                        ingredient, ingredient_transformation)

    return ingredient_list


def get_new_ingredient_list(ingredient_list):
    for ingredient in ingredient_list['ingredients']:
        if ':' in ingredient:
            new_ingredient = ingredient.split(':')[1]
            ingredient_list['ingredients'] = ingredient_list['ingredients'].replace(
                ingredient, new_ingredient)

    return ingredient_list


def get_new_steps(allrecipes_steps, ingredient_list):
    # print(ingredient_list)
    for ingredient in ingredient_list['ingredients']:
        # print(ingredient)
        if ':' in ingredient:
            old_ingredient = ingredient.split(':')[0]
            # print(old_ingredient)
            new_ingredient = ingredient.split(':')[1]
            # print(new_ingredient)
            allrecipes_steps = [step.replace(old_ingredient, new_ingredient)
                                for step in allrecipes_steps]

    return allrecipes_steps


def transform_unedited_recipe(ingredient_list, allrecipes_steps):

    new_steps = get_new_steps(allrecipes_steps, ingredient_list)
    new_ingredient_list = get_new_ingredient_list(ingredient_list)
    print('\n')
    print('Ingredients:')
    print(new_ingredient_list)
    print('\n')
    print('Steps:')
    i = 0
    for step in new_steps:
        i += 1
        if step:
            print(str(i) + ')   ' + step)
    print('\n')
