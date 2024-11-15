import sqlite3

def init_db():
    conn = sqlite3.connect('criminal.db')
    cursor = conn.cursor()
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS known_faces (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        city TEXT NOT NULL
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS face_encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        person_id INTEGER NOT NULL,
        encoding BLOB NOT NULL,
        FOREIGN KEY (person_id) REFERENCES known_faces(id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS detection_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        criminal_name TEXT NOT NULL,
        last_location TEXT NOT NULL,
        time DATETIME DEFAULT (DATETIME('now', 'localtime')),
        detected_frame BLOB NOT NULL
    )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
