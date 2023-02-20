import sys
import os.path
sys.path.append(os.path.dirname(sys.path[0]))

import sqlite3
import json

# Initializing paths to the database and json files
path_to_db = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, os.pardir, 'db/db.sqlite3'))
path_to_json = os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir, 'HTN_2023_BE_Challenge_Data.json'))

# Connect to SQLite3 DB
conn = sqlite3.connect(path_to_db)
cur = conn.cursor()

# Create schema for database tables

sql_create_hackers_table = \
""" 
CREATE TABLE IF NOT EXISTS hackers (
    hacker_id INTEGER,
    name TEXT NOT NULL,
    company TEXT NOT NULL,
    email TEXT NOT NULL,
    phone TEXT NOT NULL,
    PRIMARY KEY (hacker_id AUTOINCREMENT)
);
"""

sql_create_skills_table = \
""" 
CREATE TABLE IF NOT EXISTS skills (
    skill_id INTEGER,
    name TEXT NOT NULL,
    rating TEXT NOT NULL,
    hacker_id INTEGER,
    PRIMARY KEY (skill_id AUTOINCREMENT),
    FOREIGN KEY (hacker_id) REFERENCES hackers(hacker_id)
);
"""

cur.execute(sql_create_hackers_table)
cur.execute(sql_create_skills_table)

# Load JSON into a dictionary and extract the information into the SQLite tables
with open(path_to_json, 'r') as json_file:
    data = json.load(json_file)

    # Verifies that data is not already stored within the hacker and skills table in the db
    cur.execute('SELECT EXISTS (SELECT 1 FROM hackers)')
    hacker_count = cur.fetchone()[0]

    cur.execute('SELECT EXISTS (SELECT 1 FROM skills)')
    skill_count = cur.fetchone()[0]

    # Resets the tables if there is already data stored
    if hacker_count > 0 and skill_count > 0:
        cur.execute('DELETE FROM hackers')
        cur.execute('DELETE FROM SQLITE_SEQUENCE WHERE name=hackers;')

        cur.execute('DELETE FROM skills')
        cur.execute('DELETE FROM SQLITE_SEQUENCE WHERE name=skills;')

        print(f"The values inside the hackers and skills tables were reset with the JSON file at {}.", path_to_json) 


    idh = 1
    ids = 1
    for idx, hacker in enumerate(data):
        hacker_data = (idh, hacker['name'], hacker['company'], hacker['email'], hacker['phone'])
        cur.execute('INSERT INTO hackers VALUES (?, ?, ?, ?, ?)', hacker_data)

        for entry in hacker['skills']:
            skill_data = (ids, entry['skill'], entry['rating'], idx+1)
            cur.execute('INSERT INTO skills VALUES (?, ?, ?, ?)', skill_data)

            ids += 1
        idh += 1

conn.commit()
conn.close()