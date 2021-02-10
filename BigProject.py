import pandas as pd
import spotipy
import math
from tkinter import *
from spotipy.oauth2 import SpotifyClientCredentials
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from statistics import mode

client_id = "2414011f2fab4d93ab24db4093524758"
client_secret = "b4b85483ecac42cfa2d9e8b255137757"
sp = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id, client_secret))

def obliczanie_odleglosci():
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
        odległości.append([round(odległość,2), features[i]["id"], titles[i], artists[i][0]["name"]])
    odległości.sort()

def potwierdzenie():
    obliczanie_odleglosci()
    k = int(pole_tekstowe.get())
    pole_tekstowe.delete(0, 'end')
    print("Posortowane odległości:", odległości)
    for i in range(k):
        proponowane.append(odległości[i])
    print("\nOto proponowane piosenki: \n")
    for utwor in proponowane:
        print("\n", utwor)

def button1_action():
    button1.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('danceability')

def button2_action():
    button2.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('energy')

def button3_action():
    button3.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('key')

def button4_action():
    button4.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('acousticness')

def button5_action():
    button5.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('instrumentalness')

def button6_action():
    button6.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('liveness')

def button7_action():
    button7.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('loudness')

def button8_action():
    button8.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('mode')

def button9_action():
    button9.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('speechiness')

def button10_action():
    button10.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('tempo')

def button11_action():
    button11.config(relief=SUNKEN, state=DISABLED)
    wybrane_cechy.append('valence')

def reset():
    button1.config(relief=RAISED, state=NORMAL)
    button2.config(relief=RAISED, state=NORMAL)
    button3.config(relief=RAISED, state=NORMAL)
    button4.config(relief=RAISED, state=NORMAL)
    button5.config(relief=RAISED, state=NORMAL)
    button6.config(relief=RAISED, state=NORMAL)
    button7.config(relief=RAISED, state=NORMAL)
    button8.config(relief=RAISED, state=NORMAL)
    button9.config(relief=RAISED, state=NORMAL)
    button10.config(relief=RAISED, state=NORMAL)
    button11.config(relief=RAISED, state=NORMAL)
    wybrane_cechy.clear()
    proponowane.clear()
    odległości.clear()
# playlist = sp.user_playlist("Reassuring", "52KwifcwbsyxMfXUhcpMO4") # ID playlisty to ten fragment linku po ukośniku i przed znakiem zapytania
# def search():
#     # wyszukiwanie piosenki
#     szukaj = input("Wpisz tytuł piosenki")
#     results = sp.search(q=szukaj, limit=10)
#     for idx, track in enumerate(results['tracks']['items']):
#         print(idx, track['name'])

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
    artists.append(songs[i]["track"]["artists"])

features = sp.audio_features(ids)
target_id = "3cyHz6vzksSQ92KEkr0wu3"
target = sp.audio_features(target_id)
odległości = []
proponowane = []
wybrane_cechy = []
licznik_cech = len(wybrane_cechy)

nest = Tk()
nest.title("Likeable songs")
nest.geometry("1200x600")
nest.config(bg="NavajoWhite1")

left_frame1= Frame(nest, width = 200, height = 75, bg = "powderblue")
left_frame1.grid(row = 0, column = 0, padx = 25, pady = 25)

left_frame2 = Frame(nest, width = 200, height = 450, bg="powderblue")
left_frame2.grid(row = 1, column = 0, padx = 25)

mid_frame1 = Frame(nest, width = 200, height = 75, bg = "powderblue")
mid_frame1.grid(row = 0, column = 1, padx = 25, pady = 25)

mid_frame2 = Frame(nest, width = 400, height = 450, bg = "powderblue")
mid_frame2.grid(row = 1, column = 1)

cechy = Label(left_frame1, text ="Cechy", relief=RAISED, width = 15, height = 2, font=("Arial", 14))
cechy.grid(padx = 27, pady = 10)

wybor_knn = Label(mid_frame1, text="Ile piosenek zaproponować?", width = 30, font=("Arial", 14))
wybor_knn.grid(row = 0, column = 1, padx = 25, pady=1)

pole_tekstowe = Entry (mid_frame1)
pole_tekstowe.grid(row = 1, column = 1)

button_submit= Button(mid_frame1, text="Zatwierdź", command = potwierdzenie)
button_submit.grid(row=2, column = 1)
button1 = Button(left_frame2, text="danceability", width = 15,  font=("Arial", 12), command = button1_action)
button1.grid(row = 1, column = 0, padx = 40, pady=3)
button2 = Button(left_frame2, text="energy", width = 15, font=("Arial", 12), command = button2_action)
button2.grid(row = 2, column = 0, padx = 0, pady=3)
button3 = Button(left_frame2, text="key", width = 15, font=("Arial", 12), command = button3_action)
button3.grid(row = 3, column = 0, padx = 0, pady=3)
button4 = Button(left_frame2, text="acousticness", width = 15, font=("Arial", 12), command = button4_action)
button4.grid(row = 4, column = 0, padx = 0, pady=3)
button5 = Button(left_frame2, text="instrumentalness", width = 15, font=("Arial", 12), command = button5_action)
button5.grid(row = 5, column = 0, padx = 0, pady=3)
button6 = Button(left_frame2, text="liveness", width = 15,  font=("Arial", 12), command = button6_action)
button6.grid(row = 6, column = 0, padx = 0, pady=3)
button7 = Button(left_frame2, text="loudness", width = 15, font=("Arial", 12), command = button7_action)
button7.grid(row = 7, column = 0, padx = 0, pady=3)
button8 = Button(left_frame2, text="mode", width = 15, font=("Arial", 12), command = button8_action)
button8.grid(row = 8, column = 0, padx = 0, pady=3)
button9 = Button(left_frame2, text="speechiness", width = 15, font=("Arial", 12), command = button9_action)
button9.grid(row = 9, column = 0, padx = 0, pady=3)
button10 = Button(left_frame2, text="tempo", width = 15, font=("Arial", 12), command = button10_action)
button10.grid(row = 10, column = 0, padx = 0, pady=3)
button11 = Button(left_frame2, text="valence", width = 15,  font=("Arial", 12), command = button11_action)
button11.grid(row = 11, column = 0, padx = 0, pady=3)
reset_button = Button(left_frame2, text = "reset", width = 15, bg="indian red", font=("Arial", 12), command=reset)
reset_button.grid(row=12, column = 0, pady=3)

nest.mainloop()
