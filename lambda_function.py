# proxy server for lambda function
import requests
import pickle


def lambda_handler(event, context):
    if "method" not in event or "url" not in event:
        return {"statusCode": 400, "body": "Missing method or URL in the request"}

    method = event["method"]
    url = event["url"]
    headers = event.get("headers", {})
    data = event.get("data", None)  # Request body
    params = event.get("params", None)  # Query parameters
    auth = event.get("auth", None)  # Authentication
    timeout = event.get("timeout", None)  # Timeout
    # You can add more options as needed

    try:
        response = requests.request(
            method,
            url,
            headers=headers,
            data=data,
            params=params,
            auth=auth,
            timeout=timeout,
        )

        if response.status_code == 200:
            response_data = pickle.dumps(response)
            return {
                "statusCode": 200,
                "body": response_data,
                "headers": {"Content-Type": "application/octet-stream"},
            }

        return {"statusCode": response.status_code, "body": "Request failed"}

    except Exception as e:
        return {"statusCode": 500, "body": str(e)}
