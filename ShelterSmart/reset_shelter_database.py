import sqlite3

connection = sqlite3.connect("shelter.db")

connection.execute("""
    CREATE TABLE animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    species TEXT,
    breed TEXT,
    sex TEXT,
    age INTEGER,
    status TEXT,
    spay_neuter TEXT,
    date_arrived DATE,
    how_acquired TEXT,
    vaccines_needed TEXT,
    medical_conditions TEXT,
    location TEXT,
    sponsored TEXT,
    notes TEXT
    )""")
connection.execute("""    CREATE TABLE deleted_animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    species TEXT,
    breed TEXT,
    sex TEXT,
    age INTEGER,
    status TEXT,
    spay_neuter TEXT,
    date_arrived DATE,
    how_acquired TEXT,
    vaccines_needed TEXT,
    medical_conditions TEXT,
    location TEXT,
    sponsored TEXT,
    notes TEXT
    )""")
connection.execute("""
    CREATE TABLE adopted_animals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    species TEXT,
    breed TEXT,
    sex TEXT,
    age INTEGER,
    status TEXT,
    spay_neuter TEXT,
    date_arrived DATE,
    how_acquired TEXT,
    vaccines_needed TEXT,
    medical_conditions TEXT,
    location TEXT,
    sponsored TEXT,
    notes TEXT,
    adoption_date DATE,
    adopter_first_name TEXT,
    adopter_last_name TEXT,
    adopter_address TEXT,
    adopter_phone TEXT
    );
""")

connection.commit()
connection.close()