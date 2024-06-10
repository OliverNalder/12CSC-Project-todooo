import sqlite3
conn = sqlite3.connect('acc_info.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE acc_info (id INTEGER PRIMARY KEY, username char(100) NOT NULL, password char(100) NOT NULL)")
conn.execute("INSERT INTO acc_info (username,password) VALUES ('sigma','alpha')")
conn.commit()