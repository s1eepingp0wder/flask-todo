from flask_boilerplate import create_app

def test_config():
    assert not create_app().testing
    assert create_app({'TESTING': True}).testing

def test_index(client):
    response = client.get('/')
    assert response.data == b'This is a boilerplate.'

def test_hello(client):
    response = client.get('/hello')
    assert response.data == b'Hello World!'

    response = client.get('/hello?name=Dentz')
    assert response.data == b'Hello Dentz!'

def test_number(client):
    response= client.get('/number/1')
    assert response.data == b'Number: 1'

    response = client.get('/number/2')
    assert response.data== b'Number: 2'

    response = client.get('/number/apple')
    assert response.status_code== 404

def test_method_route(client):
    response= client.get('/method')
    assert response.data== b'HTTP Method: GET'

    response= client.post('/method')
    assert response.data== b'HTTP Method: POST'

    response= client.patch('/method')
    assert response.data== b'HTTP Method: PATCH'

    response= client.put('/method')
    assert response.data== b'HTTP Method: PUT'

    response= client.delete('/method')
    assert response.data== b'HTTP Method: DELETE'

def test_status_route(client):
    response = client.get('/status?c=400')
    assert response.status_code == 400

    response= client.get('/status?c=500')
    assert response.status_code == 500

    response = client.get('/status?c=200')
    assert response.status_code== 200
