import pandas as pd
import spotipy
import tkinter as tk
from spotipy.oauth2 import SpotifyClientCredentials
import math
from statistics import mode

client_id = "2414011f2fab4d93ab24db4093524758"
client_secret = "b4b85483ecac42cfa2d9e8b255137757"

sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id, client_secret))

# playlist = sp.user_playlist("Reassuring", "52KwifcwbsyxMfXUhcpMO4") # ID playlisty to ten fragment linku po ukośniku i przed znakiem zapytania
def search():
    # wyszukiwanie piosenki
    szukaj = input("Wpisz tytuł piosenki")
    results = sp.search(q=szukaj, limit=10)
    for idx, track in enumerate(results['tracks']['items']):
        print(idx, track['name'])

sp.trace=False
playlist = sp.user_playlist("2020 - IMPALA Album of the Year Award - Albums", "3lyIN15h9uVlkvPKahuOfX") # ID playlisty to ten fragment linku po ukośniku i pytajnikiem
songs = playlist["tracks"]["items"]
print("Liczba piosenek: ", len(songs))       # nie rozumiem, dlaczego na tym etapie pobiera tylko 100 piosenek z playlisty? Powinny być 283
ids = []
titles = []
artists = []

for i in range(len(songs)):
    ids.append(songs[i]["track"]["id"])
    titles.append(songs[i]["track"]["name"])
    artists.append(songs[i]["track"]["artists"])        # mam problem, żeby dogrzebać się do samej nazwy artysty, bo to jakiś słownik w liście

features = sp.audio_features(ids)
target_id = "3cyHz6vzksSQ92KEkr0wu3"
target = sp.audio_features(target_id)
odległości = []
proponowane = []
wybrane_cechy = []
print("Cześć! Mam dla Ciebie utwory, które mogą Ci się spodobać!")
k = int(input("Ile utworów mam zaproponować?\n"))
while True:
    print("Jakie cechy mam wziąć pod uwagę?")
    print("Wybierz cechy, a następnie naciśnij 'G', żeby zatwierdzić wybór")
    print("0 - danceability, 1 - energy, 2 - key, 3 - acousticness, 4 - instrumentalness, 5 - liveness, 6 - loudness, 7 - mode, 8 - speechiness, 9 - tempo, q - valence\n")
    wybor = input()
    if wybor == '0':
        wybrane_cechy.append('danceability')
    if wybor == '1':
        wybrane_cechy.append('energy')
    if wybor == '2':
        wybrane_cechy.append('key')
    if wybor == '3':
        wybrane_cechy.append('acousticness')
    if wybor == '4':
        wybrane_cechy.append('instrumentalness')
    if wybor == '5':
        wybrane_cechy.append("liveness")
    if wybor == '6':
        wybrane_cechy.append("loudness")
    if wybor == '7':
        wybrane_cechy.append("mode")
    if wybor == '8':
        wybrane_cechy.append("speechiness")
    if wybor == '9':
        wybrane_cechy.append("tempo")
    if wybor == 'q':
        wybrane_cechy.append("valence")
    elif wybor == 'g':
        break
print(wybrane_cechy)
for i in range(len(songs)):
    if 'danceability' in wybrane_cechy:
        subt_danceability = target[0]["danceability"]-features[i]["danceability"]
    else:
        subt_danceability = 0
    if 'energy' in wybrane_cechy:
        subt_energy = target[0]["energy"]-features[i]["energy"]
    else:
        subt_energy = 0
    if 'key' in wybrane_cechy:
        subt_key = target[0]["key"]-features[i]["key"]
    else:
        subt_key = 0
    if 'acousticness' in wybrane_cechy:
        subt_acousticness = target[0]["acousticness"]-features[i]["acousticness"]
    else:
        subt_acousticness = 0
    if 'instrumentalness' in wybrane_cechy:
        subt_instrumentalness = target[0]["instrumentalness"]-features[i]["instrumentalness"]
    else:
        subt_instrumentalness = 0
    if 'liveness' in wybrane_cechy:
        subt_liveness = target[0]["liveness"]-features[i]["liveness"]
    else:
        subt_liveness = 0
    if 'loudness' in wybrane_cechy:
        subt_loudness = target[0]["loudness"]-features[i]["loudness"]
    else:
        subt_loudness = 0
    if 'mode' in wybrane_cechy:
        subt_mode = target[0]["mode"]-features[i]["mode"]
    else:
        subt_mode = 0
    if 'speechiness' in wybrane_cechy:
        subt_speechiness = target[0]["speechiness"]-features[i]["speechiness"]
    else:
        subt_speechiness = 0
    if 'tempo' in wybrane_cechy:
        subt_tempo = target[0]["tempo"]-features[i]["tempo"]
    else:
        subt_tempo = 0
    if 'valence' in wybrane_cechy:
        subt_valence = target[0]["valence"]-features[i]["valence"]
    else:
        subt_valence = 0

    odległość = math.sqrt(subt_danceability**2+subt_energy**2+subt_key**2+subt_acousticness**2+subt_instrumentalness**2+subt_liveness**2+subt_loudness**2
                          +subt_mode**2+subt_speechiness**2+subt_tempo**2+subt_valence**2)
    odległości.append([round(odległość,2), features[i]["id"], titles[i], artists[i]])
odległości.sort()
print("Posortowane odległości:", odległości)
for i in range(k):
    proponowane.append(odległości[i])
print("\nOto proponowane piosenki: \n")
for utwor in proponowane:
    print("\n", utwor)
