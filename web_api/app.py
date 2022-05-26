from flask import Flask
from flask_restful import Resource, Api
from db_api.db import FeedBacks, session
import json
from config import *


app = Flask(__name__)
api = Api(app)


class Feedbackes(Resource):
    def get_data(self) -> json:
        response = session.query(
            FeedBacks.tg_id,
            FeedBacks.created_on,
            FeedBacks.username,
            FeedBacks.end,
            FeedBacks.feedback,
            FeedBacks.photo,
        ).all()
        result = [row.__dict__ for row in response]
        return json.dumps(result)

    @logger.catch()
    def get(self):
        return self.get_data()


api.add_resource(Feedbackes, '/')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False)
