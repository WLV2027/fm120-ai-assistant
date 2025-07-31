import openai
import streamlit as st
import pandas as pd

# Set your OpenAI API key
api_key = st.secrets["OPENAI_API_KEY"]
client = openai.OpenAI(api_key=api_key)

# Core function to generate responses
def get_response(input_text, mode):
    if mode == "Feedback":
        prompt = f"""You are an FM120 TA. Evaluate this student answer and explain any conceptual errors using clear language:
Answer: {input_text}"""
    elif mode == "Socratic":
        prompt = f"""You are an FM120 TA. Help the student reflect using Socratic-style questions without revealing the answer:
Answer: {input_text}"""
    else:
        prompt = f"""You are an FM120 TA. Create a thoughtful variant of this problem by changing orientation, fluid type, or boundary conditions:
Problem: {input_text}"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    return response.choices[0].message.content

# Streamlit UI
st.title("FM120 AI Instructional Assistant")

mode = st.selectbox("Choose Instructional Mode", ["Feedback", "Socratic", "Variant"])
user_input = st.text_area("Paste student answer or problem text here")

if st.button("Get Response") and user_input:
    output = get_response(user_input, mode)
    st.subheader("AI Output")
    st.write(output)

    # Optional logging
    if "log" not in st.session_state:
        st.session_state["log"] = []
    st.session_state["log"].append({"Mode": mode, "Input": user_input, "Response": output})

    if st.button("Download Log as CSV"):
        df = pd.DataFrame(st.session_state["log"])
        df.to_csv("fm120_session_log.csv", index=False)
        st.success("Log saved as fm120_session_log.csv")
