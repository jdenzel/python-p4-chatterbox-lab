from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import asc

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():
    
    messages = []
    if request.method == 'GET':
        for message in Message.query.order_by(asc(Message.created_at)).all():
            message_dict = {
            "body": message.body,
            "id": message.id
            }
            messages.append(message_dict)

        response = make_response(
            messages,
            200
        )
        return response
        
    elif request.method == 'POST':
        json_data = request.get_json()
        new_message = Message(
            body = json_data["body"],
            username = json_data["username"],
        ) 

        db.session.add(new_message)
        db.session.commit()

        message_dict = new_message.to_dict()

        response = make_response(
            message_dict,
            201
        )

        return response
    
    

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    messages = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH':

        json_data = request.get_json()
        messages.body = json_data['body']
        db.session.add(messages)
        db.session.commit()

        messages_dict = messages.to_dict()

        response = make_response(
            messages_dict,
            200
        )
        return response
    
    elif request.method == 'DELETE':
        db.session.delete(messages)
        db.session.commit()

        response_body = {
            "delete_successful": True,
            "message": "Review deleted."    
        }

        response = make_response(
            response_body,
            200
        )

        return response

if __name__ == '__main__':
    app.run(port=5555)
