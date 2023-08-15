import io
import boto3
import pandas as pd
import streamlit as st
import constants as const
import bedrock_util as bu
import time

def translate(tab):
    if tab.button('Translate Refresh'):
        st.experimental_rerun()
        
    df = pd.DataFrame({"Files":const.listFiles(const.output_bucket, const.output_dump)})
    option = tab.selectbox("Select File", df, key="translateTabBox")
    if not option:
        return False

    tab.divider()
    session = boto3.Session()
    s3 = session.client('s3', region_name=const.region_name)
    data = s3.get_object(Bucket=const.output_bucket, Key=option)
    content = data['Body'].read().decode()
    textArea = tab.text_area("Input Context", value=content, height=200, key="translateTabArea")
    tab.divider
    
    form = tab.form("translate-form", clear_on_submit=False)
    langChoice = form.selectbox("Select File", const.lang_dict, key="translateTabLang", index=0)
    submitted = form.form_submit_button("Translate")
    if submitted and langChoice:
        content = textArea
        session = boto3.Session()
        translate = session.client('translate', region_name=const.region_name)
        output_lang = const.lang_dict[langChoice]
        result = translate.translate_text(Settings={'Formality': 'FORMAL','Profanity': 'MASK'},
            Text=content, SourceLanguageCode="auto", TargetLanguageCode=output_lang)
        tab.markdown(const.escape_str(result["TranslatedText"]))
    
