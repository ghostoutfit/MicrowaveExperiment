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
    q5 = st.text_area("E. What are the expected results of your experiment? Why?")

# ---- Right Column: GPT Assistant ----
with right_col:
    st.header("AI Group Coach")

    names = st.text_input("What are your names?")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "last_sent" not in st.session_state:
        st.session_state.last_sent = ""

    def generate_response(trigger_source, user_input=""):
        button_instructions = {
            "experiment": "Evaluate our experiment. Ask short questions to help us improve it, especially for safety and data quality.",
            "begin": "We're not sure how to begin. Give us 1–2 helpful next steps or questions to think about.",
            "chat": "Continue the conversation in a short, curious way. Ask a follow-up based on what the student wrote."
        }

        user_input_defaults = {
            "experiment": "We think our experiment is ready. Can you check it?",
            "begin": "We’re not sure where to start. What do you suggest?",
        }

        if not user_input:
            user_input = user_input_defaults.get(trigger_source, "(No message)")

        system_prompt = f"""
You are a friendly lab coach helping students design and reflect on their microwave oven experiment. Keep responses short, thoughtful, and question-based.

Names: {names}

Rules:
- Never explain how microwave radiation works. Ask questions instead.
- If the experiment is unsafe, don’t approve it. Instead, ask what they could change.
- Refer students back to the worksheet (left side) when appropriate.
- Be brief, helpful, and curious. Never long-winded.

Student task: {button_instructions.get(trigger_source, 'Custom message')}
Current plan:
A. {q1}
B. {q2}
C. {q3}
D. {q4}
E. {q5}

Student message: {user_input}
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

    # --- Chat Input at the Top ---
    with st.form(key="chat_form", clear_on_submit=True):
        user_chat = st.text_input("Type a message and press Enter:", key="chat_input")
        submitted = st.form_submit_button("Send")
        if submitted and user_chat and user_chat != st.session_state.last_sent:
            generate_response("chat", user_chat)
            st.session_state.last_sent = user_chat

    # --- Action Buttons ---
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 We have an experiment—how does it look?"):
            generate_response("experiment")
    with col2:
        if st.button("🧭 We’re not sure how to begin..."):
            generate_response("begin")

    # --- Chat Display in Reverse Chronological Order (Newest First) ---
    st.markdown("### 🧠 Conversation")
    for name, user, reply in reversed(st.session_state.chat_history):
        st.markdown(f"**{name if name else 'Student'}:** {user}")
        st.markdown(f"**AI:** {reply}")
        st.markdown("---")
