import sqlite3
from passlib.context import CryptContext

user_db = sqlite3.connect('./static/db/users.db')
hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
user_table = 'users'
admin_table = 'admin'

def create_user_table():
    if not is_table_exists(user_table):
        cursor = user_db.cursor()
        cursor.execute(f"""CREATE TABLE {user_table} 
        (email TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT)
        """)
        user_db.commit()
        return {'message': f'add table: {user_table}'}
    return {'message': f'{user_table} already exists'}

def create_admin_table():
    if not is_table_exists(admin_table):
        cursor = user_db.cursor()
        cursor.execute(f"""CREATE TABLE {admin_table} 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        username TEXT NOT NULL,
        password TEXT NOT NULL)
        """)
        user_db.commit()
        return {'message': f'add table: {admin_table}'}
    return {'message': f'{admin_table} already exists'}

def add_user(email, username, password, role='user'):
    if get_user_by_email(email):
        return {'message': "Email already exists"}
    hashed_password = hash_password(password)
    cursor = user_db.cursor()
    cursor.execute(f"INSERT INTO {user_table} VALUES (?, ?, ?, ?)", (email, username, hashed_password, role))
    user_db.commit()
    return {'massage': f'add {email} accounts'}

def update_user(email, username, password, role='user'):
    hashed_password = hash_password(password)
    cursor = user_db.cursor()
    cursor.execute(f"UPDATE {user_table} SET username = ?, password = ?, role = ? WHERE email = ?", (username, hashed_password, role, email))
    user_db.commit()
    return {'message': f'update {email} accounts'}

def delete_user(email):
    cursor = user_db.cursor()
    cursor.execute(f'DELETE FROM {user_table} WHERE email = ?', (email,))
    user_db.commit()
    return {'message': f'delete {email} accounts'}

def get_user_by_email(email):
    cursor = user_db.cursor()
    cursor.execute(f"SELECT * FROM {user_table} WHERE email = ?", (email, ))
    user = cursor.fetchone()
    if user:
        return {'email': user[0], 'username': user[1], 'password': user[2], 'role': user[3]}
    return None

def hash_password(password):
    return hash_context.hash(password)

def verify_password(password, hashed_password):
    return hash_context.verify(password, hashed_password)

def generate_tmp_password():
    import random
    import string

    letters = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(letters) for i in range(8))
    return temp_password

def reset_password(email):
    user = get_user_by_email(email)
    if user:
        temp_password = generate_tmp_password()
        hashed_temp_password = hash_password(temp_password)
        cursor = user_db.cursor()
        cursor.execute(f"UPDATE {user_table} SET password = ? WHERE email = ?", (hashed_temp_password, email))
        user_db.commit()
        return {'message': f'reset {email} accounts password randomly'}
    return {'message': f'{email} accounts not found'}

def is_table_exists(tablename):
    cursor = user_db.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{tablename}'")
    result = cursor.fetchone()
    if result:
        return True
    return False