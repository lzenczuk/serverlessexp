import json
import boto3
import datetime


def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    dynamodb = boto3.resource('dynamodb')
    requests_table = dynamodb.Table('RequestsTable')
    requests_table.put_item(
        Item={
            'PageId': event['page_id'],
            'Info': {
                'Title': 'Test',
                'Time': str(datetime.datetime.now())
            }
        }
    )
    return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """
