# http://flask.pocoo.org/docs/1.0/quickstart/#routing

# Built in Python stuff
import datetime
import time

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
	ts= time.time()
	st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
	# print(st)
	todo_list=[
		['Item 1', 'Description 1', st, True],
		['Item 2', 'Description 2', st, False],
		['Item 3', 'Description 3', st, False],
	]
	@app.route('/', methods=['GET', 'POST'])
	def index():
		return render_template('index.html', len= len(todo_list), todos= todo_list, st= st)

	# End App
	return app
