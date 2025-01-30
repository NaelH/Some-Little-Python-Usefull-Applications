import sqlite3
def maj():
    conn = sqlite3.connect("bdd.db")
    cur = conn.cursor()

    # Creation des tables
    cur.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username VARCHAR(25) NOT NULL,
                password TEXT NOT NULL,
                rank TEXT DEFAULT 'usr',
                disabled INTEGER DEFAULT 0)""")
    conn.commit()

    cur.execute("INSERT INTO users(username,password,rank,disabled) VALUES(?,?,?,?)", ("admin","admin","adm",0))
    conn.commit()
    cur.executescript("""
                    CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                    username_exp VARCHAR(25) NOT NULL,
                    username_dest TEXT NOT NULL,
                    message TEXT NOT NULL,
                    lu INTEGER DEFAULT 0)""")
    conn.commit()
    cur.close()
    conn.close()
