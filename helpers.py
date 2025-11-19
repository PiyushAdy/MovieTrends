import pandas as pd
import numpy as np
from io import BytesIO
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

df = pd.read_csv('imdb.csv')
df.replace("\\N",np.nan,inplace=True)
df["startYear"]=pd.to_datetime(df["startYear"],errors='coerce').dt.year
df["endYear"]=pd.to_datetime(df["endYear"],errors='coerce').dt.year
df['genres'] = df['genres'].str.replace("\\N","").str.split(',')
df_exploded = df.explode('genres')


def get_unique_genres():
   
    unique_genres = df_exploded['genres'].dropna().unique().tolist()
    return unique_genres


def get_unique_years():

    unique_years=df['startYear'].dropna().unique().tolist()
    return unique_years

def get_top10_both(genre,year,HTML=True):

    df_filtered = df_exploded[(df_exploded["genres"] == genre) & (df_exploded["startYear"] == year)].sort_values(by='averageRating', ascending=False).head(10)
    if(HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]


def get_top10_genre(genre,HTML=True):
    df_filtered = df_exploded[df_exploded["genres"]==genre].sort_values(by='averageRating',ascending=False).head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]

def get_top10_year(year,HTML=True):
 
    df_filtered = df[df["startYear"]==year].sort_values(by='averageRating',ascending=False).head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]


def get_top10_any(HTML=True):
    df_filtered= df.sort_values(by="averageRating",ascending=False).reset_index().head(10)
    if (HTML):
        return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']].to_html(classes='movies-table',header=True)
    return df_filtered.loc[:,['primaryTitle','averageRating','startYear','genres']]



def get_yearwise_runtime(HTML=False):

    df['runtimeMinutes'] = pd.to_numeric(df['runtimeMinutes'], errors='coerce')
    df['runtimeMinutes'] = df['runtimeMinutes'].fillna(0)
    yearly_runtime = df.groupby('startYear')['runtimeMinutes'].mean()
    yearly_runtime = yearly_runtime.reset_index()
    yearly_runtime.rename(columns={"runtimeMinutes": "Average_Runtime"}, inplace=True)
    if HTML:
        return yearly_runtime.to_html(classes='runtime-table', header=True)
    return yearly_runtime.to_json(orient='records')


def get_year_vs_genre(HTML=False):
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

def get_yearwise_count(HTML=False):
    yearwise_count = df.groupby('startYear')['imdbID'].count()
    yearwise_count = yearwise_count.reset_index()  
    yearwise_count.rename(columns={"imdbID": "Count"}, inplace=True)
    if HTML:
        return yearwise_count.to_html(classes='runtime-table', header=True)
    return yearwise_count.to_json(orient="records")



def generate_graph(data,key1,key2, filename="static/graph.png",title="Graph"):
    x = [item[key1] for item in data]
    y = [item[key2] for item in data]
    plt.figure(figsize=(12, 6))
    plt.plot(x, y, marker='o')
    plt.xlabel(key1)
    plt.ylabel(key2)
    plt.title(title)
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    
