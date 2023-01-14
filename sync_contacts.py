

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

# Now let's get the list of contacts from the destination account
destination_contacts = destination_service.people().list(resourceName='people/me', personFields='names,emailAddresses').execute()

# Create a dictionary of destination contacts with email addresses as keys
destination_contacts_dict = {contact['emailAddresses'][0]['value']: contact for contact in destination_contacts['connections']}

# Now let's loop through the list of contacts from the source account
for contact in source_contacts['connections']:
    source_email = contact['emailAddresses'][0]['value']
    # Check if the contact already exists in the destination account
    if source_email in destination_contacts_dict:
        # Update the contact if it already exists
        destination_service.people().updateContact(resourceName=destination_contacts_dict[source_email]['resourceName'], body=contact).execute()
    else:
        # Create the contact if it doesn't exist
        destination_service.people().createContact(body=contact).execute()
