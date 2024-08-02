from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your actual Notion integration details
NOTION_DATABASE_ID = 'your_notion_database_id'
NOTION_API_TOKEN = 'your_notion_api_token'
NOTION_API_URL = 'https://api.notion.com/v1/pages'

# Headers for Notion API requests
NOTION_HEADERS = {
    'Authorization': f'Bearer {NOTION_API_TOKEN}',
    'Content-Type': 'application/json',
    'Notion-Version': '2021-08-16',  # Use the correct Notion API version
}

def create_notion_page(data):
    notion_data = {
        'parent': {'database_id': NOTION_DATABASE_ID},
        'properties': {
            'Name': {'title': [{'text': {'content': data.get('name', '')}}]},
            'Email': {'rich_text': [{'text': {'content': data.get('email', '')}}]},
            'Message': {'rich_text': [{'text': {'content': data.get('message', '')}}]},
        }
    }
    response = requests.post(NOTION_API_URL, headers=NOTION_HEADERS, json=notion_data)
    return response

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400

    # Example of extracting data; adjust based on your Webflow form fields
    name = data.get('name')
    email = data.get('email')
    message = data.get('message')

    # Send data to Notion
    notion_response = create_notion_page({
        'name': name,
        'email': email,
        'message': message
    })

    if notion_response.status_code == 200:
        return jsonify({'status': 'Success'}), 200
    else:
        return jsonify({'error': 'Failed to create page in Notion'}), notion_response.status_code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
