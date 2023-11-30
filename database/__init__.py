import aiosqlite
from datetime import datetime, timedelta

async def initialize():
    async with aiosqlite.connect('database/database.db') as db:
        cursor = await db.cursor()
        await cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bans (
            user_id INTEGER PRIMARY KEY,
            user_first_name TEXT,
            chat_id INTEGER,
            until_date TEXT
            );
            """
        )
        await cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS mutes (
            user_id INTEGER PRIMARY KEY,
            user_first_name TEXT,
            chat_id INTEGER,
            until_date TEXT
            );
            """
        )
        await db.commit()


async def request(str: str, command=False, *args):
    async with aiosqlite.connect('database/database.db') as db:
        cursor = await db.cursor()
        await cursor.execute(str, (args))
        if command:
            await db.commit()
        else:
            data = await cursor.fetchall()
            await db.commit()
            return data


async def update_bans():
    async with aiosqlite.connect('database/database.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM bans")
        data = await cursor.fetchall()
        for element in data:
            date = datetime.strptime(element[3], '%Y-%m-%d %H:%M:%S.%f')
            if (date - datetime.now())<timedelta(seconds=0):
                await request(f"DELETE FROM bans WHERE user_id = ?", False, element[0])


async def update_mutes():
    async with aiosqlite.connect('database/database.db') as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM mutes")
        data = await cursor.fetchall()
        for element in data:
            date = datetime.strptime(element[3], '%Y-%m-%d %H:%M:%S.%f')
            if (date - datetime.now())<timedelta(seconds=0):
                await request(f"DELETE FROM mutes WHERE user_id = ?", False, element[0])
