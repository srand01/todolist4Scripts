from flask import Flask, request, jsonify, g, session
import sqlite3
import bcrypt

DATABASE = 'todolist.db'
app = Flask(__name__)
app.config.from_object(__name__)

def create_table():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        #users table
        cursor.execute('''CREATE TABLE IF NOT EXISTS "users"
                        (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `username` TEXT NOT NULL UNIQUE,
                        `password` TEXT NOT NULL)''')
        #entries table
        cursor.execute('''CREATE TABLE IF NOT EXISTS "entries"
                        (`id` INTEGER PRIMARY KEY AUTOINCREMENT,
                        `what_to_do` TEXT,
                        `due_date` TEXT,
                        `status` TEXT,
                        `username` TEXT)''')
        db.commit()
        db.close()
        
# Function to stablish database connection
def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = sqlite3.connect(app.config['DATABASE'])
    return g.sqlite_db

# Middleware function to extract username from the session
@app.before_request
def process_request():
    username = request.cookies.get('username')
    request.username = username

@app.route("/api/items", methods=['GET'])
def get_items():
    db = get_db()
    username = request.username
    cur = db.execute('SELECT what_to_do, due_date, status, username FROM entries WHERE username=?', (username,))
    entries = cur.fetchall()
    tdlist = [dict(what_to_do=row[0], due_date=row[1], status=row[2], username=row[3]) for row in entries]
    return jsonify(tdlist)

@app.route("/api/items", methods=['POST'])
def add_item():
    db = get_db()
    username = request.username
    print('username POST')
    print(username)
    db.execute('INSERT INTO entries (what_to_do, due_date, username) VALUES (?, ?, ?)',
           [request.json['what_to_do'], request.json['due_date'], username])
    db.commit()
    return jsonify({'status': 'success'})

@app.route("/api/items/<item>", methods=['DELETE'])
def delete_item(item):
    db = get_db()
    db.execute("DELETE FROM entries WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({'status': 'success'})

@app.route("/api/items/<item>", methods=['PUT'])
def mark_item(item):
    db = get_db()
    db.execute("UPDATE entries SET status='done' WHERE what_to_do='"+item+"'")
    db.commit()
    return jsonify({'status': 'success'})

# Function to register a new user
def register_user(username, password):
    db = get_db()
    # Hashing the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    cursor = db.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    db.commit()
    db.close()
    
@app.route("/api/register", methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']
    register_user(username, password)
    return jsonify({'message': 'User registered successfully'})

#start of login section
@app.route("/api/login", methods=['POST'])
def login():
    data = request.json
    if 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Both username and password are required'}), 400

    username = data['username']
    password = data['password']
    user = authenticate_user(username, password)
    if user:
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'error': 'Invalid username or password'}), 401

# Function to authenticate user login
def authenticate_user(username, password):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    user = cursor.fetchone()
    db.close()
    if user:
        # Verifying the hashed password using bcrypt
        if bcrypt.checkpw(password.encode('utf-8'), user[2]):
            return user
    return None
#end of login section

#close db
@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

if __name__ == '__main__':
    create_table()
    app.run(port=5001)
