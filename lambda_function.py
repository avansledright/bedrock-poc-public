import boto3
from botocore.exceptions import ClientError
import json
import helper as h
import os 
import prompts as prompts

s3 = boto3.client("s3")

def lambda_handler(event, context):
    modelid = os.environ['MODELID']
    print("Starting Code.")
    print(event)

    # Get file location from SQS Event
    for record in event['Records']:
        msg_body = json.loads(record['body'])
        print("Message Body:")
        print(msg_body)
        for record in msg_body['Records']:
            bucket_name = record['s3']['bucket']['name']
            bucket_key = record['s3']['object']['key']

    # Get file from S3 
    report_file = h.s3_actions.get_object(bucket_name, bucket_key)
    if report_file != False:
        # Send variable to Bedrock
        print("Sending file to Bedrock")
        # Build paramaters for model: https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters.html
        # Based on input we should select a prompt from the prompts.py file
        prompt_to_send = prompts.return_prompt(report_file, "testPrompt")
        body = {
            "prompt": prompt_to_send,
            "max_tokens_to_sample": 300,
            "temperature": 0.1,
            "top_p": 0.9
        }
        accept = 'application/json'
        contentType = 'application/json'
        # Not sure we need the below line
        #bedrock_client = h.bedrock_actions.get_bedrock_client(model_name=modelid)

        # Return Psuedo code
        bedrock_response = h.bedrock_actions.invoke_model(json.dumps(body, indent=2).encode('utf-8'), contentType, accept, modelId=modelid)
        print(bedrock_response)
        response_body = json.loads(bedrock_response.get('body').read())
        print(response_body)
        # Compile Psuedo code and technical document

    else:
        print("Failed to get file from S3. Exiting.")
        return False
    

    # Upload to S3
    output_bucket = "genai-poc-outputs"
    if h.s3_actions.put_object(output_bucket, response_body, bucket_key) == True:
        print("Successfully put object into bucket")
        return True
        # # Report done to SQS
        # print("Removing message from queue")
        # if h.sqs_actions.delete_message("myQueueURL", "myMessageId") == True:
        #     print("Completed processing")
        #     return True
        # else:
        #     print("Failed to remove message from queue")
        #     print("Putting message in DLQ")
        #     return False

    else:
        print("Failed to upload object. Exiting...")
        return False
    
    
        

