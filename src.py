# !/usr/bin/env python3
import requests
import json
import pandas as pd
import unicodecsv as csv

# Method to seperate/filter out extra genres from the data
def Seperate_Genre(Dict,data):
    newDict = Dict
    Genre = data['Genre']
    List = Genre.split(",")
    num = 1
    for genre in List:
        newDict['Genre' +str(num)] = genre
        num+= 1
    for j in range(num,4):
        newDict['Genre' +str(j)] = ""
    return newDict
        
# Method to fetch data and add it to a dictionary
def get_data(data):
    response_result = data['Response']
    Dictionary = {}
    if(response_result == 'True'):
        Dictionary['imdbID'] = data['imdbID']
        Dictionary['Title'] = data['Title']
        Dictionary['Plot'] = data['Plot']
    Dictionary = Seperate_Genre(Dictionary,data)
    return Dictionary

def main():
    movie_count = 0
    index = 9120
    movies = pd.read_csv('links.csv')
    fieldNames = ['imdbID', 'Title', 'Plot', 'Genre1', 'Genre2', 'Genre3'];
    with open('dataset.csv','wb') as csvfile:
        csvwriter = csv.DictWriter(csvfile, fieldNames, extrasaction='ignore')
        csvwriter.writeheader()
        for i in range(0,index):
            if movies['imdbId'][i] > 100000:
                response = requests.get("http://www.omdbapi.com/?i=tt0"+str(movies['imdbId'][i])+"&apikey=")
                data = json.loads(response.text)
                type = data['Type']
                print(type)
                res = data['Response']
                if res == 'True':
                    if type == 'movie' and data['Plot'] > 50 and data['Genre'] != 'N/A':
                        movie_count += 1
                        Dict = get_data(data)
                        print(Dict)
                        csvwriter.writerow(Dict)
                        Dict = {}
                else:
                    continue

if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()