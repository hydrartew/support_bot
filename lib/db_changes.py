import datetime
import sqlite3 as sq


# создание нового пользователя
async def new_registration(data: tuple):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute('INSERT INTO user VALUES (NULL, ?, ?, ?, ?, ?)', data)

    con.commit()
    cur.close()
    con.close()


# подтверждение регистрации
async def accept_registration(user_id: int):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("UPDATE user SET user_status = 'accepted' WHERE user_id = ?", (str(user_id),))

    con.commit()
    cur.close()
    con.close()


# статус регистрации: отклонён
async def cancelled_registration(user_id: int):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("UPDATE user SET user_status = 'cancelled' WHERE user_id = ?", (str(user_id),))

    con.commit()
    cur.close()
    con.close()


# добавить сообщение в чат с админом (поддержкой)
async def support_messages(ticket_id: int, user_id: str, message_id: int, message: str):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    # Добавить сообщение для запроса
    cur.execute('INSERT INTO messages VALUES(NULL, ?, ?, ?, ?, ?)',
                (ticket_id, str(user_id), message_id, message, date_now))

    con.commit()
    cur.close()
    con.close()


# создание тикета
async def create_ticket(user_id: str):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    dt = datetime.datetime.now()
    date_now = dt.strftime('%d.%m.%Y %H:%M:%S')

    # проверить, есть ли тикет с таким user_id, если нет - None, если есть - pass
    cur.execute("SELECT ticket_id FROM tickets WHERE user_id = ? AND ticket_status = 'new'", (str(user_id),))
    ticket_id = cur.fetchone()

    if ticket_id is None:  # если тикета нет в БД
        cur.execute('INSERT INTO tickets VALUES(NULL, ?, ?, ?)', (str(user_id), 'new', date_now))
        con.commit()

    cur.close()
    con.close()


# изменить статус тикета (at_work / closed)
async def change_ticket_status(ticket_id: any, ticket_status: str):
    con = sq.connect('user_info.db')
    cur = con.cursor()

    cur.execute("UPDATE tickets SET ticket_status = ? WHERE ticket_id = ?", (ticket_status, int(ticket_id)))

    con.commit()
    cur.close()
    con.close()
