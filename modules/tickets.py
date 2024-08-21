import sqlite3
import discord

conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        user INTEGER,
        channel INTEGER
    )
''')
conn.commit()
conn.close()



def get_from_user(user:int) -> int:
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE user=?', (user,))
    data = c.fetchone()
    conn.close()
    return data


def add_user(user:int, channel:int) -> None:
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('INSERT INTO tickets VALUES (?, ?)', (user, channel))
    conn.commit()
    conn.close()


def remove_user(user:int) -> None:
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('DELETE FROM tickets WHERE user=?', (user,))
    conn.commit()
    conn.close()


def get_all() -> list:
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets')
    data = c.fetchall()
    conn.close()
    return data


def get_from_channel(channel:int) -> int:
    conn = sqlite3.connect('data/data.db')
    c = conn.cursor()
    c.execute('SELECT * FROM tickets WHERE channel=?', (channel,))
    data = c.fetchone()
    conn.close()
    return data