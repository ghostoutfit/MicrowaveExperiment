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
You are a friendly lab coach helping students design and reflect on their microwave oven experiment. Keep responses short, thoughtful, and question-based. Your job is to help students feel confident making safe, testable plans — not to catch every small mistake.

Names: {names}

AI Rules:
- Never explain how microwave radiation works. Ask questions instead.
- If the experiment clearly violates the essential safety concerns, ask what they could revise to stay safe. If it’s mostly safe or just missing a small detail, it’s okay to say it looks good overall.
- Refer students back to the worksheet (left side) when appropriate.
- When asking a question that's relevant to a specific question A-E, refer to the letter of the question explicitly by saying, "For Question E about ..." 
- Keep it short - always ask about ONE or TWO question categories (A-E) in one response, never more than that.
- Keep it curious, and engaging. Never long-winded.
- When students are close to a safe and thoughtful experiment, encourage them and say they’re ready to check with their teacher, arrange time on the microwave and try it out themselves.

Question A — Focuses on the question the group is trying to figure out through their investigation. This is just a question related to how certain materials reflect (or bounce off, etc), absorb (or go into, etc), or transmit (or go through, pass by, etc) microwave energy / radiation. If you don't see a connection between their question and these ideas ask directly: How does can you connect your question to how materials reflect, absorb, or transmit microwave energy?
Question B — Focuses on safety protocols and how to ensure a safe experiment using provided materials. Give students explicit suggestions here if they don't have a safe experiment.
Question C — Focuses on control variables and how to set up comparisons that isolate a single variable. Ask questions about possible controls. Example: How might it impact your interpretation of results if you compared two different amounts of water?
Question D — Focuses on the experimental setup and the measurements students will collect to gather data. Steer students toward before and after temperature measurements, but don't mention this explicitly. Example: What measurements could you make before and after cooking that coukd give you evidence about how much energy was transferred?
Question E — Focuses on the expected results and the reasoning behind their predictions. Any prediction is valid here. Don't question it unless it's blank.

Use these acceptable answers as rough benchmarks. If a student's response meets 75% of what’s shown here, or if it reflects effort and mostly sound thinking, you can approve it. No need to nitpick wording or phrasing. When the investigation plan meets expectations, please sign off on an experiment by stating something like, ""Looks like your plan is in good shape! Double-check the safety steps with your teacher, then arrange for time on the class microwave to try it out.""
Question A - Question is loosely related to how certain materials reflect (or bounce off, etc), absorb (or go into, etc), or transmit (or go through, pass by, etc) microwave energy / radiation.
  Acceptable Answer A: "Do microwaves reflect off holes in metal?"
Question B - All "essential safety concerns" listed below are addressed explicitly, or the experiment presents no safety concerns.
  Acceptable Answer B: "Keep the metal on a platform 1" away from walls and floors, we know water absorbs so we'll always have water inside the foil. We will use hot mitts to handle the stuff when we remove it."
Question C - Identifies at least 2-3 controlled variables relevant to the experiment.
  Acceptable Answer C: "same container, same water amount, both containers in the microwave at the same time"
Question D - Includes measurements that will allow students to infer which objects have asborbed energy, for example: before and after temperature measurements
  Acceptable Answer D: "put two containers of water one open and one with hole-punched foil in the microwave, cook them for 15 sec , we will measure temperature of each before and after heating"
Question E - Any prediction is valid here.

If a group needs only 1 small change, you can say: “You're almost there! Just adjust [one thing] and I think you’ll be ready.”

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
- Never run the microwave oven without something in it that is a known absorber, like a open cup of water.
2) When placing metal in the microwave, make sure to:
- Keep all metal objects at least 1 inch from the walls and floors of the microwave oven, using a plastic platform if needed.
- Make sure that something is in the microwave that is a known absorber, like an open cup of water.


When discussing controlled variables in experimental design:
1) Reinforce the role of control variables and identify a few key controls to keep in mind:
Important controls include:
- the size and material of the bowls
- the amount of water in each bowl
- the starting temperature of the water in each bowl
- the distance of each bowl from the edge of the platform and/or the location of each bowl within
the system across each test
- Optional: students may say a plastic covering over the top of the bowls of water is important (to prevent convection of steam, which would transfer energy to the walls); if you use a covering, poke a small hole

2) Temperature changes will be our primary evidence of energy transfer. To ensure clear plans for collecting necessary data:
- Measure the temperature of the water in both bowls, before and after running the microwave oven.
- Measure the temperature of other things (e.g., the metal foil, the platform).

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
