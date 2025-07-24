import streamlit as st

st.set_page_config(page_title="Working Parent Burnout Check", layout="centered")

st.title("🧠 Working Parent Burnout Check")
st.write("This tool is based on the validated scale by Gawlik & Melnyk (2022).")
st.write("Answer a few questions to check your burnout level. This is a demo version with 2 questions.")

# --- Questions & Scoring ---
questions = [
    "I get/feel easily irritated with my children.",
    "I feel that I am not the good parent that I used to be to my child(ren)."
]

options = ["Not at all", "A little", "Somewhat", "Moderately so", "Very much so"]
points = {"Not at all": 0, "A little": 1, "Somewhat": 2, "Moderately so": 3, "Very much so": 4}

score = 0
responses = []

for i, q in enumerate(questions, 1):
    answer = st.radio(f"Q{i}: {q}", options, key=f"q{i}")
    responses.append(answer)
    score += points[answer]

# --- Submit ---
if st.button("Submit"):
    st.subheader("📊 Your Score:")
    st.write(f"**{score} out of {len(questions)*4}**")

    if score <= 2:
        st.success("No or few signs of burnout.")
    elif score <= 4:
        st.warning("Mild burnout – take care of yourself.")
    else:
        st.error("Moderate to high burnout – consider taking action and seeking support.")

    st.caption("Scale: Copyright © Kate Gawlik and Bernadette Mazurek Melnyk, 2022")
