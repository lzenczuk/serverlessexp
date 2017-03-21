import boto3
import datetime


def create_category(category_name, path):
    dynamodb = boto3.resource('dynamodb')
    categories_query_table = dynamodb.Table('CategoriesQueryTable')

    create_time = str(datetime.datetime.now())

    response = categories_query_table.put_item(
        Item={
            'category_name': category_name,
            'parent_category': path,
            'status': 'new',
            'create_time': create_time,
            'update_time': create_time
        }
    )

    print("Inserted category to dynamodb: " + str(response))


def update_category_status(category_name, status):
    dynamodb = boto3.resource('dynamodb')
    categories_query_table = dynamodb.Table('CategoriesQueryTable')

    update_time = str(datetime.datetime.now())

    response = categories_query_table.update_item(
        Key={'category_name': category_name},
        UpdateExpression="set status = :s, update_time = :u",
        ExpressionAttributeValues={
            ':s': status,
            ':u': update_time
        },
        ReturnValues="UPDATED_NEW"
    )

    print("Updated category in dynamodb: " + str(response))


def get_categories():
    dynamodb = boto3.resource('dynamodb')
    categories_query_table = dynamodb.Table('CategoriesQueryTable')

    response = categories_query_table.scan()

    print("Categories in dynamodb: " + str(response))
    return response['Items']
