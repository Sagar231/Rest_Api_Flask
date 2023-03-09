from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
import sqlite3
from models.items import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be left blank'
                        )


    @jwt_required()
    def get(self,name):
        item  = ItemModel.find_by_name(name)
        if item:
            return item.json()

        return {"massage":"item not found"},404
        #most popular http code is 200

    def post(self,name):
        if ItemModel.find_by_name(name):
            return {"massage":f"Item with name {name} already exixts." },400 #bad request

        data = Item.parser.parse_args()
        item = ItemModel(name , data['price'])
        try:
            item.save_to_db()
        except:
            return {"massage": "An error occurred inserting the item"} , 500
        #500 = internal server error

        return item.json() ,201

    def delete(self,name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'massage':'item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,data['price'])
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)
        items = []
        for row in result:
            items.append({'name':row[0],'price':row[1]})

        connection.close()

        return {"items":items}