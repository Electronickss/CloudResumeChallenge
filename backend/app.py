import os
import json
import boto3


def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["TABLE_NAME"])

    response = table.update_item(
        Key={"id": "visitor_count"},
        UpdateExpression="ADD #cnt :inc",
        ExpressionAttributeNames={"#cnt": "count"},
        ExpressionAttributeValues={":inc": 1},
        ReturnValues="ALL_NEW",
    )

    count = int(response["Attributes"]["count"])

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET,POST,OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type",
        },
        "body": json.dumps({"count": count}),
    }
