
# coding: utf-8

# In[ ]:


import bs4
import requests


# In[ ]:


# Load the page
url = "https://www.allrecipes.com/recipe/213656/amazing-crusted-chicken/"
response = requests.get(url)
soup = bs4.BeautifulSoup(response.text, 'lxml')


# In[ ]:


# Find the ingredients
ingredients = [ingredient.text for ingredient in soup.find_all('span', attrs={'itemprop': 'ingredients'})]
ingredients


# In[ ]:


# Find the steps
steps = [step.text for step in soup.find_all('span', {'class': 'recipe-directions__list--item'})]
steps

