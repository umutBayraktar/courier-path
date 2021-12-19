from pymongo import MongoClient
from config import *



mongo_connector = MongoClient(
    MONGO_HOST,MONGO_PORT
)

navigation_db = mongo_connector.navigation
couriers = navigation_db["courier"]
senders = navigation_db["sender"]


def get_courier_count():
    count = 0 
    for x in couriers.find({}):
        count +=1
    return count

def get_sender_count():
    count = 0 
    for x in senders.find({}):
        count +=1
    return count


def add_courier_to_mongo(id, data):
    temp_data = data.copy()
    temp_data["id"] = id
    couriers.insert_one(temp_data)

def add_sender_to_mongo(id,data):
    temp_data = data.copy()
    temp_data["id"] = id
    senders.insert_one(temp_data)

def add_order_to_mongo(sender_id,order_data):
    sender = senders.find_one({"id":sender_id})
    #import pdb; pdb.set_trace()
    orders = sender["orders"]
    order_id = len(orders) + 1
    order_data["id"] = order_id
    orders.append(order_data)
    senders.update_one({"id":sender_id},{"$set":{"orders":orders}})


def get_empty_senders():
    sender_list = senders.find({"orders.courier":0})
    return sender_list

def get_senders_empty_orders(sender_id):
    sender = senders.find_one({"id":sender_id})
    empty_order_list = []
    for order in sender["orders"]:
        if order["courier"] == 0:
            empty_order_list.append(order)
    return empty_order_list


def get_sender_object(sender_id):
    sender = senders.find_one({"id":sender_id})
    return sender#{"latitude":sender["latitude"],"longitude":sender["longitude"]}