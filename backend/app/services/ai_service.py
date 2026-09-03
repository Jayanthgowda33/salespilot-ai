"""
This is the brain of the product. Every AI feature funnels through
this one file: lead scoring, meeting summarization, sentiment
analysis, follow-up email drafting, and next-action recommendation.

For the MVP we call Anthropic's Claude API directly with a plain
prompt and ask it to return JSON. Once this works, this is exactly
where you would swap in LangGraph (for multi-step agent reasoning)
and pgvector/RAG (to give the model the lead's full history instead
of just one message) without touching any other part of the app.
"""

import json
import httpx

from app.config import settings

ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"
MODEL = "claude-sonnet-5"


async def _call_claude(prompt: str) -> str:
    headers = {
        "x-api-key": settings.ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": MODEL,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}],
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(ANTHROPIC_URL, headers=headers, json=payload)
        if response.status_code != 200:
            print("ANTHROPIC API ERROR:", response.status_code, response.text)
        response.raise_for_status()
        data = response.json()
        return data["content"][0]["text"]


async def score_lead(lead_data: dict, activities: list[str]) -> dict:
    """
    Looks at a lead's details plus their activity history (emails,
    calls, meeting notes) and returns a score, a short summary,
    a deal probability, and a recommended next action — all in one
    call, to keep AI cost and latency low.
    """
    activity_text = "\n".join(f"- {a}" for a in activities) or "No activity logged yet."

    prompt = f"""You are a B2B sales intelligence assistant. Analyze this lead and
return ONLY valid JSON, no other text, no markdown fences.

Lead details:
Name: {lead_data.get('name')}
Company: {lead_data.get('company_name')}
Source: {lead_data.get('source')}
Status: {lead_data.get('status')}

Recent activity:
{activity_text}

Return JSON in exactly this shape:
{{
  "score": <integer 0-100, how promising this lead is>,
  "summary": "<one or two sentence summary of where things stand>",
  "deal_probability": <float 0.0-1.0>,
  "next_best_action": "<one concrete, specific action the rep should take next>"
}}"""

    raw = await _call_claude(prompt)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


async def summarize_meeting(transcript: str) -> dict:
    prompt = f"""Summarize this sales call/meeting transcript. Return ONLY valid JSON,
no markdown fences.

Transcript:
{transcript}

Return JSON in exactly this shape:
{{
  "summary": "<3-4 sentence summary>",
  "sentiment": "<positive, neutral, or negative>",
  "key_points": ["<point 1>", "<point 2>"]
}}"""
    raw = await _call_claude(prompt)
    raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


async def generate_follow_up_email(lead_data: dict, context: str) -> str:
    prompt = f"""Write a short, friendly, professional follow-up sales email to
{lead_data.get('name')} at {lead_data.get('company_name')}.
Context: {context}
Keep it under 120 words. Return only the email body, no subject line, no extra text."""
    return await _call_claude(prompt)
