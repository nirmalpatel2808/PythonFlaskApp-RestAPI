import uuid
from flask import Flask, request
from flask_smorest import abort
from db import items,stores

app = Flask(__name__)

@app.get("/")
def home_page():
    return "This is Home Page"
    
@app.get("/store")
def get_stores():
    return {"stores":list(stores.values())}

@app.post("/store")
def create_store():
    store_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**store_data, "id":store_id}
    stores[store_id] = store
    return store, 201
    
@app.post("/item")
def create_item():
    item_data = request.get_json()
    if (
        "price" not in item_data 
        or "store_id" not in item_data 
        or "name" not in item_data
        
    ):
        abort(400,message="Bad Request, Ensure 'Price','Store_Id' and 'Name' are included in JSON Payload")
    
    for item in items.values():
        if (
            item_data["name"] == item["name"] and 
            item_data["store_id"] == item["store_id"]
        ):
            abort (400,message=f"Item Already Exists")
            
    if item_data["store_id"] not in stores:
        abort(404,message="Store Not Found...!")
    item_id = uuid.uuid4().hex
    item = {**item_data,"id":item_id} 
    items[item_id] = item
    return item,201

@app.post("/item")
def get_all_items():
    return "Hello World"
    return {"items":list(items.values())}
    
@app.get("/store/<string:store_id>")
def get_store(store_id):
    try:
        return stores[store_id] 
    except KeyError:
        abort(404,message="Store Not Found...!")

@app.get("/item/<string:item_id>")
def get_item(item_id):
    try:
        return items[item_id]
    except KeyError:    
        abort(404,message="Item Not Found...!")

@app.delete("/item/<string:item_id>")
def delete_item(item_id):
    try:
        del items[item_id]
        return {"message":"Item Deleted"}
    except KeyError:    
        abort(404,message="Item not found...!")
        
@app.delete("/store/<string:store_id>")
def delete_store(store_id):
    try:
        del stores[store_id]
        return {"message":"Store Deleted"}
    except KeyError:    
        abort(404,message="Store not found...!")

@app.put("/item/<string:item_id>")
def update_item(item_id):
    item_data = request.get_json()
    if "price" not in item_data or "name" not in item_data:
        abort(400,message="Ensure 'Price' and 'Item name' included in Json Payload.")
    try:
        item = items[item_id]
        item |= item_data
        return item
    except KeyError:    
        abort(404,message="Item not found...!")

@app.get("/item")
def get_all_item():
    return {"items":list(items.values())}