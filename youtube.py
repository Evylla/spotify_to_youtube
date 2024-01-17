import os
import time
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.errors import HttpError

scopes = ["https://www.googleapis.com/auth/youtube.readonly", "https://www.googleapis.com/auth/youtube", "https://www.googleapis.com/auth/youtube.force-ssl"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "0"

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


def you_checar_musica_na_playlist(musica, playlist_id):
    lista_id = []
    try:
        request = youtube.playlistItems().list(
            part="snippet",
            playlistId=playlist_id
        )
        response = request.execute()
        if len(response['items']) == 0:
            return True
        for i in response['items']:
            lista_id.append(i['snippet']['resourceId']['videoId'])
        if musica in lista_id:
            return False
        return True

    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")


def you_remover_musica_da_playlist(id_playlistItem):
    try:
        request = youtube.playlistItems().delete(
        body={{
            "id": id_playlistItem
            }
        }
    )
        response = request.execute()
        return response
    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")

# print(you_remover_musica_da_playlist())

def you_listar_playlists():
    try:
        lista_playlists = []
        request = youtube.playlists().list(
            part="snippet",
            mine=True
        )
        response = request.execute()
        for playlist in response['items']:
            playlist = f"nome da playlist: {playlist['snippet']['title']}\nid da playlist: {playlist['id']}"
            lista_playlists.append(playlist)
        return lista_playlists
    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")


def you_pesquisar_musica(musica):
    try:
        request = youtube.search().list(
        part="snippet",
        maxResults=20,
        q=musica
        )
        response = request.execute()
        musica_pesquisada = response["items"][0]
        return(musica_pesquisada)
    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")


def you_criar_playlist(nome_playlist):
    try:
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
    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")



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
                raise Exception("Falha ao tentar adicionar a música múltiplas vezes.")