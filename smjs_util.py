import boto3, json
import constants as const

endpoint_name = const.smjs_endpoint

MAX_LENGTH = 1024
NUM_RETURN_SEQUENCES = 1
TOP_K = 0
TOP_P = 0.7
DO_SAMPLE = True
CONTENT_TYPE = 'application/json'

def generate_response(prompt):
    session = boto3.Session()
    client = session.client('sagemaker-runtime')
    
    payload = {'text_inputs': prompt, 
           'max_length': MAX_LENGTH, 
           'num_return_sequences': NUM_RETURN_SEQUENCES,
           'top_k': TOP_K,
           'top_p': TOP_P,
           'do_sample': DO_SAMPLE}
    payload = json.dumps(payload).encode('utf-8')
    
    response = client.invoke_endpoint(EndpointName=endpoint_name, 
                                  ContentType=CONTENT_TYPE, 
                                  Body=payload)
                                  
    model_predictions = json.loads(response['Body'].read())
    generated_text = model_predictions['generated_texts'][0]
    return generated_text