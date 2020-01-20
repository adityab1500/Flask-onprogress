from flask import Flask, request
from flask_restful import Resource, Api
from secure_check import authenticate, identity
from flask_jwt import JWT, jwt_required
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Migrate(app, db)

api = Api(app)
jwt = JWT(app, authenticate, identity)

# puppies = [{'name':'Rufus'},{name:'Frankie'},......]

#############################################################


class Puppy(db.Model):

    name = db.Column(db.String(80), primary_key=True)

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name}


class PuppyNames(Resource):
    def get(self, name):
        # print(puppies)
        # for pup in puppies:
        #     if pup['name'] == name:
        #         return pup

        pup = Puppy.query.filter_by(name=name).first()
        
        if pup:
            return pup.json()

        return {'name': None}, 404  # If you request a puppy not yet in the puppies list

    def post(self, name):
        # Add  the dictionary to list
        # pup = {'name': name}
        # puppies.append(pup)
        # # Then return it back
        # print(puppies)
        # return pup
        pup = Puppy(name=name)
        db.session.add(pup)
        db.session.commit()

        return pup.json()

    def delete(self, name):

        # for ind, pup in enumerate(puppies):
        #     if pup['name'] == name:
        #         # don't really need to save this
        #         delted_pup = puppies.pop(ind)
        #         return {'note': 'delete successful'}

        pup = Puppy.query.filter_by(name=name).first()
        if pup:
            db.session.delete(pup)
            db.session.commit()
            return {'note': 'delete success'}
        return {'note': 'delete failed'}


class AllNames(Resource):
    def get(self):
        # return all the puppies :)
        puppies = Puppy.query.all()

        return [pup.json() for pup in puppies]


api.add_resource(PuppyNames, '/puppy/<string:name>')
api.add_resource(AllNames, '/puppies')

if __name__ == '__main__':
    app.run(debug=True)
