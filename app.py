import streamlit as st
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

st.set_page_config(layout="wide", page_title="Microwave Oven Investigation Planner")

# ---- Left Column: Worksheet ----
st.title("Oven Investigation Plan")
left_col, right_col = st.columns(2)

with left_col:
    st.header("Worksheet")

    q1 = st.text_area("A. What question are you trying to answer in the investigation you are planning?")
    q2 = st.text_area("B. What do you need to keep in your experimental design to maintain safety protocols?")
    q3 = st.text_area("C. A good experiment uses control variables and conditions to clarify how specific changes have affected the outcome. How will you use controls to allow you to compare and interpret results?")
    q4 = st.text_area("D. Describe your setup, and what measurement you plan to collect. How many trials would you want to do?")
    q5 = st.text_area("E. What variables need to be held constant? How will you control them?")
    q6 = st.text_area("F. What are the expected results of your experiment? Why?")

# ---- Right Column: GPT Assistant ----
with right_col:
    st.header("AI Group Coach")

    tone = st.selectbox(
        "Choose your assistant's tone:",
        ["🧪 Lab Teammate", "😄 Silly Skeptic", "🧐 Sophisticated Scientist"]
    )

    names = st.text_input("What are your names?")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    def generate_response(trigger_source, user_input=""):
        tone_descriptions = {
            "🧪 Lab Teammate": "Casual, curious, and collaborative. Ask helpful questions.",
            "😄 Silly Skeptic": "Playful, sarcastic, and smart. Ask silly questions that spark thinking.",
            "🧐 Sophisticated Scientist": "Serious and precise. Challenge ideas and ask for evidence."
        }

        button_instructions = {
            "experiment": "Evaluate our experiment. Ask short questions to help us improve it, especially for safety and data quality.",
            "waiting": "We're waiting for microwave access. Offer us two short thinking activities to pick from (A or B).",
            "results": "We finished a trial. Help us figure out what it means with quick, pointed questions.",
            "chat": "Continue the conversation in a short, curious way. Ask a follow-up based on what the student wrote."
        }

        system_prompt = f"""
You are an AI assistant in a Streamlit classroom tool, helping students improve their microwave oven experiment. You always speak briefly—just a few sentences max.

Tone: {tone_descriptions[tone]}
Names: {names}

Rules:
- Never explain how microwave radiation works. Ask questions instead.
- If the experiment is unsafe, don’t approve it. Instead, ask what they could change.
- Refer students back to the worksheet (left side) when appropriate.
- Keep it short, curious, and engaging. Never long-winded.

Student task: {button_instructions.get(trigger_source, 'Custom message')}
Current plan:
A. {q1}
B. {q2}
C. {q3}
D. {q4}
E. {q5}
F. {q6}

Student message: {user_input if user_input else '(none yet)'}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append((names, user_input, reply))
        except Exception as e:
            st.session_state.chat_history.append(("ERROR", user_input, f"Error: {str(e)}"))

    # ---- Action Buttons ----
    st.markdown("### Choose an action:")
    b1, b2, b3 = st.columns(3)
    with b1:
        if st.button("🚀 We have an experiment—how does it look?"):
            generate_response("experiment")
    with b2:
        if st.button("⏳ What should we do while we’re waiting?"):
            generate_response("waiting")
    with b3:
        if st.button("📊 How can I interpret my results?"):
            generate_response("results")

    # ---- Free Chat Field ----
    st.markdown("---")
    user_chat = st.text_input("Or respond here to keep the conversation going:")

    if st.button("Send"):
        if user_chat.strip():
            generate_response("chat", user_chat)

    # ---- Display Chat History ----
    st.markdown("### 🧠 AI Conversation")
    for name, user, reply in st.session_state.chat_history:
        st.markdown(f"**{name if name else 'Student'}:** {user}")
        st.markdown(f"**AI:** {reply}")
