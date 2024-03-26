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
from models import db, Users, People, Planets, Starships, Favorites

from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
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


# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = "secret-bpn"  # Change this!
jwt = JWTManager(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.

@app.route("/login", methods=["POST"])
def login():
    email = request.json.get("email", None)
    password = request.json.get("password", None)

    query_result = Users.query.filter_by(email=email).first()

    if query_result is None:
        return jsonify({"msg": "Bad request"}), 401
    

    if email != query_result.email or password != query_result.password:
        return jsonify({"msg": "Bad request"}), 401

    access_token = create_access_token(identity=email)
    return jsonify(access_token=access_token)



# Protect a route with jwt_required, which will kick out requests
# # without a valid JWT present.

@app.route('/users/favorites/', methods=['GET'])
@jwt_required()
def get_user_favorites_protected():
    current_user = get_jwt_identity()
    current_user_data = Users.query.filter_by(email=current_user).first()

    query_result = Favorites.query.filter_by(users_id=current_user_data.serialize()['id']).all()
    print(current_user_data.serialize())
    print(query_result)

    if len(query_result) == 0:

        return jsonify({"msg": "There aren't any favorites yet"}), 404
    
    elif query_result:
            # results = [favorite.serialize() for favorite in query_results]
            results = list(map(lambda item: item.serialize(),query_result))
    
            print(results)
            return jsonify({"msg": "Ok", "results": results}), 200
    
    else: 
        return jsonify({"msg": "There aren't any favorites yet"}), 404
  
    
## Sign Up User

@app.route("/signup", methods=["POST"])
def signup():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    name= request.json.get("name", None)

    query_result = Users.query.filter_by(email=email).first()
  

   
    if query_result is None:

        new_user = Users(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"msg": "New user created"}), 200
    
    
    
    else :
        return jsonify({"msg": "User exist, try recover your password"}), 200
    
        



# PEOPLE

