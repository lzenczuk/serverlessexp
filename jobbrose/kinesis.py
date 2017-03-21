import boto3
import json


def publish_event(topic, dict):
    kinesis = boto3.client('kinesis')
    kr = kinesis.put_record(
        StreamName=topic,
        Data=json.dumps(dict),
        PartitionKey='one'
    )

    print("Published kinesis message: " + str(kr))
