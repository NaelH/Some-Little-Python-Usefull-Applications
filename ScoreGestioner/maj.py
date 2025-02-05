import sqlite3
def maj():
    conn = sqlite3.connect("bdd.db")
    cur = conn.cursor()

    # Creation des tables
    cur.executescript("""
                DROP TABLE IF EXISTS score;
                CREATE TABLE score (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
                username VARCHAR(25) NOT NULL,
                score INTEGER NOT NULL)""")
    conn.commit()

    donnee = [
        ('935nlhu', '0'),
        ('964asrt', '100'),
        ("907arbe", '12')
    ]

    cur.executemany("INSERT INTO score(username, score) VALUES (?,?)", donnee)
    conn.commit()
    cur.close()
    conn.close()
