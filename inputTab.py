import io
import boto3
import pandas as pd
import streamlit as st
import constants as const

input_bucket = const.input_bucket
output_bucket = const.output_bucket
output_prefix = const.output_dump
region_name = const.region_name

def uploadFileToS3(bucket, fileName, fileBytes):
    session = boto3.Session()
    s3 = session.client('s3', region_name=region_name)
    s3.upload_fileobj(io.BytesIO(fileBytes), 
    bucket, fileName)

def listFiles(bucket, prefix=""):
    result = []
    session = boto3.Session()
    s3 = session.client('s3', region_name=region_name)
    response = s3.list_objects(Bucket=bucket, Prefix=prefix)
    if not "Contents" in response:
        return result
    for obj in response["Contents"]:
        result.append(obj["Key"])
    return result
    
def supportedFileType(file):
    if file.type == "application/pdf":
        return True
    else:
        return False

def processPDF(tab, file):
    uploadFileToS3(input_bucket, file.name, file.getvalue())
    
    # call textract
    session = boto3.Session()
    textract = session.client('textract')
    rsp = textract.detect_document_text(
            Document={
                'S3Object': {
                    'Bucket': input_bucket,
                    'Name': file.name,
                }
            })
    
    # generate flat dump
    dump = ''
    for block in rsp['Blocks']:
        if block['BlockType'] == "LINE":
            dump = dump + block['Text'] + ' '
    uploadFileToS3(output_bucket, output_prefix + file.name + ".txt", bytes(dump, 'utf-8'))
    c2 = tab.container()
    c2.write(const.escape_str(dump))

def uploader(tab):
    if tab.button('Input Refresh'):
        st.experimental_rerun()

    form = tab.form("upload-form", clear_on_submit=True)
    file = form.file_uploader("File Uploader")
    submitted = form.form_submit_button("Upload!")

    if submitted and file is not None:
        if file.type == "application/pdf":
            with st.spinner('processing...'):
                processPDF(tab, file)
        else:
            st.error('File type not supported. Please upload a different file')


    # a container to show all files in input_bucket
    tab.divider()
    c1 = tab.container()
    df = pd.DataFrame({"Files":listFiles(input_bucket)})
    c1.dataframe(df,hide_index=True, width=250)
    
        