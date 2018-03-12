# EECS337 - Group 13 - Recipes Parser and Transformer

## Prerequisites

* Pandas
* Re.py
* BeautifulSoup 4.4
* Requests
* Glob
* Argparse

## Running

The main file to call is allrecipes.py. We use an argument parser to input different options.
First we need a URL to scrape from allrecipes.com
```
python allrecipes.py -url https://www.allrecipes.com/...
```

### Options

* -list - lists all the ingredients, tools, and methods used in the recipe
* -parse - creates a computer friendly format for the recipe directions
* -transform - prompts the user to transform the recipe to a few different options

### Option Combinations
* -list
* -parse
* -transform
* -list -transform
* -parse -transform

Here are a few examples:
```
python allrecipes.py -url https://www.allrecipes.com/... -list
```
or
```
python allrecipes.py -url https://www.allrecipes.com/... -parse -transform
```
