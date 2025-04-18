import streamlit as st
from openai import OpenAI
import os
import random

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

st.set_page_config(layout="wide", page_title="Microwave Oven Investigation Planner")

# --- Helpers ---
def pick_random_names(name_string, used_names, count=2):
    names = [name.strip() for name in name_string.split(",") if name.strip()]
    if len(names) < count:
        return None, "This activity is meant for a group. Try to find more people to work with."
    available_names = [n for n in names if n not in used_names]
    if len(available_names) < count:
        available_names = names
        used_names.clear()
    chosen = random.sample(available_names, count)
    for name in chosen:
        used_names.add(name)
    return chosen, None

# --- Session State ---
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "last_sent" not in st.session_state:
    st.session_state.last_sent = ""
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "name_input" not in st.session_state:
    st.session_state.name_input = ""

# --- Layout ---
st.title("Oven Investigation Plan")
left_col, right_col = st.columns(2)

with left_col:
    st.header("Worksheet")
    q1 = st.text_area("A. What question are you trying to answer in the investigation you are planning?")
    q2 = st.text_area("B. What do you need to keep in your experimental design to maintain safety protocols?")
    q3 = st.text_area("C. A good experiment uses control variables and conditions to clarify how specific changes have affected the outcome. How will you use controls to allow you to compare and interpret results?")
    q4 = st.text_area("D. Describe your setup, and what measurement you plan to collect. How many trials would you want to do?")
    q5 = st.text_area("E. What are the expected results of your experiment? Why?")

with right_col:
    st.header("AI Group Coach")
    st.text_input("What are your names? (Separate with commas)", key="name_input")

    def generate_response(trigger_source, user_input=""):
        name_input = st.session_state.get("name_input", "")
        chosen_names, error_msg = pick_random_names(name_input, st.session_state.used_names, count=2)
        if error_msg:
            st.warning(error_msg)
            return
        name_a, name_b = chosen_names

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

AI Rules:
- Never explain how microwave radiation works. Ask questions instead.
- If the experiment clearly violates the essential safety concerns, ask what they could revise to stay safe. If it’s mostly safe or just missing a small detail, it’s okay to say it looks good overall.
- Refer students back to the worksheet (left side) when appropriate.
- When asking a question that's relevant to a specific question A–E, refer to the letter of the question explicitly by saying, "For Question E about ..." 
- Keep it short — always ask about ONE or TWO question categories (A–E) in one response, never more than that.
- Keep it curious and engaging. Never long-winded.
- When students are close to a safe and thoughtful experiment, encourage them and say they’re ready to check with their teacher, arrange time on the microwave and try it out themselves.

Question A — Focuses on the question the group is trying to figure out through their investigation. This is just a question related to how certain materials reflect (or bounce off, etc), absorb (or go into, etc), or transmit (or go through, pass by, etc) microwave energy / radiation. If you don't see a connection between their question and these ideas ask directly: How does can you connect your question to how materials reflect, absorb, or transmit microwave energy?
Question B — Focuses on safety protocols and how to ensure a safe experiment using provided materials. Give students explicit suggestions here if they don't have a safe experiment.
Question C — Focuses on control variables and how to set up comparisons that isolate a single variable. Ask questions about possible controls. Example: How might it impact your interpretation of results if you compared two different amounts of water?
Question D — Focuses on the experimental setup and the measurements students will collect to gather data. Steer students toward before and after temperature measurements, but don't mention this explicitly. Example: What measurements could you make before and after cooking that could give you evidence about how much energy was transferred?
Question E — Focuses on the expected results and the reasoning behind their predictions. Any prediction is valid here. Don't question it unless it's blank.

Use these acceptable answers as rough benchmarks. If a student's response meets 75% of what’s shown here, or if it reflects effort and mostly sound thinking, you can approve it. No need to nitpick wording or phrasing. When the investigation plan meets expectations, please sign off on an experiment by stating something like, "Looks like your plan is in good shape! Double-check the safety steps with your teacher, then arrange for time on the class microwave to try it out."

Available materials for experiment:
- 8 microwave-safe glass bowls (100-250 mL) with plastic lids
- microwave-safe plastic wrap (or lids) to lay on top of the glass bowls
- 2 sheets of heavy-duty aluminum foil (~8” x 12”)
- 2 sheets of hole-punched heavy-duty aluminum foil (~8” x 12”)
- cardboard and paper sheets
- 1 gallon of room-temperature tap water
- 3 microwave-safe plastic cutting boards to serve as a platform
- 4 microwave-safe plastic bowls (1” tall) to serve as spacers under the cutting board
- IR thermometer
- 1 graduated cylinder (100 mL)
- blocks of assorted metals: aluminum, brass, copper, iron

Essential Safety concerns:
 1) To prevent any overheating:
- Limit the length of time for each test to 15 seconds on high power.
- Never run the microwave oven without something in it that is a known absorber, like an open cup of water.
2) When placing metal in the microwave, make sure to:
- Keep all metal objects at least 1 inch from the walls and floors of the microwave oven, using a plastic platform if needed.
- Make sure that something is in the microwave that is a known absorber, like an open cup of water.

Controlled variables in experimental design:
- the size and material of the bowls
- the amount of water in each bowl
- the starting temperature of the water
- the distance of each bowl from the edge/platform
- plastic covering with hole (optional)

Temperature change is the main evidence for energy transfer. Encourage students to plan for before/after measurements of water temperature, and optionally of foil or platform.

Student task: {button_instructions.get(trigger_source, 'Custom message')}
Current plan:
A. {q1}
B. {q2}
C. {q3}
D. {q4}
E. {q5}

Please address one of your questions to **{name_a}**, and the other to **{name_b}**, using the format:

**Question for {name_a}, about Part A:**  
[Your question here]

**Question for {name_b}, about Part B:**  
[Your question here]

Use Markdown-style bold formatting. Do not repeat the names elsewhere in your message.
"""

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "system", "content": system_prompt}],
                temperature=0.7
            )
            reply = response.choices[0].message.content.strip()
            st.session_state.chat_history.append(("Group", user_input, reply))
        except Exception as e:
            st.session_state.chat_history.append(("ERROR", user_input, f"Error: {str(e)}"))

    # Chat input
    with st.form(key="chat_form", clear_on_submit=True):
        user_chat = st.text_input("Type a message and press Enter:", key="chat_input")
        submitted = st.form_submit_button("Send")
        if submitted and user_chat and user_chat != st.session_state.last_sent:
            generate_response("chat", user_chat)
            st.session_state.last_sent = user_chat

    # Action buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🚀 We have an experiment—how does it look?"):
            generate_response("experiment")
    with col2:
        if st.button("🧭 We’re not sure how to begin..."):
            generate_response("begin")

    # Chat display
    st.markdown("### 🧠 Conversation")
    for name, user, reply in reversed(st.session_state.chat_history):
        st.markdown(f"**{name}:** {user}")
        st.markdown(f"**AI:** {reply}")
        st.markdown("---")
