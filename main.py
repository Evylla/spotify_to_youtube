import os
from youtube import *
from spotify import *

def main():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    escolha = input("""o que você deseja fazer?
                    \n1 - Listar playlists do spotify
                    \n2 - Listar músicas do spotify
                    \n3 - Transferir músicas curtidas do spotify para playlist no youtube
                    \n'S' - para sair""")
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
        id_playlist_destino = input("Digite o id da playlist de destino")

    

if __name__ == "__main__":
    main()