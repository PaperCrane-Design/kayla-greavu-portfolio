"""Streamlit front end for the DSC670/DSC680 final AI marketing project.

Run locally:
    streamlit run streamlit_app.py

Required for real model output:
    export OPENAI_API_KEY="your_key"
    export FINE_TUNED_MODEL="ft:gpt-4.1-mini-2025-04-14:..."
"""
from __future__ import annotations

from pathlib import Path
from typing import Dict, Optional

import pandas as pd
import plotly.express as px
import streamlit as st

from marketing_generator import (
    MarketingRequest,
    build_product_context,
    generate_with_fine_tuned_model,
    get_model_name,
)

APP_DIR = Path(__file__).parent
DATA_FILES = {
    "Vehicle MSRP data": APP_DIR / "data.csv",
    "Car sales data": APP_DIR / "Car_sales.csv",
    "Automobile MPG data": APP_DIR / "Automobile.csv",
    "Car price prediction data": APP_DIR / "car_price_prediction_.csv",
}

st.set_page_config(
    page_title="AI Marketing Content Generator",
    page_icon="📣",
    layout="wide",
)


@st.cache_data(show_spinner=False)
def load_csv(path: Path) -> pd.DataFrame:
    return pd.read_csv(path)


def clean_label(value: object) -> str:
    if pd.isna(value):
        return ""
    return str(value).strip()


def dataset_selector() -> tuple[str, pd.DataFrame]:
    available = {name: path for name, path in DATA_FILES.items() if path.exists()}
    if not available:
        st.warning("No project CSV files were found beside the app. Upload a CSV to continue.")
        uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded is None:
            return "Uploaded data", pd.DataFrame()
        return uploaded.name, pd.read_csv(uploaded)

    dataset_name = st.selectbox("Choose a project dataset", list(available.keys()))
    return dataset_name, load_csv(available[dataset_name])


def show_dataset_summary(dataset_name: str, df: pd.DataFrame) -> Optional[Dict[str, object]]:
    st.subheader("1. Explore the project data")
    if df.empty:
        return None

    metric_cols = st.columns(4)
    metric_cols[0].metric("Rows", f"{len(df):,}")
    metric_cols[1].metric("Columns", f"{len(df.columns):,}")
    metric_cols[2].metric("Missing cells", f"{int(df.isna().sum().sum()):,}")
    metric_cols[3].metric("Dataset", dataset_name)

    with st.expander("Preview data", expanded=False):
        st.dataframe(df.head(50), use_container_width=True)

    selected_row = None
    label_cols = [col for col in ["Make", "Brand", "Manufacturer", "name"] if col in df.columns]
    model_cols = [col for col in ["Model", "name"] if col in df.columns]

    st.markdown("#### Select a vehicle/product example to include in the marketing prompt")
    if label_cols or model_cols:
        label_col = label_cols[0] if label_cols else model_cols[0]
        options = df.index[: min(len(df), 500)].tolist()

        def option_label(idx: int) -> str:
            row = df.loc[idx]
            label = clean_label(row.get(label_col, "Vehicle"))
            model = clean_label(row.get(model_cols[0], "")) if model_cols else ""
            year = clean_label(row.get("Year", row.get("model_year", "")))
            return " | ".join([part for part in [label, model, year] if part]) or f"Row {idx}"

        row_idx = st.selectbox("Product example", options, format_func=option_label)
        selected_row = df.loc[row_idx].to_dict()
        st.info(build_product_context(selected_row))

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    if len(numeric_cols) >= 1:
        st.markdown("#### Quick visual")
        x_candidates = [col for col in ["Year", "model_year", "Make", "Brand", "Manufacturer", "Vehicle_type"] if col in df.columns]
        y_default = "MSRP" if "MSRP" in numeric_cols else ("Price" if "Price" in numeric_cols else numeric_cols[0])
        y_col = st.selectbox("Metric to chart", numeric_cols, index=numeric_cols.index(y_default))
        if x_candidates:
            x_col = st.selectbox("Group by", x_candidates)
            chart_df = df[[x_col, y_col]].dropna()
            if not chart_df.empty:
                if chart_df[x_col].nunique() > 25:
                    chart_df = chart_df.groupby(x_col, as_index=False)[y_col].mean().sort_values(y_col, ascending=False).head(20)
                else:
                    chart_df = chart_df.groupby(x_col, as_index=False)[y_col].mean().sort_values(y_col, ascending=False)
                fig = px.bar(chart_df, x=x_col, y=y_col, title=f"Average {y_col} by {x_col}")
                st.plotly_chart(fig, use_container_width=True)

    return selected_row


