import sqlite3 as sq


# таблица с информацией о пользователях
async def create_table_user():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS user(
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id VARCHAR(20) NOT NULL, 
                login VARCHAR(20) NOT NULL, 
                fullname VARCHAR(128) NOT NULL, 
                user_status VARCHAR(10) NOT NULL, 
                registration_date VARCHAR(20))""")

    cur.close()
    con.close()


# таблица с сообщениями пользователей
async def create_table_messages():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS messages(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_id INTEGER NOT NULL,
                user_id VARCHAR(20) NOT NULL, 
                message_id INTEGER NOT NULL, 
                message TEXT NOT NULL,  
                message_date VARCHAR(20))""")

    cur.close()
    con.close()


# таблица с тикетами
async def create_table_tickets():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    # ticket_status - new / at_work / close
    cur.execute("""CREATE TABLE IF NOT EXISTS tickets(
                ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id VARCHAR(20) NOT NULL, 
                ticket_status VARCHAR(8) NOT NULL,
                ticket_created_at VARCHAR(20))""")

    cur.close()
    con.close()
