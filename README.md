# Architectural Design Assistant

It is a full-stack, AI-powered creative tool designed to support architects and engineers during the early design phase. The system transforms textual briefs and rough sketches into refined architectural concepts, while also providing design narratives and basic compliance insights.
The project focuses on practical system design, clean separation of concerns, and scalable AI integration, rather than attempting to over-engineer prematurely.

#**Problem Statement**
Architectural concept design is traditionally:
Time-consuming,
Highly iterative,
Dependent on manual interpretation of vague briefs and sketches,
Difficult to validate early against design constraints and codes

The objective of this project is to:
Reduce iteration time in early-stage design,
Assist creativity rather than replace human designers,
Provide structured AI feedback grounded in architectural reasoning,
Enable rapid experimentation with design alternatives

## Features

### Frontend
- React interface with drawing tools
- Interactive sketch input and annotation
- 3D design preview and manipulation
- Design iteration and version control
- User authentication and project management

### Backend
- FastAPI with architectural project management
- SQLite/PostgreSQL for design data and user projects
- Image processing pipeline for sketch analysis
- Integration with design reference databases
- JWT authentication with OAuth support structure

### AI Integration
- GPT-4V/Gemini integration structure (mock mode available)
- Design concept generation
- Code compliance checking AI
- Design narrative generation

## Setup Instructions
### Backend Setup
1. Navigate to the backend directory:
```bash
cd backend
```
2. Create a virtual environment (if not already created):
```bash
python -m venv venv
```
3. Activate the virtual environment:
- Windows:
```bash
venv\Scripts\activate
```
- Linux/Mac:
```bash
source venv/bin/activate
```
4. Install dependencies:
```bash
pip install -r requirements.txt
```
5. Create a `.env` file in the backend directory (optional, defaults are provided):
```env
DATABASE_URL=sqlite:///./architect.db
SECRET_KEY=your-secret-key-change-in-production
OPENAI_API_KEY=your-openai-api-key-here
LLM_MODE=mock
```
6. Run the backend server:
```bash
uvicorn app.main:app --reload --port 8000
```
The API will be available at `http://localhost:8000`
API documentation: `http://localhost:8000/docs`

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd architectural-assistant
```
2. Install dependencies:
```bash
npm install
```
3. Start the development server:
```bash
npm start
```
The frontend will be available at `http://localhost:3000`

## Usage

1. **Register/Login**: Create an account or login with existing credentials
2. **Create Project**: Click "New Project" to create a new architectural project
3. **Enter Brief**: Enter your design requirements in the text area
4. **Sketch (Optional)**: Draw a rough sketch using the canvas
5. **Generate Design**: Click "Generate Design" to get AI-generated design concepts
6. **Review**: View the design narrative, compliance notes, and 3D preview

## API Endpoints

### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `POST /auth/login/json` - Login with JSON body
- `GET /auth/me` - Get current user info

### Projects
- `GET /projects/` - List user projects
- `POST /projects/` - Create new project
- `GET /projects/{id}` - Get project details
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project
- `POST /projects/{id}/sketch` - Save sketch data

### AI
- `POST /ai/generate_design` - Generate design from brief and sketch
- `POST /ai/generate_design/form` - Generate design (form data)
- `POST /ai/ask` - Ask AI questions

## Configuration

### Backend Environment Variables
- `DATABASE_URL`: Database connection string (default: SQLite)
- `SECRET_KEY`: JWT secret key
- `OPENAI_API_KEY`: OpenAI API key (optional, for real AI features)
- `LLM_MODE`: "mock" or "openai" (default: "mock")
- `EMBEDDING_MODE`: "mock" or "openai" (default: "mock")
- `CORS_ORIGINS`: Comma-separated list of allowed origins

### Mock Mode
The application runs in "mock" mode by default, which means:
- No external API calls are made
- Design generation returns sample responses
- Perfect for development and testing
- No API keys required

To enable real AI features, set `LLM_MODE=openai` and provide an `OPENAI_API_KEY`.

## Project Structure

```
.
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── core/         # Core configuration
│   │   ├── models/       # Database models
│   │   ├── schemas/      # Pydantic schemas
│   │   ├── ai/           # AI services and agents
│   │   └── main.py       # FastAPI application
│   ├── requirements.txt
│   └── .env
├── architectural-assistant/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   └── App.tsx       # Main app component
│   └── package.json
└── README.md
```

## Development

### Running Both Servers

You can run both servers simultaneously:

**Terminal 1 (Backend):**
```bash
cd backend
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # Linux/Mac
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 (Frontend):**
```bash
cd architectural-assistant
npm start
```


## Troubleshooting

1. **CORS Errors**: Make sure the backend CORS_ORIGINS includes your frontend URL
2. **Database Errors**: Ensure the database file has write permissions (SQLite) or database is accessible (PostgreSQL)
3. **Authentication Errors**: Check that SECRET_KEY is set in backend/.env
4. **AI Generation Fails**: In mock mode, this should work. For real AI, ensure OPENAI_API_KEY is set

## Key Assumptions

Given the open-ended nature of the assignment, the following assumptions were made:
1. Early-stage design assistance is more valuable than final construction drawings.
2. Sketch inputs are conceptual, not CAD-accurate.
3. Code compliance checking is advisory, not legally binding.
4. Real-time collaboration and GPU-heavy features are future extensions, not MVP blockers.
5. AI models may evolve; the system should be model-agnostic

## Future Enhancements

- Full OAuth implementation (Google/GitHub)
- Real-time collaboration with SSE
- Advanced 3D model loading
- Image processing for sketch analysis
- Docker deployment with GPU support
- Advanced compliance checking
- Design version history

## License

MIT

