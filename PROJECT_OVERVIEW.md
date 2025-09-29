# Tata Communications AI Idea Generation Platform

A full-stack web application that leverages AI agent teams to collaboratively analyze and develop business ideas across different domains using CrewAI and OpenAI.

## Architecture Overview

### Backend (`backend/`)
- **Framework:** FastAPI with Socket.IO for real-time communication
- **AI Engine:** CrewAI framework with OpenAI GPT-3.5-turbo
- **Core Features:**
  - Three specialized AI agent crews: Product Management, Marketing, and HR
  - Real-time streaming of agent conversations via WebSocket
  - Sequential task execution with specialized agent roles

### Frontend (`frontend/`)
- **Framework:** React 19 with TypeScript
- **Styling:** TailwindCSS with Tata branding
- **Features:**
  - Three-step workflow interface
  - Real-time agent conversation streaming
  - Professional document presentation

## AI Agent Teams

### Product Management Crew
- **Product Manager:** Creates comprehensive PRDs
- **Market Research Analyst:** Analyzes market trends and competition
- **Lead Software Engineer:** Assesses technical feasibility
- **Product Designer:** Defines UX/UI requirements

### Marketing Crew
- **Marketing Manager:** Oversees marketing strategy
- **Content Strategist:** Develops content strategy
- **SEO Specialist:** Creates SEO optimization plans
- **Social Media Manager:** Designs social media campaigns

### HR Crew
- **HR Manager:** Manages HR policy development
- **Employee Relations Specialist:** Handles employee engagement
- **Legal Compliance Officer:** Ensures regulatory compliance
- **Talent Acquisition Specialist:** Develops recruitment strategies

## Technical Implementation

### Backend Components
- `main.py`: FastAPI server with Socket.IO integration
- `agents.py`: AI agent definitions with specialized roles
- `tasks.py`: Task creation functions for each crew type
- `crew.py`: Crew composition and workflow management

### Frontend Components
- `App.tsx`: Main application with three-tab interface
- Socket.IO client for real-time communication
- Responsive design with professional styling

## Current Status

### Working Features
- ✅ User idea submission with team selection
- ✅ AI agent crew creation and task execution
- ✅ Agent conversation collection and chat-style display
- ✅ Final document generation and display
- ✅ Professional UI with loading states and navigation
- ✅ Three-tab interface (Form → Conversation → Document)

### Technical Configuration
- **Python Version:** 3.13.5
- **CrewAI Version:** 0.201.1 (latest)
- **OpenAI Model:** GPT-3.5-turbo
- **Communication:** Socket.IO (non-streaming for complete results)
- **Frontend:** React 19 with TypeScript, TailwindCSS

### Recent Improvements (Latest Update)
- **Removed real-time streaming:** Changed from streaming agent conversations to displaying complete results after processing
- **Enhanced UX:** Added loading spinner and "AI Agents are Working..." message during processing
- **Chat-style conversation display:** Agent conversations now show as formatted chat messages with clear agent identification
- **Improved navigation:** Added navigation buttons between conversation and final document views
- **Better error handling:** Enhanced error states and user feedback

## Workflow Process

1. **Idea Submission:** User selects team type and submits business idea
2. **Loading State:** UI shows loading spinner while AI agents collaborate
3. **Agent Processing:** CrewAI creates specialized crew and executes sequential tasks
4. **Results Display:** Agent conversations and final document presented together
5. **Navigation:** Users can switch between conversation view and final document view

## Development Setup

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## Key Features

- **Multi-domain Expertise:** Specialized agent teams for different business contexts
- **Batch Processing:** AI agents collaborate and deliver complete results after processing
- **Chat-style Conversations:** Clear visualization of how different agents contributed to the final result
- **Professional Output:** Generate structured business documents (PRDs, marketing plans, HR policies)
- **Intuitive Navigation:** Three-tab interface for seamless workflow
- **Loading States:** Clear feedback during processing with professional loading indicators
- **Scalable Architecture:** Easy to add new agent teams and capabilities
- **Modern Tech Stack:** FastAPI, React 19, CrewAI 0.201.1, OpenAI integration

## Future Enhancements

- Additional agent teams (Finance, Legal, Operations)
- Document export functionality (PDF, Word)
- User authentication and project management
- Integration with additional AI models
- Advanced analytics and reporting