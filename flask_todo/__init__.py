# http://flask.pocoo.org/docs/1.0/quickstart/#routing
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

	request_methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE']
	@app.route('/', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
	def index():
		# return 'This is a boilerplate.'
		return render_template('index.html', len= len(request_methods), request_methods= request_methods, method= request.method)

	@app.route('/hello')
	def hello():
		for key, value in request.args.items():
			print(f"{key}: {value}")
		name = request.args.get('name', 'World')
		# return f"Hello {name}!"
		return render_template('hello.html', name=name)

	@app.route('/number/<int:n>')
	def number_route(n):
		return f"Number: {n}"

	@app.route('/method', methods=['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
	def method_route():
		return f"HTTP Method: {request.method}"

	@app.route('/status')
	def status_route():
		code = request.args.get('c', 200)
		response = make_response('', code)

	@app.route('/calculate', methods=['GET', 'POST'])
	def calculate_page():
		result= None
		if request.method=="GET":
			return render_template('calculate.html', result= result)
		elif request.method=="POST":
			x= float(request.form['x'])
			y= float(request.form['y'])
			action= request.form['action']
			if action=="Add":
				result= x + y
			elif action=="Subtract":
				result= x-y
			elif action=="Multiply":
				result = x * y
			elif action=="Divide":
				result = x/y
			return render_template('calculate.html', result= result, x=x, y=y)

		return response
	# End App
	return app
