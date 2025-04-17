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

    worksheet_data = {
        "Question": q1,
        "Safety": q2,
        "Control Conditions": q3,
        "Setup": q4,
        "Measurements": q5,
        "Expected Results": q6
    }

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
            "🧪 Lab Teammate": "You are a calm, precise lab partner. Guide students with questions that encourage them to think critically about their investigation plan.",
            "😄 Silly Skeptic": "You are a fun, energetic teammate who loves science. Ask silly but smart questions to help your friends question their own assumptions and ideas.",
            "🧐 Sophisticated Scientist": "You are a scientist who always wants more evidence and clearer reasoning. Push students to be more rigorous."
        }

        button_instructions = {
            "experiment": "We have an experiment. Please evaluate it. Ask questions to help us improve it, especially around clarity, safety, and whether it will produce useful data.",
            "waiting": "We're waiting for our turn with the microwave. Give us two activity options (A or B) to deepen our thinking while we wait.",
            "results": "We've done a trial. Help us interpret what happened, based on our experiment design."
        }

        system_prompt = f"""
You are an AI assistant supporting students as they design and reflect on a microwave oven experiment. You appear in a Streamlit app with worksheet info on the left and student conversation on the right.

Student tone: {tone_descriptions[tone]}

🌟 Behavior Guidelines:
- Always use students' names naturally in the conversation (from: {names})
- Never explain how microwave radiation works. Ask questions to help students explain or revise their thinking instead.
- Never store data or give final answers.
- If the experiment violates safety rules (e.g., no water, reused foil, no platform, more than 15 seconds, exposed foil edges), don’t approve it—ask them to revise.
- If the experiment looks good and safe, you may summarize it in one paragraph to copy-paste.
- Always encourage students to revise their ideas in the worksheet.

🧪 Student request: {button_instructions.get(trigger_source, 'Student typed a custom question.')}

💬 Current Plan:
A. {q1}
B. {q2}
C. {q3}
D. {q4}
E. {q5}
F. {q6}

{"Custom student message: " + user_input if user_input else ""}
        """

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content
            st.session_state.chat_history.append((trigger_source.upper(), reply))
        except Exception as e:
            st.session_state.chat_history.append(("ERROR", f"Error: {str(e)}"))

    # ---- Button triggers ----
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

    st.markdown("---")
    user_text = st.text_input("Or ask a custom question:")
    if st.button("Submit question"):
        if user_text.strip():
            generate_response("custom", user_text)

    st.markdown("### 🧠 AI Responses")
    for source, msg in st.session_state.chat_history:
        st.markdown(f"**{source}**")
        st.info(msg)
