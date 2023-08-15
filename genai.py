import streamlit as st
import boto3
import botocore
import inputTab
import processTab
import translateTab
import comprehendTab
import crawlTab

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if not check_password():
    st.stop()

inputT, processT, translateT, comprehendT, crawlT = st.tabs(["Input", "GenAI", "Translate", "Comprehend", "Web"])

if "messages" not in st.session_state:
    st.session_state.messages = []

if "crawl_content" not in st.session_state:
        st.session_state.crawl_content = ""

if "crawl_summary" not in st.session_state:
        st.session_state.crawl_summary = ""
    
inputTab.uploader(inputT)
processTab.process(processT)
translateTab.translate(translateT)
comprehendTab.process(comprehendT)
crawlTab.process(crawlT)