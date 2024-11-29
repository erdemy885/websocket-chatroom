from flask import render_template, request, redirect, url_for, session, Blueprint
from string import ascii_uppercase
from datetime import datetime, timezone
from sockets import rooms
import random

frontend_bp = Blueprint(
    "frontend",
    __name__,
    url_prefix="/",
    template_folder="templates",
    static_folder="static"
)

def generate_unique_code(length):
    while True:
        code = ""
        for _ in range(length):
            code += random.choice(ascii_uppercase)
            
        if code not in rooms:
            break
    
    return code

@frontend_bp.route("/", methods=["POST", "GET"])
def home():
    session.clear()
    if request.method == "POST":
        name = request.form.get("name")
        code = request.form.get("code")
        join = request.form.get("join", False)
        create = request.form.get("create", False)

        if not name:
            return render_template("home.html", error="Please enter a name.", code=code, name=name)
        
        if join != False and not code:
            return render_template("home.html", error="Please enter a room code.", code=code, name=name)
        
        room = code.strip().upper()
        if create != False:
            room = generate_unique_code(4)
            rooms[room] = {"members": 0, "messages": []}
            date = datetime.now(timezone.utc)
            content={
                "name": name,
                "message": "created the room",
                "time": int(date.timestamp())
            }
            rooms[room]["messages"].append(content)
        elif room not in rooms:
            return render_template("home.html", error="Room does not exist.", code=code, name=name)
        
        session["room"] = room
        session["name"] = name
        return redirect(url_for("frontend.room"))

    return render_template("home.html")

@frontend_bp.route("/room")
def room():
    room = session.get("room")
    if room is None or session.get("name") is None or room not in rooms:
        return redirect(url_for("frontend.home"))
    
    return render_template("room.html", code=room, messages=rooms[room]["messages"])