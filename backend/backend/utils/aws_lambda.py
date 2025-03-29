import json
from typing import Any

import boto3


def manually_trigger_route_via_lambda(
    method: str, route: str, cookies: dict[str, str]
) -> None:
    """
    Since I can't just call another route asynchronously and return early from inside my
    app, I can manually invoke the lambda with a simulated request. I found this mock
    apigateway event in the mangum repo.
    """
    lambda_client = boto3.client("lambda")

    list_functions_response = lambda_client.list_functions()
    functions = list_functions_response.get("Functions", [])

    if functions:
        # Get the name of the first (and only?) Lambda function
        # TODO: Might need to change this to the first function with 'sam-app' in it.
        lambda_function_name = functions[0]["FunctionName"]
    else:
        # Shouldn't ever get here. There literally needs to be a lambda to get here.
        raise Exception("No Lambda functions found in your account.")

    # This event payload mocks the AWS APIGateway event. I found it in the
    # mangum repo. They use it for their tests.
    payload: dict[str, Any] = {
        "path": "",
        "body": "",
        "headers": {
            "Accept": (
                "text/html,application/xhtml+xml,"
                "application/xml;q=0.9,image/webp,*/*;q=0.8"
            ),
            "Accept-Encoding": "gzip, deflate, lzma, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Forwarded-Proto": "https",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-Mobile-Viewer": "false",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Tablet-Viewer": "false",
            "CloudFront-Viewer-Country": "US",
            "Cookie": "cookie1; cookie2",
            "Host": "test.execute-api.us-west-2.amazonaws.com",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-For": "192.168.100.1, 192.168.1.1",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https",
        },
        "pathParameters": {"proxy": "hello"},
        "requestContext": {
            "accountId": "123456789012",
            "resourceId": "us4z18",
            "stage": "Prod",
            "requestId": "41b45ea3-70b5-11e6-b7bd-69b5aaebc7d9",
            "identity": {
                "cognitoIdentityPoolId": "",
                "accountId": "",
                "cognitoIdentityId": "",
                "caller": "",
                "apiKey": "",
                "sourceIp": "192.168.100.1",
                "cognitoAuthenticationType": "",
                "cognitoAuthenticationProvider": "",
                "userArn": "",
                "userAgent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/52.0.2743.82 Safari/537.36 OPR/39.0.2256.48"
                ),
                "user": "",
            },
            "resourcePath": "/{proxy+}",
            "httpMethod": "GET",
            "apiId": "123",
        },
        "resource": "/{proxy+}",
        "httpMethod": "GET",
        "queryStringParameters": "",
        "multiValueQueryStringParameters": "",
        "stageVariables": {"stageVarName": "stageVarValue"},
    }

    payload["path"] = route
    payload["headers"]["Cookie"] = (
        f"{"; ".join('='.join([k,v]) for k, v in cookies.items())}"
    )
    payload["httpMethod"] = method

    try:
        invoke_response = lambda_client.invoke(
            FunctionName=lambda_function_name,
            InvocationType="Event",  # Asynchronous invocation
            Payload=json.dumps(payload),
        )

        # Check if the invocation was successful
        if invoke_response["StatusCode"] == 202:
            print("Lambda function invoked successfully!")
        else:
            print("Failed to invoke Lambda function. Response:", invoke_response)
    except Exception as e:
        print("Error invoking Lambda function:", str(e))
