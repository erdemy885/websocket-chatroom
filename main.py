from flask import Flask
from sockets import socketio
from frontend import frontend_bp

app = Flask(__name__)
app.register_blueprint(frontend_bp)

socketio.init_app(app)

app.config["SECRET_KEY"] = "abcdefg"

if __name__ == "__main__":
    socketio.run(app)