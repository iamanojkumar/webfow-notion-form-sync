import requests
import json

# Replace these with your actual Webflow API details
WEBFLOW_API_TOKEN = 'b715a9cb0438b135cc22966f76f66613895db0b3c28e28294b05a7469b266fe2'
SITE_ID = '660844f8e825fc2c6025e172'
FORM_ID = '66ace0dfed1fd71b421f01e5'

# Replace these with your actual Notion API details
NOTION_DATABASE_ID = 'e40af1dba4be4b40b93a95a5eb662f45'
NOTION_API_TOKEN = 'secret_EU6lsUCuIMro9cCy0NE54BJLuE7nkKamQoNUIh3Bgfj'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

# Headers for Webflow API requests
WEBFLOW_HEADERS = {
    'Authorization': f'Bearer {WEBFLOW_API_TOKEN}',
    'accept': 'application/json'
}

# Headers for Notion API requests
NOTION_HEADERS = {
    'Authorization': f'Bearer {NOTION_API_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'  # Use the correct Notion API version
}

def get_webflow_form_submissions():
    url = f'https://api.webflow.com/v2/forms/{FORM_ID}/submissions'
    response = requests.get(url, headers=WEBFLOW_HEADERS)
    response.raise_for_status()
    return response.json()

def create_notion_page(submission):
    form_response = submission.get('formResponse', {})
    name = form_response.get('Name', 'No Name')
    email = form_response.get('Email', 'No Email')
    
    notion_data = {
        'parent': {'database_id': NOTION_DATABASE_ID},
        'properties': {
            'Name': {  # Assuming 'Name' is a title property
                'title': [
                    {'text': {'content': name}}
                ]
            },
            'Email': {  # Assuming 'Email' is a property of type email
                'email': email
            }
        }
    }
    response = requests.post(NOTION_API_URL, headers=NOTION_HEADERS, json=notion_data)
    print(f"Notion API Response: {response.status_code} - {response.text}")  # Debug: Print Notion API response
    return response

# Fetch Webflow form submissions
try:
    form_submissions = get_webflow_form_submissions()
    print("Fetched Form Submissions:", json.dumps(form_submissions, indent=2))  # Debug: Pretty print fetched submissions
except requests.exceptions.HTTPError as e:
    print(f"HTTP error occurred: {e}")

# Process each submission and send it to Notion
for submission in form_submissions.get('formSubmissions', []):
    print("Processing Submission:", json.dumps(submission, indent=2))  # Debug: Pretty print each submission being processed
    notion_response = create_notion_page(submission)
    if notion_response.status_code == 200:
        print(f'Successfully added submission to Notion: {submission.get("id")}')
    else:
        print(f'Failed to add submission to Notion: {submission.get("id")}, Error: {notion_response.text}')
