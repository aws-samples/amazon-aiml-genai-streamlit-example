import io
import boto3
import pandas as pd
import streamlit as st
import constants as const
import bedrock_util as bu
import time

def process(tab):
    if tab.button('Web Refresh'):
        st.experimental_rerun()
        
    df = pd.DataFrame({"Files":const.listFiles(const.output_bucket, const.output_dump)})
    option = tab.selectbox("Select File", df, key="webTabBox")
    if not option:
        return False

    tab.divider()
    session = boto3.Session()
    s3 = session.client('s3', region_name=const.region_name)
    data = s3.get_object(Bucket=const.output_bucket, Key=option)
    content = data['Body'].read().decode()
    textArea = tab.text_area("Input Context", value=content, height=200, key="webTabArea")
    tab.divider
    
    # lets call comprehend for entity extraction
    form = tab.form("entity-form", clear_on_submit=True)
    form.markdown("Detect Key Entities:")
    submitted = form.form_submit_button("Detect Entities")
    formOutput = form.empty()
    if submitted:
        session = boto3.Session()
        comprehend = session.client('comprehend', region_name=const.region_name)
        response = comprehend.detect_entities(Text=textArea, LanguageCode='en')
        df = pd.DataFrame(response["Entities"])
        formOutput.dataframe(df)

    # lets call comprehend for PII extraction
    form2 = tab.form("pii-form", clear_on_submit=True)
    form2.markdown("Detect Personally Identifiable Information:")
    submitted2 = form2.form_submit_button("Detect PII")
    formOutput2 = form2.empty()
    if submitted2:
        session = boto3.Session()
        comprehend = session.client('comprehend', region_name=const.region_name)
        response2 = comprehend.detect_pii_entities(Text=textArea, LanguageCode='en')
        df2 = pd.DataFrame(response2["Entities"])
        df2["PII"] = df2.apply(lambda x: textArea[x['BeginOffset']:x['EndOffset']], axis=1)
        formOutput2.dataframe(df2)