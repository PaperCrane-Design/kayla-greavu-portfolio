# AI-Powered Marketing Content Generator

This Streamlit app is the final web-application deliverable for the AI-powered marketing content generator project. It builds on the previous fine-tuning milestone by placing the model behind a user-friendly interface.

## What the app does

- Loads the provided vehicle/car datasets for sample product context.
- Lets the user select a vehicle or product row to enrich the marketing prompt.
- Collects business type, target audience, platform, tone, keywords, and call to action.
- Sends the structured prompt to the configured fine-tuned OpenAI model.
- Displays and downloads generated marketing copy.

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Set your model credentials:

```bash
export OPENAI_API_KEY="your_api_key"
export FINE_TUNED_MODEL="ft:gpt-4.1-mini-2025-04-14:YOUR-ORG:small-business-marketing:YOUR-ID"
```

Run the app:

```bash
streamlit run streamlit_app.py
```

## Files

- `streamlit_app.py` - Main Streamlit user interface.
- `marketing_generator.py` - Prompt-building and fine-tuned OpenAI model utilities.
- `requirements.txt` - Python dependencies.
- CSV data files should be placed in the same folder as the app.

## Responsible AI note

Generated copy should always be reviewed before publication for accuracy, bias, brand fit, privacy, and compliance.
