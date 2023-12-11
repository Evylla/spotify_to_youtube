import os
from youtube import *
from spotify import *

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    escolha = input("""o que você deseja fazer?
                    \n1 - Listar playlists do spotify
                    \n2 - Listar músicas do spotify
                    \n3 - Listar músicas de uma playlist do spotify
                    \n4 - Transferir músicas de uma playlist no spotify para uma playlist no youtube
                    \n'S' - para sair\n\n""")
    if escolha.upper() == 'S':
        print("Tchau!")
        SystemExit
    elif escolha == '1':
        nome_usuario = input("Digite seu nome de usuário: ")
        print(spot_listar_playlists(nome_usuario))
    elif escolha == '2':
        musicas = spot_listar_musicas()
        for i in musicas:
            print(i)
    elif escolha == '3':
        id_playlist = input("ID da playlist: ")
        musicas = spot_listar_musicas_playlist(id_playlist)
        for i in musicas:
            print(i)
    elif escolha == '4':
        res = input("A playlist destino já existe no youtube?\n1 - Sim\n2 - Não\n")
        if res == '1':
            id_playlist_destino = input("ID da playlist no youtube: ")
            id_playlist_spotify = input("ID da playlist no spotify: ")
            musicas_spot = spot_listar_musicas_playlist(id_playlist_spotify)
            for i in musicas_spot:
                new_musica = you_pesquisar_musica(i)
                you_inserir_musicas_na_playlist(new_musica['id']['videoId'], id_playlist_destino)
                print(f"inserindo: {new_musica}")
    

if __name__ == "__main__":
    main()