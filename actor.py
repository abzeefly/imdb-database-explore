#!/usr/bin/python3

"""
This is a sample program for COMP3311 20T1 Assignment 2 to illustrate how to write an 
executable python code, take in commandline an argument, and connect to a sqlite3 db.
For simplicity (make it short and easier to read), it does not include much error checking,
exception handling and comments.
"""


import sqlite3,sys

if len(sys.argv) != 2 :
  print("Usage:",sys.argv[0],"ACTOR NAME")
  sys.exit(1)

actor_name = sys.argv[1]

con = sqlite3.connect('a2.db')

cur = con.cursor()

cur.execute('SELECT m.title, d.name, m.year, m.content_rating, r.imdb_score FROM movie m, actor a, acting an ,rating r, director d WHERE m.id = an.movie_id and a.id = an.actor_id and r.movie_id = m.id and d.id = m.director_id and UPPER(a.name) = UPPER("{}") ORDER BY case when m.year is null then 1 else 0 end, m.year, m.title'.format(actor_name))

count = 1
while True:
  t = cur.fetchone()
  if t == None:
    break
  title, name, year, rating, score = t
  if year is None:
    print('{}. {} -- {} ({}, {})'.format(count,title,name, float(rating), score))
  else:
    print('{}. {} -- {} ({}, {}, {})'.format(count,title,name, year, float(rating), score))
  count +=1   

con.close()


