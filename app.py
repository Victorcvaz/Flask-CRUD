from flask import Flask, Response, request
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import json


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/flaskcrud'
db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(100))

    def to_json(self):
        return {"id": self.id, "name": self.name, "email": self.email}

# Select All

@app.route("/users", methods=["GET"])
def select_users():
    users_object = Users.query.all()
    users_json = [users.to_json() for users in users_object]

    return get_response(200, "users", users_json)

# Select One

@app.route("/user/<id>", methods=["GET"])
def select_one(id):
    user_object = Users.query.filter_by(id=id).first()
    user_json = user_object.to_json()

    return get_response(200, "user", user_json)

# Register

@app.route("/user", methods=["POST"])
def create_user():
    body = request.get_json()

    # Valid the parameters
    # Or use TRY and Catch

    try:
        user = Users(name=body["name"], email=body["email"])
        db.session.add(user)
        db.session.commit()
        return get_response(201, "user", user.to_json(), "Create successfully")
    except Exception as e:
        print("Error", e)
        return get_response(400, "user", {}, "register error")


# Update

@app.route("/user/<id>", methods=["PUT"])
def update_user(id):
    user_object = Users.query.filter_by(id=id).first()
    body = request.get_json()

    try:
        if("name" in body):
            user_object.name = body["name"]
        if("email" in body):
            user_object.email = body["email"]
        db.session.add(user_object)
        db.session.commit()
        return get_response(200, "user", user_object.to_json(), "Create successfully")
    except Exception as e:
        print("Error", e)
        return get_response(400, "user", {}, "Register error")


# Delete

@app.route("/user/<id>", methods=["DELETE"])
def delet_user(id):
    user_object = Users.query.filter_by(id=id).first()

    try:
        db.session.delete(user_object)
        db.session.commit()
        return get_response(200, "user", user_object.to_json(), "Delete successfully")
    except Exception as e:
        print("Error", e)
        return get_response(400, "user", {}, "Delete error")


def get_response(status, content_name, content, msg=False):
    body = {}
    body[content_name] = content

    if(msg):
        body["msg"] = msg
    return Response(json.dumps(body), status=status, mimetype="application/json")
app.run()