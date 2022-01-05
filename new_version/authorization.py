
import tekore as tk

def authorize():
     CLIENT_ID = "2afef6b7aa8741d7965c4c2bff76cd80"
     CLIENT_SECRET = "24fadda8993d47e7bf555217479fddbf"
     app_token = tk.request_client_token(CLIENT_ID, CLIENT_SECRET)
     return tk.Spotify(app_token)
