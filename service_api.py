from flask import Flask, Request
from flask_restful import Resource, Api, reqparse, abort
from database_actions import get_info_by_part_name

app = Flask(__name__)
api = Api(app)

req_put_args = reqparse.RequestParser()
req_put_args.add_argument("name", type=str, required=True)


class InfoByPartName(Resource):  # входные данные - название детали
    def get(self, part_name):
        return get_info_by_part_name(part_name)


class InfoByArticle(Resource):  # входные данные только артикул
    def get(self):  # один артикул
        pass

    def post(self):  # список артикулов
        pass


class InfoByArticleAndBrand(Resource):  # входные данные - артикул и бренд
    def get(self, part_name, brand):
        pass


api.add_resource(InfoByPartName, "/by_part_name/<str:part_name>")
api.add_resource(InfoByArticle, "/by_article/<str:article>")
api.add_resource(InfoByPartName, "/by_article_brand/<str:part_name>/<str:brand>")

if __name__ == "__main__":
    app.run(debug=True)
