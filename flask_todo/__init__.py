# http://flask.pocoo.org/docs/1.0/quickstart/#routing

# Built in Python stuff
import datetime
import time
import random

# Imported packages
from flask import Flask, request, make_response, render_template

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

	# Let's make some lists.
	st = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
	# print(st)
	todo_list=[
		['Buy a 1969 Chevy Camaro', 'I want a cool car.', st, False],
		['Get Married', 'I want to elope.', st, False],
		['Go to Canada', 'Specifically to Vancouver.', st, False],
		['Eat breakfast', 'Eat food.', st, True],
	]
	@app.route('/', methods=['GET'])
	def index():
		return render_template('index.html', len= len(todo_list), todos= todo_list, st= st)

	cool_task_names =['Save Planet Mars', 'Buy that Sweet Dreamhouse', 'Take Over the World', 'Buy that final Ultravox album', 'Move to France', 'Move to England', 'Buy a Psychedelic Furs album', 'Go see The Good The Bad Queen', 'Defeat Ganon', 'Save Hyrule', 'Defeat Bowser', 'Save the Mushroom Kingdom', 'Wash my socks', 'Share a Friendship Bracelet with Damon Albarn', 'Achieve World Peace', 'Get a gold tooth', 'Crowd surf at the concert', 'Find The One 💙']
	@app.route('/create', methods=['GET', 'POST'])
	def create_task():
		# Was this a POST request or a GET one?
		if request.method== "GET":
			# Just render the template.
			return render_template('create.html', len= len(todo_list), todos= todo_list, st= st, task_names= cool_task_names, random= random)
		else:
			new_task=[]
			x= request.form['name']
			y= request.form['description']
			new_task.append(x)
			new_task.append(y)
			right_now = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			new_task.append(right_now)
			new_task.append(False)
			print(x,y)
			todo_list.append(new_task)
		return render_template('create.html', len= len(todo_list), todos= todo_list, st= st, task_names= cool_task_names, random= random)

	# End App
	return app
