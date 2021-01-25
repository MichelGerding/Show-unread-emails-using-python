from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    GMAIL = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = GMAIL.users().messages().list(userId="me", q='label:unread').execute()
    messages = results.get('messages');

    for msg in messages:
        txt = GMAIL.users().messages().get(userId='me', id=msg['id']).execute();

        # print(txt)
        try:
            payload = txt['payload']
            headers = payload['headers']

            for d in headers:
                if d['name'] == 'Subject':
                    subject = d['value']
                if d['name'] == 'From':
                    sender = d['value']
                if d['name'] == 'To':
                    reciever = d['value']
                
                

            print("Subject: ", subject) 
            print("To: ", reciever) 
            print("From: ", sender)
            print("-"*20)
        except:
            pass

if __name__ == '__main__':
    main()