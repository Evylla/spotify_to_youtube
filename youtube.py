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

def listar_musicas_playlist(id_playlist, nextPageToken=''):

    try:

        request = youtube.playlistItems().list(
        part= "snippet",
        playlistId= id_playlist,
        pageToken= nextPageToken,
        maxResults = 50
        )
        response = request.execute()
        
        return response

    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")
    
 
def you_listar_musicas_playlist(id_playlist):
    lista_musicas = {}
    res = listar_musicas_playlist(id_playlist)
    for i in res['items']:
        lista_musicas[i['snippet']['resourceId']['videoId']] = i['id']

    while True:
        if 'nextPageToken' in res:
            res = listar_musicas_playlist(id_playlist, nextPageToken=res['nextPageToken'])
            for i in res['items']:
                lista_musicas[i['snippet']['resourceId']['videoId']] = i['id']
        else:
            break
    
    return lista_musicas


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


def you_remover_musica_da_playlist(id_playlist_item):
    try:
        request = youtube.playlistItems().delete(
        id=id_playlist_item
        )
        response = request.execute()
        print(response)
        
    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")
    

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
            

def you_atualizar_playlist(playlist_destino_id, lista_musicas_atuais):
    lista_ids_youtube = you_listar_musicas_playlist(playlist_destino_id)
    lista_ids_musica_spotify = []
    
    try:

        ## AQUI NESSE CASO É PARA ADICIONAR AS MÚSICAS NOVAS
        for musica in lista_musicas_atuais:
            musica_id = you_pesquisar_musica(musica)
            lista_ids_musica_spotify.append(musica_id['id']['videoId'])
        for i in lista_ids_musica_spotify:
            if you_checar_musica_na_playlist(i, playlist_destino_id) == False:
                continue
            print("musica nova adicionada")
            you_inserir_musicas_na_playlist(i, playlist_destino_id)

        ## NESSE CASO É PARA REMOVER MUSICAS ANTIGAS
        for musica, id_na_playlist in lista_ids_youtube.items():
            if musica in lista_ids_musica_spotify:
                continue
            you_remover_musica_da_playlist(id_na_playlist)
            print(f"musica removida: {musica, id_na_playlist}")
        

    except HttpError as e:
        raise Exception(f"Ocorreu um erro: {e.resp.status}")
    