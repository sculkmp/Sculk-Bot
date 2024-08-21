import sqlite3

conn = sqlite3.connect('data/giveaways.db')
c = conn.cursor()

c.execute(f'''CREATE TABLE IF NOT EXISTS AllTable (
    channel INTEGER,
    message INTEGER,
    prize TEXT,
    participants INTEGER,
    timestamp INTEGER,
    winners INTEGER
)''')

### Create table named by id of message for giveaway command
def create_table(id:str):
    c.execute(f'''CREATE TABLE IF NOT EXISTS T{id} (
        user_id INTEGER
    )''')
    conn.commit()
    
### Add user to table
def add_user(id, user_id):
    c.execute(f'INSERT INTO T{id} (user_id) VALUES ({user_id})')
    conn.commit()

### Remove user from table
def remove_user(id, user_id):
    c.execute(f'DELETE FROM T{id} WHERE user_id = {user_id}')
    conn.commit()

### Get all users from table
def get_users(id):
    c.execute(f'SELECT * FROM T{id}')
    return c.fetchall()

### Get user from table
def get_user(id, user_id):
    c.execute(f'SELECT * FROM T{id} WHERE user_id = {user_id}')
    return c.fetchone()

### Get count of users from table
def count_users(id):
    c.execute(f'SELECT COUNT(*) FROM T{id}')
    return c.fetchone()[0]

### Drop table
def drop_table(id):
    c.execute(f'DROP TABLE T{id}')
    conn.commit()
    
### Drop all tables
def drop_all_tables():
    c.execute('SELECT name FROM sqlite_master WHERE type="table"')
    tables = c.fetchall()
    for table in tables:
        c.execute(f'DROP TABLE {table[0]}')
    conn.commit()
    

class manage:
    def create(channel, id, prize, participants, timestamp, winners):
        c.execute(f'''INSERT INTO AllTable (channel, message, prize, participants, timestamp, winners) 
                      VALUES (?, ?, ?, ?, ?, ?)''', (channel, id, prize, participants, timestamp, winners))
        conn.commit()
    
    def get(id):
        c.execute(f'SELECT * FROM AllTable WHERE message = {id}')
        return c.fetchone()
    
    def remove(id):
        c.execute(f'DELETE FROM AllTable WHERE message = {id}')
        conn.commit()
        
    def get_all():
        c.execute('SELECT * FROM AllTable')
        return c.fetchall()

    def update(id, participants):
        c.execute(f'UPDATE AllTable SET participants = {participants} WHERE message = {id}')
        conn.commit()