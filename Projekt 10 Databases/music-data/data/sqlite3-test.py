import sqlite3

Option_state = False
Choose_option = 0
Search_list = []
search_query = []
con = sqlite3.connect("music.db")
con.row_factory = sqlite3.Row

print(f"Press 1 to list artists \nPress 2 to list albums \nPress 3 to list tracks \nPress 4 for specific search")
Choose_option = input("Choose your input search")
if Choose_option is not 0:
    Option_state = True

while Option_state == True:
    if Choose_option == 1:
        res = con.execute(f"select * from artist;")

        artists = res.fetchall()
        for t in artists:
            print("Name:",t[0], ":::","Id:", t[1])

    elif Choose_option == 2: 
        res = con.execute(f"select * from album;")

        albums = res.fetchall()
        for t in albums:
            print("Name:",t[0], ":::","Id:", t[1])

search_term = input("Seperate search term by comma:")
Search_list.append(search_term)
print("LIST:", Search_list)

for i in Search_list:
    res = con.execute(f"select {Search_list[i]} from track;")
    search_query.append(res)

tracks = res.fetchall()
for t in tracks:
    print(search_term,t[search_term])



### MUSIC PLAYER :3 ###
#    Press 1 to list artists
#    Press 2 to list albums
#    Press 3 to list tracks