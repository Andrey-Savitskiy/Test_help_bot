from flask_restful import Resource
from db_api.db import FeedBacks, session
import json
from config import *


class HalperBotFeedback(Resource):
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
