import sqlite3 as sq

# Добавление информации в базу данных
async def db_start():
    global db, cur

    db = sq.connect('servey.db')  # Создание соединения с базой данных
    cur = db.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profile (
            user_id TEXT PRIMARY KEY, 
            name TEXT, 
            age INTEGER, 
            description TEXT, 
            photo TEXT
        )
    """)
    db.commit()

async def create_profile(user_id):
    user = cur.execute('SELECT 1 FROM profile WHERE user_id = ?', (user_id,)).fetchone()

    if not user:
        cur.execute('INSERT INTO profile (user_id, name, age, description, photo) VALUES (?, NULL, NULL, NULL, NULL)', (user_id,))
        db.commit()

async def edit_profile(state, user_id):
    async with state.proxy() as data:
        name = data.get('name', '')
        age = data.get('age', '')
        description = data.get('description', '')
        photo = data.get('photo', '')

        cur.execute(
            'UPDATE profile SET name = ?, age = ?, description = ?, photo = ? WHERE user_id = ?',
            (name, age, description, photo, user_id))
        db.commit()

async def db_close():
    db.close()
