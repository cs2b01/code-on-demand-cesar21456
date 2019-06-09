from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import json
import time
db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


@app.route('/users', methods = ['GET'])
def get_users():
    session = db.getSession(engine)
    dbResponse = session.query(entities.User)
    data = []
    for user in dbResponse:
        data.append(user)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


##asdfgdsadfdgd
@app.route('/users', methods = ['POST'])
def create_user():
    c =  json.loads(request.form['values'])
    user = entities.User(
        username=c['username'],
        name=c['name'],
        fullname=c['fullname'],
        password=c['password']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/users', methods = ['PUT'])
def update_user():
    session = db.getSession(engine)
    id = request.form['key']
    user = session.query(entities.User).filter(entities.User.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(user, key, c[key])
    session.add(user)
    session.commit()
    return 'Updated User'

@app.route('/users', methods = ['DELETE'])
def delete_user():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.User).filter(entities.User.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/users/<id>', methods = ['GET'])
def get_user(id):
    db_session = db.getSession(engine)
    users = db_session.query(entities.User).filter(entities.User.id == id)
    for user in users:
        js = json.dumps(user, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')

##asdsaadsdsa

@app.route('/message', methods = ['GET'])
def get_message():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Message)
    data = []
    for message in dbResponse:
        data.append(message)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/message',methods=['POST'])
def create_message():
    c = json.loads(request.form['values'])
    user = entities.Message(
        content=c['content'],
        user_from_id=c['user_from']['username']['id'],
        user_to_id=c['user_to']['username']['id']
    )
    session = db.getSession(engine)
    session.add(user)
    session.commit()
    return 'Created User'

@app.route('/message', methods = ['PUT'])
def update_message():
    session = db.getSession(engine)
    id = request.form['key']
    message = session.query(entities.Message).filter(entities.Message.id == id).first()
    c =  json.loads(request.form['values'])
    for key in c.keys():
        setattr(message, key, c[key])
    session.add(message)
    session.commit()
    return 'Updated Message'

@app.route('/message', methods = ['DELETE'])
def delete_message():
    id = request.form['key']
    session = db.getSession(engine)
    messages = session.query(entities.Message).filter(entities.Message.id == id)
    for message in messages:
        session.delete(message)
    session.commit()
    return "Deleted Message"


@app.route('/authenticate', methods=['POST'])
def authenticate():

    #1. Get Request
    message=json.loads(request.data)
    username= message['username']
    password=message['password']
    #2. Look in databse
    session=db.getSession(engine)
    try:
        user=session.query(entities.User).filter(entities.User.username==username).filter(entities.User.password==password).one()
        message={'message':'Authorized'}
        return Response(message,status=200,mimetype='application/json')
    except Exception:
        message = {'message': 'UNAuthorized'}
        return Response(message,status=401,mimetype='application/json')

@app.route('/chat/<username>/')
def chat(username):
    db_session = db.getSession(engine)
    usuario= db_session.query(entities.User).filter(entities.User.username==username).one()
    mensajes = db_session.query(entities.User).filter(entities.User.id!=usuario.id).all()
    return render_template('chat.html', messages=mensajes)

@app.route('/chat/<username>/<id>')
def mostrar_mensajes(username,id):
    db_session=db.getSession(engine)
    usuario = db_session.query(entities.User).filter(entities.User.username == username).one()
    mensajes2 = db_session.query(entities.User).filter(entities.User.id != usuario.id).all()
    mensajes1 = db_session.query(entities.Message).filter(entities.Message.user_from_id == id).filter(entities.Message.user_to_id==usuario.id).all()
    return render_template('chat.html', messages=mensajes2,mensajes=mensajes1)



if __name__ == '__main__':
    app.secret_key  = ".."
    app.run(port=8081, threaded=True, host=('127.0.0.1'))

