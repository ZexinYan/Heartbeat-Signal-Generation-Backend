import pymongo
from bson.objectid import ObjectId
from hsg.database.constant import DataBaseConstant


class UserTable:
    _client = None
    _table = None

    @staticmethod
    def table():
        if UserTable._table is None:
            UserTable._client = pymongo.MongoClient("mongodb://localhost:27017/")
            UserTable._table = UserTable._client[DataBaseConstant.DATABASE_NAME][DataBaseConstant.USER_TABLE]
            UserTable._table.create_index('email', unique=True)
        return UserTable._table

    def find(self, condition=None):
        users_list = []
        table = self.table()
        if condition is None:
            find_result = table.find()
        else:
            find_result = table.find(condition)
        for each in find_result:
            each['_id'] = str(each['_id'])
            users_list.append(each)
        return users_list

    def insert_one(self, item):
        table = self.table()
        x = table.insert_one(item)
        return str(x.inserted_id)

    def update_one(self, _id, new_values):
        table = self.table()
        query = {"_id": ObjectId(_id)}
        new_values = {"$set": new_values}
        return table.update_one(query, new_values)

    def delete_one(self, _id):
        table = self.table()
        return table.delete_one({"_id": ObjectId(_id)})


if __name__ == '__main__':
    user_table = UserTable.table()
    insert_id = user_table.insert_one({
        'username': "zexiny",
        'password': "12344",
        'phone': "6693386680",
        'email': "zexiny@andrew.cmu.edu"
    })
    print(f'insert_id: {insert_id}')
