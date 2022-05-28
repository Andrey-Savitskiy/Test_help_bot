from flask import Flask
from flask_restful import Resource, Api
from db_api.db import FeedBacks, session
import json
from config import *


app = Flask(__name__)
api = Api(app)


class App(Resource):
    def get_data(self) -> json:
        query = session.query(
            FeedBacks.tg_id,
            FeedBacks.created_on,
            FeedBacks.username,
            FeedBacks.end,
            FeedBacks.feedback,
            FeedBacks.photo,
        )

        result = [dict(row) for row in query.all()]
        return result

    @logger.catch()
    def get(self):
        return self.get_data()


api.add_resource(App, '/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
