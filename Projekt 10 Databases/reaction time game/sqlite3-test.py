import sqlite3

con = sqlite3.connect("Projekt 10 Databases/music-data/data/music.db") # Connection

res = con.execute("select * from artist;")

print(res)