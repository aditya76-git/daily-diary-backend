class Config:
    #Flask App Secret Key
    APP_SECRET_KEY = ""

    FLASK_JWT_SECRET_KEY = ""

    SUPABASE_URL = ""

    SUPABASE_KEY = ""

    #Supabase Table Config

    USERS_TABLE_NAME = "users"
    USERS_CATEGORIES_TABLE_NAME = "categories"
    USERS_ENTRIES_TABLE_NAME = "entries"
    USERS_STREAKS_TABLE_NAME = "streaks"

    ADMIN_USERNAME = "aditya76"

    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

    GOOGLE_CLIENT_ID = ""
    
    GOOGLE_CLIENT_SECRET = ""

    # This is used to encrypt diary title and entries
    AES_SECRET = b""

    # This is the frontend html file which will be used to do the callback

    # Change http://127.0.0.1:5500 to the path where you frontend is deployed
    CLIENT_CALLBACK_REDIRECT_URL = "http://127.0.0.1:5500/callback.html"
