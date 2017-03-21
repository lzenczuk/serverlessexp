import json
import boto3
import datetime
import base64
import pprint

from jobbrose import s3
from jobbrose import dynamodb
from jobbrose import kinesis
from jobbrose import page
from jobbrose import server

from awslambdautils import lambda_events


def hello(event, context):
    print(event)
    query = json.loads(event['body'])

    error_messages = []
    page_id = ''
    content = ''

    print("-----------> kinesis")

    category_message = {
        'jsession': None,
        'names': [],
        'url': None,
        'level': 2
    }

    print("REQKIN publis path: " + str(category_message))
    kinesis.publish_event('testx', category_message)
    print("-----------> kinesis done")

    if 'page_id' in query:
        page_id = query['page_id']
    else:
        error_messages.append("Missing page_id param")

    if 'content' in query:
        content = query['content']

    if len(error_messages) != 0:
        body = {
            'errors': error_messages
        }

        response = {
            "statusCode": 400,
            "body": json.dumps(body)
        }

        return response
    else:
        dynamodb = boto3.resource('dynamodb')
        requests_table = dynamodb.Table('RequestsTable')

        insert_time = str(datetime.datetime.now())

        requests_table.put_item(
            Item={
                'PageId': page_id,
                'Info': {
                    'Content': content,
                    'Time': insert_time
                }
            }
        )
        body = {
            'page_id': page_id,
            'content': content,
            'insert_time': insert_time
        }

        response = {
            "statusCode": 200,
            "body": json.dumps(body)
        }

        return response

    # Use this code if you don't use the http event with the LAMBDA-PROXY integration
    """
    return {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "event": event
    }
    """


def categories_tree_handler(event, context):
    query = None

    event_type = lambda_events.get_event_type(event)

    if event_type == lambda_events.EventType.KINESIS:
        records = lambda_events.get_kinesis_event_json_data_list(event)
        if len(records) != 1:
            print("Incorrect number of records in kinesis event. Expecting 1, was " + str(len(records)))
            return

        query = records[0]

    else:
        print("Unknown event event_type: " + str(event_type))
        return

    print(query)

    cp = go_to_category_page(query['url'], query['jsession'], query['names'])

    if not cp['success']:
        print(cp['error'])
        return

    if not cp['page'].contain_categories():
        print("----> Table page?")
        return

    for category in cp['page'].get_categories():
        category_path = query['names'][:]
        category_path.append(category['name'])

        if query['level'] > 0:
            print("CATKIN publis path: " + str(category_path) + " level: " + str(query['level'] - 1))
            kinesis.publish_event('testx',
                                  {'jsession': None, 'url': None, 'names': category_path, 'level': query['level'] - 1}
                                  )

        dynamodb.create_category(category['name'], query['names'])


def go_to_category_page(url, jsession, names):
    print('==========> Checking: ' + str(jsession) + '; ' + str(url) + '; ' + str(names))

    result = server.get_page(url, jsession)

    if result['success']:
        p = page.JobbrosePage(result['page'])
        if not names:
            print("==========> No names. Return result.")
            return {'success': True, 'page': p, 'jsession': jsession}
        else:
            print("==========> Have names. Checking subcategories.")
            if not p.contain_categories():
                print("==========> Expecting subcategories but not found. Return error.")
                return {'success': False, 'error': 'Error. No subcategories. ' + str(names)}

            categories = p.get_categories()
            print("==========> Have subcategories: " + str(len(categories)))
            for category in categories:
                print("==========> Checking subcategory: " + category['name'])
                if category['name'] == names[0]:
                    print("==========> Subcategory '" + category['name'] + "' equal '" + names[0] + "'. Going deeper.")
                    return go_to_category_page(server.main_url + category['link'], result['jsession'], names[1:])
                else:
                    print("==========> Subcategory '" + category['name'] + "' not equal '" + names[0] + "'. Skipping")

            print("Error. Subcategory matching name '" + names[0] + "' not found")
            return None


def get_all_categories_handler(event, context):
    print("------> getting categories")

    categories_tree = {}

    categories = dynamodb.get_categories()

    for category in categories:
        node = categories_tree
        print("category: " + category['category_name'] + "; category path: " + str(category['parent_category']))
        for parent in category['parent_category']:
            if parent in node:
                node = node[parent]
            else:
                node[parent] = {}
                node = node[parent]

        if category['category_name'] in node:
            print("----> Error. Category: " + category['category_name'] + " is already in tree!?")
        else:
            node[category['category_name']] = {}

    response = {
        "statusCode": 200,
        "body": json.dumps(categories_tree)
    }

    return response


# if __name__ == '__main__':
#    start_page_handler(None, None)

