import streamlit as st
import pandas as pd
import os
from langchain_community.chat_models import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent

# Load your GROQ API key from environment variable or Streamlit secret
GROQ_API_KEY = "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"

# Load Excel files
@st.cache_data
def load_data():
    onboarding = pd.read_excel("OC Onboarding Information.xlsx", sheet_name=None)
    report = pd.read_excel("The Alex Ideas Report.xlsx", sheet_name=None)
    return onboarding, report

# Combine relevant sheets into one DataFrame per file
def combine_onboarding_data(onboarding_sheets):
    frames = []
    for sheet_name, df in onboarding_sheets.items():
        df['Sheet'] = sheet_name
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

def combine_report_data(report_sheets):
    frames = []
    for sheet_name, df in report_sheets.items():
        df['Sheet'] = sheet_name
        frames.append(df)
    return pd.concat(frames, ignore_index=True)

# Main app
def main():
    st.set_page_config(page_title="Revenue & Occupancy Agent", layout="wide")
    st.title("📊 Revenue & Occupancy AI Agent")

    # Load data
    onboarding_sheets, report_sheets = load_data()
    onboarding_df = combine_onboarding_data(onboarding_sheets)
    report_df = combine_report_data(report_sheets)

    st.sidebar.header("Data Preview")
    if st.sidebar.checkbox("Show OC Onboarding Data"):
        st.dataframe(onboarding_df.head(50))
    if st.sidebar.checkbox("Show Ideas Report Data"):
        st.dataframe(report_df.head(50))

    # Create Groq agent
    if not GROQ_API_KEY:
        st.error("Missing API key. Please set GROQ_API_KEY in your environment or Streamlit secrets.")
        return

    st.info("Loading AI agent...", icon="💡")
    llm = ChatOpenAI(
        # api_key=GROQ_API_KEY,
                     openai_api_key=GROQ_API_KEY,
                     openai_api_base="https://api.groq.com/openai/v1",
                      model_name="deepseek-r1-distill-llama-70b")

    st.success("AI Agent Ready ✅")

    agent = create_pandas_dataframe_agent(
        llm,
        [onboarding_df, report_df],
        verbose=True,
        handle_parsing_errors=True,
        allow_dangerous_code=True 
    )

    # Question input
    user_question = st.text_input("Ask a question about revenue or occupancy:", 
                                  placeholder="e.g., What is the OTB revenue for August vs STLY?")
    if user_question:
        with st.spinner("Thinking..."):
            try:
                response = agent.run(user_question)
                st.markdown("### ✅ Answer")
                st.success(response)
            except Exception as e:
                st.error(f"Error: {str(e)}")


if __name__ == "__main__":
    main()
