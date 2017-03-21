import base64
import json


def enum(**enums):
    return type('Enum', (), enums)


EventType = enum(
    UNKNOWN="unknown",
    KINESIS="kinesis",
    SNS="sns",
    DYNAMODB="dynamodb"
)


def get_event_type(event):
    if 'Records' in event:
        # stream like events
        records = event['Records']

        if len(records) == 0:
            return EventType.UNKNOWN

        record = records[0]

        if 'kinesis' in record:
            return EventType.KINESIS

        if 'Sns' in record:
            return EventType.SNS

        if 'dynamodb' in record:
            return EventType.DYNAMODB

    return EventType.UNKNOWN


def get_kinesis_event_json_data_list(event):
    records = []

    for record in event['Records']:
        data = base64.b64decode(record['kinesis']['data'])
        records.append(json.loads(data))

    return records


def get_sns_event_json_data_list(event):
    records = []

    for record in event['Records']:
        data = record['Sns']['Message']
        records.append(json.loads(data))

    return records
