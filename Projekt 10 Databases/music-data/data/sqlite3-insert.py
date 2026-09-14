import sqlite3, time, datetime

con = sqlite3.connect("test-insert.db") # connection
con.row_factory = sqlite3.Row

sql = """CREATE TABLE IF NOT EXISTS posts(
        date TEXT,
        username TEXT,
        title TEXT,
        body TEXT,
        likes INTEGER
    )"""

con.execute(sql)
con.commit()

now = datetime.datetime.now()
donatelink = "https://www.coca-colastore.com/share-a-coke-personalized-12-fl-oz-can-of-coca-cola"

while True:
    print(f"Press 1 to input new data \nPress 2 to search from information \nPress 3 to change data \nPress 4 to list all information\nPress 5 to donate")
    Choose_option = input("Choose your input search: ")
    if Choose_option is not 0:
        Option_state = True

        while Option_state:

            if Choose_option == 1:
                print(f"Type the following information to add to the database:")
                username = input("Username: ")
                title = input("Title: ")
                date = now.strftime("%Y-%m-%d %H:%M:%S")
                body = input("Body: ")
                likes = input("Likes: ")
                id = input("ID: ")
                con.execute("INSERT INTO posts(username,title,date,body,likes,id) VALUES (?,?,?,?,?,?);",(username,title,date,body,likes,id))
                con.commit()

            elif Choose_option == 2:
                print("You can find information from the following data: Username, Title and id")
                search_term = input("Input your searchterm all lower case letters: ")
                search_term2 = input("Input your specific username, title or id")
                res = con.execute(f"select {search_term} from db WHERE {search_term2};")

                results = res.fetchall()
                for i in results:
                    print("Username: ",i[0], ":::","Title: ", i[1], ":::", "Date: ", i[2], ":::", "Body: ", i[3], ":::", "Likes: ", i[4], ":::", "ID: ", i[5])
            elif Choose_option == 3:
                A
            elif Choose_option == 4:
                print(f"here is our way for you to donate to out further creation of this platform: {donatelink}")
    #res = con.execute("select * from track where name like ?;", [search_term])
    #tracks = res.fetchall()

    #print("Results:")
    #for t in tracks:
    #    print(t['duration']/(1000*60), t[2], t['name'])
    #print('I Love femboys')

