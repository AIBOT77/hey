import io
import os
from typing import Optional

import pandas as pd
import streamlit as st

from utils import (
	SlideSpec,
	build_pptx,
	create_charts_from_dataframe,
	generate_pitch_outline,
	parse_brand_color,
)


st.set_page_config(page_title="Pitch Deck Generator", page_icon="🚀", layout="wide")

st.title("🚀 Hackathon Pitch Deck Generator")

with st.sidebar:
	st.header("Settings")
	api_status = "✅" if os.getenv("OPENAI_API_KEY") else "⚠️ Set OPENAI_API_KEY"
	st.caption(f"OpenAI: {api_status}")
	audience = st.text_input("Audience", value="General tech judges")
	tone = st.selectbox("Tone", ["Confident", "Visionary", "Pragmatic", "Playful"], index=0)
	num_slides = st.slider("Number of slides", 5, 12, 8)
	brand_color = st.text_input("Brand color (hex)", value="#3366FF")
	brand_font = st.text_input("Brand font", value="Arial")
	logo_file = st.file_uploader("Logo (optional)", type=["png", "jpg", "jpeg"])

col1, col2 = st.columns([3, 2])
with col1:
	problem = st.text_area(
		"Your idea / problem statement",
		height=160,
		placeholder=(
			"Describe the problem, your solution, and what's unique. "
			"Include any traction or plan you have."
		),
	)
	csv_file = st.file_uploader("Upload CSV for charts (optional)", type=["csv"])
	go = st.button("Generate deck", type="primary")

with col2:
	st.markdown("### Tips")
	st.write(
		"- Keep the problem crisp.\n"
		"- Add 1-2 proof points (users, signups, retention, insight).\n"
		"- Judges love clarity: what, who, why now, how big, why you."
	)

if go:
	if not problem.strip():
		st.error("Please enter your idea/problem statement.")
		st.stop()
	with st.spinner("Thinking through your story..."):
		try:
			slides = generate_pitch_outline(problem, audience, tone, num_slides)
		except Exception as e:
			st.error(f"OpenAI error: {e}")
			st.stop()
		st.success("Outline ready")
		st.markdown("### Outline preview")
		for idx, s in enumerate(slides, start=1):
			st.markdown(f"**{idx}. {s.title}**")
			for b in s.bullets[:5]:
				st.write(f"- {b}")
			if s.notes:
				st.caption(s.notes)
			st.divider()
		# Load CSV and make charts
		charts = None
		if csv_file is not None:
			try:
				df = pd.read_csv(csv_file)
				charts = create_charts_from_dataframe(df)
				st.info(f"Included {len(charts)} chart(s) from CSV")
			except Exception as e:
				st.warning(f"CSV issue: {e}")
		brand_rgb = parse_brand_color(brand_color)
		logo_bytes: Optional[bytes] = logo_file.read() if logo_file else None
		with st.spinner("Composing your slides..."):
			pptx_bytes = build_pptx(slides, brand_rgb=brand_rgb, charts=charts, logo_image=logo_bytes, brand_font=brand_font)
		st.success("Deck ready!")
		st.download_button(
			label="Download PPTX",
			data=pptx_bytes,
			file_name="pitch_deck.ai.pptx",
			mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
		)

st.caption("Built fast for hackathons ✨")