from langchain_google_community.gmail.utils import build_resource_service, get_gmail_credentials
import os
from dotenv import load_dotenv

load_dotenv()



class AuthGmailToolKit():

    def __init__(self):
        self.tools= []
        self.authentication()
        self.api_resource= build_resource_service(credentials=self.credentials)

    def authentication(self):
        self.credentials= get_gmail_credentials(
            token_file="token.json",
            scopes=[os.getenv("SCOPES_EMAIL")],
            client_secrets_file= os.getenv("PATH_TO_CREDENTIALS_OAuth_2_0"),
        )

