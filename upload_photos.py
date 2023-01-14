def get_date_from_file_name(file_name):
        # Extract the date from the file name using regex or string manipulation
        # Example: if the file name is in the format "YYYY-MM-DD_photo.jpg", you can extract the date as:
        date_string = file_name.split("_")[0]
        # Parse the date string into a datetime object
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d")
        # Format the date as required by the Google Photos API (YYYY-MM-DDTHH:MM:SS.SSSZ)
        return date.isoformat() + 'Z'

def upload_photos(folder_path):
    try:
        # Authenticate and construct the Google Photos API client
        credentials = Credentials.from_authorized_user_info(info=info, scopes=["https://www.googleapis.com/auth/photoslibrary"])
        service = build('photoslibrary', 'v1', credentials=credentials)

        # Iterate through all photos in the specified folder
        for photo in os.listdir(folder_path):
            # Get the photo's file name and directory name
            file_name = os.path.basename(photo)
            directory_name = os.path.basename(os.path.dirname(photo))
            creation_date = get_date_from_file_name(file_name)
            # Open the photo file
            with open(os.path.join(folder_path, photo), 'rb') as photo_file:
                # Upload the photo to Google Photos
                body = {
                    'newMediaItems': [{
                        'description': file_name,
                        'simpleMediaItem': {
                            'fileName': file_name,
                            'uploadToken': service.mediaItems().upload(body=photo_file, mimetype='image/jpeg').execute()
                            'mediaMetadata': {
                                'creationTime': creation_date
                            }
                        }
                    }]
                }
                service.mediaItems().batchCreate(body=body).execute()

    except HttpError as error:
        print(f'An error occurred: {error}')
        raise error
