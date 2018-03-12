# Work done by Diego

import re
import pandas as pd

import data
import recipe


def get_individual_steps(allrecipes_steps, primary_methods_all, secondary_methods_all):
    individual_steps = []
    for step in allrecipes_steps:
        individual_steps = individual_steps + step.split('.')

    individual_steps = split_clauses(
        individual_steps, primary_methods_all, secondary_methods_all)
    individual_steps = split_clauses(
        individual_steps, primary_methods_all, secondary_methods_all)

    individual_steps = list(filter(None, individual_steps))

    for i in range(len(individual_steps)):
        individual_steps[i] = individual_steps[i].lstrip()

    return individual_steps


def split_clauses(individual_steps, primary_methods_all, secondary_methods_all):
    for step in individual_steps:
        clause_regex = ', and \w+'
        clause_found = re.search(clause_regex, step, re.IGNORECASE)
        split = False
        if clause_found is not None:
            clause_found = clause_found.group()
            for method in primary_methods_all:
                method_tmp = method + ' '
                if method_tmp in clause_found:
                    split = True
            for method in secondary_methods_all:
                method_tmp = method + ' '
                if method_tmp in clause_found:
                    split = True
        if split:
            step_index = individual_steps.index(step)
            step_split = step.split(', and ')
            step_split[0] = step_split[0].lstrip()
            step_split[1] = step_split[1].lstrip()
            individual_steps = individual_steps[0:step_index] + \
                step_split + individual_steps[step_index + 1:]

    return individual_steps


def create_database(url, total_ingredients_used=None, new_steps=None):
    allrecipes_ingredients, allrecipes_steps = data.get_recipe_online(url)

    if new_steps is not None:
        allrecipes_steps = new_steps

    measurements_all = data.get_measurements()
    ingredients_all = data.get_ingredients_all()
    tools_all = data.get_tools()
    primary_methods_all = data.get_primary_cooking_methods()
    secondary_methods_all = data.get_secondary_cooking_methods()

    if total_ingredients_used is None:
        total_ingredients_used = recipe.get_ingredient_info(
            allrecipes_ingredients, ingredients_all, measurements_all)

    primary_methods_used = recipe.get_step_info(
        allrecipes_steps, primary_methods_all)
    secondary_methods_used = recipe.get_step_info(
        allrecipes_steps, secondary_methods_all)
    tools_used = recipe.get_step_info(allrecipes_steps, tools_all)

    df = pd.DataFrame(columns=['Method', 'Tool', 'Ingredients', 'Time'])
    individual_steps = get_individual_steps(
        allrecipes_steps, primary_methods_all, secondary_methods_all)
    for step in individual_steps:
        method = recipe.get_keyword(step, primary_methods_used)
        if method is None:
            method = recipe.get_keyword(step, secondary_methods_used)

        tool = recipe.get_keyword(step, tools_used)

        ingredients = []
        step_tmp = step
        while(recipe.get_keyword(step_tmp, total_ingredients_used['ingredients']) is not None):
            ingredient = recipe.get_keyword(
                step_tmp, total_ingredients_used['ingredients'])
            step_tmp = step_tmp.replace(ingredient, '')
            ingredients.append(ingredient)

        time_regex = '\d+ .{0,8}(minute(s?)|hour(s?))'
        time = re.search(time_regex, step, re.IGNORECASE)
        if time is not None:
            time = time.group()

        df = df.append({'Method': method, 'Tool': tool,
                        'Ingredients': ingredients, 'Time': time}, ignore_index=True)

    return df


# print(create_database("https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/?internalSource=streams&referringId=95&referringContentType=recipe%20hub&clickId=st_recipes_mades"))
