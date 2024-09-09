import json
import os
import mysql.connector
from mysql.connector import Error
from getpass import getpass

# Database connection
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='sss_assignment_sep24',
        password='doitnow',
        database='weather_db'
    )

# Add user to database
def add_user(username, password_hash):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)", (username, password_hash))
    connection.commit()
    cursor.close()
    connection.close()

# Fetch user ID by username
def get_user_id(username):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id , password_hash FROM users WHERE username = %s", (username,))
    result = cursor.fetchone()
    cursor.close()
    connection.close()
    return result if result else None

# Add search history to database
def add_search_history(user_id, location, weather_data):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO search_history (user_id, location, weather_data) VALUES (%s, %s, %s)",
                   (user_id, location, weather_data))
    connection.commit()
    cursor.close()
    connection.close()

# Get user search history
def get_user_history(user_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT search_time, location, weather_data FROM search_history WHERE user_id = %s ORDER BY search_time DESC", (user_id,))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return result


def save_session(user_id):
    with open('session.json', 'w') as f:
        json.dump({'user_id': user_id}, f)

def load_session():
    if os.path.exists('session.json'):
        with open('session.json', 'r') as f:
            return json.load(f).get('user_id')
    return None

def clear_session():
    if os.path.exists('session.json'):
        os.remove('session.json')