import sqlite3


con = sqlite3.connect('db.sqlite3')


def sql_fetch(con):

    cursorObj = con.cursor()

    cursorObj.execute('SELECT * FROM base_task')

    print(cursorObj.fetchall())

sql_fetch(con)