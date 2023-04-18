__doc__ = "Manage user.db"

import sqlite3
import random
import string
from cryptography.fernet import Fernet
from passlib.context import CryptContext
import smtp

user_db = sqlite3.connect('./static/db/users.db')
hash_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

USER_TABLE = 'users'
ADMIN_TABLE = 'admin'

def create_user_table() -> dict:
    """ create user table"""
    if not is_table_exists(USER_TABLE):
        cursor = user_db.cursor()
        cursor.execute(f"""CREATE TABLE {USER_TABLE} 
        (email TEXT PRIMARY KEY,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT)
        """)
        user_db.commit()
        return {'message': f'add table: {USER_TABLE}'}
    return {'message': f'{USER_TABLE} already exists'}

def create_admin_table() -> dict:
    """create admin table"""
    if not is_table_exists(ADMIN_TABLE):
        cursor = user_db.cursor()
        cursor.execute(f"""CREATE TABLE {ADMIN_TABLE} 
        (id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        key TEXT NOT NULL)
        """)
        user_db.commit()
        return {'message': f'add table: {ADMIN_TABLE}'}
    return {'message': f'{ADMIN_TABLE} already exists'}


def add_admin(email: str, username: str, password: str):
    admin = get_admin()
    if admin:
        return {'message': 'amdin account exists'}
    key = Fernet.generate_key().decode()
    encrypt_password = Fernet(key.encode()).encrypt(password.encode())
    cursor = user_db.cursor()
    cursor.execute(f"INSERT INTO {ADMIN_TABLE} (email, username, password, key) VALUES (?, ?, ?, ?)", (email, username, encrypt_password, key))
    user_db.commit()
    return {'message': 'successfuly add admin account'}


def get_admin() -> dict:
    """get admin account"""
    cursor = user_db.cursor()
    cursor.execute(f"SELECT * FROM {ADMIN_TABLE}")
    result = cursor.fetchone()
    if result:
        return {'email': result[1], 'username': result[2], 'password': result[3], 'key':result[4]}
    return None

def add_user(email: str, username: str, password: str, role: str='user') -> dict:
    """add user data to users table"""
    if get_user_by_email(email):
        return {'message': "Email already exists"}
    hashed_password = hash_password(password)
    cursor = user_db.cursor()
    cursor.execute(f"INSERT INTO {USER_TABLE} VALUES (?, ?, ?, ?)", \
                     (email, username, hashed_password, role))
    user_db.commit()
    if role == 'admin':
        add_admin(email, username, password)
    return {'massage': f'add {email} accounts'}

def update_user(email, username, password, role='user'):
    """update user data to users table"""
    hashed_password = hash_password(password)
    cursor = user_db.cursor()
    cursor.execute(f"UPDATE {USER_TABLE} SET username = ?, password = ?, role = ? \
                     WHERE email = ?", (username, hashed_password, role, email))
    user_db.commit()
    return {'message': f'update {email} accounts'}

def delete_user(email):
    """delete user data from users table"""
    cursor = user_db.cursor()
    cursor.execute(f'DELETE FROM {USER_TABLE} WHERE email = ?', (email,))
    user_db.commit()
    return {'message': f'delete {email} accounts'}

def get_user_by_email(email: str):
    """fetch user data from users table"""
    cursor = user_db.cursor()
    cursor.execute(f"SELECT * FROM {USER_TABLE} WHERE email = ?", (email, ))
    user = cursor.fetchone()
    if user:
        return {'email': user[0], 'username': user[1], 'password': user[2], 'role': user[3]}
    return None

def hash_password(password):
    """hash password"""
    return hash_context.hash(password)

def verify_password(password, hashed_password):
    """verify password"""
    return hash_context.verify(password, hashed_password)

def generate_tmp_password():
    """generate temporaty password"""
    letters = string.ascii_letters + string.digits
    temp_password = ''.join(random.choice(letters) for i in range(8))
    return temp_password

def reset_password(email):
    """reset new password"""
    user = get_user_by_email(email)
    if user:
        temp_password = generate_tmp_password()
        hashed_temp_password = hash_password(temp_password)

        cursor = user_db.cursor()
        cursor.execute(f"UPDATE {USER_TABLE} SET password = ? WHERE email = ?", \
                       (hashed_temp_password, email))
        user_db.commit()
        smtp.send_email(email, f"Subject:Password change\n\nYour password is set to {temp_password}")
        return {'message': f'reset {email} accounts password randomly'}
    return {'message': f'{email} accounts not found'}

def is_table_exists(tablename):
    """check table exists"""
    cursor = user_db.cursor()
    cursor.execute(f"SELECT name FROM sqlite_master WHERE type = 'table' AND name = '{tablename}'")
    result = cursor.fetchone()
    if result:
        return True
    return False
