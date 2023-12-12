import requests
import base64
from urllib.parse import urlencode
import webbrowser
from settings import *

client_id = SPOTIFY_CLIENT_ID
client_secret = SPOTIFY_SECRET_KEY
auth_header = base64.urlsafe_b64encode(f'{client_id}:{client_secret}'.encode('ascii'))
scope = 'playlist-read-collaborative user-library-read playlist-read-private'

url_tracks = 'https://api.spotify.com/v1/me/tracks'

# PEGANDO O CÓDIGO
def get_code():
    link_autorizacao = "https://accounts.spotify.com/authorize?"
    auth_headers = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": "http://localhost:7777/callback",
        "scope": scope,
        "show_dialog": True
    }
   
    # r_code = requests.get(link_autorizacao + urlencode(auth_headers))
    # code = r_code.json()

    webbrowser.open(link_autorizacao + urlencode(auth_headers))
    url = input("cole a url aqui: ")
    index_id = url.index('=')
    code = url[index_id + 1:]
    return code


code = get_code()

token_headers = {
    'Authorization': f'Basic {auth_header.decode("ascii")}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

token_data = {
    "grant_type": "authorization_code",
    "code": code,
    "redirect_uri": "http://localhost:7777/callback"
}

TOKEN_URL = 'https://accounts.spotify.com/api/token'

# Make a request to the /token endpoint to get an access token
access_token_request = requests.post(url=TOKEN_URL, data=token_data, headers=token_headers)
access_token_response_data = access_token_request.json()
access_token = access_token_response_data['access_token']

user_headers = {
    "Authorization": "Bearer " + access_token,
    "Content-Type": "application/json"
}

user_params = {
    "limit": 50,
}

def spot_listar_playlists(user_id, user_headers=user_headers, user_params=user_params):
    
    url_playlists = f"https://api.spotify.com/v1/users/{user_id}/playlists"
    playlists = requests.get(url_playlists, headers=user_headers, params=user_params)
    response_playlists = playlists.json()
    limite = response_playlists['total']
    lista_playlists = []
    offset = 0
    continuar = True

    while continuar:

        if response_playlists['next'] == None:
            continuar = False
            user_params = {"offset": offset, "limit": (limite - offset)}
            playlists = requests.get(url_playlists, headers=user_headers, params=user_params)
            for item in response_playlists["items"]:
                playlist = (f"nome: {item['name']} musicas: {item['tracks']['total']}\n{item['id']}")
                lista_playlists.append(playlist)
            return lista_playlists
        else:
            for item in response_playlists["items"]:
                playlist = (f"nome: {item['name']} musicas: {item['tracks']['total']}\n{item['id']}")
                lista_playlists.append(playlist)
            playlists = requests.get(url_playlists, headers=user_headers, params=user_params)
            response_playlists = playlists.json()
            offset += 50
            print(f"{offset} playlists")
    return lista_playlists


def spot_listar_musicas_playlist(playlist_id, user_headers=user_headers, user_params=user_params):
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"
    r = requests.get(url, headers=user_headers, params=user_params)
    response = r.json()
    limite = response['total']
    lista = []
    offset = 0
    continuar = True
    while continuar:
        if response['next'] == None:
            continuar = False
            user_params = {"offset": offset, "limit": (limite - offset)}
            r = requests.get(url, headers=user_headers, params=user_params)
            for item in response["items"]:
                for artist in item['track']['artists']:
                    nome = artist['name']
                musica = f"{item['track']['name']} - {nome}"
                lista.append(musica)
            return lista
        else:
            for item in response["items"]:
                for artist in item['track']['artists']:
                    nome = artist['name']
                musica = f"{item['track']['name']} - {nome}"
                lista.append(musica)
            r = requests.get(response_tracks['next'], headers=user_headers, params=user_params)
            response_tracks = r.json()
            offset += 50
            print(f"{offset} músicas")
    return lista

def spot_listar_musicas(user_headers=user_headers, user_params=user_params):

    tracks = requests.get(url_tracks, headers=user_headers, params=user_params)
    response_tracks = tracks.json()
    limite = response_tracks['total']
    lista_musicas = []
    offset = 0
    continuar = True
    while continuar:

        if response_tracks['next'] == None:
            continuar = False
            user_params = {"offset": offset, "limit": (limite - offset)}
            r = requests.get(url_tracks, headers=user_headers, params=user_params)
            for item in response_tracks["items"]:
                for artist in item['track']['artists']:
                    nome = artist['name']
                musica = f"nome: {item['track']['name']} - artista: {nome}"
                lista_musicas.append(musica)
            return lista_musicas
        else:
            for item in response_tracks["items"]:
                for artist in item['track']['artists']:
                    nome = artist['name']
                musica = f"nome: {item['track']['name']} - artista: {nome}"
                lista_musicas.append(musica)
            r = requests.get(response_tracks['next'], headers=user_headers, params=user_params)
            response_tracks = r.json()
            offset += 50
            print(f"{offset} músicas")
    return lista_musicas
