import streamlit as st
import urllib.parse

import requests

def send_email(email, score):
    service_id = "service_5mdfy5o"
    template_id = "template_ssn7zho"
    public_key = "d2wpyHuhfsjppcRiN"

    payload = {
        "service_id": service_id,
        "template_id": template_id,
        "user_id": public_key,
        "template_params": {
            "user_email": email,
            "burnout_score": score
        }
    }

    headers = {
        "Content-Type": "application/json"
    }

    response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, headers=headers)
    return response.status_code == 200

st.set_page_config(page_title="Working Parent Burnout Check", layout="centered")

# --- Заголовок і опис ---
st.title("🧠 Working Parent Burnout Check")
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
        st.success("You’re doing well — no or very few signs of burnout. Keep listening to yourself and taking care of your energy.")
    elif score <= 20:
        st.info("You may be experiencing mild burnout. Try to build in small breaks, moments of rest, and ask for help when you need it.")
    elif score <= 30:
        st.warning("Your score suggests moderate burnout. This is a good time to slow down, reassess your load, and connect with support if possible.")
    else:
        st.error("You’re showing signs of severe burnout. You don’t have to handle this alone — please consider speaking with a mental health professional.")

    # --- Email форма ---
    st.markdown("---")
    st.subheader("📩 Want to keep a copy?")
    st.markdown("Enter your email if you’d like to take this result to your therapist or track your score over time.")
    user_email = st.text_input("Your email")
    if st.button("📨 Send to my email"):
    if user_email:
        if send_email(user_email, score):
            st.success(f"✅ Your result was sent to {user_email}!")
        else:
            st.error("⚠️ Something went wrong while sending your result. Please try again.")
    else:
        st.warning("Please enter a valid email address.")
        
    # --- Кнопки соцмереж ---
    st.markdown("---")
    st.subheader("📣 Other parents might need this too")
    st.markdown("Sharing your experience can help others notice what they’re feeling too — and remind them they’re not alone.")

    share_text = f"Parental burnout is more common than we think. I scored {score}/40 in this 2-minute test. Check in with yourself 👉 [link]"
    app_url = "https://burnout.streamlit.app/"  
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

