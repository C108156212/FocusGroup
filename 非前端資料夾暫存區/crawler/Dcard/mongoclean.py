from pymongo import MongoClient


def MongoClean():
    conn = MongoClient(host='localhost', port=27017)
    db = conn['Data']
    collection = db['Dcard02']

    deleteData = collection.aggregate([
        {'$group': {
            '_id': {'firstField': "$content", 'secondField': "$time", 'thirdField': "$comment"},
            'uniqueIds': {'$addToSet': "$_id"},
            'count': {'$sum': 1}
        }},
        {'$match': {
            'count': {'$gt': 1}
        }}
    ])
    first = True
    for d in deleteData:
        first = True
        for did in d['uniqueIds']:
            if first != True:  # 第一個不刪除
                collection.delete_one({'_id': did})
            first = False
    print('cleandone')
