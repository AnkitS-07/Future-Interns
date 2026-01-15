from dotenv import load_dotenv
load_dotenv()

from google.cloud import dialogflow
import os

PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")

def detect_intent(text, session_id="user-session"):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(
        text=text,
        language_code="en"
    )

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            "session": session,
            "query_input": query_input
        }
    )

    return response.query_result
