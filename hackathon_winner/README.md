# Hackathon Pitch Deck Generator

An AI-powered Streamlit app that turns your problem statement into a polished pitch deck (PPTX) with optional data-driven charts.

## Quickstart

1. Export your OpenAI key:
```bash
export OPENAI_API_KEY=sk-your-key
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py --server.headless true --server.port 7860
```

4. In the UI, enter your idea, audience, and tone. Optionally upload a CSV for charts, choose a brand color, and click Generate.

## Notes
- Exports a `.pptx` you can download and present.
- Works great for hackathon demos and investor pitches.