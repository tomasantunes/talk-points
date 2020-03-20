import sqlite3
from pprint import pprint 

def connect_db():
	return sqlite3.connect("talk-points.db")

db = connect_db()

def init():
	db = connect_db()
	c = db.cursor()

	sql_characters_table = """ CREATE TABLE IF NOT EXISTS characters (
							id integer PRIMARY KEY,
							name text,
							n_jokes integer,
							n_tickets integer,
							n_solutions integer
						); """

	c.execute(sql_characters_table)

def insertCharacter(name):
	db = connect_db()
	db.execute('INSERT INTO characters (name) VALUES (?)', [name])
	db.commit()

def menu():
	step1 = input("Press 1 to insert a character. \nPress 2 to choose an existing character. \nPress 3 to display scores. \nPress 4 to exit. \n")

	if (step1 == "1"):
		name = input("Choose a name: ")
		insertCharacter(name)
		menu()
	elif (step1 == "2"):
		name = input("Choose a name: ")
		n_jokes = input("Number of jokes: ")
		n_tickets = input("Number of tickets: ")
		n_solutions = input("Number of solutions: ")

		db = connect_db()
		query = db.execute('SELECT * FROM characters WHERE name = ?', [name])
		rows = query.fetchall()
		r = rows[0]
		c = {
			"name": r[1],
			"n_jokes": r[2] + int(n_jokes),
			"n_tickets": r[3] + int(n_tickets),
			"n_solutions": r[4] + int(n_solutions)
		}

		db = connect_db()
		db.execute('UPDATE characters SET n_jokes = ?, n_tickets = ?, n_solutions = ? WHERE name = ?;', (c["n_jokes"], c["n_tickets"], c["n_solutions"], c["name"]))
		db.commit()
		menu()
	elif (step1 == "3"):
		db = connect_db()
		query = db.execute('SELECT * FROM characters')
		rows = query.fetchall()
		characters = []

		for r in rows:
			characters.append({
				"name": r[1],
				"n_jokes": r[2],
				"n_tickets": r[3],
				"n_solutions": r[4]
			})

		for c in characters:
			print("\n-----------------------------------------------\n")
			print("Name: " + c["name"])
			print("No. of jokes: " + str(c["n_jokes"]))
			print("No. of tickets: " + str(c["n_tickets"]))
			print("No. of solutions: " + str(c["n_solutions"]))
			print("\n-----------------------------------------------\n")

		menu()
	elif (step1 == "4"):
		quit()

init()
menu()
