from flask_socketio import join_room, leave_room, send, SocketIO
from datetime import datetime
from flask import session

rooms = {}
socketio = SocketIO()

@socketio.on("message")
def message(data):
    room = session.get("room")
    if room not in rooms:
        return
    
    date = datetime.now()
    
    content = {
        "name": session.get("name"),
        "message": data["data"],
        "time": date.strftime("%m/%d/%Y %I:%M:%S %p")
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{session.get('name')} said: {data['data']}")

@socketio.on("connect")
def connect(auth):
    room = session.get("room")
    name = session.get("name")
    if not room or not name:
        return
    if room not in rooms:
        leave_room(room)
        return
    date = datetime.now()

    content = {
        "name": name,
        "message": "has entered the room",
        "time": date.strftime("%m/%d/%Y %I:%M:%S %p")
    }

    join_room(room)
    send(content, to=room)
    rooms[room]["messages"].append(content)
    rooms[room]["members"] += 1
    print(f"{name} joined room {room}")

@socketio.on("disconnect")
def disconnect():
    room = session.get("room")
    name = session.get("name")
    leave_room(room)

    if room in rooms:
        rooms[room]["members"] -= 1
        if rooms[room]["members"] <= 0:
            del rooms[room]
            return

    date = datetime.now()

    content = {
        "name": name,
        "message": "has left the room",
        "time": date.strftime("%m/%d/%Y %I:%M:%S %p")
    }

    send(content, to=room)
    rooms[room]["messages"].append(content)
    print(f"{name} has left room {room}")
