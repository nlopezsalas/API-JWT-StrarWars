from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Favorites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'), nullable=True)
    planets_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)
    starships_id = db.Column(db.Integer, db.ForeignKey('starships.id'), nullable=True)
    users_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)

    def __repr__(self):
        return '<Favorites %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "people_id": self.people_id,
            "planets_id": self.planets_id,
            "starships_id": self.starships_id,
            "users_id": self.users_id
            # do not serialize the password, its a security breach
        }



class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    

class People(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    eye_color = db.Column(db.String(120), unique=True, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    PeopleFavorites = db.relationship(Favorites)

    def __repr__(self):
        return '<People %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "eye_color": self.eye_color,
            "height": self.height
            # do not serialize the password, its a security breach
        }
    

class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=True, nullable=False)
    population = db.Column(db.Integer, nullable=False)
    PlanetsFavorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Planets %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "population": self.population
            # do not serialize the password, its a security breach
        }
    

class Starships(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=False, nullable=False)
    model = db.Column(db.String(120), unique=True, nullable=False)
    passengers = db.Column(db.Integer, nullable=False)
    StarshipsFavorites = db.relationship(Favorites)

    def __repr__(self):
        return '<Starships %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "model": self.model,
            "passengers": self.passengers
            # do not serialize the password, its a security breach
        }