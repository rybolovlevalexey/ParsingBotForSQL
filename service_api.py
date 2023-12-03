from flask import Flask, Request
from flask_restful import Resource, Api, reqparse, abort

app = Flask(__name__)
api = Api(app)

req_put_args = reqparse.RequestParser()
req_put_args.add_argument("name", type=str, required=True)

class InfoByPartName(Resource):
    def get(self, part_name):
        return