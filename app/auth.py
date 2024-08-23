from oauthlib.oauth2 import WebApplicationClient
from config import Config


google_client = WebApplicationClient(Config.GOOGLE_CLIENT_ID)