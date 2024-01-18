import os
from youtube import *
from spotify import *

def main():
    try:
        n = [0, 1, 2, 3, 4, 5, 6]
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

        escolha = input("""\n\nO que você deseja fazer?
                        \n1 - Listar playlists do spotify
                        \n2 - Listar músicas do spotify
                        \n3 - Listar músicas de uma playlist do spotify
                        \n4 - Transferir músicas de uma playlist no spotify para uma playlist no youtube
                        \n5 - Listar playlists do youtube
                        \n6 - Atualizar playlist já existente
                        \n0 - para sair\n\n""")
        
        if int(escolha) not in n:
            print("Por favor escolha uma das opções:\n")
            main()

        if int(escolha.upper()) == 0:
            print("Tchau!")
            raise SystemExit
        
        elif int(escolha) == 1:
            nome_usuario = input("Digite seu nome de usuário: ")
            response_playlists = spot_listar_playlists(nome_usuario)
            for i in response_playlists:
                print(i)

        elif int(escolha) == 2:
            musicas = spot_listar_musicas()
            for i in musicas:
                print(i)

        elif int(escolha) == 3:
            id_playlist = input("""ID da playlist: 
                                \nSe você não souber o ID da playlist pressione '0', volte para o menu inicial e use uma das opções para listar suas playlists e pegar o ID da playlist desejada.\n""")
            if id_playlist == '0':
                main()
            else:
                musicas = spot_listar_musicas_playlist(id_playlist)
                for i in musicas:
                    print(i)

        elif int(escolha) == 4:
            res = input("A playlist destino já existe no youtube?\n1 - Sim\n2 - Não\nSe você não souber o ID da playlist pressione '0', volte para o menu inicial e use uma das opções para listar suas playlists e pegar o ID da playlist desejada.\n")
            if int(res) == 0:
                main()

            elif int(res) == 1:
                id_playlist_destino = input("ID da playlist no youtube: ")
                id_playlist_spotify = input("ID da playlist no spotify: ")
                musicas_spot = spot_listar_musicas_playlist(id_playlist_spotify)
                for i in musicas_spot:
                    new_musica = you_pesquisar_musica(i)
                    if you_checar_musica_na_playlist(new_musica['id']['videoId'], id_playlist_destino) == False:
                        print("não inserida")
                        continue
                    you_inserir_musicas_na_playlist(new_musica['id']['videoId'], id_playlist_destino)
                    print("inserida")
                        

            elif int(res) == 2:
                nome_playlist = input("Vamos criar uma nova. Dê um nome para ela: ")
                id_nova_playlist = you_criar_playlist(nome_playlist)
                id_playlist_spotify = input("ID da playlist no spotify: ")
                # print(f'id: {id_nova_playlist}')
                musicas_spot = spot_listar_musicas_playlist(id_playlist_spotify)
                for i in musicas_spot:
                    new_musica = you_pesquisar_musica(i)
                    if you_checar_musica_na_playlist(new_musica['id']['videoId'], id_nova_playlist) == False:
                        continue
                    you_inserir_musicas_na_playlist(new_musica['id']['videoId'], id_nova_playlist)
                    
        elif int(escolha) == 5:
            lista_playlists = you_listar_playlists()
            for i in lista_playlists:
                print(i)

        elif int(escolha) == 6:
            id_playlist_no_youtube = input("Digite o id da playlist no youtube: ")
            id_playlist_no_spotify = input("Digite o id da playlist no spotify: ")
            you_atualizar_playlist(id_playlist_no_youtube, spot_listar_musicas_playlist(id_playlist_no_spotify))

    except Exception:
        print("Houve um erro")
        main()

if __name__ == "__main__":
    while True:
        main()