import base64
from agents import RunContextWrapper
from .model import EmailAgentContext
from .connection import service

async def on_email_summarize_handoff(context: RunContextWrapper[EmailAgentContext]):

    try:
        # Assuming email_id is part of context, retrieve it from context
        from .main import email_id
        message = service.users().messages().get(userId='me', id = email_id).execute()
        # message = service.users().messages().get(userId='me', id="1967078900308559").execute()

        context.context.receiver = message['payload']['headers'][0]['value']

        headers = message['payload']['headers']
        for header in headers:
            if header['name'] == 'From':
                context.context.sender = header['value']
                # context.context.sender = header['value']
                # print('Email Sender Context', context.context.sender)
            
            elif header['name'] == 'Subject':
                context.context.subject =  header['value']
                # print(f"Email Subject Context: {context.context.subject}")

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
                        context.context.body = body
                        # print('Email Body Context <===========>', context.context.body)

        print('Context at last', context.context)

    except Exception as error:
        print(f"An error occurred: {error}")
        return "Failed to fetch email"