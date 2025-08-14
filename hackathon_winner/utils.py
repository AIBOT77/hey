import io
import json
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import pandas as pd
from openai import OpenAI
from pptx import Presentation
from pptx.enum.text import PP_PARAGRAPH_ALIGNMENT
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor


@dataclass
class SlideSpec:
	"""Specification for a single slide."""
	title: str
	bullets: List[str]
	notes: Optional[str] = None


def parse_brand_color(color_str: str) -> Tuple[int, int, int]:
	"""Parse brand color in hex like '#3366FF' or '3366FF' to RGB tuple."""
	if not color_str:
		return (51, 102, 255)  # Default blue
	c = color_str.strip().lstrip('#')
	if len(c) != 6:
		return (51, 102, 255)
	try:
		return tuple(int(c[i:i+2], 16) for i in (0, 2, 4))  # type: ignore[return-value]
	except Exception:
		return (51, 102, 255)


def _openai_client() -> OpenAI:
	api_key = os.getenv("OPENAI_API_KEY")
	if not api_key:
		raise RuntimeError("OPENAI_API_KEY is not set in environment")
	return OpenAI(api_key=api_key)


def generate_pitch_outline(
	problem_statement: str,
	audience: str,
	tone: str,
	num_slides: int = 8,
) -> List[SlideSpec]:
	"""Use OpenAI to generate a JSON outline for a pitch deck."""
	client = _openai_client()
	system = (
		"You are an expert startup storyteller. Produce a tight, high-signal pitch deck outline as JSON. "
		"Focus on clarity, persuasion, and concrete traction or plan."
	)
	user = (
		f"Problem: {problem_statement}\n"
		f"Audience: {audience}\n"
		f"Tone: {tone}\n"
		f"Slides: {num_slides}\n"
		"Return JSON with 'slides': [ { 'title': str, 'bullets': [str...], 'notes': str? } ]."
	)
	resp = client.chat.completions.create(
		model="gpt-4o-mini",
		messages=[
			{"role": "system", "content": system},
			{"role": "user", "content": user},
		],
		temperature=0.5,
		response_format={"type": "json_object"},
	)
	content = resp.choices[0].message.content or "{}"
	try:
		parsed: Dict = json.loads(content)
	except json.JSONDecodeError:
		parsed = {"slides": []}
	slides: List[SlideSpec] = []
	for s in parsed.get("slides", [])[:num_slides]:
		title = str(s.get("title", "Slide"))
		bullets = [str(b) for b in s.get("bullets", [])]
		notes = s.get("notes")
		slides.append(SlideSpec(title=title, bullets=bullets, notes=notes))
	if not slides:
		# Fallback minimal deck
		slides = [
			SlideSpec(title="Problem", bullets=[problem_statement[:120]]),
			SlideSpec(title="Solution", bullets=["AI-powered app", "Clear value prop"]),
			SlideSpec(title="Market", bullets=["Target users", "Size", "Why now"]),
			SlideSpec(title="Traction", bullets=["Prototype", "Early users", "KPIs"]),
		]
	return slides


def create_charts_from_dataframe(df: pd.DataFrame, max_charts: int = 2) -> List[io.BytesIO]:
	"""Create simple charts from uploaded CSV and return images as byte streams."""
	charts: List[io.BytesIO] = []
	if df.empty:
		return charts
	numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
	if len(numeric_cols) < 1:
		return charts
	# Chart 1: line plot of first numeric column
	col = numeric_cols[0]
	fig, ax = plt.subplots(figsize=(6, 4))
	df[col].plot(ax=ax)
	ax.set_title(f"Trend of {col}")
	ax.grid(True, alpha=0.3)
	buf1 = io.BytesIO()
	fig.savefig(buf1, format="png", bbox_inches="tight")
	plt.close(fig)
	buf1.seek(0)
	charts.append(buf1)
	# Chart 2: if available, bar plot of top categories by sum of second numeric vs first categorical
	if len(numeric_cols) >= 2:
		second = numeric_cols[1]
		cat_cols = [c for c in df.columns if c not in numeric_cols]
		if cat_cols:
			cat = cat_cols[0]
			agg = df.groupby(cat)[second].sum().sort_values(ascending=False).head(8)
			fig2, ax2 = plt.subplots(figsize=(6, 4))
			agg.plot(kind="bar", ax=ax2)
			ax2.set_title(f"{second} by {cat}")
			ax2.grid(True, axis="y", alpha=0.3)
			buf2 = io.BytesIO()
			fig2.savefig(buf2, format="png", bbox_inches="tight")
			plt.close(fig2)
			buf2.seek(0)
			charts.append(buf2)
	return charts


def build_pptx(
	slides: List[SlideSpec],
	brand_rgb: Tuple[int, int, int],
	charts: Optional[List[io.BytesIO]] = None,
	logo_image: Optional[bytes] = None,
	brand_font: str = "Arial",
) -> bytes:
	"""Build a PPTX in-memory from slides and optional charts."""
	prs = Presentation()
	# Adjust slide size to 16:9 default already; keep defaults
	for index, spec in enumerate(slides, start=1):
		layout = prs.slide_layouts[1]  # Title and Content
		slide = prs.slides.add_slide(layout)
		title = slide.shapes.title
		title.text = spec.title
		title.text_frame.paragraphs[0].font.size = Pt(40)
		title.text_frame.paragraphs[0].font.bold = True
		# Brand title color
		title.text_frame.paragraphs[0].font.color.rgb = RGBColor(*brand_rgb)
		body = slide.placeholders[1].text_frame
		# Clear default
		body.clear()
		for b in spec.bullets[:8]:
			p = body.add_paragraph()
			p.text = b
			p.level = 0
			p.font.size = Pt(20)
			p.font.name = brand_font
		# Notes as subtle footer
		if spec.notes:
			left = Inches(0.5)
			top = Inches(6.5)
			width = Inches(9)
			height = Inches(0.6)
			textbox = slide.shapes.add_textbox(left, top, width, height)
			p = textbox.text_frame.paragraphs[0]
			p.text = spec.notes
			p.font.size = Pt(12)
			p.font.color.rgb = RGBColor(120, 120, 120)
			p.alignment = PP_PARAGRAPH_ALIGNMENT.LEFT
		# Optional logo
		if logo_image:
			left = Inches(9)
			top = Inches(0.2)
			stream = io.BytesIO(logo_image)
			stream.seek(0)
			slide.shapes.add_picture(stream, left, top, height=Inches(0.6))
	# Append chart slides
	if charts:
		for idx, chart_stream in enumerate(charts, start=1):
			layout = prs.slide_layouts[5]  # Title Only
			slide = prs.slides.add_slide(layout)
			slide.shapes.title.text = f"Chart {idx}"
			left = Inches(0.5)
			top = Inches(1.2)
			width = Inches(9.0)
			height = Inches(5.5)
			chart_stream.seek(0)
			slide.shapes.add_picture(chart_stream, left, top, width=width, height=height)
	# Save to bytes
	buf = io.BytesIO()
	prs.save(buf)
	buf.seek(0)
	return buf.read()