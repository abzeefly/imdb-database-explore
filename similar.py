#!/usr/bin/python3

"""
This is a sample program for COMP3311 20T1 Assignment 2 to illustrate how to write an 
executable python code, take in commandline an argument, and connect to a sqlite3 db.
For simplicity (make it short and easier to read), it does not include much error checking,
exception handling and comments.
"""


import sqlite3,sys
import numpy
from operator import itemgetter
movie = sys.argv[1]
size = int(sys.argv[2])
con = sqlite3.connect('a2.db')

cur = con.cursor()
cur.execute('SELECT m.id,m.title, g.genre FROM movie m, genre g WHERE g.movie_id = m.id and UPPER(m.title) = UPPER("{}")'.format(movie))
movie_genres = []
while True:
    t = cur.fetchone()
    if t == None:
        break
    m_id, m_title,genre  = t
    if genre not in movie_genres:
        movie_genres.append(genre)

num_movie_genre = len(movie_genres)

if num_movie_genre is 1 :
    movie_genres = movie_genres[0]
else:
    movie_genres= tuple(movie_genres)

cur.execute('SELECT m.id,m.title, k.keyword FROM movie m, keyword k WHERE k.movie_id = m.id and UPPER(m.title) = UPPER("{}")'.format(movie))
movie_keywords = []
while True:
    t = cur.fetchone()
    if t == None:
        break
    m_id, m_title,keyword  = t
    if keyword not in movie_keywords:
        movie_keywords.append(keyword)
num_movie_keywords = len(movie_keywords)

if num_movie_keywords is 1 :
    movie_keywords = movie_keywords[0]
else:
    movie_keywords= tuple(movie_keywords)

cur.execute('drop view if exists genre_table')
create_table = """
                CREATE VIEW genre_table as 
                SELECT m.id as id,m.title as title,m.year as year, g.genre as genre, count(g.genre) as genre_count
                FROM movie m, genre g
                WHERE g.movie_id = m.id 
                and g.genre in {}
                GROUP BY m.id
                ORDER BY genre_count DESC
            """
            #     union all
            #     SELECT m.id as id,m.title as title, g.genre genre, k.keyword as keyword,
            #     r.imdb_score as score, r.num_voted_users as votes
            #     FROM movie m, genre g, keyword k, rating r
            #     WHERE g.movie_id = m.id 
            #     and k.movie_id = m.id
            #     and r.movie_id = m.id 
            #     and g.genre in {}
            #     and r.imdb_score IS NULL
            # """
cur.execute(create_table.format(movie_genres))

cur.execute('drop view if exists keyword_table')
create_table = """
                CREATE VIEW keyword_table as 
                SELECT m.id as id,m.title as title,m.year as year, k.keyword as keyword, count(keyword) as keyword_count
                FROM movie m, keyword k
                WHERE k.movie_id = m.id 
                and k.keyword in {}
                GROUP BY m.id
                ORDER BY keyword_count DESC
            """
cur.execute(create_table.format(movie_keywords))

cur.execute('drop view if exists combine')
join_tables = """
                CREATE VIEW combine as 
                SELECT g.title as m_title,g.year as m_year, g.id as m_id, g.genre_count as genre_count, IFNULL(k.keyword_count,0) as keyword_count
                FROM genre_table g
                LEFT JOIN keyword_table k ON
                g.id = k.id
                GROUP BY m_id
                ORDER BY genre_count DESC
            """
cur.execute(join_tables)

cur.execute('drop view if exists final_table')
final_table = """
                CREATE VIEW final_table AS
                SELECT c.m_id as m_id, c.genre_count as genre_count, c.keyword_count as keyword_count,
                c.m_title as m_title, IFNULL(c.m_year,"") as year, r.imdb_score as score, r.num_voted_users as votes
                FROM combine c
                LEFT JOIN rating r ON
                r.movie_id = c.m_id
                GROUP BY c.m_id
                ORDER BY genre_count DESC, keyword_count DESC, score DESC, votes DESC
                LIMIT 1,{}
            """
cur.execute(final_table.format(size))

cur.execute('Select * from final_table')
count = 1
while True:
    t = cur.fetchone()
    if t == None:
        break
    m_id, genre,keyword,title,year,score,votes= t
    if year is "":
        print('{}. {} [{}, {}, {}, {}]'.format(count,title,genre,keyword,float(score),votes)) 
    else:
        print('{}. {} ({}) [{}, {}, {}, {}]'.format(count,title,year,genre,keyword,float(score),votes))
    count +=1

con.close()


