import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "client_secret.json"

# Get credentials and create an API client
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(client_secrets_file, scopes)
credentials = flow.run_local_server(port=0)
youtube = googleapiclient.discovery.build(api_service_name, api_version, credentials=credentials)

request = youtube.playlists().list(
        part="id,contentDetails,snippet",
        mine=True
    )
response = request.execute()
lista = response['items']


def you_listar_playlists():
    for playlist in lista:
        print(f"nome da playlist: {playlist['snippet']['title']}")
        print(f"id da playlist: {playlist['id']}")

def you_pesquisar_musica(musica):
    request = youtube.search().list(
    part="snippet",
    maxResults=20,
    q=musica
    )
    response = request.execute()
    musica_pesquisada = response["items"][0]

    return(musica_pesquisada)


def you_inserir_musicas_na_playlist(musica, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            "snippet": {
            "playlistId": playlist_id,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": musica
            }
            }
        }
    )
    response = request.execute()

    print(response)

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    print(you_inserir_musicas_na_playlist("QUwxKWT6m7U"))
    

if __name__ == "__main__":
    main()