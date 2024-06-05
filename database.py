import sqlite3
conn = sqlite3.connect('todo.db') # Warning: This file is created in the current directory
conn.execute("CREATE TABLE todo (id INTEGER PRIMARY KEY, task char(100) NOT NULL, status bool NOT NULL, progress INTEGER NOT NULL)")
conn.execute("INSERT INTO todo (task,status,progress) VALUES ('Read A-byte-of-python to get a good introduction into Python',1,0)")
conn.execute("INSERT INTO todo (task,status,progress) VALUES ('Visit the Python website',1,0)")
conn.execute("INSERT INTO todo (task,status,progress) VALUES ('Test various editors for and check the syntax highlighting',1,0)")
conn.execute("INSERT INTO todo (task,status,progress) VALUES ('Choose your favorite WSGI-Framework',1,0)")
conn.commit()