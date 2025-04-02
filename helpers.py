import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib
matplotlib.use('Agg') # Use a non-interactive backend to prevent thread crashes in flask
import matplotlib.pyplot as plt

df = pd.read_csv('imdb.csv')
df.replace("\\N",np.nan,inplace=True)
df["startYear"]=pd.to_datetime(df["startYear"],errors='coerce').dt.year
df["endYear"]=pd.to_datetime(df["endYear"],errors='coerce').dt.year
df['genres'] = df['genres'].str.replace("\\N","").str.split(',')
df_exploded = df.explode('genres')

#Function to get unique genres
def get_unique_genres():
    #Returns a list of unique genres
    unique_genres = df_exploded['genres'].dropna().unique().tolist()
    return unique_genres

#Function to get unique years
def get_unique_years():
    #Returns a list of unique years
    unique_years=df['startYear'].dropna().unique().tolist()
    return unique_years

#function to get Top 10 movies using BOth Genres & yaers
def get_top10_both(genre,year,HTML=True):
    #Returns top 10 movies based on the genre and year 
    #year should be in int and genre is string
    df_filtered = df_exploded[(df_exploded["genres"] == genre) & (df_exploded["startYear"] == year)].sort_values(by='averageRating', ascending=False).head(10)
    if(HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]

#Function to get Top 10 movies based on genre
def get_top10_genre(genre,HTML=True):
    #Returns top 10 movies based on the genre
    df_filtered = df_exploded[df_exploded["genres"]==genre].sort_values(by='averageRating',ascending=False).head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]

#Function to get Top 10 movies based on year 
def get_top10_year(year,HTML=True):
    #Returns top 10 movies based on the year
    #year should be in int
    df_filtered = df[df["startYear"]==year].sort_values(by='averageRating',ascending=False).head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]

#Function to get Top 10 movies of all time from all genres
def get_top10_any(HTML=True):
    df_filtered= df.sort_values(by="averageRating",ascending=False).reset_index().head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]


#function to get yearwise average runtime of movies
def get_yearwise_runtime(HTML=False):
    #Returns yearwise average runtime of movies in JSON format
    df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')
    df['runtimeMinutes'] = df['runtimeMinutes'].fillna(0)
    yearly_runtime = df.groupby('startYear')['runtimeMinutes'].mean()
    yearly_runtime = yearly_runtime.reset_index()
    yearly_runtime.rename(columns={"runtimeMinutes": "Average_Runtime"}, inplace=True)
    if HTML:
        return yearly_runtime.to_html(classes='runtime-table', header=True)
    return yearly_runtime.to_json(orient='records')

#function to get year vs Genre
def get_year_vs_genre(HTML=False):
    #Returns year vs genre in JSON format where key is year and list of genre is the value
    year_table=df_exploded.pivot_table(
        index='startYear',
        columns='genres',
        values='imdbID',
        aggfunc='count'
    )
    year_table = year_table.fillna(0)
    year_table = year_table.reset_index()
    if HTML:
        return year_table.to_html(classes='genre-table', header=True)
    return year_table.to_json(orient="records")

#function to get yearwise count of total movies
def get_yearwise_count(HTML=False):
    #Returns yearwise count of total movies in JSON format
    yearwise_count = df.groupby('startYear')['imdbID'].count()
    yearwise_count = yearwise_count.reset_index()  
    yearwise_count.rename(columns={"imdbID": "Count"}, inplace=True)
    if HTML:
        return yearwise_count.to_html(classes='runtime-table', header=True)
    return yearwise_count.to_json(orient="records")


#function to generate a graph of json using matplotlib
def generate_graph(data,key1,key2, filename="static/graph.png",title="Graph"):
    #data should be a list of dictionaries
    x = [item[key1] for item in data]
    y = [item[key2] for item in data]
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker='o')
    # plt.bar(x,y)
    plt.xlabel(key1)
    plt.ylabel(key2)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
