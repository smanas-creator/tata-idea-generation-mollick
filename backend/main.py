import sys
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import socketio
import os
from crew import create_product_crew, create_marketing_crew, create_hr_crew
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allows the frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins='http://localhost:3000')
socket_app = socketio.ASGIApp(sio)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Mount the socket.io app
app.mount("/socket.io", socket_app)

class StreamToSocketIO:
    def __init__(self, sid):
        self.sid = sid

    def write(self, data):
        for line in data.splitlines():
            if line.strip():  # Only emit non-empty lines
                asyncio.create_task(sio.emit('message', line, room=self.sid))
        sys.stdout.flush() # Explicitly flush stdout

    def flush(self):
        pass

class CrewOutputCapturer:
    def __init__(self, sid):
        self.sid = sid
        self.original_stdout = sys.stdout
        self.stream_to_socket = StreamToSocketIO(sid)

    def __enter__(self):
        sys.stdout = self.stream_to_socket
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout # No need to flush original_stdout here anymore

@sio.on('connect')
async def connect(sid, environ):
    print(f'connect {sid}')
    print(f'Frontend connected: {sid}') # Added log

@sio.on('disconnect')
async def disconnect(sid):
    print(f'disconnect {sid}')

@sio.on('idea')
async def idea(sid, data):
    print(f'Received idea from {sid}: {data}')
    print(f'Idea received from frontend: {data}') # Added log
    team = data.get('team')
    idea_text = data.get('idea')

    if not team or not idea_text:
        print("Missing team or idea")
        await sio.emit('error', {'message': 'Team and idea are required.'}, room=sid)
        return

    print(f"Creating crew for team: {team}")
    crew = None
    if team == 'Product Management':
        crew = create_product_crew(idea_text)
    elif team == 'Marketing':
        crew = create_marketing_crew(idea_text)
    elif team == 'HR':
        crew = create_hr_crew(idea_text)

    if crew:
        print("Crew created successfully. Kicking off...")
        try:
            with CrewOutputCapturer(sid):
                result = crew.kickoff()
                print(f"Crew kickoff finished. Result: {result}") # This will now go to socket
            await sio.emit('final_result', str(result), room=sid)
        except Exception as e:
            print(f"An error occurred during crew kickoff: {e}")
            await sio.emit('error', {'message': str(e)}, room=sid)
        finally:
            print("Restored stdout")
    else:
        print(f"Invalid team selected: {team}")
        await sio.emit('error', {'message': 'Invalid team selected.'}, room=sid)

import sys