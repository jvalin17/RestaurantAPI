from flask import Flask
from ratingController import ratingController
from userController import userController
from restaurantController import restaurantController

app = Flask(__name__)

app.register_blueprint(restaurantController)
app.register_blueprint(userController)
app.register_blueprint(ratingController)



if __name__ == '__main__':
    app.debug = True
    app.run(port=5002)
