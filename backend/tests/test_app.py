import json
import os
import boto3
import moto
import pytest
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from app import lambda_handler


@pytest.fixture(autouse=True)
def aws_mock():
    with moto.mock_aws():
        yield


@pytest.fixture(autouse=True)
def setup_table(aws_mock):
    dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
    dynamodb.create_table(
        TableName="test-visitor-counter",
        KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
        AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
        BillingMode="PAY_PER_REQUEST",
    )
    os.environ["TABLE_NAME"] = "test-visitor-counter"
    yield
    os.environ.pop("TABLE_NAME", None)


def make_event(method="POST"):
    return {
        "requestContext": {"http": {"method": method}},
        "body": None,
    }


class Context:
    function_name = "test"
    function_version = "$LATEST"
    invoked_function_arn = "arn:aws:lambda:us-east-1:123456789012:function:test"
    memory_limit_in_mb = 128
    aws_request_id = "test-request-id"
    log_group_name = "/aws/lambda/test"
    log_stream_name = "test-stream"


def test_returns_200():
    resp = lambda_handler(make_event(), Context())
    assert resp["statusCode"] == 200


def test_returns_json():
    resp = lambda_handler(make_event(), Context())
    body = json.loads(resp["body"])
    assert "count" in body


def test_first_visit_returns_1():
    resp = lambda_handler(make_event(), Context())
    body = json.loads(resp["body"])
    assert body["count"] == 1


def test_increments_on_subsequent_visits():
    lambda_handler(make_event(), Context())
    lambda_handler(make_event(), Context())
    resp = lambda_handler(make_event(), Context())
    body = json.loads(resp["body"])
    assert body["count"] == 3


def test_cors_headers():
    resp = lambda_handler(make_event(), Context())
    headers = resp["headers"]
    assert headers["Access-Control-Allow-Origin"] == "*"
    assert "GET" in headers["Access-Control-Allow-Methods"]
    assert "POST" in headers["Access-Control-Allow-Methods"]
