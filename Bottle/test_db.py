#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

import sqlite3

db = sqlite3.connect('test.db')
db.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY, item CHAR(100) NOT NULL)")
db.execute("INSERT INTO test(item) VALUES ('testtest')")
db.commit()
db.close()

## OK
