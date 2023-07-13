import sqlite3 as sq


# проверка на запись в БД
async def exist_registration(user_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute('SELECT user_status FROM user WHERE user_id = ?', (str(user_id),))
    exist = cur.fetchone()

    cur.close()
    con.close()

    if exist is None:
        return True  # юзера нет в БД
    return exist[0]  # юзер уже зарегистрирован, вывести его статус (created/accepted/cancelled)


# выбор пользователей со статусом 'created'
async def select_registration():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM user WHERE user_status = 'created'")
    exist = cur.fetchone()

    cur.close()
    con.close()

    return exist


# список зарегистрированных пользователей
async def accepted_users():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT user_id FROM user WHERE user_status = 'accepted'")
    list_users = cur.fetchall()

    cur.close()
    con.close()

    # список кортежей в список чисел
    list_users = [int(ele[0]) for ele in list_users]

    return list_users


# получить id тикета по user_id
async def select_ticket_id(user_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT ticket_id FROM tickets WHERE user_id = ? AND ticket_status = 'new'", (str(user_id),))
    ticket_id = cur.fetchone()

    cur.close()
    con.close()

    return ticket_id[0]


# получить все записи из таблицы "tickets", где ticket_status == new/at_work
# (т.е. получить всех пользователей, написавших в чат с админом)
async def new_tickets():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM tickets WHERE ticket_status IN ('new', 'at_work')")
    tickets = cur.fetchall()

    cur.close()
    con.close()

    return tickets


# получить все сообщения в тикете
async def select_messages_in_ticket(ticket_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM messages WHERE ticket_id = ?", (int(ticket_id),))
    info = cur.fetchall()

    cur.close()
    con.close()

    return info


# получить login по user_id
async def select_login(user_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT login FROM user WHERE user_id = ?", (str(user_id),))
    login = cur.fetchone()

    cur.close()
    con.close()

    return login[0]


# получить все ticket_id, где ticket_status == new/at_work
async def tickets_ids():
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT ticket_id FROM tickets WHERE ticket_status IN ('new', 'at_work')")
    ids = cur.fetchall()

    cur.close()
    con.close()

    return list(*zip(*ids))


# получить полную запись о пользователе по user_id
async def select_user_by_user_id(user_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT * FROM user WHERE user_id = ?", (str(user_id),))
    user = cur.fetchall()

    cur.close()
    con.close()

    return user[0]


# получить user_id по ticket_id
async def select_user_id_by_ticket_id(ticket_id: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT user_id FROM tickets WHERE ticket_id = ?", (int(ticket_id),))
    user_id = cur.fetchone()

    cur.close()
    con.close()

    return user_id[0]


# получить message_id по id (id - primary key)
async def select_message_id_by_id(id_primary_key: any):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("SELECT message_id FROM messages WHERE id = ?", (int(id_primary_key),))
    message_id = cur.fetchone()

    cur.close()
    con.close()

    return message_id[0]
