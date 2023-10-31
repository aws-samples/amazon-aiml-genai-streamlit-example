import io
import boto3
import pandas as pd
import streamlit as st
import constants as const
import bedrock_util as bu
import time
from googlesearch import search

def filter_response (response):
    result = []
    for e in response['Entities']:
        for m in e['Mentions']:
            s = m['MentionSentiment']['Sentiment']
            if  s == 'POSITIVE' or s == 'NEGATIVE':
                obj = {}
                obj['Text'] = m['Text']
                obj['Type'] = m['Type']
                obj['Sentiment'] = s
                obj['BeginOffset'] = m['BeginOffset']
                obj['EndOffset'] = m['EndOffset']
                result.append(obj)
    return result

def perform_query(query):
    response = []
    for i in search(query,stop=3):
        response.append(i)
    return response

def process(tab):
    if tab.button('Crawl Refresh'):
        st.session_state.crawl_content = ""
        st.session_state.crawl_summary = ""
        st.experimental_rerun()

    form = tab.form("crawl-form", clear_on_submit=False)
    crawlInput = form.text_input("Webpage to process")
    submitted = form.form_submit_button("Download Info")
    formOutput = form.empty()
    if crawlInput and submitted:
        content = const.getTextFromWeb(crawlInput)
        info = const.truncate(content, const.ctx_sz)
        prompt = "Context: " + info + "\n" + "for above context write summary:"
        summary = bu.call_model_claude(prompt)
        st.session_state.crawl_content = content
        st.session_state.crawl_summary = summary
    
    if st.session_state.crawl_summary:
        expander = tab.expander("Content", expanded=False)
        expander.markdown(const.escape_str(st.session_state.crawl_content))
        summaryS = st.session_state.crawl_summary.strip()
        textArea = tab.text_area("Summary", value=summaryS, height=200, key="crawlTabArea")
    
    # lets call comprehend for entity extraction
    form = tab.form("web-entity-form", clear_on_submit=True)
    form.markdown("Detect Key Entities:")
    submitted = form.form_submit_button("Detect Entities")
    formOutput = form.empty()
    if submitted and st.session_state.crawl_content:
        session = boto3.Session()
        comprehend = session.client('comprehend', region_name=const.region_name)
        response = comprehend.detect_entities(Text=st.session_state.crawl_content, LanguageCode='en')
        df = pd.DataFrame(response["Entities"])
        formOutput.dataframe(df)
            
    # lets call comprehend for entity extraction
    form2 = tab.form("web-entity-form2", clear_on_submit=True)
    form2.markdown("Detect Sentiment:")
    submitted2 = form2.form_submit_button("Detect Sentiment")
    form2Output1 = form2.empty()
    form2Output2 = form2.empty()
    if submitted2 and st.session_state.crawl_content:
        session = boto3.Session()
        comprehend = session.client('comprehend', region_name=const.region_name)
        response = comprehend.detect_sentiment(Text=st.session_state.crawl_content[:const.byte_sz], LanguageCode='en')
        form2Output1.markdown("Overall sentiment is: " + response['Sentiment'])
        response = comprehend.detect_targeted_sentiment(Text=st.session_state.crawl_content[:const.byte_sz], LanguageCode='en')
        form2Output2.dataframe(filter_response(response))