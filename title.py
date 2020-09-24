#!/usr/bin/python3

"""
This is a sample program for COMP3311 20T1 Assignment 2 to illustrate how to write an 
executable python code, take in commandline an argument, and connect to a sqlite3 db.
For simplicity (make it short and easier to read), it does not include much error checking,
exception handling and comments.
"""


import sqlite3,sys

if len(sys.argv) != 2 :
    print("Usage:",sys.argv[0],"TITLE")
    sys.exit(1)

title = sys.argv[1]

con = sqlite3.connect('a2.db')

cur = con.cursor()

cur.execute('SELECT m.id, m.title,m.year,m.content_rating,r.imdb_score, g.genre FROM movie m, genre g, rating r WHERE g.movie_id = m.id and m.id = r.movie_id and m.title LIKE "%{}%"'.format(title))
#
movie_genres = {}
while True:
    t = cur.fetchone()
    if t == None:
        break
    m_id, m_title,year,rating,score,genre  = t
    if m_id not in movie_genres:
        movie_genres[m_id] =[genre]
    else:
        movie_genres[m_id].append(genre)
  
cur.execute('SELECT m.id, m.title,m.year,m.content_rating,r.imdb_score FROM movie m, rating r WHERE m.id = r.movie_id and m.title LIKE "%{}%" ORDER BY case when m.year is null then 1 else 0 end, m.year, r.imdb_score DESC, m.title'.format(title))
count = 1
genres = []
while True:
    t = cur.fetchone()
    if t == None:
        break
    m_id, m_title,year,rating,score  = t
    genres = movie_genres.get(m_id)
    if year is None:
        print('{}. {} ({}, {}) [{}]'.format(count,m_title,rating,float(score),','.join(genres)))
    else:
        print('{}. {} ({}, {}, {}) [{}]'.format(count,m_title,year,rating,float(score),','.join(genres)))
    count +=1

con.close()
