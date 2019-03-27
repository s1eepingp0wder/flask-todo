# http://flask.pocoo.org/docs/1.0/quickstart/#routing

# Built in Python stuff
import datetime
import time
import random
import psycopg2

# Imported packages
from flask import Flask, request, make_response, render_template, flash, redirect, url_for

def page_not_found(e):
	return render_template('404.html')

def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.register_error_handler(404, page_not_found)

	app.config.from_mapping(
		SECRET_KEY='dev',
		)

	if test_config is None:
		app.config.from_pyfile('config.py', silent=True)
	else:
		app.config.from_mapping(test_config)

	# Database Stuff.

	conn = psycopg2.connect("dbname=todo-app user=csetuser")
	cur= conn.cursor()

	# Real quick... What's the time?
	st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	# Thanks, mate!

	# Let's do some trickery: Look for this table! If you can't find it, make it.
	try:
		# Can we get in?
		cur.execute("SELECT * FROM tasks;")
	except:
		# No. It doesn't exist. Let's make it.
		cur.execute("CREATE TABLE tasks(name TEXT, description TEXT, time TIMESTAMP, completed BOOLEAN DEFAULT false, task_id SERIAL PRIMARY KEY)")
		cur.execute("INSERT INTO tasks (name, description, time, completed) VALUES (%s, %s, %s, %s)", ("Hello, World!", "Your first task is to read this task!", st, False))
		print("Created table \"tasks\".")


	sql_query = 'SELECT name, description, time, completed, task_id FROM tasks ORDER BY time DESC'
	cur.execute(sql_query)
	todo_list = cur.fetchall()
	# print(todo_list)

	@app.route('/', methods=['GET'])
	def index():
		cur.execute(sql_query)
		todo_list = cur.fetchall()
		print(todo_list)
		return render_template('index.html', todos= todo_list, st= st)

	cool_task_names =['Save Planet Mars', 'Buy that Sweet Dreamhouse', 'Take Over the World', 'Buy that final Ultravox album', 'Move to France', 'Move to England', 'Buy a Psychedelic Furs album', 'Go see The Good The Bad Queen', 'Defeat Ganon', 'Save Hyrule', 'Defeat Bowser', 'Save the Mushroom Kingdom', 'Wash my socks', 'Share a Friendship Bracelet with Damon Albarn', 'Achieve World Peace', 'Get a gold tooth', 'Crowd surf at the concert', 'Find The One 💙']
	@app.route('/create', methods=['GET', 'POST'])
	def create_task():
		# Was this a POST request or a GET one?
		if request.method== "GET":
			# Just render the template.
			return render_template('create.html', todos= todo_list, st= st, task_names= cool_task_names, random= random)
		else:
			task_name= request.form['name']
			task_desc= request.form['description']
			cur.execute("INSERT INTO tasks (name, description, time, completed) VALUES (%s, %s, %s, %s)", (task_name, task_desc, st, False))
			conn.commit()
			flash(f"Your task \"{task_name}\" was added!")
		return render_template('create.html', todos= todo_list, st= st, task_names= cool_task_names, random= random)

	def get_task(id):
		cur.execute('SELECT task_id FROM tasks WHERE task_id= %s', [id])
		task = cur.fetchone()
		return task

	@app.route('/<int:id>/update', methods=['GET', 'POST'])
	def update(id):
		print(f"Updating Task ID {id}")
		get_task(id)
		cur.execute('UPDATE tasks SET completed = %s WHERE task_id= %s',[True, id])
		conn.commit()
		return redirect(url_for('index'))

	# def update_task(id):
	# 	task = get_task(id)
	# 	if request.method == 'POST':
	# 		task_action = request.form['action']
	# 		db = cur.execute('UPDATE tasks SET completed = true WHERE task_id= %s',[id])
	# 		conn.commit()
	# 		return redirect(url_for('/'))

	# End App
	return app
