#!/usr/bin/env python
# coding: utf-8

# # Project: Investigate a Dataset - [tmdb-movies.csv]
# 
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# ### Dataset Description 
# 
# > This data set contains information about 10,000 movies collected from The Movie Database (TMDb), including user ratings and revenue. 
#   - Certain columns, like ‘cast’ and ‘genres’, contain multiple values separated by pipe (|) characters.
#   - The final two columns ending with “_adj” show the budget and revenue of the associated movie in terms of 2010 dollars, accounting for inflation over time.
# 
# ### Question(s) for Analysis
# #### Question No 1 : are the Run times of movies changes over the time ?
# #### Question No 2 : what are the Longest and shortest Movies ?
# #### Question No 3 : what is the year with most number of movies releases ?
# #### Question No 4 : What are the movies with heighest and lowest profit ?
# #### Question No 5:  which movie has the most voting counts ?
# #### Question No 6: what are the most popular genre over the years?
# #### Question No 7: who are the top 10 directors with the most number of movies ?
# #### Question No 8: what are the Top 10 Production compines with the most number of movies ?
# #### Question No 9: what are the Top 10 Profitable Movies ?

# In[3]:


# Use this cell to set up import statements for all of the packages that you
#   plan to use.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Remember to include a 'magic word' so that your visualizations are plotted
#   inline with the notebook. See this page for more:
#   http://ipython.readthedocs.io/en/stable/interactive/magics.html
get_ipython().run_line_magic('matplotlib', 'inline')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# > In this section of the report, load in the data, check for cleanliness, and then trim and clean the dataset for analysis.

# In[4]:


# Load your data and print out a few lines. Perform operations to inspect data
#   types and look for instances of missing or possibly errant data.
df=pd.read_csv('tmdb-movies.csv')
df.head()


# 
# ### Data Cleaning
#  

# In[5]:


# the dimensions of the dataframe
df.shape


# In[6]:


# the datatypes of the columns
df.dtypes


# In[7]:


# although the datatype for imdb_id appears to be object, further investigation shows it's a string
type(df['imdb_id'][0])


# In[9]:


# although the datatype for original_title appears to be object, further investigation shows it's a string
type(df['original_title'][0])


# #### Concalusion: Pandas actually stores pointers to strings in dataframes and series, which is why object instead of str appears as the datatype. so that strings will appear as objects in Pandas. 

# In[10]:


# summary of the dataframe,including the number of non-null values in each column
df.info()


# In[17]:


# the number of unique values in each column
df.nunique()


# In[12]:


# using means to fill in missing values
df.fillna(df.mean(), inplace=True)
# confirm correction with info()
df.info()


# In[13]:


# check for duplicates in the data
sum(df.duplicated())


# In[14]:


# drop duplicates
df.drop_duplicates(inplace=True)
# confirm correction by rechecking for duplicates in the data
sum(df.duplicated())


# In[16]:


df.nunique()


# In[18]:


df=df.drop(columns = ['homepage','imdb_id','cast','tagline','budget_adj','revenue_adj'])
df.describe()


# In[19]:


print("Number of Rows",df.shape[0])
print("Number of columns",df.shape[1])


# In[25]:


#check any missing values 
df.isnull().values.any()


# In[22]:


df.isnull().sum()


# In[23]:


#check duplicted values 
df.duplicated().any()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# 
# 
# > Investigate the stated question(s) from multiple angles.
# 
# ### Research Question 1 Are the Run times of movies changes over the time ?

# In[27]:


# Run times of movies > 60 minutes = 1 hour
df=df[df['runtime']>60]
df.describe()


# In[28]:


#histogram to explain the changes of movies run times over the time 
plt.hist(df['runtime'],range=(60,200) , bins = 20)
plt.title('Movies Run times ')
plt.xlabel('minutes')
plt.ylabel('No. of Movies')
plt.show()


# ## we can see that the most of the movies runtime between 85 to 120 minutes

# In[32]:


# Avg movies runtimes over the years
movies_group=df['runtime'].groupby(df['release_year']).describe()
avg_runtime_by_year = movies_group['mean']
avg_runtime_min = movies_group['mean'] - movies_group['std']
avg_runtime_max = movies_group['mean'] + movies_group['std']


# In[34]:


print (avg_runtime_by_year)


# In[35]:


print (avg_runtime_min)


# In[36]:


print (avg_runtime_max)


# #### we can see clearly that the avg. runtimes of movies over years not changed very much over time.

# ### Research Question 2  what are the Longest and shortest Movies ?

# In[37]:


print(df.original_title[df.runtime == df.runtime.max()])
print(df.runtime[df.runtime == df.runtime.max()])


# #### the longest Moive : [The Story of Film: An Odyssey] with runtimes 900 Minutes

# In[38]:


print(df.original_title[df.runtime == df.runtime.min()])
print(df.runtime[df.runtime == df.runtime.min()])


# #### the shortest movies with runtimes 61 minutes: 
#  - Ju-on: Shiroi rÃ´jo
#  - Aziz Ansari: Dangerously Delicious
#  - Zach Galifianakis: Live at the Purple Onion
#  - Bill Hicks: Relentless

# ### Research Question 3  what is the year with most number of movies releases ?

# In[53]:


df['release_year'].hist(figsize=(8,8));


# In[47]:


plt.figure(figsize=(30,15))
sns.countplot(df['release_year'])
plt.title('Movies Released per year')
plt.xlabel('release year')
plt.ylabel('No of movies')
plt.show()


# #### 2014 is the Most year have the Movies releases about 680 Moives releases

# ### Research Question 4   What are the movies with heighest and lowest profit ?

# > **Tip**:  PROFIT = REVENUE - BUDGET   so i will creat nwe col with name " PROFIT" by the above equation

