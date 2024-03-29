from flask_restful import Resource
from models.storemodel import  StoreModel

class Stores(Resource):

    def get(self, name):
        store = StoreModel.find_by_name(name)
        if store:
            return store.json()

        return {"message":"Store not found"},404

    def post(self, name):
        if StoreModel.find_by_name(name):
            return {"message":"Store {} already exists".format(name)}, 400
        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {"message":"Error occured creating db"},500

        return store.json(), 201

    def delete(self,name):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message":"Store deleted"}


class StoreList(Resource):
    def get(self):
        return {"stores":[store.json() for store in StoreModel.query.all()]}