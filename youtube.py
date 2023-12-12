import os
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = {"installed":{"client_id":"1068298087577-fh38aj01t8l4jsg8ful5ggm7u2bdg2gk.apps.googleusercontent.com","project_id":"spot-to-you-407121","auth_uri":"https://accounts.google.com/o/oauth2/auth","token_uri":"https://oauth2.googleapis.com/token","auth_provider_x509_cert_url":"https://www.googleapis.com/oauth2/v1/certs","client_secret":"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","redirect_uris":["http://localhost"]}}

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

musica = you_pesquisar_musica("Stephen Sanchez - Mountain Peaks")
print(musica['id']['videoId'])

def you_criar_playlist(nome_playlist):

    request = youtube.playlists().insert(
    part="snippet",
    body={
        "snippet": {
        "title": nome_playlist
        }
    }
    )
    response = request.execute()

    return response['id']

print(you_criar_playlist('teste2'))

def you_inserir_musicas_na_playlist(musica, playlist_id):
    max_tentativas = 5
    tentativas = 0
    while tentativas < max_tentativas:
        try:
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
            return response
        except HttpError as e:
            if e.resp.status == 409 and 'SERVICE_UNAVAILABLE' in str(e):
                tentativas += 1
                time.sleep(5)
            else:
                raise Exception("Failed to add the song to the playlist after multiple retries.")

    print(response)
