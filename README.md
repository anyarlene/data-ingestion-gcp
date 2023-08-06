# Airtable to BigQuery ETL Pipeline

This project contains two main components:

1. ETL Logic: Hosted on Google App Engine, this component handles the extraction of data from Airtable and loads it into Google BigQuery.
2. Scheduler Logic: Using a combination of Google Cloud Functions and Google Cloud Scheduler, this component is responsible for triggering the ETL process at specified intervals.

## Setup
### Prerequisites
- Google Cloud SDK installed and initialized
- Airtable account with API access
- Google Cloud Project with billing enabled
- Enable Google App Engine, Google Secret Manager, Google Cloud Scheduler, and Google Cloud Functions for your project.

### Configuring Google Secret Manager
Store all the sensitive credentials in Google Secret Manager:

1. Airtable API Key
2. Airtable Base/Table endpoint
3. Google Cloud Project ID
4. BigQuery Credentials (if using service account-based authentication)
5. BigQuery Dataset ID and Table ID
6. App Engine URL
Use the `gcloud` command line or the GCP console to store these secrets.

### Deployment
1. Deploying the ETL Logic to App Engine:
```gcloud app deploy app_engine_etl.py```
2. Deploying the Scheduler Logic:
First, deploy the Cloud Function:

```gcloud functions deploy trigger_etl_process --runtime python310 --trigger-topic YOUR_TRIGGER_TOPIC --allow-unauthenticated``````
Then, create a Cloud Scheduler job to trigger the Cloud Function at your desired frequency:

1. Go to the Cloud Scheduler dashboard in the GCP console.
2. Click "Create job".
3. Set your desired frequency (e.g., every day at 2am would be `0 2 * * *`).
4. For the Target, choose "Pub/Sub".
For the Topic, select the Cloud Pub/Sub topic that will trigger the Cloud Function (`YOUR_TRIGGER_TOPIC`).
