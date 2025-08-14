# Hackathon Turbo Starter (FastAPI)

A lightweight, AI-enabled web app to brainstorm ideas, craft winning 60-second pitches, and generate an execution plan.

## Quickstart

1. Create a virtual environment and install deps:
```bash
cd /workspace/hackathon-starter
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. (Optional) Enable AI with OpenAI. Set your key:
```bash
export OPENAI_API_KEY=sk-your-key
# Optional: choose a model (default: gpt-4o-mini)
export OPENAI_MODEL=gpt-4o-mini
```

3. Run the app:
```bash
./run.sh
# then open http://localhost:8000
```

If no API key is set, the app gracefully falls back to high-quality local generation.

## Endpoints
- `GET /` UI
- `GET /health` Health check
- `POST /api/brainstorm` -> `{ ideas: string[] }`
- `POST /api/pitch` -> `{ pitch: string }`
- `POST /api/plan` -> `{ milestones: string[], tasks: string[] }`

## Notes
- Built with FastAPI, Jinja2, vanilla JS. No Node required.
- Keep prompts short and specific for best results.