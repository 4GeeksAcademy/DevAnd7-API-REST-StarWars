"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planet
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)


#ENDPOINTS USER
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()

    return jsonify([u.serialize() for u in users]), 200



#ENDPOINTS PEOPLE:
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()

    return jsonify([p.serialize() for p in people]),200

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_id(people_id):
    person = People.query.get(people_id)
    if not person:
        return jsonify({'msg':'People not found'}), 404
    return jsonify(person.serialize()), 200


#ENDPOINTS PLANETS:
@app.route('/planets', methods=['GET'])
def get_planets():
    planet = Planet.query.all()

    return jsonify([p.serialize() for p in planet]),200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet_id(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({'msg':'Planet not found'}), 404
    return jsonify(planet.serialize()), 200




# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
