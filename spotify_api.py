from dotenv import load_dotenv
import requests, os
import base64
from requests import post, get
import json



load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
redirect_uri = "https://localhost:8000/callback"

'''Authorization'''
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode(encoding="utf-8")
    auth_base64 = str(base64.b64decode(auth_bytes)) #fix problem

    api_url = "https://accounts.spotify.com/api/token"
    headers = {
        # "Authorization": "Basic " + auth_base64,
        "Authorization": "Basic ",
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(api_url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


token = "BQA_itvHGHMETOHPFVnGf3VL8W71vT0l9gekqXevIz6xyMVQLKI3Fldl_p1P1eqHjVS8IX3neXIKtCUIjSjwF3dxFhNgpIs6BjOS1K_edAuy0Twy7-o"

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

'''Search Artist'''
def search_artist(token, artist_name):
    api_url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f'?q={artist_name}&type=artist&limit=1'

    query_url = api_url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]['items']

    if len(json_result) == 0:
        print("No artist")
        return None
    return json_result[0]

'''Get Top 10 Tracks'''
def get_songs_from_artist(token, artist_id):
    api_url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(api_url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

'''Create Playlist on Spotify'''
def create_playlist_on_spotify(name, description, public):
    api_url = "https://api.spotify.com/v1/users/22b7o67nitwh5375vtdc4stxq/playlists"
    headers = get_auth_header(token)
    data = {
        "name": name,
        "description": description,
        "public": public
    }
    result = post(api_url, headers=headers, data=data)
    json_result = json.loads(result.content)
    return json_result

'''Requests'''
#token = get_token()

result = search_artist(token, "Set it off")
artist_id = result["id"]
songs = get_songs_from_artist(token, artist_id)

for idx, song in enumerate(songs):
    print(f"{idx + 1}.{song['name']}")

make_playlist = create_playlist_on_spotify("Tops", "Top 10 Tracks from your Favorite Artist", False)
print(f"Playlist: {make_playlist}")