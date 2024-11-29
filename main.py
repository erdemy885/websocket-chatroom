from flask import Flask
from sockets import socketio
from frontend import frontend_bp
import os

app = Flask(__name__)
app.register_blueprint(frontend_bp)

socketio.init_app(app)

app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

if __name__ == "__main__":
    socketio.run(app)
