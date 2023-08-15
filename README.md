## AWS Sample: 
Using Streamlit to consume AWS AI/ML & GenAI services

This example uses streamlit to showcase a simple and intuitive user-interface. It allows the user to:
1. Upload single-page PDF files into  genAI-app and store it in user-supplied S3 input-bucket
2. Covert the PDF into text and store it in user-supplie S3 output-bucket
3. Use langchain and bedrock (Titan Model) to do LLM text processing on the uploaded-file or user-inputs
4. Use AWS Translate service to translate uploaded-file or user-input
5. Use AWS comprehend service for entity recognition and PII extraction on uploaded-file or user-inputs
6. Download a webpage and use Bedrock for summary and Comprehend for sentiment and targetted sentiment

## Getting Started
1. It is recommended to use a Cloud9 environment as it comes bundled with AWS CLI pre-installed
2. Streamlit runs on port 8501 by default, allow this in Security-Group associated with Cloud9 instance

Once the Cloud9 environment is setup, this example requires at least python 3.8. To install python 3.8:
```
sudo amazon-linux-extras install python3.8
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.8 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.8 1
```

Clone the sample repository:
```
'git clone https://github.com/aws-samples/amazon-aiml-genai-streamlit-example'
```

Download libraries & setup a virtual environment so all python dependencies are stored within project directory:
```
Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ ./download-dependencies.sh
Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ python -m venv .venv
Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ source .venv/bin/activate
(.venv) Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ pip install -r requirements.txt
```

Create a directory and file to store global password for the steamlit application:
```
Admin:~/environment/amazon-aiml-genai-streamlit-example (main) $ less .streamlit/secrets.toml

# .streamlit/secrets.toml

password = "Your-Password"
```

Update resources in the constants.py file:
```
input_bucket = "your-input-s3-bucket"
output_bucket = "your-output-s3-bucket"
bedrock_ep_url = "the-bedrock-endpoint-url"
region_name = "your-region"
```

Ensure that the Role/permissions associated with your Cloud9 instance can access:
1. Required S3 buckets
2. Textract, Translate, Comprehend and Bedrock services

## Now we run the sample streamlit application
To run the streamlit application, run the following command:
```
(.venv) Admin:~/environment/amazon-aiml-genai-streamlit-example (master) $ streamlit run genai.py 

Collecting usage statistics. To deactivate, set browser.gatherUsageStats to False.


  You can now view your Streamlit app in your browser.

  Network URL: http://a.b.c.e:8501
  External URL: http://w.x.y.z:8501
```

There are some sample single-page PDF files to try:
```
Admin:~/environment/amazon-aiml-genai-streamlit-example (master) $ ls pdf-samples/
bank-statement.pdf  payslip.pdf
```


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

