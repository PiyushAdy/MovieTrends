from flask import Flask, render_template, request, redirect, url_for, session
from helpers import *
from pandas import isnull
from numpy import isnan
# from gemini import *
from gemini_lite import *
import json 

app=Flask(__name__)

@app.route('/')
@app.route("/dashboard")
def index():
    genre_lst=list(get_unique_genres())
    year_lst=sorted(list(get_unique_years()),reverse=True)
    return render_template('dashboard_V2.html',genre_lst=genre_lst,year_lst=year_lst)

@app.route("/top-10-movies",methods=["GET"])
def top10():
    genre=request.args.get('genre',None)
    year=request.args.get('year',None)
    if genre =="":
        genre=None
    if year=="":
        year=None
    try:
        if year!=None:
            year=float((request.args.get('year',None)))
    except:
        return "Invalid Year Provided"
    if year is None and genre is not None:
        data=get_top10_genre(genre)
        heading=f"Top 10 {genre} Movies"
        data_type="Genre"
    elif year is not None and genre is None:
        data=get_top10_year(year)
        heading=f"Top 10 Movies of {year}"
        data_type="Year"
    elif year is  not  None and genre is not None:
        data=get_top10_both(genre,year)
        heading=f"Top 10 {genre} Movies of {year}"
        data_type="Genre and Year"
    else:
        data=get_top10_any()
        heading="Top 10 Movies of all time from all genres"
        data_type=""
    return render_template("top10.html",table_data=data,heading=heading,AI_analysis=Interpret_HTML(data,data_type))


@app.route("/runtime")
def runtime():
    data=json.loads(get_yearwise_runtime())
    table_data=get_yearwise_runtime(HTML=True)
    generate_graph(data,key1="startYear",key2="Average_Runtime",filename="static/runtime_graph.png",title="Yearwise Average Runtime of Movies")
    return render_template("Runtime.html",table_data=table_data,heading="Yearwise Average Runtime of Movies",AI_analysis=Interpret_HTML(data,"Yearwise Average Runtime of Movies"))

@app.route("/count")
def yearwise_count():
    data=json.loads(get_yearwise_count())
    table_data=get_yearwise_count(HTML=True)
    generate_graph(data,key1="startYear",key2="Count",filename="static/yearwise_count_graph.png",title="Yearwise Count of Movies")
    return render_template("Count.html",table_data=table_data,heading="Yearwise Count of Movies",AI_analysis=Interpret_HTML(data,"Yearwise Count of Movies"))

@app.route("/year-vs-genre")
def year_vs_genre():
    data=get_year_vs_genre()
    table_data=get_year_vs_genre(HTML=True)
    return render_template("genre_distribution_V2.html",table_data=table_data,heading="Year vs Genre",AI_analysis=Interpret_HTML(data,"Year vs Genre"))

if __name__=="__main__":
    app.run(host="0.0.0.0",debug=True)
