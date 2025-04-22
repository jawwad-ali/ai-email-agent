from googleapiclient.errors import HttpError
import base64
import re
from connection import service

def main():
  """Shows basic usage of the Gmail API.
  Lists the user's Gmail labels.
  """
  

#   try:
#     # Call the Gmail API
#     service = build("gmail", "v1", credentials=creds)
#     results = service.users().labels().list(userId="me").execute()
#     labels = results.get("labels", [])

#     if not labels:
#       print("No labels found.")
#       return
#     print("Labels:")
#     for label in labels:
#       print(label["name"])

#   except HttpError as error:
#     # TODO(developer) - Handle errors from gmail API.
#     print(f"An error occurred: {error}")


############ Email
def get_message(service, message_id):
    try:
        # Fetch the full message details
        message = service.users().messages().get(userId='me', id=message_id).execute()

        # Print basic message details (headers)
        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'From':
                print(f"From: {header['value']}")
            elif header['name'] == 'Subject':
                print(f"Subject: {header['value']}")
        
        # Get the payload of the email
        payload = message['payload']
        body = None
        
        # Check if the email is multipart (i.e., has parts like text, HTML, attachments)
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':  # Check for plain text
                    body = part['body'].get('data', '')
                    if body:
                        body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8')
                        print(f"Plain Text Body: {body}")

        else:
            # If no parts, fallback to the main body
            body = payload['body'].get('data', '')
            if body:
                body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8')
                print(f"Body: {body}")
    
    except Exception as error:
        print(f"An error occurred: {error}")

# Function to clean HTML content by removing HTML tags
def clean_html(html_content):
    # Remove the HTML tags using regular expressions
    clean_text = re.sub(r'<.*?>', '', html_content)
    return clean_text

if __name__ == "__main__":
    get_message(service, '1965e455ddac2e05')
    main()