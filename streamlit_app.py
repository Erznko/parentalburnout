import streamlit as st
import urllib.parse

st.set_page_config(page_title="Working Parent Burnout Check", layout="centered")

# --- Заголовок і опис ---
st.title("🧠 Working Parent Burnout Check")
st.write("Based on the validated Working Parent Burnout Scale by Gawlik & Melnyk (2022).")
st.markdown("""
This self-check is for informational purposes only and is not a clinical diagnosis.  
If your score concerns you, consider speaking with a healthcare professional.
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

score = 0
for i, q in enumerate(questions, 1):
    answer = st.radio(f"Q{i}: {q}", options, key=f"q{i}")
    if i in [4, 10]:
        score += reverse_map[answer]
    else:
        score += score_map[answer]

# --- Результат ---
if st.button("Submit"):
    st.subheader("📊 Your Score:")
    st.write(f"**{score} out of 40**")

    if score <= 10:
        st.success("No or few signs of burnout. Keep taking care of yourself!")
    elif score <= 20:
        st.info("Mild burnout – time to build in some self-care and stress relief.")
    elif score <= 30:
        st.warning("Moderate burnout – consider changes and seek support if needed.")
    else:
        st.error("Severe burnout – please consider speaking to a mental health professional. You deserve support.")

    # --- Email форма ---
    st.markdown("---")
    st.subheader("📩 Want to keep this result?")
    st.markdown("Enter your email address to send this result to yourself (e.g., to share with a therapist).")
    user_email = st.text_input("Your email")
    if st.button("Send to my email (demo)"):
        if user_email:
            st.success(f"✅ Your result would be sent to {user_email} (email sending not enabled in demo).")
        else:
            st.warning("Please enter a valid email address.")

    # --- Кнопки соцмереж ---
    st.markdown("---")
    st.subheader("📣 Help raise awareness")
    st.markdown("Share your experience (anonymously or not) to help others understand what working parents go through.")

    share_text = f"I just took the Working Parent Burnout self-check and scored {score}/40. It really made me reflect. Try it here:"
    app_url = "https://your-app-link.com"  # 🔁 Заміни на свій Streamlit URL
    tweet = f"{share_text} {app_url}"
    tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet)
    linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + urllib.parse.quote(app_url)
    fb_url = "https://www.facebook.com/sharer/sharer.php?u=" + urllib.parse.quote(app_url)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[🔗 Share on LinkedIn]({linkedin_url})")
    with col2:
        st.markdown(f"[🐦 Share on Twitter/X]({tweet_url})")
    with col3:
        st.markdown(f"[📘 Share on Facebook]({fb_url})")

    st.caption("Scale copyright © Kate Gawlik and Bernadette Mazurek Melnyk, 2022")

