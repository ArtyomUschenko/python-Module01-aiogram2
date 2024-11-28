import sqlite3 as sq


# Добавления информации в базу данны

async def db_start():
    global db, cur

    db = sq.connect('servey.db') #create a database connection
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS profile (user_id TEXT PRIMARY KEY, name TEXT, age INTEGER, description TEXT, photo TEXT)")
    db.commit()


async def create_profile(user_id):
    user = cur.execute('SELECT 1 FROM profile WHERE user_id == "{key}"'.format(key=user_id)).fetchone()

    if not user:
        cur. execute('INSERT INTO profile VALUES (?, ?, ?, ?, ?)', (user_id, '', '', '',''))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        cur.execute(
            'UPDATE profile SET name = "{}", age = "{}", description = "{}", photo = "{}" WHERE user_id == "{}"'.format(
                data['name'], data['age'], data['description'], data['photo'], user_id))
        db.commit()