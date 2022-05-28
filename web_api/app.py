from flask import Flask
from flask_restful import Api
from resourses.app_classes import HalperBotFeedback


app = Flask(__name__)
api = Api(app)

api.add_resource(HalperBotFeedback, '/')


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
