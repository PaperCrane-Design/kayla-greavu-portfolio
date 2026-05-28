"""Utilities for the AI-powered marketing content Streamlit app.

This module keeps OpenAI/fine-tuned-model calls separate from the UI so the
application is easier to test, reuse, and explain in a portfolio repository.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Dict, Optional


SYSTEM_MESSAGE = (
    "You are a helpful marketing content assistant for small businesses. "
    "Create clear, practical, brand-safe marketing copy. Use the requested "
    "platform, tone, target audience, and keywords. Keep the content specific, "
    "friendly, and easy for a small business owner to edit."
)

DEFAULT_MODEL_PLACEHOLDER = "ft:gpt-4.1-mini-2025-04-14:YOUR-ORG:small-business-marketing:YOUR-ID"


@dataclass
class MarketingRequest:
    """Structured information passed from Streamlit to the content generator."""

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
        """Convert the request into the same structured style used for fine-tuning."""
        return (
            f"Business type: {self.business_type}\n"
            f"Target audience: {self.audience}\n"
            f"Platform: {self.platform}\n"
            f"Tone: {self.tone}\n"
            f"Keywords: {self.keywords}\n"
            f"Desired length: {self.length}\n"
            f"Call to action: {self.call_to_action}\n"
            f"Product or dataset context: {self.product_context}\n"
            f"Task: {self.task}"
        )


def get_model_name() -> str:
    """Return the configured fine-tuned model name.

    For the submitted class project, set this in Streamlit secrets or as an
    environment variable named FINE_TUNED_MODEL. The placeholder reminds the
    student where to paste the final model name from the OpenAI dashboard.
    """
    return os.getenv("FINE_TUNED_MODEL", DEFAULT_MODEL_PLACEHOLDER)


def generate_with_fine_tuned_model(request: MarketingRequest, model_name: Optional[str] = None) -> str:
    """Generate marketing copy with the configured OpenAI fine-tuned model.

    If credentials/model configuration are missing, the function returns a local
    demo response so the Streamlit app can still be previewed and screenshotted.
    This fallback should be replaced by real fine-tuned output for final grading.
    """
    model_name = model_name or get_model_name()
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key or "YOUR-" in model_name:
        return demo_marketing_copy(request, model_name)

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model=model_name,
            input=[
                {"role": "system", "content": SYSTEM_MESSAGE},
                {"role": "user", "content": request.to_prompt()},
            ],
            temperature=0.7,
            max_output_tokens=500,
        )
        return response.output_text.strip()
    except Exception as exc:  # pragma: no cover - shown in UI instead
        return (
            "The app could not reach the fine-tuned OpenAI model. "
            "Check OPENAI_API_KEY and FINE_TUNED_MODEL, then rerun.\n\n"
            f"Technical message: {exc}"
        )


def demo_marketing_copy(request: MarketingRequest, model_name: str) -> str:
    """Local placeholder output for app previews without OpenAI credentials."""
    cta = request.call_to_action.strip() or "Visit us today to learn more."
    context_sentence = f" Highlight: {request.product_context.strip()}" if request.product_context.strip() else ""
    return (
        f"Demo output using configured model placeholder `{model_name}`.\n\n"
        f"{request.business_type.title()} customers deserve simple, helpful information before they buy. "
        f"For {request.audience}, this {request.platform.lower()} uses a {request.tone.lower()} tone "
        f"to spotlight {request.keywords or 'the business value'}.{context_sentence}\n\n"
        f"Ready for a better experience? {cta}\n\n"
        "Suggested hashtags: #SmallBusiness #LocalMarketing #CustomerFirst"
    )


def build_product_context(row: Optional[Dict[str, object]]) -> str:
    """Create a readable product description from a selected dataset row."""
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
