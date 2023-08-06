import requests
from google.cloud import secretmanager

# Setup Secret Manager client
secret_client = secretmanager.SecretManagerServiceClient()

# Fetch all required secrets from Secret Manager
def fetch_secret(secret_name):
    secret_version = f"projects/{project_id}/secrets/{secret_name}/versions/latest"
    return secret_client.access_secret_version(name=secret_version).payload.data.decode('UTF-8')

project_id = fetch_secret("project_id")
APP_ENGINE_URL = fetch_secret("app_engine_url")

def trigger_etl_process(data, context):
    """Cloud Function to be triggered by Cloud Scheduler.
    This function sends a request to the App Engine service to start the ETL process.
    """
    response = requests.post(APP_ENGINE_URL)
    
    if response.status_code == 200:
        return f"Triggered ETL process: {response.json()}"
    else:
        return f"Failed to trigger ETL process: {response.text}", 500
