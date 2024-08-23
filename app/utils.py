import re
import hashlib
import requests
from flask_bcrypt import Bcrypt
from config import Config
from datetime import datetime
import base64
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding

def hash_password(password):
    bcrypt = Bcrypt()
    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    return password_hash


def check_password(password, password_hash):
    bcrypt = Bcrypt()
    return bcrypt.check_password_hash(password_hash, password)


def get_google_provider_cfg():
    return requests.get(Config.GOOGLE_DISCOVERY_URL).json()


def extract_emojis(text):
    # Regular expression to match emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U000024CF"
                               u"\U0001F910-\U0001F93A"
                               u"\U0001F930-\U0001F93F"
                               u"\U0001F920-\U0001F927"
                               u"\U0001F980-\U0001F991"
                               u"\U0001F9A0-\U0001F9CF"
                               u"\U0001FA00-\U0001FA6F"
                               u"\U0001FA70-\U0001FAFF"
                               "]+", flags=re.UNICODE)

    # Find all emojis in the text
    emojis = re.findall(emoji_pattern, text)

    # Split combined emojis into separate elements
    separate_emojis = [emoji for combined in emojis for emoji in combined]

    return separate_emojis



def generate_tokens(text):
    words = text.lower().split()
    return [hashlib.sha256(word.encode()).hexdigest() for word in words]


def encrypt(data):
        cipher = AES.new(Config.AES_SECRET, AES.MODE_CBC, iv=bytes([0] * 16))
        encrypted = cipher.encrypt(
            Padding.pad(data.encode(), 16)
        )
        return base64.b64encode(encrypted).decode()

def decrypt(data):
    try:
        cipher = AES.new(
            Config.AES_SECRET,
            AES.MODE_CBC,
            iv=bytes([0] * 16)
        )
        return Padding.unpad(cipher.decrypt(base64.b64decode(data)), 16).decode()
    
    except Exception as e:
        return data
    




def base64_encode(string):
    # Convert the string to bytes
    string_bytes = string.encode('utf-8')
    
    # Perform Base64 encoding
    base64_bytes = base64.b64encode(string_bytes)
    
    # Convert the result back to a string
    base64_string = base64_bytes.decode('utf-8')
    
    return base64_string



class StreakManager:
    def __init__(self, date_str):
        self.date_str = date_str

    @staticmethod
    def is_within_24hrs(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        return abs((date - now).days) <= 1

    @staticmethod
    def is_between_24_48hrs(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        return 1 < abs((date - now).days) <= 2

    @staticmethod
    def is_beyond_48hrs(date_str):
        date = datetime.strptime(date_str, "%Y-%m-%d")
        now = datetime.now()
        return abs((date - now).days) > 2


    def can_add_streak(self):
        if self.is_within_24hrs(self.date_str) or self.is_beyond_48hrs(self.date_str):
            return False
        elif self.is_between_24_48hrs(self.date_str):
            return True