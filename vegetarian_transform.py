from pprint import pprint
import random

# Assuming lacto-ovo vegetarian diet: eat eggs and dairy products, but no meat, poultry or fish. 
meat_and_fish = set(['beef', 'steak', 'turkey', 'chicken', 'turkey', 'bacon', 'ham', 'pork', 'lamb', 'fish', 'cod', 'salmon', 'tuna', 'sardines', 'sheep', 'duck', 'veal'])
meat_substitutes = set(['seitan', 'tofu', 'tempeh', 'beans', 'chickpeas', 'mushrooms', 'jackfruit', 'eggplant', 'lentils', 'cauliflower'])
seafood = set(['calimari', 'shrimp', 'oyster', 'clam', 'prawns', 'lobster', 'crayfish', 'mussels', 'octopus'])
seafood_substitues =  set(['eggplant', 'tofu', 'mashed chickpeas'])


test_string = "Stir fry a pound of chicken and some shrimp"
test_string_reverse = "Stir fry a pound of chickpeas and some tofu"

def to_vegetarian(ingredients):
	for word in ingredients.split():
		if word in meat_and_fish:
			chosen_substitute = random.sample(meat_substitutes, 1)[0]
			ingredients = ingredients.replace(word, chosen_substitute)

		if word in seafood:
			chosen_substitute = random.sample(seafood_substitues, 1)[0]
			ingredients = ingredients.replace(word, chosen_substitute)

	return ingredients

def from_vegetarian(ingredients):
	for word in ingredients.split():
		if word in meat_substitutes:
			chosen_substitute = random.sample(meat_and_fish, 1)[0]
			ingredients = ingredients.replace(word, chosen_substitute)

		if word in seafood_substitues:
			chosen_substitute = random.sample(seafood, 1)[0]
			ingredients = ingredients.replace(word, chosen_substitute)

	return ingredients


print(to_vegetarian(test_string))
print(from_vegetarian(test_string_reverse))