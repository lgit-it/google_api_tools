from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# First, let's build the service object for the source account
source_creds = Credentials.from_authorized_user_info(info=source_user_info)
source_service = build('people', 'v1', credentials=source_creds)



# Now let's build the service object for the destination account
destination_creds = Credentials.from_authorized_user_info(info=destination_user_info)
destination_service = build('people', 'v1', credentials=destination_creds)

# Now let's get the list of contacts from the source account
source_contacts = source_service.people().list(resourceName='people/me', personFields='names,emailAddresses').execute()

# Now let's loop through the list of contacts and create them in the destination account
for contact in source_contacts['connections']:
    destination_service.people().createContact(body=contact).execute()
