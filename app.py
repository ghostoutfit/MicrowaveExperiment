
import streamlit as st
from openai import OpenAI

# Set your OpenAI API key here or use environment variable
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
    q3 = st.text_area("C. What is in your control condition(s)? How will you use it to compare results?")
    q4 = st.text_area("D. Draw and label the setup. (You can describe it in words for now)")
    q5 = st.text_area("E. What measurements should we collect? How many trials are needed?")
    q6 = st.text_area("F. What variables need to be held constant? How will you control them?")
    q7 = st.text_area("G. What are the expected results of your experiment? Why?")

    worksheet_data = {
        "Question": q1,
        "Safety": q2,
        "Control Conditions": q3,
        "Setup": q4,
        "Measurements": q5,
        "Controlled Variables": q6,
        "Expected Results": q7
    }

# ---- Right Column: GPT Assistant ----
with right_col:
    st.header("AI Group Coach")

    tone = st.selectbox(
        "Choose your assistant's tone:",
        ["🧪 Neutral Lab Coach", "😄 Playful Teammate", "🧐 Skeptical Scientist"]
    )

    user_question = st.text_input("Please choose which tone your group would prefer, then tell me your names. If you're working alone, say so.")

    if st.button("Submit"):
        if user_question.strip() == "":
            st.warning("Please enter a question or ask for a suggestion.")
        else:
            tone_instructions = {
                "🧪 Neutral Lab Coach": "You are a calm, precise lab coach. Guide students with questions that encourage them to think critically about their investigation plan.",
                "😄 Playful Teammate": "You are a fun, energetic teammate who loves science. Ask silly but smart questions to help your friends think deeper.",
                "🧐 Skeptical Scientist": "You are a skeptical scientist who always wants more evidence and clearer reasoning. Push students to be more rigorous."
            }

            system_prompt = f"""
            You are a helpful, friendly, and curious lab partner speaking in short, easy to understand sentences at an 8th grade level to students, as they plan an experiment using a microwave oven.

            Once students give you their names, use their names to ask questions to students directly. If a user says they're working alone, reply with encouragement to find at least one other student to work with, such as: This assistant isn't intended to be used while working alone. Try to find at least one other student to work with, then come back. 
            
            The goal of the experiment should be ultimately be to obtain data that helps students infer see whether the part of the system is reflecting, absorbing, or transmitting microwave radiation.
            
            Your job is to help students think for themselves. Don’t give answers — instead, ask open-ended, Socratic questions that get them to talk as a group and revise their ideas.
            
            Always speak in clear, friendly language appropriate for 13- to 14-year-olds.

            Use their current plan to ask helpful follow-up questions. If their plan is missing something important, gently ask questions to help them figure out what they might add. If they seem confused, help them clarify where to focus their attention.

            Do not explain. Ask and challenge — but always leave room for them to figure it out.
            """


            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content":
                    "Here is our current plan:\\n"
                    f"A. {q1}\\n"
                    f"B. {q2}\\n"
                    f"C. {q3}\\n"
                    f"D. {q4}\\n"
                    f"E. {q5}\\n"
                    f"F. {q6}\\n"
                    f"G. {q7}\\n\\n"
                    f"We need help with this: {user_question}"
                }
            ]
            

            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=messages,
                    temperature=0.7
                )
                reply = response.choices[0].message.content
                st.markdown("**AI Response:**")
                st.info(reply)
            except Exception as e:
                st.error(f"Error: {str(e)}")