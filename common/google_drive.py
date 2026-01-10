import os
import functools
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from pathlib import Path
from config import GOOGLE_DRIVE_ROOT_FOLDER_ID


def handle_broken_pipe_error(max_retries=3):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(self, *args, **kwargs)
                except BrokenPipeError as bpe:
                    print(f"Caught BrokenPipeError: {bpe}")
                    retries += 1
                    self.authenticate()
            else:
                raise

        return wrapper

    return decorator


class GoogleDriveWrapper:
    def __init__(self):
        self.service_account_key_path = Path(os.getcwd(), 'google_client_secret.json').__str__()
        self.credentials = None
        self.drive_service = None
        self.root_folder_id = GOOGLE_DRIVE_ROOT_FOLDER_ID
        self.authenticate()

    def authenticate(self) -> None:
        self.credentials = service_account.Credentials.from_service_account_file(
            self.service_account_key_path,
            scopes=['https://www.googleapis.com/auth/drive'],
        )

        self.credentials.refresh(Request())
        self.drive_service = build('drive', 'v3', credentials=self.credentials)

    @handle_broken_pipe_error(max_retries=3)
    def upload_file(self, folder_id, file_path) -> str:
        file_metadata = {'name': os.path.basename(file_path), 'parents': [folder_id]}
        media = MediaFileUpload(file_path, mimetype='application/octet-stream')

        try:
            uploaded_file = self.drive_service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()

            print(f'File uploaded with ID: {uploaded_file["id"]}')
            return uploaded_file["id"]
        except Exception as e:
            print(f'Error uploading file: {e}')
            return ''

    def list_root_files(self) -> list:
        return self.list_files(self.root_folder_id)

    @handle_broken_pipe_error(max_retries=3)
    def download_file(self, file_id, destination_path) -> None:
        request = self.drive_service.files().get_media(fileId=file_id)
        with open(destination_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            try:
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f'Download {int(status.progress() * 100)}%.')
            except Exception as e:
                print(f'Error downloading file: {e}')

    @handle_broken_pipe_error(max_retries=3)
    def create_folder(self, folder_name: str) -> str:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': ['root']
        }

        try:
            folder = self.drive_service.files().create(
                body=folder_metadata,
                fields='id'
            ).execute()
            print(f'✅ Folder created: {folder_name} → ID: {folder["id"]}')
            return folder['id']
        except Exception as e:
            print(f'❌ Error creating folder: {e}')
            return ''

    @handle_broken_pipe_error(max_retries=3)
    def share_file(self, file_id: str, email: str, role: str = "writer"):
        permission = {
            'type': 'user',
            'role': role,  # 'reader', 'writer', or 'commenter'
            'emailAddress': email
        }
        try:
            self.drive_service.permissions().create(
                fileId=file_id,
                body=permission,
                sendNotificationEmail=False,  # Optional: skip email
                fields='id'
            ).execute()
            print(f"✅ Access granted to {email} for file {file_id}")
        except Exception as e:
            print(f"❌ Error sharing file: {e}")

    @handle_broken_pipe_error(max_retries=3)
    def list_files(self, folder_id: str) -> list:
        results = self.drive_service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields='files(id, name, mimeType)'
        ).execute()

        files = results.get('files', [])
        return files

    @handle_broken_pipe_error(max_retries=3)
    def remove_file(self, file_id) -> None:
        try:
            self.drive_service.files().delete(fileId=file_id).execute()
            print(f'File with ID {file_id} deleted successfully.')
        except Exception as e:
            print(f'Error deleting file: {e}')