# In[80]:


#creation Profit Col.
df['Profit'] = df['revenue'] - df['budget']
df.describe()


# In[56]:


# the Max Profit Movies 
print(df.original_title[df['Profit']==df['Profit'].max()])


# In[57]:


# the Min Profit Movies 
print(df.original_title[df['Profit']==df['Profit'].min()])


# #### The Max Profit Movie is Avatar 
# #### The Min Profit Movie is The Warrior's Way

# ### Research Question 5   which movie has the most voting counts ?

# In[58]:


#the movie which has the most voting counts
print(df.original_title[df['vote_count']==df['vote_count'].max()])


# #### INCEPTION MOVIE has the most voting counts

# ### Research Question 6   what are the most popular genre over the years?

# In[62]:


# Creat genres sum 
genres = df['genres'].str.get_dummies(sep='|')
genres_sum = df['genres'].str.get_dummies(sep='|').sum().reset_index()
# Plot most popluar genres sum over the years 
plt.figure(figsize=(30,15))
sns.barplot(x=genres.columns, y=genres.sum(), data= genres_sum)
plt.title('Most popular genre over the yaers')
plt.xlabel('Genres')
plt.ylabel('Count')
plt.show()


# #### the most generes over the years are:
# - DARAMA 
# - COMEDY
# - THRILLER
# - ACTION
# - ROMANCE
# - HORROR
# - ADVENTURE

# ### Research Question 7 who are the top 10 directors with the most number of movies ?

# In[65]:


df['director'].value_counts().head(10).plot.bar(figsize=(15,10), color = 'blue')
plt.show()


# #### TOP 10 Directors as shown 
# - WOODY ALLEN 
# - CLINT EASTWOOD
# - STEVEN SPIELBERG
# - MARTIN SCARSESE
# - RIDLEY SCOTT
# - STEVEN SODERBERGH
# - RON HOWARD
# - JOEL SCHUMACHER
# - BRIAN DE PALMA
# - Barry LEVINSON

# ### Research Question 8 what are the Top 10 Production compines with the most number of movies ?

# In[64]:


df['production_companies'].value_counts().head(10).plot.bar(figsize=(15,10), color = 'orange')
plt.show()


# #### TOP 10 Production Compaines as shown 
# - PARAMOUNT PICTURES
# - UNIVERSAL PICTURES
# - WARNER BROS
# - COLUMBIA PICTURES
# - M-G-M
# - WALT DISNEY
# - NEW LINE
# - TOUCHSTONE PICTURES
# - 20th Century FOX
# - 20 th century fox film Corporation

# ### Research Question 9 what are the Top 10 Profitable Movies ?

# In[74]:


#the top 10 Most Profit Movies
plt.figure(figsize=(40,20))
top_profit = df[['original_title','Profit']].sort_values('Profit', ascending = False).head(10)
sns.barplot(x='original_title', y='Profit', data=top_profit, palette='Blues_r')
plt.xlabel('original_title')
plt.ylabel('Profit')
plt.title('10 Most Profit Movies')
plt.show()


# #### THE TOP 10 Profitable Movies are:
# - AVATAR
# - STAR WARS THE FORCE AWAKEN
# - TITANIC
# - JURASSIC WORLD
# - FURIOUS 7
# - THE AVENGERES
# - HARRY POTTER PART1 : Harry Potter and the Deathly Hallows
# - THE AVENGERES AGE OF ULTRON
# - FROZEN 
# - THE NET

# <a id='conclusions'></a>
# ## Conclusions
# 
# > **1**: the most of the movies runtime between 85 to 120 minutes and the avg. runtimes of movies over years not changed very much over time.
# 
# > **2**: the longest Moive : [The Story of Film: An Odyssey] with runtimes 900 Minutes and the shortest movies with runtimes 61 minutes are:
#  - Ju-on: Shiroi rÃ´jo
#  - Aziz Ansari: Dangerously Delicious
#  - Zach Galifianakis: Live at the Purple Onion
#  - Bill Hicks: Relentless
# 
# > **3**: 2014 is the Most year have the Movies releases about 680 Moives releases
# 
# > **4**: The Max Profit Movie is Avatar & The Min Profit Movie is The Warrior's Way
# 
# > **5**: INCEPTION MOVIE has the most voting counts
# 
# > **6**: the most generes over the years are:
# - DARAMA 
# - COMEDY
# - THRILLER
# - ACTION
# - ROMANCE
# - HORROR
# - ADVENTURE
# 
# > **7**: TOP 10 Directors as shown 
# - WOODY ALLEN 
# - CLINT EASTWOOD
# - STEVEN SPIELBERG
# - MARTIN SCARSESE
# - RIDLEY SCOTT
# - STEVEN SODERBERGH
# - RON HOWARD
# - JOEL SCHUMACHER
# - BRIAN DE PALMA
# - Barry LEVINSON
# 
# > **8**: TOP 10 Production Compaines as shown 
# - PARAMOUNT PICTURES
# - UNIVERSAL PICTURES
# - WARNER BROS
# - COLUMBIA PICTURES
# - M-G-M
# - WALT DISNEY
# - NEW LINE
# - TOUCHSTONE PICTURES
# - 20th Century FOX
# - 20 th century fox film Corporation
# 
# > **9**:THE TOP 10 Profitable Movies are:
# - AVATAR
# - STAR WARS THE FORCE AWAKEN
# - TITANIC
# - JURASSIC WORLD
# - FURIOUS 7
# - THE AVENGERES
# - HARRY POTTER PART1 : Harry Potter and the Deathly Hallows
# - THE AVENGERES AGE OF ULTRON
# - FROZEN 
# - THE NET

# In[77]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])

