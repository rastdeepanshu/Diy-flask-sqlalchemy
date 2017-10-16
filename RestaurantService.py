from flask import Flask, request
from flask.json import jsonify

import Database as db
import Authenticate as a
import Response

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/restaurants", methods=['GET'])
@a.requires_auth
def get_restaurants():
    s = db.Session()
    return jsonify([rest.serialize for rest in s.query(db.Restaurant).all()])


@app.route("/restaurants", methods=['POST'])
@a.requires_auth
def create_restaurant():
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
        return Response.unsupported()

    json = request.get_json()
    rest = db.Restaurant()
    rest.name = json['name']
    rest.address = json['address']
    owners = json['owners']

    s = db.Session()

    for o in owners:
        owner = None
        if 'id' in o:
            owner = s.query(db.Owner).get(o['id'])
            if owner is None:
                owner = db.Owner(o['name'], o['age'], o['gender'])
        else:
            owner = db.Owner(**o)
        rest.owners.append(owner)

    s.add(rest)
    s.flush()
    s.commit()
    return Response.successful()


@app.route("/restaurants/<rest_id>", methods=['GET'])
@a.requires_auth
def get_restaurant(rest_id):
    s = db.Session()
    return jsonify(s.query(db.Restaurant).get(rest_id).serialize)


@app.route("/restaurants/<rest_id>", methods=['PUT'])
@a.requires_auth
def update_restaurant(rest_id):
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
        return Response.unsupported()

    json = request.get_json()

    s = db.Session()
    rest = s.query(db.Restaurant).get(rest_id)
    rest.name = json['name']
    rest.address = json['address']
    rest.owners = []
    owners = json['owners']

    for o in owners:
        owner = None
        if 'id' in o:
            owner = s.query(db.Owner).get(o['id'])
            if owner is None:
                owner = db.Owner(o['name'], o['age'], o['gender'])
        else:
            owner = db.Owner(**o)
        rest.owners.append(owner)

    s.commit()
    return Response.successful()


@app.route("/restaurants/<rest_id>", methods=['DELETE'])
@a.requires_auth
def delete_restaurant(rest_id):
    s = db.Session()
    s.query(db.Restaurant).filter_by(id=rest_id).delete()
    s.execute(db.delete_restaurant(rest_id))
    s.commit()
    return Response.successful()


@app.route("/restaurants/<rest_id>/owners", methods=['GET'])
@a.requires_auth
def get_restaurant_owners(rest_id):
    s = db.Session()
    rest = s.query(db.Restaurant).get(rest_id)
    return jsonify([owner.serialize for owner in rest.owners])


@app.route("/owners", methods=['GET'])
@a.requires_auth
def get_owners():
    s = db.Session()
    return jsonify([owner.serialize for owner in s.query(db.Owner).all()])


@app.route("/owners", methods=['POST'])
@a.requires_auth
def create_owner():
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
        return Response.unsupported()

    json = request.get_json()
    owner = db.Owner(**json)

    s = db.Session()
    s.add(owner)
    s.flush()
    s.commit()
    return Response.successful()


@app.route("/owners/<owner_id>", methods=['GET'])
@a.requires_auth
def get_owner(owner_id):
    s = db.Session()
    return jsonify(s.query(db.Owner).get(owner_id).serialize)


@app.route("/owners/<owner_id>", methods=['PUT'])
@a.requires_auth
def update_owner(owner_id):
    if 'Content-Type' not in request.headers or request.headers['Content-Type'] != 'application/json':
        return Response.unsupported()

    json = request.get_json()

    s = db.Session()
    owner = s.query(db.Owner).get(owner_id)

    owner.name = json['name']
    owner.age = json['age']
    owner.gender = json['gender']

    s.commit()
    return Response.successful()


@app.route("/owners/<owner_id>", methods=['DELETE'])
@a.requires_auth
def delete_owner(owner_id):
    s = db.Session()
    s.query(db.Owner).filter_by(id=owner_id).delete()
    s.execute(db.delete_owner(owner_id))
    s.commit()
    return Response.successful()


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(port=8080, threaded=True)
