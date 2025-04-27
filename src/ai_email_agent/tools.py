import base64
import re
from agents import function_tool
from ai_email_agent.connection import service
from agents import RunContextWrapper
from ai_email_agent.model import EmailAgentContext

@function_tool
def get_email_by_id(email_id: str | int) -> str:
    """
    Fetches an email by its email ID using the Gmail API.

    Args:
        email_id (str | int): The ID of the email message to fetch.

    Returns:
        str: The email body or a message indicating an error.
    """
    try:
        # Fetch the full message details using the Gmail API
        message = service.users().messages().get(userId='me', id=email_id).execute()
        
        # headers = message['payload']['headers']
        # for header in headers:

            # if header['name'] == 'From':
            #     print('Email sent from', header['value'])

            # elif header['name'] == 'Subject':
            #     print("Emails Subject", header['value'])

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
                        # print('body', body)
                        return body
                        
    except Exception as error:
        print(f"An error occurred: {error}")
        return "Failed to fetch email"

@function_tool("sir_qasim")
def sir_qasim():
    return "I am AI ENGINEER"

@function_tool("ameen")
def sir_ameen():
    return "I am CLOUD EXPERT"
