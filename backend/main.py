import sys
import io
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
import asyncio
import socketio
import os
import re
from crew import create_product_crew, create_marketing_crew, create_hr_crew
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "https://tata-idea-frontend-el4g3hgpn-manas-sharmas-projects-187f8ce5.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sio = socketio.AsyncServer(async_mode='asgi', cors_allowed_origins=[
    'http://localhost:3000',
    'http://localhost:3001',
    'https://tata-idea-frontend-el4g3hgpn-manas-sharmas-projects-187f8ce5.vercel.app'
])
socket_app = socketio.ASGIApp(sio)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Mount the socket.io app
app.mount("/socket.io", socket_app)

class AgentConversationCapturer:
    def __init__(self):
        self.conversations = []
        self.original_stdout = sys.stdout
        self.captured_output = io.StringIO()

    def __enter__(self):
        sys.stdout = self.captured_output
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout = self.original_stdout
        self.parse_conversations()

    def parse_conversations(self):
        """Parse the captured output and extract only the meaningful agent final answers"""
        output = self.captured_output.getvalue()

        # Look for final answer blocks in the CrewAI output
        final_answer_pattern = r'Agent:\s*([^│\n]+).*?Final Answer:\s*(.+?)(?=╰|Agent:|$)'
        matches = re.findall(final_answer_pattern, output, re.DOTALL)

        for agent_name, answer in matches:
            agent_name = agent_name.strip()
            # Clean up the answer by removing box characters and extra whitespace
            clean_answer = re.sub(r'[│╭╮╯╰─]+', '', answer)
            clean_answer = re.sub(r'\s*\|\s*', '\n', clean_answer)
            clean_answer = re.sub(r'\n\s*\n', '\n\n', clean_answer)
            clean_answer = clean_answer.strip()

            # Remove "Thought:" lines and other CrewAI metadata
            lines = clean_answer.split('\n')
            filtered_lines = []
            for line in lines:
                line = line.strip()
                if (line and
                    not line.startswith('Thought:') and
                    not line.startswith('🚀 Crew:') and
                    not line.startswith('📋 Task:') and
                    not line.startswith('Status:') and
                    not line.startswith('Assigned to') and
                    not line.startswith('Using Tool:') and
                    not re.match(r'^[a-f0-9-]{36}$', line)):  # Task IDs
                    filtered_lines.append(line)

            if filtered_lines:
                final_answer = '\n'.join(filtered_lines).strip()
                if final_answer and len(final_answer) > 20:  # Only add substantial responses
                    self.conversations.append({
                        'agent': agent_name,
                        'message': final_answer
                    })

        # If no final answers found, try alternative patterns for agent outputs
        if not self.conversations:
            # Look for any agent sections with meaningful content
            agent_sections = re.split(r'Agent:\s*([^│\n]+)', output)
            current_agent = None

            for i, section in enumerate(agent_sections):
                if i % 2 == 1:  # This is an agent name
                    current_agent = section.strip()
                elif current_agent and section.strip():
                    # This is the content for the current agent
                    clean_content = re.sub(r'[│╭╮╯╰─]+', '', section)
                    clean_content = re.sub(r'\s*\|\s*', '\n', clean_content)
                    clean_content = re.sub(r'\n\s*\n', '\n\n', clean_content)

                    # Extract meaningful content
                    lines = clean_content.split('\n')
                    meaningful_lines = []
                    for line in lines:
                        line = line.strip()
                        if (line and
                            len(line) > 10 and
                            not line.startswith('Task:') and
                            not line.startswith('Status:') and
                            not line.startswith('🚀') and
                            not line.startswith('📋') and
                            not line.startswith('Using Tool:') and
                            not re.match(r'^[a-f0-9-]{36}$', line)):
                            meaningful_lines.append(line)

                    if meaningful_lines:
                        content = '\n'.join(meaningful_lines).strip()
                        if len(content) > 50:  # Only substantial content
                            self.conversations.append({
                                'agent': current_agent,
                                'message': content
                            })
                            current_agent = None

    def get_conversations(self):
        return self.conversations

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
            print("Executing crew.kickoff() with conversation capture...")
            with AgentConversationCapturer() as capturer:
                result = crew.kickoff()
            print(f"Crew kickoff completed. Result type: {type(result)}")

            conversations = capturer.get_conversations()
            print(f"Captured {len(conversations)} agent conversations")

            # Send both conversations and final result together
            await sio.emit('complete_result', {
                'conversations': conversations,
                'final_document': str(result)
            }, room=sid)
            print("Sent complete_result to frontend")

        except Exception as e:
            print(f"An error occurred during crew kickoff: {e}")
            import traceback
            traceback.print_exc()
            await sio.emit('error', {'message': str(e)}, room=sid)
    else:
        print(f"Invalid team selected: {team}")
        await sio.emit('error', {'message': 'Invalid team selected.'}, room=sid)