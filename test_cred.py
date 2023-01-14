
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build



import google.oauth2.credentials

import google_auth_oauthlib.flow

from google.oauth2 import service_account



auth_credentials = service_account.Credentials.from_service_account_info(credentials)

source_service = build('people', 'v1', credentials=auth_credentials)
source_contacts = source_service.people().list(resourceName='people/me', personFields='names,emailAddresses').execute()

for contact in source_contacts['connections']:
    print(contact)