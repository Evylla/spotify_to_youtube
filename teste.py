url = 'http://localhost:7777/callback?code=AQDzHUJFr7vj39r3JAmctLicrXaoHlNYmITvNUWiMb1yZZ2S2beaNYmy3IohiWbsx_r6ARnaTtgGggBVlyaG_wXaoD230hs6h1BQhEeAbZYlvTC-x-oj1IoJVAhD7fft4kt58F5ST24ZB8C9JE2sKaOfOFFgIwxiSOhuH1uvdyUWcEn8tmbn3njuaI8yEiiR1r_-TGM'

index_id = url.index('=')
code = url[index_id + 1:]
print(code)
