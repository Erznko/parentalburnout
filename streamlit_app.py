import streamlit as st
import urllib.parse
import requests

st.set_page_config(page_title="Working Parent Burnout Check", layout="centered")

# --- Ініціалізація session state ---
if "email_sent" not in st.session_state:
    st.session_state.email_sent = False
if "email_error" not in st.session_state:
    st.session_state.email_error = False
if "form_submitted" not in st.session_state:
    st.session_state.form_submitted = False

# --- EmailJS ---
def send_email(email, score):
    payload = {
        "service_id": "service_5mdfy5o",
        "template_id": "template_ssn7zho",
        "user_id": "d2wpyHuhfsjppcRiN",
        "template_params": {
            "user_email": email,
            "burnout_score": score
        }
    }
    headers = {"Content-Type": "application/json"}
    response = requests.post("https://api.emailjs.com/api/v1.0/email/send", json=payload, headers=headers)
    return response.status_code == 200

# --- Заголовок і опис ---
st.title("🧠 Working Parent Burnout Check")
st.write("Based on the validated Working Parent Burnout Scale by Gawlik & Melnyk (2022).")
st.markdown("""
This 10-question scale is here to help you pause and reflect.
If your score feels confronting, it’s not a verdict, and it’s not your fault — you just need more support and care for yourself.
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
    answer = st.radio(f"Q{i}: {q}", options, key=f"q{i}")
    answers.append(answer)

if st.button("✅ Submit"):
    st.session_state.form_submitted = True

if st.session_state.form_submitted:
    score = 0
    for i, ans in enumerate(answers):
        if i + 1 in [4, 10]:
            score += reverse_map[ans]
        else:
            score += score_map[ans]

    st.markdown("---")
    st.subheader("📟 Your result")
    st.write(f"Your score: **{score}/40**")
    st.caption("This is not a diagnosis — but it’s a useful tool for reflection.")

    # --- Email форма ---
    st.markdown("---")
    st.subheader("📩 Want to keep a copy?")
    user_email = st.text_input("Your email")
    if st.button("📨 Send to my email"):
        if user_email:
            success = send_email(user_email, score)
            st.session_state.email_sent = success
            st.session_state.email_error = not success
        else:
            st.warning("Please enter a valid email address.")

    if st.session_state.email_sent:
        st.success(f"✅ Your result was sent to {user_email}!")
    elif st.session_state.email_error:
        st.error("⚠️ Something went wrong while sending your result. Please try again later.")

    # --- Кнопки соцмереж ---
    st.markdown("---")
    st.subheader("📣 Other parents might need this too")
    st.markdown("Sharing your experience can help others notice what they’re feeling too — and remind them they’re not alone.")

    share_text = f"Parental burnout is more common than we think. I scored {score}/40 in this 2-minute test. Check in with yourself 👈"
    app_url = "https://burnout.streamlit.app/"
    tweet = f"{share_text} {app_url}"
    tweet_url = "https://twitter.com/intent/tweet?text=" + urllib.parse.quote(tweet)
    linkedin_url = "https://www.linkedin.com/sharing/share-offsite/?url=" + urllib.parse.quote(app_url)
    fb_url = "https://www.facebook.com/sharer/sharer.php?u=" + urllib.parse.quote(app_url)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"[🔗 Share on LinkedIn]({linkedin_url})")
    with col2:
        st.markdown(f"[🦆 Share on Twitter/X]({tweet_url})")
    with col3:
        st.markdown(f"[📘 Share on Facebook]({fb_url})")

    st.caption("Scale copyright © Kate Gawlik and Bernadette Mazurek Melnyk, 2022")
