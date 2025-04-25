import base64
import re
from agents import function_tool
from ai_email_agent.connection import service

@function_tool('get_email')
def get_email_by_id(message_id: str | int) -> str:
    """
    Fetches an email by its message ID using the Gmail API.

    Args:
        email_model (EmailModel): An instance of the EmailModel class containing service and message_id.

    Returns:
        str: This function prints the email details to the console, including sender, subject, and body.
    """
    try:
        # Fetch the full message details
        message = service.users().messages().get(userId='me', id=message_id).execute()
        
        # Fetch the full message details using the Gmail API
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
                        return "Successfully fetched"

        else:
            # If no parts, fallback to the main body
            body = payload['body'].get('data', '')
            if body:
                body = base64.urlsafe_b64decode(body.encode('ASCII')).decode('utf-8')
                print(f"Body: {body}")
                return "I am an else block"

    except Exception as error:
        print(f"An error occurred: {error}")
        return "Failed to fetch email"