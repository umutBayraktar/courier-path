from pydantic import BaseModel
from fastapi import FastAPI
from operator import itemgetter
from mongo_connector import *
from haversine import haversine
app = FastAPI()



class Courier(BaseModel):
    full_name: str


class Sender(BaseModel):
    name : str
    latitude: float
    longitude: float


class Order(BaseModel):
    receiver: str
    latitude: float
    longitude: float
    courier : int


class Coordinates(BaseModel):
    latitude: float
    longitude: float

class CourierPathInfo(BaseModel):
    sender: int
    latitude: float
    longitude: float


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/add/courier/")
async def add_courier(courier: Courier):
    couriers_count = get_courier_count()
    couriers_index = couriers_count + 1
    courier = courier.dict()

    add_courier_to_mongo(couriers_index, courier)
    return courier

@app.post("/add/sender/")
async def add_sender(sender: Sender):
    sender_count = get_sender_count()
    sender_index = sender_count + 1
    sender = sender.dict()
    temp = {}
    temp["latitude"] = sender["latitude"]
    temp["longitude"] = sender["longitude"]
    temp["orders"] = []
    add_sender_to_mongo(sender_index, temp)
    return sender

@app.post("/add/order/{sender_id}")
async def add_order(sender_id:int, order: Order):
    order = order.dict()
    add_order_to_mongo(sender_id,order)
    return order



@app.post("/get/sender/")
async def get_sender(coordinates:Coordinates):
    coordinates = coordinates.dict()
    courier_latitude = coordinates["latitude"]
    courier_longitude = coordinates["longitude"]

    min_distance = 100000000
    min_sender_id = 0
    empty_senders = get_empty_senders()
    for sender in empty_senders:
        sender_latitude = sender["latitude"]
        sender_longitude = sender["longitude"]
        distance = haversine(sender_latitude,sender_longitude,courier_latitude,courier_longitude)
        if distance < min_distance:
            min_distance = distance
            min_sender_id = sender["id"]
    return {"sender": min_sender_id, "distance":min_distance}


def find_next_order(prev_order, order_list):
    new_order_list = []
    for order in order_list:
        distance = haversine(prev_order["latitude"],prev_order["longitude"],order["latitude"],order["longitude"])
        order["distance"] = distance
        new_order_list.append(order)
    sorted_list = sorted(new_order_list, key=itemgetter('distance'))
    next_order = sorted_list[0]
    return next_order


@app.post("/get/path/{sender_id}:")
async def get_path(sender_id: int):
    #import pdb; pdb.set_trace()
    sender = get_sender_object(sender_id)
    empty_orders = get_senders_empty_orders(sender_id)
    first_order = find_next_order(sender, empty_orders)
    path_list = []
    path_list.append(first_order)
    empty_orders.remove(first_order)
    prev_order = first_order 
    for i in range(len(empty_orders)):
        next_order = find_next_order(prev_order, empty_orders)
        path_list.append(next_order)
        empty_orders.remove(next_order)
        prev_order = next_order
    return {"empty_orders":empty_orders, "path_list":path_list}