def show_generator_form(product_context: str) -> None:
    st.subheader("2. Generate marketing copy with the fine-tuned model")
    model_name = get_model_name()
    st.caption(f"Configured model: `{model_name}`")

    with st.form("marketing_form"):
        col1, col2 = st.columns(2)
        with col1:
            business_type = st.text_input("Business type", "local car dealership")
            audience = st.text_input("Target audience", "local shoppers comparing reliable vehicles")
            platform = st.selectbox(
                "Platform",
                ["Facebook", "Instagram", "Google Ad", "Website copy", "Email newsletter", "TikTok caption"],
            )
            tone = st.selectbox("Tone", ["friendly", "professional", "confident", "helpful", "warm and cheerful"])
        with col2:
            keywords = st.text_area(
                "Keywords",
                "reliable cars, fair pricing, fuel efficiency, local dealership",
                height=100,
            )
            task = st.selectbox(
                "Content task",
                [
                    "Create one social media post with a call to action.",
                    "Write a short promotional email.",
                    "Create a Google ad headline and description.",
                    "Write homepage hero copy.",
                    "Create three caption options.",
                ],
            )
            call_to_action = st.text_input("Call to action", "Schedule a test drive today")
            length = st.radio("Length", ["Short", "Medium", "Detailed"], horizontal=True)

        st.text_area("Dataset/product context sent to the model", product_context, height=100, disabled=True)
        submitted = st.form_submit_button("Generate marketing copy", type="primary")

    if submitted:
        request = MarketingRequest(
            business_type=business_type,
            audience=audience,
            platform=platform,
            tone=tone,
            keywords=keywords,
            task=task,
            product_context=product_context,
            call_to_action=call_to_action,
            length=length,
        )
        with st.spinner("Generating content..."):
            output = generate_with_fine_tuned_model(request)
        st.markdown("### Generated marketing copy")
        st.success(output)
        st.download_button(
            "Download generated copy",
            data=output,
            file_name="generated_marketing_copy.txt",
            mime="text/plain",
        )


def show_about() -> None:
    st.sidebar.title("Project controls")
    st.sidebar.markdown(
        "This app turns structured business inputs and optional vehicle dataset details "
        "into marketing copy using the fine-tuned small-business marketing model."
    )
    st.sidebar.markdown("**Setup for final submission**")
    st.sidebar.code("OPENAI_API_KEY=...\nFINE_TUNED_MODEL=ft:gpt-4.1-mini-...", language="bash")


def main() -> None:
    show_about()
    st.title("📣 AI-Powered Marketing Content Generator")
    st.write(
        "A Streamlit application that builds on the fine-tuned OpenAI marketing model "
        "from the previous milestone and surfaces it as a portfolio-ready web app."
    )

    dataset_name, df = dataset_selector()
    selected_row = show_dataset_summary(dataset_name, df)
    product_context = build_product_context(selected_row)
    show_generator_form(product_context)

    st.markdown("---")
    st.caption(
        "Responsible AI note: Users should review generated copy for accuracy, bias, "
        "brand fit, and legal/compliance requirements before publishing."
    )


if __name__ == "__main__":
    main()
