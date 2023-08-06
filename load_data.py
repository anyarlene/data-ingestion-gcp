from flask import Flask, jsonify
import requests
from google.cloud import bigquery, secretmanager
import json

app = Flask(__name__)

# Setup Secret Manager client
secret_client = secretmanager.SecretManagerServiceClient()

# Fetch all required secrets from Secret Manager
def fetch_secret(secret_name):
    secret_version = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    return secret_client.access_secret_version(name=secret_version).payload.data.decode('UTF-8')

project_id = fetch_secret("project_id")

# Fetch Airtable API Key and Base/Table
airtable_api_key = fetch_secret("airtable_api_key")
airtable_base_table = fetch_secret("airtable_base_table")
AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{airtable_base_table}"
AIRTABLE_HEADERS = {
    "Authorization": f"Bearer {airtable_api_key}"
}

# Fetch BigQuery Credentials, Dataset ID, and Table ID
bigquery_credentials = json.loads(fetch_secret("bigquery_credentials"))
BIGQUERY_DATASET_ID = fetch_secret("bigquery_dataset_id")
BIGQUERY_TABLE_ID = fetch_secret("bigquery_table_id")
bigquery_client = bigquery.Client(credentials=bigquery_credentials)

@app.route('/transfer', methods=['GET', 'POST'])
def transfer_data():
    # Fetch records from Airtable
    response = requests.get(AIRTABLE_ENDPOINT, headers=AIRTABLE_HEADERS)
    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch data from Airtable"}), 500
    records = response.json().get('records', [])

    # Process and insert data to BigQuery
    rows_to_insert = [record['fields'] for record in records]
    
    if rows_to_insert:
        table_ref = bigquery_client.dataset(BIGQUERY_DATASET_ID).table(BIGQUERY_TABLE_ID)
        errors = bigquery_client.insert_rows_json(table_ref, rows_to_insert)
        if errors:
            return jsonify({"error": errors}), 500
    
    return jsonify({"status": "Data transferred successfully", "record_count": len(rows_to_insert)}), 200

if __name__ == "__main__":
    app.run(port=8080, debug=True)
