import sqlite3

# Initialize database
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    # Create a table to store user messages
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL
    )
    """)
    
    conn.commit()
    conn.close()

# Save message to database
def save_message(user_id, role, content):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    INSERT INTO conversations (user_id, role, content)
    VALUES (?, ?, ?)
    """, (user_id, role, content))
    
    conn.commit()
    conn.close()

# Retrieve conversation history
def get_history(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT role, content FROM conversations WHERE user_id = ?
    """, (user_id,))
    
    history = [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    return history

# Clear conversation history
def clear_history(user_id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    
    cursor.execute("""
    DELETE FROM conversations WHERE user_id = ?
    """, (user_id,))
    
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()
