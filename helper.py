import boto3
from botocore.exceptions import ClientError
import json

s3 = boto3.client("s3")
sqs = boto3.client("sqs", region_name="us-west-2")
bedrock = boto3.client("bedrock", region_name="us-west-2")
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")

class bedrock_actions:
    # Creates a boto3 client for bedrock:
    def get_bedrock_client(model_name):
        try:
            response = bedrock.get_foundation_model(
                modelIdentifier=model_name
            )
            return response
        except ClientError as e:
            print("Failed to get model information")
            print(e)
            return False
        
    # Invoke the model with some values:
    # This will need to be tweaked this is just psuedo code
    def invoke_model(body, contentType, accept, modelId):
        print(f"Body being sent: {body}")
        try:
            response = bedrock_runtime.invoke_model(
                body=body,
                contentType=contentType,
                accept=accept,
                modelId=modelId
            )
            return response
        except ClientError as e:
            print("Failed to invoke Bedrock model")
            print(e)
            return False

class sqs_actions:
    def delete_message(queue_name, message_id):
        try:
            response = sqs.delete_message(
                QueueUrl=queue_name,
                ReceiptHandle=message_id
            )
            return True
        except ClientError as e:
            print("Failed to remove message from queue")
            print(e)
            return False
class s3_actions:
    # Grabs object from an S3 bucket, reads it and returns it to the caller
    # If an error happens it will return false
    def get_object(bucket_name, path):
        try:
            file = s3.get_object(
                Bucket=bucket_name,
                Key=path
            )
            return file['Body'].read().decode('utf-8')
        except ClientError as e:
            print("Failed to get object")
            print(e)
            return False
    
    #Uploads an object to a S3 bucket
    def put_object(bucket_name, body, key):
        try:
            s3.put_object(
                Bucket=bucket_name,
                Body=json.dumps(body).encode('utf-8'),
                Key=key
            )
            return True
        except ClientError as e:
            print("Failed to put object")
            print(e)
            return False