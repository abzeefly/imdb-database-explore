#!/usr/bin/python3

"""
This is a sample program for COMP3311 20T1 Assignment 2 to illustrate how to write an 
executable python code, take in commandline an argument, and connect to a sqlite3 db.
For simplicity (make it short and easier to read), it does not include much error checking,
exception handling and comments.
"""


import sqlite3,sys
import numpy

if len(sys.argv)  < 4 :
  print("Usage:",sys.argv[0],"TOO FEW ARGUMENTS PROVIDED")
  sys.exit(1)

if len(sys.argv)  > 5 :
  print("Usage:",sys.argv[0],"TOO MANY ARGUMENTS PROVIDED")
  sys.exit(1)

if len(sys.argv)  is 5 :

    user_input = sys.argv[1]
    user_genres = user_input.split('&')
    num_genres = len(user_genres)
    user_genres = tuple(user_genres)

    size = sys.argv[2]
    start_year = sys.argv[3]
    end_year = sys.argv[4]


    con = sqlite3.connect('a2.db')

    cur = con.cursor()

    cur.execute('SELECT m.id, m.title, g.genre FROM movie m, genre g WHERE m.id = g.movie_id and g.genre in {}'.format(user_genres))

    count = 1
    movie_dict = {}
    result = []
    while True:
        t = cur.fetchone()
        if t == None:
            break
        m_id, title, genre = t
        if m_id not in movie_dict:
            movie_dict[m_id] = 1
        else:
            movie_dict[m_id] += 1

    for (key,value) in movie_dict.items():
        if value is num_genres:
            result.append(key)

    if len(result) is 1:
        result = result[0]
    else:
        result = tuple(result)

    cur.execute('SELECT m.id, m.title,m.year,m.content_rating, m.lang,r.imdb_score,r.num_voted_users FROM movie m, rating r WHERE m.year IS NOT NULL and m.id = r.movie_id and m.id in {} and m.year >= {} and m.year <={} ORDER BY r.imdb_score DESC, r.num_voted_users DESC LIMIT {} '.format(result, start_year, end_year, size))

    count = 1
    genres = []
    while True:
        t = cur.fetchone()
        if t == None:
            break
        m_id, title,year,rating,lang,score,votes = t
        print('{}. {} ({}, {}, {}) [{}, {}]'.format(count,title,year,rating,lang,float(score),votes))

        count +=1

    con.close()

else:
    size = sys.argv[1]
    start_year = sys.argv[2]
    end_year = sys.argv[3]

    con = sqlite3.connect('a2.db')

    cur = con.cursor()
    cur.execute('SELECT m.id, m.title,m.year,m.content_rating, m.lang,r.imdb_score,r.num_voted_users FROM movie m, rating r WHERE m.year IS NOT NULL and m.id = r.movie_id and m.year >= {} and m.year <={} ORDER BY r.imdb_score DESC, r.num_voted_users DESC LIMIT {} '.format(start_year, end_year, size))

    count = 1
    genres = []
    while True:
        t = cur.fetchone()
        if t == None:
            break
        m_id, title,year,rating,lang,score,votes = t
        print('{}. {} ({}, {}, {}) [{}, {}]'.format(count,title,year,rating,lang,float(score),votes))

        count +=1

    con.close()


