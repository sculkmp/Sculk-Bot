import sqlite3
import math
import discord
from DiscordLevelingCard import RankCard, Settings


conn = sqlite3.connect('data/data.db')
c = conn.cursor()
c.execute(f'''CREATE TABLE IF NOT EXISTS Levels (
    user INTEGER,
    experience INTEGER
)''')


def add_user(user_id:int, experience:int):
    c.execute(f'INSERT INTO Levels (user, experience) VALUES ({user_id}, {experience})')
    conn.commit()

def remove_user(user_id:int):
    c.execute(f'DELETE FROM Levels WHERE user = {user_id}')
    conn.commit()

def get_user(user_id:int):
    c.execute(f'SELECT * FROM Levels WHERE user = {user_id}')
    value = c.fetchone()
    return value[1] if value else None

def update(user_id:int, experience:int):
    c.execute(f'UPDATE Levels SET experience = {experience} WHERE user = {user_id}')
    conn.commit()

def close():
    conn.close()


def level_to_exp(level:int, base:int=25, exponent:float=0.75):
    return math.floor(base * (level ** (1/exponent)))

def exp_to_level(experience:int, base:int=25, exponent:float=0.75):
    return math.floor((experience / base) ** exponent)


async def generate_card(user:discord.User):
    experience = get_user(user.id)
    experience = 0 if not experience else experience
    level = exp_to_level(experience)
    
    card_settings = Settings(
        background="https://images.pexels.com/photos/573130/pexels-photo-573130.jpeg",
        text_color="white",
        bar_color="#ffffff"
    )
    
    card = await RankCard(
        settings=card_settings,
        avatar=user.avatar.url if user.avatar else "https://cdn.discordapp.com/embed/avatars/0.png",
        level=level,
        current_exp=experience,
        max_exp=level_to_exp(level+1),
        username=user.name,
    ).card1(resize = 100)
    
    return card