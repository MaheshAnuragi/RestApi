from flask import Flask, jsonify, request
import sqlite3
import requests
import json

app = Flask(__name__)
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                      (id INTEGER PRIMARY KEY AUTOINCREMENT,
                       first_name TEXT,
                       last_name TEXT,
                       age INTEGER,
                       gender TEXT,
                       email TEXT,
                       phone TEXT,
                       birth_date TEXT)''')
    conn.commit()
    conn.close()

def save_user(user):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO users
                      (id,first_name, last_name, age, gender, email, phone, birth_date)
                      VALUES (?,?, ?, ?, ?, ?, ?, ?)''',
                   (user['id'],user['firstName'], user['lastName'], user['age'],
                    user['gender'], user['email'], user['phone'], user['birthDate']))
    conn.commit()
    conn.close()

def fetch_users_by_first_name(first_name):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE first_name LIKE ?", (f"%{first_name}%",))
    rows = cursor.fetchall()
    conn.close()

    # Format the rows as dictionaries with desired key order
    users = []
    for row in rows:
        # Define the desired order of keys
        key_order = ["id", "first_name", "last_name", "age", "gender", "email", "phone", "birth_date"]
        
        # Create the user dictionary with sorted keys
        user = {key: row[index] for index, key in enumerate(key_order)}
        users.append(user)
    
    return users

def search_users_in_database(first_name):
    users = fetch_users_by_first_name(first_name)
    if users:
        # Manually serialize the data using json.dumps to preserve key order
        users_json = json.dumps(users, indent=2)  # You can adjust the indent value for formatting
        response = app.response_class(
            response=users_json,
            status=200,
            mimetype='application/json'
        )
        return response
    else:
        response = requests.get(f"https://dummyjson.com/users/search?q={first_name}")
        # response = response.json()
        if response.status_code == 200:
            data = response.json()
            fetched_users = data.get("users", [])
            if isinstance(fetched_users, list):
                for user in fetched_users:
                    save_user(user)
                return jsonify(fetched_users)
            else:
                return jsonify({'message': 'Invalid response from external API.'}), 500
        else:
            return jsonify({'message': 'Error occurred while fetching users from external API.'}), 500

@app.route('/api/users', methods=['GET', 'POST'])
def search_users():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        if first_name:
            return search_users_in_database(first_name)
        else:
            return jsonify({'message': 'Missing first_name parameter'}), 400
    else:
        return '''
        <div style="display: flex; justify-content: center; align-items: center; height: 100vh;">
            <form method="POST" action="/api/users">
                <input type="text" name="first_name" placeholder="Enter First Name" required>
                <input type="submit" value="Search">
            </form>
        </div>
        '''
    
@app.route('/')
def home():
    return """
    <a href="/api/users"> search User</a>
    
    """

if __name__ == '__main__':
    create_table()
    app.run(debug=True)