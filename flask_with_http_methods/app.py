from flask import Flask, make_response, jsonify, request, render_template

app = Flask(__name__)

stock = {
    "fruit": {
        "apple": 30,
        "banana": 45,
        "cherry": 1000
    }
}

# GET - fetch a resource from the server
# POST - create a new resource on the server
# PUT - create/override a collection/data on the server
# PATCH - create/update a collection/data on the server
# DELETE - delete a collection/data on the server

@app.route("/get-text")
def get_text():
    return "some text"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/qs")
def qs():
    if request.args:
        req = request.args
        return " ".join(f"{k} : {v}" for k, v in req.items())
    return "No query"


@app.route("/stock")
def get_stock():
    return make_response(jsonify(stock), 200)


@app.route("/stock/<collection>")
def get_collection(collection):
    """Returns the collection from stock"""

    if collection in stock:
        return make_response(jsonify(stock[collection]), 200) 
    else:
        return make_response(jsonify({"error": "Item not found"}), 400)


@app.route("/stock/<collection>/<member>")
def get_member(collection, member):
    """Returns the qty of the member of the collection"""

    if collection in stock:
        member = stock[collection].get(member)

        if member:
            return make_response(jsonify(member), 200)
        else:
            return make_response(jsonify({"error": "Unknown member"}), 400)
    else:
        return make_response(jsonify({"error": "Collection not found"}), 400)


@app.route("/add-collection", methods=["GET", "POST"])
def add_collection():
    """
    Renders a template if the method is GET
    Creates a collection if the method is POST
    and if collection does not exist
    """

    if request.method == "POST":
        req = request.form

        collection = req.get("collection")
        member = req.get("member")
        qty = req.get("qty")

        if collection in stock:
            message = "Collection already exists"
        else:
            stock[collection] = {member: qty}
            message = "Collection created"

        return render_template("add_collection.html", stock=stock, message=message)

    else:
        return render_template("add_collection.html", stock=stock)


@app.route("/stock/<collection>", methods=["POST"])
def create_collection(collection):
    """ Creates a new collection if it does not exist """

    req = request.get_json() 
    if collection in stock:
        return make_response(jsonify({"error": "Collection already exists"}), 400)
    else:
        # stock.update({collection: req})
        stock[collection] = req
        return make_response(jsonify({"message": "Collection created"}), 200)


@app.route("/stock/<collection>", methods=["PUT"])
def put_collection(collection):
    """ 
    Replaces or creates a collection. Excepted body: {"member: : qty}
    Whole collection will be replaced
    """

    req = request.get_json()

    stock[collection] = req
    return make_response(jsonify({"message": "Collection replaced"}), 200)


@app.route("/stock/<collection>", methods=["PATCH"])
def patch_collection(collection):
    """ Updates or created a new collection. Expected body: {"member": qty} """

    req = request.get_json()

    if collection in stock:
        for k,v in req.items():
            stock[collection][k] = v
        
        return make_response(jsonify({"message": "Collection updated"}), 200)
    else:
        stock[collection] = req
        return make_response(jsonify({"message": "Collection created"}), 200)

@app.route("/stock/<collection>/<member>", methods=["PATCH"])
def patch_member(collection, member):
    """ Updates or creates a collection member. Expected body: {"qty": value} """

    req = request.get_json()

    if collection in stock:
        for k, v in req.items():
            if member in stock[collection]:
                stock[collection][member] = v
                return make_response(jsonify({"message": "Collection member added"}), 200)
            else:
                stock[collection][member] = v
                return make_response(jsonify({"message": "Collection member created"}), 200)
    else:
        return make_response(jsonify({"message": "Collection not found"}), 400)
            

# Doubt
@app.route("/stocks/<collection>", methods=["POST"])
def patch_collection_v2(collection):
    """ Updates or created a new collection. Expected body: {"member": qty} """

    req = request.get_json()

    if collection in stock:
        for k,v in req.items():
            stock[collection][k] = v
        
        return make_response(jsonify({"message": "Collection updated"}), 200)
    else:
        stock[collection] = req
        return make_response(jsonify({"message": "Collection created"}), 200)


@app.route("/stock/<collection>", methods=["DELETE"])
def delete_collection(collection):
    """ if the collection exist, delete it"""

    if collection in stock:
        del stock[collection]
        return make_response(jsonify({}), 204) # Action enacted
    else:
        return make_response(jsonify({"message": "Collection not found"}), 400)


@app.route("/stock/<collection>/<member>", methods=["DELETE"])
def delete_member(collection, member):
    """  if the collection and member exist, delete it """

    if collection in stock:
        if member in stock[collection]:
            del stock[collection][member]
            return make_response(jsonify({}), 204)
        else:
            return make_response(jsonify({"error": "Member not found"}), 400)
    else:
        return make_response(jsonify({"error": "Collection not found"}), 400)