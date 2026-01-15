from dotenv import load_dotenv
load_dotenv()

import streamlit as st
from dialogflow_utils import detect_intent
from gpt_fallback import gpt_response
from sentiment import get_sentiment
from escalation import escalate_to_human
from chat_logger import log_chat

st.set_page_config(page_title="Customer Support Bot")

st.title("💬 Smart Customer Support Chatbot")

user_input = st.text_input("Ask your question")

if user_input:
    result = detect_intent(user_input)

    if result.intent.is_fallback:
        reply = gpt_response(user_input)
    else:
        reply = result.fulfillment_text

    sentiment = get_sentiment(user_input)
    if sentiment == "angry":
        st.warning("⚠️ We sense frustration. Escalating to support.")
        reply = escalate_to_human(user_input)

    log_chat("web_user", user_input, reply)
    st.success(reply)

st.markdown(
    "<p style='text-align:center;font-size:12px;'>Made with 💡 by Ankit Sarkar</p>",
    unsafe_allow_html=True
)
