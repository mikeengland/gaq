import os
from collections import namedtuple
from functools import reduce

import requests
from flask import (
    Flask,
    jsonify,
    request,
)
from flask_cors import CORS
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

app = Flask(__name__)

CORS(app)


@app.route('/api/query', methods=['POST'])
def get_report():
    """
    Endpoint that is used to fetch the report from Google Ads.

    Expects the following parameters:
        - loginCustomerId: The ID of the account that you want to query's parent MCC
        - customerId: The ID of the account that you want to query
        - query: The query string e.g. "select campaign.id from campaign"

    :return: JSON response
    """
    api_response = get_report_data(request.json['loginCustomerId'], request.json['customerId'], request.json['query'])
    if 'error' in api_response:
        response = jsonify(api_response)
        response.status_code = 400
        return response
    transformed = transform(api_response)
    return jsonify(transformed)


def get_report_data(login_customer_id, customer_id, query):
    """
    Authenticates and queries the Google Ads reporting API

    :param login_customer_id: The ID of the account that you want to query's parent MCC
    :param customer_id: The ID of the account that you want to query
    :param query: The query string e.g. "select campaign.id from campaign"
    :return: Response JSON from the Google Ads JSON API
    """
    env_creds = get_credentials_from_environment()
    credentials = Credentials(
        None,
        refresh_token=env_creds.refresh_token,
        client_id=env_creds.client_id,
        client_secret=env_creds.client_secret,
        token_uri='https://accounts.google.com/o/oauth2/token'
    )
    credentials.refresh(Request())
    headers = {
        'Authorization': f'Bearer {credentials.token}',
        'developer-token': env_creds.developer_token,
        'login-customer-id': str(login_customer_id),
    }
    url = f'https://googleads.googleapis.com/v1/customers/{customer_id}/googleAds:search'
    response = requests.post(url, data={'query': query}, headers=headers)
    return response.json()


def get_credentials_from_environment():
    creds = namedtuple('Credentials', ['refresh_token', 'client_id', 'client_secret', 'developer_token'])
    creds.refresh_token = os.environ.get('GAQ_REFRESH_TOKEN')
    creds.client_id = os.environ.get('GAQ_CLIENT_ID')
    creds.client_secret = os.environ.get('GAQ_CLIENT_SECRET')
    creds.developer_token = os.environ.get('GAQ_DEVELOPER_TOKEN')
    return creds


def transform(results):
    """
    Transforms the Google Ads JSON response into a response which matches the
    query columns.

    :param results: Raw Google Ads JSON response
    :return: Data in the format {<column1>: value1, <column2>: value2...}
    """
    transformed = []
    field_masks = results['fieldMask'].split(',')
    for result in results['results']:
        row = {}
        for mask in field_masks:
            row[mask] = deep_get(result, mask.split('.'))

        transformed.append(row)
    return transformed


def deep_get(dictionary, keys):
    """
    Get the data out of the dictionary at the given nested key path.

    :param dictionary: Dictionary to retrieve the data from at the given keys path
    :param keys: ['a', 'b', 'c']
    :return: Value
    """
    return reduce(lambda d, key: d.get(key) if d else None, keys, dictionary)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
