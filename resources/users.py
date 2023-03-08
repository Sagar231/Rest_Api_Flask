import sqlite3
from flask_restful import Resource,reqparse
from models.users import UserModel

class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("username",
                        type=str,
                        required=True,
                        help="Cannot be left blank"
                        )
    parser.add_argument("password",
                        type=str,
                        required=True,
                        help="Cannot be left blank"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
           return {"massage":"A user with that username already exists. "} ,400

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "INSERT INTO users VALUES (NULL,?,?)"
        cursor.execute(query,(data['username'],data['password']))

        connection.commit()
        connection.close()

        return {"massage":"User created successfully"},201
