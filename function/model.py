def hello_gcs(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    file = event
    print(f"Processing file: {file['name']}.")
    import requests

    url = 'https://api.github.com/repos/bala280597/AI-Model-Application/actions/workflows/train.yml/dispatches'
    data = '{"ref":"main"}'
    x = requests.post(url, data = data,auth = ('bala280597', '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'),headers={"Accept": "application/vnd.github.v3+json"})
    print(f'API invoke sucessfully : {x.status_code}')
