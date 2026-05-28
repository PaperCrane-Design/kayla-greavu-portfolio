"""Utilities for the AI-powered marketing content Streamlit app."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional

from dotenv import load_dotenv

load_dotenv()

SYSTEM_MESSAGE = (
    "You are a professional marketing copywriter for small businesses. "
    "Write natural, engaging, human-sounding marketing content tailored to the requested platform. "
    "Do not list raw dataset fields or technical labels. "
    "Turn product details into persuasive and conversational marketing language. "
    "Match the requested tone and audience. "
    "Include a clear call to action and relevant hashtags when appropriate."
)

DEFAULT_MODEL = "gpt-4.1-mini"


@dataclass
class MarketingRequest:
    business_type: str
    audience: str
    platform: str
    tone: str
    keywords: str
    task: str
    product_context: str = ""
    call_to_action: str = ""
    length: str = "Short"

    def to_prompt(self) -> str:
        return f"""
Create realistic marketing content.

Business Type:
{self.business_type}

Target Audience:
{self.audience}

Platform:
{self.platform}

Tone:
{self.tone}

Keywords to include naturally:
{self.keywords}

Desired Length:
{self.length}

Call To Action:
{self.call_to_action}

Task:
{self.task}

Product Information:
{self.product_context}

Instructions:
- Make the content sound natural and human.
- Do not copy raw labels like "Engine HP", "MSRP", "Transmission Type", or "Vehicle Style".
- Turn product details into appealing customer benefits.
- Match the style to the selected platform.
- For Facebook, write like a real local business post.
- Include light emojis only if they fit naturally.
- Include 2 to 4 relevant hashtags if appropriate.
"""


def get_model_name() -> str:
    return os.getenv("FINE_TUNED_MODEL", DEFAULT_MODEL)


def generate_with_fine_tuned_model(
    request: MarketingRequest,
    model_name: Optional[str] = None,
) -> str:
    model_name = model_name or get_model_name()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return (
            "Missing OpenAI API key. Please add OPENAI_API_KEY to your .env file "
            "and restart the Streamlit app."
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)

        response = client.responses.create(
            model=model_name,
            input=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": request.to_prompt()},
            ],
            temperature=0.8,
            max_output_tokens=500,
        )

        return response.output_text.strip()

    except Exception as exc:
        return (
            "The app could not reach the OpenAI model. "
            "Check your OPENAI_API_KEY, FINE_TUNED_MODEL, and internet connection.\n\n"
            f"Technical message: {exc}"
        )


def build_product_context(row: Optional[Dict[str, object]]) -> str:
    if not row:
        return ""

    preferred_fields = [
        "Make",
        "Brand",
        "Manufacturer",
        "Model",
        "Year",
        "Vehicle Style",
        "Vehicle Size",
        "Engine Fuel Type",
        "Fuel Type",
        "Transmission Type",
        "Transmission",
        "Engine HP",
        "Horsepower",
        "highway MPG",
        "city mpg",
        "Fuel_efficiency",
        "Mileage",
        "Condition",
        "MSRP",
        "Price",
        "Price_in_thousands",
    ]

    parts = []

    for field in preferred_fields:
        value = row.get(field)

        if value is not None and str(value).strip() and str(value).lower() != "nan":
            parts.append(f"{field}: {value}")

    return "; ".join(parts[:14])
