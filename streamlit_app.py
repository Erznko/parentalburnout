import streamlit as st
import urllib.parse

st.set_page_config(page_title="Working Parent Burnout Check", layout="centered")

# --- Заголовок і опис ---
st.title("Working Parent Burnout Check")
st.write("Based on the validated Working Parent Burnout Scale by Gawlik & Melnyk (2022).")
st.markdown("""
This 10-question scale is here to help you pause and reflect.
It’s a tool designed for working parents — to check in with yourself, 
spot signs of burnout early, and (if needed) share your result with a professional.

Originally developed for clinical use, it’s been shown to reliably detect parental burnout in working parents.

If your score feels confronting, it’s not a verdict, and it’s not your fault — you just need more support 
and care for yourself. Please seek professional help if it's hard for you to cope.

This self-check is for informational purposes only and is not a clinical diagnosis.
""")

# --- Питання ---
questions = [
    "I get/feel easily irritated with my children.",
    "I feel that I am not the good parent that I used to be to my child(ren).",
    "I wake up exhausted at the thought of another day with my children.",
    "I find joy in parenting my children.",  # Reverse scored
    "I have guilt about being a working parent, which affects how I parent my children.",
    "I feel like I am in survival mode as a parent.",
    "Parenting my children is stressful.",
    "I lose my temper easily with my children.",
    "I feel overwhelmed trying to balance my job and parenting responsibilities.",
    "I am doing a good job being a parent."  # Reverse scored
]

options = ["Not at all", "A little", "Somewhat", "Moderately so", "Very much so"]
score_map = {"Not at all": 0, "A little": 1, "Somewhat": 2, "Moderately so": 3, "Very much so": 4}
reverse_map = {"Not at all": 4, "A little": 3, "Somewhat": 2, "Moderately so": 1, "Very much so": 0}

answers = []
for i, q in enumerate(questions, 1):
        answers.append(st.radio(f"Q{i}: {q}", options, key=f"q{i}"))

# --- Submit ---
if st.button("✅ Submit"):
    score = 0
    for i, answer in enumerate(answers):
        if i in [3, 9]:  # 4th and 10th questions
            score += reverse_map[answer]
        else:
            score += score_map[answer]

    st.markdown("---")
    st.subheader("🧾 Your Result")
    st.markdown(f"**Your burnout score is: `{score}` out of 40.**")

    if score >= 30:
        st.warning("This score suggests a high level of burnout. Please seek support.")
    elif score >= 20:
        st.info("You may be experiencing moderate burnout symptoms.")
    else:
        st.success("You're doing okay — but always take time for yourself.")

    # --- Кнопки соцмереж + картинки ---
st.markdown("---")
st.subheader("📣 Other parents might need this too")

st.markdown(
    """
We don’t track your data, so no auto-post — 
but here’s a text you can use and some images to go with it,  
if you want to help other parents realise that burnout is real:
"""
)

share_text = f"""Parental burnout is more common than we think.
I scored {score}/40 in this 2-minute self-check.
Check in with yourself 👉 https://burnout.streamlit.app/"""

st.code(share_text, language="markdown")

st.markdown("Right-click or long-press an image to save and share:")

# --- Відображення 5 картинок у два ряди ---
import os

image_files = ["1.jpg", "2.jpg", "3.jpg", "4.jpg", "5.jpg"]
image_path = "."

cols = st.columns(3)
for i in range(3):
    with cols[i]:
        st.image(os.path.join(image_path, image_files[i]), use_column_width=True)

cols = st.columns(2)
for i in range(3, 5):
    with cols[i - 3]:
        st.image(os.path.join(image_path, image_files[i]), use_column_width=True)

    st.caption("Scale copyright © Kate Gawlik and Bernadette Mazurek Melnyk, 2022")