@app.route('/people', methods=['GET'])
def get_all_people():
    query_results = People.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
 
    print(query_results)
    
    if results != []:
        response_body = {
        "msg": "OK",
        "results": results
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": "There aren't any people yet"}), 404



@app.route('/people/<int:people_id>', methods=['GET'])
def get_one_people(people_id):
    query_results = People.query.filter_by(id=people_id).first()
 
    print(query_results)
    
    if query_results is not None:
        response_body = {
        "msg": "OK",
        "results": query_results.serialize()
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": f"People {people_id} not found"}), 404
    

# DELETE ONE PEOPLE

# @app.route('/people/<int:people_id>', methods=['DELETE'])
# def delete_one_people(people_id):
#     query_results = People.query.filter_by(id=people_id).first()
 
#     print(query_results)
    
#     if query_results is not None:
#         response_body = {
#         "msg": "OK",
#         "results": query_results.serialize()
#     }
#         return jsonify(response_body), 200
    
#     else:
#         return jsonify({"msg": f"People {people_id} not found"}), 404
    


# PLANETS

@app.route('/planets', methods=['GET'])
def get_all_planets():
    query_results = Planets.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
 
    print(query_results)
    
    if results != []:
        response_body = {
        "msg": "OK",
        "results": results
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": "There aren't any planets yet"}), 404



@app.route('/planets/<int:planets_id>', methods=['GET'])
def get_one_planet(planets_id):
    query_results = Planets.query.filter_by(id=planets_id).first()
 
    print(query_results)
    
    if query_results is not None:
        response_body = {
        "msg": "OK",
        "results": query_results.serialize()
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": f"Planets {planets_id} not found"}), 404

# STARSHIPS

@app.route('/starships', methods=['GET'])
def get_all_starships():
    query_results = Starships.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
 
    print(query_results)
    
    if results != []:
        response_body = {
        "msg": "OK",
        "results": results
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": "There aren't any starships yet"}), 404



@app.route('/starships/<int:starships_id>', methods=['GET'])
def get_one_starship(starships_id):
    query_results = Starships.query.filter_by(id=starships_id).first()
 
    print(query_results)
    
    if query_results is not None:
        response_body = {
        "msg": "OK",
        "results": query_results.serialize()
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": f"Starship {starships_id} not found"}), 404
    
    
# USERS

@app.route('/users', methods=['GET'])
def get_all_users():
    query_results = Users.query.all()
    results = list(map(lambda item: item.serialize(), query_results))
 
    print(query_results)
    
    if results != []:
        response_body = {
        "msg": "OK",
        "results": results
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": "There aren't any users yet"}), 404
    


# GET USERS FAVORITES 
    

@app.route('/users/favorites/<int:users_id>', methods=['GET'])
def get_user_favorites(users_id):
    query_results = Favorites.query.filter_by(users_id=users_id).all()
    results = list(map(lambda item: item.serialize(), query_results))
 
    print(query_results)
    
    if results != []:
        response_body = {
        "msg": "OK",
        "results": results
    }
        return jsonify(response_body), 200
    
    else:
        return jsonify({"msg": "There aren't any favorites yet"}), 404


# Add Favorite Planet

@app.route('/favorite/planet/<int:planets_id>', methods=['POST'])
def add_favorite_planet(planets_id):
    data = request.json
    print(data)

    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    planet_exist = Planets.query.filter_by(id=data["planets_id"]).first()

    if user_exist and planet_exist:

        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], users_id=data["users_id"]).first()
        print(query_results)

        if query_results is None:
            new_favorite = Favorites(planets_id=data["planets_id"], users_id=data["users_id"])
            db.session.add(new_favorite)
            db.session.commit()
        
            return ({"msg": "Ok"}),200
    

        else:

             return ({"msg": "Favorites already exists"}), 200
        

    elif user_exist is None and planet_exist is None:
        return ({"msg": "There aren't users or planets"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif planet_exist is None:
        return ({"msg": "This planet doesn't exist"}), 400
    


# Add Favorite People
    
@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    data = request.json
    print(data)

    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    people_exist = People.query.filter_by(id=data["people_id"]).first()

    if user_exist and people_exist:

        query_results = Favorites.query.filter_by(people_id=data["people_id"], users_id=data["users_id"]).first()
        print(query_results)

        if query_results is None:
            new_favorite = Favorites(people_id=data["people_id"], users_id=data["users_id"])
            db.session.add(new_favorite)
            db.session.commit()
        
            return ({"msg": "Ok"}),200
    

        else:

             return ({"msg": "Favorites already exists"}), 200
        

    elif user_exist is None and people_exist is None:
        return ({"msg": "There aren't users or planets"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif people_exist is None:
        return ({"msg": "This character doesn't exist"}), 400
    


# Delete favorite planet

@app.route('/favorite/planet/<int:planets_id>', methods=['DELETE'])
def delete_favorite_planet(planets_id):
    data = request.json

    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    planet_exist = Planets.query.filter_by(id=data["planets_id"]).first()

    if user_exist and planet_exist:

        query_results = Favorites.query.filter_by(planets_id=data["planets_id"], users_id=data["users_id"]).first()
        print(query_results)

        if query_results:
            
            db.session.delete(query_results)
            db.session.commit()
        
            return ({"msg": "Deleted succesfull"}), 200
    

        else:

             return ({"msg": "Planet already deleted"}), 200
        

    elif user_exist is None and planet_exist is None:
        return ({"msg": "There aren't users or planets to delete"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif planet_exist is None:
        return ({"msg": "This planet doesn't exist"}), 400



# Delete Favorite Character 

@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    data = request.json

    user_exist = Users.query.filter_by(id=data["users_id"]).first()
    people_exist = People.query.filter_by(id=data["people_id"]).first()

    if user_exist and people_exist:

        query_results = Favorites.query.filter_by(people_id=data["people_id"], users_id=data["users_id"]).first()
        print(query_results)

        if query_results:
            
            db.session.delete(query_results)
            db.session.commit()
        
            return ({"msg": "Deleted succesfull"}), 200
    

        else:

             return ({"msg": "Character already deleted"}), 200
        

    elif user_exist is None and people_exist is None:
        return ({"msg": "There aren't users or characters to delete"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif people_exist is None:
        return ({"msg": "This character doesn't exist"}), 400




# Delete Favorite Character Second Way
    
@app.route('/favorite/people/<int:people_id>/<int:users_id>', methods=['DELETE'])
def delete_favorite_people_user(people_id, users_id):
    
    user_exist = Users.query.filter_by(id=users_id).first()
    people_exist = People.query.filter_by(id=people_id).first()

    if user_exist and people_exist:

        query_results = Favorites.query.filter_by(people_id=people_id, users_id=users_id).first()
        print(query_results)
   
        if query_results:
            
            db.session.delete(query_results)
            db.session.commit()
        
            return ({"msg": "Deleted succesfull"}), 200


        else:

            return ({"msg": "Character already deleted"}), 200
        
    elif user_exist is None and people_exist is None:
        return ({"msg": "There aren't users or characters to delete"}), 400
  
    elif user_exist is None:
        return ({"msg": "This user doesn't exist"}), 400

    elif people_exist is None:
        return ({"msg": "This character doesn't exist"}), 400
        

# UPDATE PEOPLE
    
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    new_data= request.json

    query_results = Favorites.query.filter_by(people_id=people_id).first()

    if query_results: 
        for key, value in new_data.items():
            setattr(query_results, key, value)  

        db.session.commit()
    
        return ({"msg": "People Updated"}), 200

    else:

        return ({"msg": "People can't updated"}), 400
        
    # elif user_exist is None and people_exist is None:
    #     return ({"msg": "There aren't users or characters to delete"}), 400
  
    # elif user_exist is None:
    #     return ({"msg": "This user doesn't exist"}), 400

    # elif people_exist is None:
    #     return ({"msg": "This character doesn't exist"}), 400   



# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
