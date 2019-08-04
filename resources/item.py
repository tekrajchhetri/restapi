from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from models.itemmodel import  ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument("price",
                        type=float,
                        required=True,
                        help="This field Price is required")

    parser.add_argument("store_id",
                        type=int,
                        required=True,
                        help="This field store id is required")



    @jwt_required()
    def get(self, name):
        try:
            item = ItemModel.find_by_name(name)

        except:
            return {"message":"Database find error"}, 500 #server error

        if item:
            return item.json()

        return {"message": "Item not found"}



    def post(self, name):

        if ItemModel.find_by_name(name):
            return {"message":"An item with name {} already exists.".format(name)},400 #400 - bad request

        requested_data = Item.parser.parse_args()
        item = ItemModel(name, **requested_data) # **requested_data === requested_data["price"], requested_data["store_id"]
        try:
           item.save_to_db()
        except:
            return {"message":"Error occured inserting the item"},500 #internal server error
        return item.json(), 201 #201 -- created

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {"message": "Item Deleted"}




    def put(self, name):
        requested_data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name,**requested_data)
        else:
            item.price = requested_data["price"]

        item.save_to_db()

        return item.json()


class Itemlist(Resource):
    def get(self):
        # list(map(lambda x: x.json(), ItemModel.query.all()))
        return {"items": [x.json() for x in ItemModel.query.all()]}

