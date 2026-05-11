import streamlit as st
import re
import string
import pandas as pd
from textblob import TextBlob

st.set_page_config(
    page_title="Text Cleaning App",
    page_icon="🧹",
    layout="wide"
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
}
h1, h2, h3, p, label, div {
    color: white !important;
}
textarea, input {
    background-color: white !important;
    color: black !important;
    border-radius: 10px !important;
}
.card {
    background-color: rgba(255,255,255,0.13);
    padding: 20px;
    border-radius: 18px;
    margin: 12px 0px;
    border: 2px solid white;
}
.stButton>button {
    background-color: #ff4b5c;
    color: white;
    border-radius: 10px;
    padding: 10px 25px;
    border: none;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "reviews" not in st.session_state:
    st.session_state.reviews = []

# ---------------- SIDEBAR ----------------
st.sidebar.title("🧹 Text Cleaning App")
page = st.sidebar.radio(
    "Select Page",
    ["🏠 Home Dashboard", "🧹 Text Cleaning", "⭐ Reviews"]
)

# ---------------- TEXT CLEANING FUNCTIONS ----------------
def remove_numbers(text):
    return re.sub(r'\d+', '', text)

def remove_punctuation_special(text):
    return re.sub(r'[^\w\s]', '', text)

def remove_extra_spaces(text):
    return " ".join(text.split())

def visible_spaces(text):
    return text.replace(" ", " ")

def clean_text_steps(text):

    steps = {}

    steps["📝 1. Original Text"] = visible_spaces(text)

    text = text.lower()
    steps["🔡 2. Lowercase Text"] = visible_spaces(text)

    text = remove_numbers(text)
    steps["🔢 3. Removed Numbers"] = visible_spaces(text)

    text = remove_punctuation_special(text)
    steps["✂️ 4. Removed Punctuation & Special Characters"] = visible_spaces(text)

    text = remove_extra_spaces(text)
    steps["📏 5. Removed Extra Spaces"] = visible_spaces(text)

    steps["✅ 6. Final Cleaned Text"] = visible_spaces(text)

    return steps

def find_sentiment(review):
    polarity = TextBlob(review).sentiment.polarity

    if polarity > 0:
        return "Positive 😊"
    elif polarity < 0:
        return "Negative 😔"
    else:
        return "Neutral 😐"

# ---------------- PAGE 1: HOME + DASHBOARD ----------------
if page == "🏠 Home Dashboard":
    st.title("🧹 Text Cleaning and Review Analysis App")

    st.markdown("""
    <div class="card">
    <h3>📌 About This Project</h3>
    <p>
    This project is a simple NLP-based Text Cleaning Tool.
    It helps users clean messy text step-by-step before using it
    for Machine Learning or Artificial Intelligence projects.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
    <h3>❓ Problem Statement</h3>
    <p>
    Raw text data may contain capital letters, numbers, punctuation,
    special characters, and extra spaces. These things can affect NLP model
    performance. So, cleaning text is an important first step in NLP.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("📊 Dashboard")

    df = pd.DataFrame(st.session_state.reviews)

    total_reviews = len(df)

    if total_reviews > 0:
        positive = len(df[df["Sentiment"] == "Positive 😊"])
        negative = len(df[df["Sentiment"] == "Negative 😔"])
        neutral = len(df[df["Sentiment"] == "Neutral 😐"])
    else:
        positive = negative = neutral = 0

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Reviews", total_reviews)
    col2.metric("Positive 😊", positive)
    col3.metric("Negative 😔", negative)
    col4.metric("Neutral 😐", neutral)

    if total_reviews > 0:
        st.subheader("📈 Sentiment Chart")
        sentiment_count = df["Sentiment"].value_counts()
        st.bar_chart(sentiment_count)
    else:
        st.info("No reviews yet. Add reviews from the Reviews page.")

# ---------------- PAGE 2: TEXT CLEANING ----------------
elif page == "🧹 Text Cleaning":
    st.title("🧹 Text Cleaning Step-by-Step")

    user_text = st.text_area(
        "Enter your messy text:",
        height=180,
        placeholder="Example: Hello!!! I am Learning NLP 123..."
    )

    if st.button("Clean Text"):
        if user_text.strip() == "":
            st.warning("Please enter some text first.")
        else:
            result = clean_text_steps(user_text)

            for step, output in result.items():

              st.markdown(f"### {step}")

              st.text(output)

# ---------------- PAGE 3: REVIEWS ----------------
elif page == "⭐ Reviews":
    st.title("⭐ User Reviews")

    name = st.text_input("Enter your name")
    review = st.text_area("Write your review about this app")

    if st.button("Submit Review"):
        if name.strip() == "" or review.strip() == "":
            st.warning("Please enter your name and review.")
        else:
            sentiment = find_sentiment(review)

            st.session_state.reviews.append({
                "Name": name,
                "Review": review,
                "Sentiment": sentiment
            })

            st.success(f"Review submitted successfully! Sentiment: {sentiment}")

    if len(st.session_state.reviews) > 0:
        st.subheader("📋 All Reviews")
        df = pd.DataFrame(st.session_state.reviews)
        st.dataframe(df, use_container_width=True)