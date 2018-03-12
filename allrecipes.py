# Work done by Sebastian and Lauren

import argparse

import data
import recipe
import instructions
import transform

# https://www.allrecipes.com/recipe/23600/worlds-best-lasagna/?internalSource=streams&referringId=95&referringContentType=recipe%20hub&clickId=st_recipes_mades

if __name__ == '__main__':

    # Set up command line parameters.
    parser = argparse.ArgumentParser(
        description='Parse and transform recipes.')

    parser.add_argument('--url', '-url', action='store',
                        default=None,
                        help=('The url to scrape from allrecipes. '))
    parser.add_argument('--list', '-list', action='store_true',
                        default=False,
                        help=('Lists all the ingredients, methods, and tools needed for the recipe.'))
    parser.add_argument('--parse', '-parse', action='store_true',
                        default=False,
                        help=('Parses out the directions of the recipe into a series of steps.'))
    parser.add_argument('--transform', '-transform', action='store_true',
                        default=False,
                        help=('Transforms the recipe from its current state to specific recipe styles.'))
    args = parser.parse_args()

    if args.url:
        if args.transform:
            print('\n')
            print('These are the possible transformations:')
            print('- vegetarian')
            print('- healthy')
            print('- italian')
            print('- chinese')
            print('\n')
            transformation = input(
                'What type of transformation would you like to perform? \n').lower()
            print('\n')
            direction = input(
                'Is this transform \'to\' or \'from\' ' + transformation + '?\n').lower()
            print('\n')

            quit = False
            while(quit == False):
                quit = True
                if transformation in ['vegetarian', 'healthy', 'italian', 'chinese']:

                    if args.list:
                        transform.transform(
                            args.url, transformation, direction, list_tag=True)
                    elif args.parse:
                        transform.transform(
                            args.url, transformation, direction, parse_tag=True)
                    else:
                        transform.transform(
                            args.url, transformation, direction)
                else:
                    transformation = input(
                        'Tranformation not possible. Please type in a transformation or type \'quit\'.\n').lower()
                    print('\n')
                    if transformation != 'quit':
                        quit = False
        elif args.list:
            recipe.list_recipe(args.url)
        elif args.parse:
            print('\n')
            print('Parsed instructions list:')
            print(instructions.create_database(args.url))
            print('\n')

    else:
        print('\n')
        print('Error: A URL is needed to parse and transform a recipe from allrecipes.com')
        print('Use -h for help information.')
        print('\n')
