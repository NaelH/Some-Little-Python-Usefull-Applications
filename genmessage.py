import connector

cursor = connector.conn.cursor()
cursor.execute("INSERT INTO messages(username_exp, username_dest, message, lu) VALUES(?,?,?,?)", ("test", "admin", "Coucou", 0))
connector.conn.commit()