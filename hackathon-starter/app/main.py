from __future__ import annotations

import os
import random
from typing import List, Dict, Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

try:
	from openai import OpenAI
except Exception:  # pragma: no cover
	OpenAI = None  # type: ignore

APP_TITLE = "Hackathon Turbo"
DEFAULT_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

app = FastAPI(title=APP_TITLE)
app.mount("/static", StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(__file__), "templates"))


class BrainstormInput(BaseModel):
	domain: str
	constraints: str | None = None
	team_size: int | None = None
	time_limit_hours: int | None = None


class PitchInput(BaseModel):
	idea: str
	judging_criteria: str | None = None


class PlanInput(BaseModel):
	idea: str
	time_limit_hours: int = 24
	team_size: int = 3


# -------- AI helpers --------

def _get_openai_client() -> Any | None:
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key or not OpenAI:
		return None
	return OpenAI(api_key=api_key)


def _ai_generate(prompt: str, max_tokens: int = 800) -> str:
	client = _get_openai_client()
	if not client:
		return _local_generate(prompt)
	try:
		result = client.chat.completions.create(
			model=DEFAULT_MODEL,
			messages=[{"role": "system", "content": "You are a concise, practical hackathon mentor."},
					 {"role": "user", "content": prompt}],
			max_tokens=max_tokens,
			temperature=0.7,
		)
		return (result.choices[0].message.content or "").strip()
	except Exception:
		return _local_generate(prompt)


_LOCAL_IDEA_BANK = [
	"AI-powered resume coach for equitable tech hiring",
	"On-device health insights from smartwatch sensors with privacy-first ML",
	"Crowdsourced accessibility maps with AR navigation",
	"Realtime ESG transparency dashboard for small retailers",
	"Voice-to-UI automation for repetitive desktop workflows",
	"Micro-grants platform for local community projects",
]


def _local_generate(prompt: str) -> str:
	# Deterministic but varied fallback
	seed = sum(ord(c) for c in prompt) % 2**32
	random.seed(seed)
	ideas = random.sample(_LOCAL_IDEA_BANK, k=min(3, len(_LOCAL_IDEA_BANK)))
	if "brainstorm" in prompt.lower():
		return "\n".join(f"- {idea}" for idea in ideas)
	if "pitch" in prompt.lower():
		return (
			"Problem: People struggle with X.\n"
			"Solution: "+ ideas[0] + ".\n"
			"Why now: commodity LLMs + easy integrations.\n"
			"Demo: simple web app with real data.\n"
			"Impact: saves time, improves outcomes."
		)
	return "\n".join(f"- Milestone: {idea}" for idea in ideas)


# -------- Routes --------

@app.get("/health")
async def health() -> Dict[str, str]:
	return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
	return templates.TemplateResponse("index.html", {"request": request, "app_title": APP_TITLE})


@app.post("/api/brainstorm")
async def brainstorm(payload: BrainstormInput) -> JSONResponse:
	prompt = (
		f"Brainstorm 10 specific hackathon ideas in the domain: {payload.domain}. "
		f"Constraints: {payload.constraints or 'none'}. Team size: {payload.team_size or 'n/a'}. "
		f"Time limit: {payload.time_limit_hours or 'n/a'} hours."
	)
	text = _ai_generate("brainstorm ideas\n" + prompt)
	ideas = [line[2:].strip() for line in text.splitlines() if line.strip().startswith("-")]
	if not ideas:
		ideas = [line.strip() for line in text.splitlines() if line.strip()]
	return JSONResponse({"ideas": ideas[:10]})


@app.post("/api/pitch")
async def pitch(payload: PitchInput) -> JSONResponse:
	criteria = payload.judging_criteria or (
		"problem clarity, innovation, feasibility, impact, demo readiness"
	)
	prompt = (
		"Write a crisp 150-200 word pitch that covers problem, solution, uniqueness, why now, "
		f"tech stack, and impact. Optimize for judging criteria: {criteria}.\nIdea: {payload.idea}"
	)
	text = _ai_generate("pitch\n" + prompt, max_tokens=500)
	return JSONResponse({"pitch": text})


@app.post("/api/plan")
async def plan(payload: PlanInput) -> JSONResponse:
	prompt = (
		f"Create a 24-hour execution plan with milestones and tasks for the idea: {payload.idea}. "
		f"Team size: {payload.team_size}. Time limit: {payload.time_limit_hours} hours. "
		"Output two sections: 'Milestones' (5 items) and 'Tasks' (10-15 items)."
	)
	text = _ai_generate("plan\n" + prompt)
	milestones: List[str] = []
	tasks: List[str] = []
	current = None
	for line in text.splitlines():
		strip = line.strip()
		if not strip:
			continue
		lower = strip.lower()
		if lower.startswith("milestones"):
			current = "m"
			continue
		if lower.startswith("tasks"):
			current = "t"
			continue
		if strip.startswith("-"):
			if current == "m":
				milestones.append(strip[2:].strip())
			elif current == "t":
				tasks.append(strip[2:].strip())
	if not milestones and not tasks:
		# Fallback: split first few lines
		lines = [l.strip("- ") for l in text.splitlines() if l.strip()]
		milestones = lines[:5]
		tasks = lines[5:15]
	return JSONResponse({"milestones": milestones[:5], "tasks": tasks[:15]})