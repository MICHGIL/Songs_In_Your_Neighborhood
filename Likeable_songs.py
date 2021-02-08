import pandas as pd
import spotipy
import math
import numpy as np
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

class SampleApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.state("zoomed")
        self.title("Likeable songs")
        # self.geometry("1500x800")
        self.config(bg="midnight blue")
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        """Destroys current frame and replaces it with a new one."""
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.grid()

class StartPage(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=1920, height = 1080, bg = "midnight blue")
        self.stworzWidgety()

    def stworzWidgety(self):
        start_frame = Frame(self, width = 1150, height = 580, bg = "powderblue")
        start_frame.place(x = 200, y = 100)
        nazwa_playlisty = Label(start_frame, text="Podaj dokładną nazwę playlisty", font=("Arial", 14), width = 40, height=2)
        nazwa_playlisty.place(x = 360, y = 100)
        ID_playlisty = Label(start_frame, text="Podaj łącze do playlisty", font=("Arial", 14), width = 40, height=2)
        ID_playlisty.place(x = 360, y = 225)
        self.entry_nazwa_playlisty = Entry(start_frame)
        self.entry_nazwa_playlisty.place(x=400, y = 155, width=360, height=30)
        self.entry_ID_playlisty = Entry(start_frame)
        self.entry_ID_playlisty.place(x=400, y=280, width=360, height=30)
        Button(start_frame, text="Zatwierdź", command = self.playlista, height=2, width=20, font=("Arial", 12)).place(x=475, y = 350)
        self.dalej = Button(start_frame, text="Dalej",
                  command=lambda: self.master.switch_frame(PageOne), height=2, width=20, font=("Arial", 12))
        self.dalej.config(relief=SUNKEN, state=DISABLED)
        self.dalej.place(x = 475, y = 500)

    def playlista(self):
        global songs
        global features
        global target
        # nazwa = "Reassuring"
        # ID = "52KwifcwbsyxMfXUhcpMO4"
        nazwa = self.entry_nazwa_playlisty.get()
        ID = self.entry_ID_playlisty.get()      # ID playlisty to ten fragment linku po ukośniku i pytajnikiem
        if ID.startswith('https://open.spotify.com/playlist/'):
            ID = ID[34:].split("?")[0]
        else:
            print("Wklej odpowiedni link")       # zamiast tego printa dobrze byłoby wstawić messagebox z informacją
        playlist = sp.user_playlist(nazwa, ID)
        songs = playlist["tracks"]["items"]
        print("Liczba piosenek: ", len(songs))    # niestety w tym API jest ograniczenie do 100 piosenek
        for i in range(len(songs)):
            ids.append(songs[i]["track"]["id"])
            titles.append(songs[i]["track"]["name"])
            artists.append(songs[i]["track"]["artists"])
        features = sp.audio_features(ids)
        self.entry_nazwa_playlisty.delete(0, 'end')
        self.entry_ID_playlisty.delete(0, 'end')
        self.dalej.config(relief=RAISED, state=NORMAL)

class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=1920, height = 1080, bg = "midnight blue")
        self.stworzWidgety()
        self.przygotuj_dane()
        self.wybrane_cechy = []
        self.odległości = []
        self.proponowane = []
        self.licznik_cech = 0

    def stworzWidgety(self):
        left_frame1= Frame(self, width = 200, height = 100, bg = "powderblue")
        left_frame1.grid(row = 0, column = 0, padx = 75)
        left_frame2 = Frame(self, width = 200, height = 500, bg="powderblue")
        left_frame2.grid(row = 1, column = 0, padx = 75)
        mid_frame1 = Frame(self, width = 200, height = 75, bg = "powderblue")
        mid_frame1.grid(row = 0, column = 1, padx = 25, pady = 25)
        self.mid_frame2 = Frame(self, width = 600, height = 500, bg = "powderblue")
        self.mid_frame2.grid(row = 1, column = 1, pady=25)
        cechy = Label(left_frame1, text ="Cechy", relief=RAISED, width = 15, height = 2, font=("Arial", 14))
        cechy.grid(padx = 27, pady = 10)
        wybor_knn = Label(mid_frame1, text="Ile piosenek zaproponować?", width = 30, font=("Arial", 14))
        wybor_knn.grid(row = 0, column = 1, padx = 25, pady=1)
        self.pole_tekstowe = Entry (mid_frame1)
        self.pole_tekstowe.grid(row = 1, column = 1)

        self.button_submit = Button(mid_frame1, text="Zatwierdź", command=self.potwierdzenie)
        self.button_submit.grid(row=2, column=1)
        self.button_submit.config(relief=SUNKEN, state=DISABLED)
        self.button1 = Button(left_frame2, text="danceability", width=15,  font=("Arial", 12), command=self.button1_action)
        self.button1.grid(row=1, column=0, padx=40, pady=3)
        self.button2 = Button(left_frame2, text="energy", width=15, font=("Arial", 12), command=self.button2_action)
        self.button2.grid(row=2, column=0, padx=0, pady=3)
        self.button3 = Button(left_frame2, text="key", width=15, font=("Arial", 12), command=self.button3_action)
        self.button3.grid(row=3, column=0, padx=0, pady=3)
        self.button4 = Button(left_frame2, text="acousticness", width=15, font=("Arial", 12), command=self.button4_action)
        self.button4.grid(row=4, column=0, padx=0, pady=3)
        self.button5 = Button(left_frame2, text="instrumentalness", width=15, font=("Arial", 12), command=self.button5_action)
        self.button5.grid(row=5, column=0, padx=0, pady=3)
        self.button6 = Button(left_frame2, text="liveness", width=15, font=("Arial", 12), command=self.button6_action)
        self.button6.grid(row=6, column=0, padx=0, pady=3)
        self.button7 = Button(left_frame2, text="loudness", width=15, font=("Arial", 12), command=self.button7_action)
        self.button7.grid(row=7, column=0, padx=0, pady=3)
        self.button8 = Button(left_frame2, text="mode", width=15, font=("Arial", 12), command=self.button8_action)
        self.button8.grid(row=8, column=0, padx=0, pady=3)
        self.button9 = Button(left_frame2, text="speechiness", width=15, font=("Arial", 12), command=self.button9_action)
        self.button9.grid(row=9, column=0, padx=0, pady=3)
        self.button10 = Button(left_frame2, text="tempo", width=15, font=("Arial", 12), command=self.button10_action)
        self.button10.grid(row=10, column=0, padx=0, pady=3)
        self.button11 = Button(left_frame2, text="valence", width=15,  font=("Arial", 12), command=self.button11_action)
        self.button11.grid(row=11, column=0, padx=0, pady=3)
        self.reset_button = Button(left_frame2, text="reset", width=15, bg="indian red", font=("Arial", 12), command=self.reset)
        self.reset_button.grid(row=12, column=0, pady=3)
        Button(self, text="Return to start page",
                  command=lambda: self.master.switch_frame(StartPage)).grid()

    def przygotuj_dane(self):
        df = pd.DataFrame(features)
        df["title"] = titles
        print(df)

    def wizualizuj_dane(self):
        if self.licznik_cech == 1:
            fig = Figure(figsize=(6, 4), dpi=100, facecolor="powderblue")
            chart = fig.add_subplot(111)
            chart.set_xlabel(self.wybrane_cechy[0])

            self.canvas = FigureCanvasTkAgg(fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
        elif self.licznik_cech == 2:
            self.canvas.get_tk_widget().pack_forget()
            fig = Figure(figsize=(6, 4), dpi=100, facecolor="powderblue")
            chart = fig.add_subplot(111)
            chart.set_xlabel(self.wybrane_cechy[0])
            chart.set_ylabel(self.wybrane_cechy[1])

            self.canvas = FigureCanvasTkAgg(fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
        elif self.licznik_cech == 3:
            self.canvas.get_tk_widget().pack_forget()
            fig = Figure(figsize=(6, 4), dpi=100, facecolor="powderblue")
            chart = fig.add_subplot(111, projection="3d")
            chart.set_xlabel(self.wybrane_cechy[0])
            chart.set_ylabel(self.wybrane_cechy[1])
            chart.set_zlabel(self.wybrane_cechy[2])

            self.canvas = FigureCanvasTkAgg(fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

    ######## ten pasek narzędzi jest trochę kłopotliwy - nie wszystko działa tak jak powinno #######
            # self.toolbar = NavigationToolbar2Tk(self.canvas, self.mid_frame2)
            # self.toolbar.update()
            # self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def obliczanie_odleglosci(self):
        for i in range(len(songs)):
            if 'danceability' in self.wybrane_cechy:
                subt_danceability = target[0]["danceability"]-features[i]["danceability"]
            else:
                subt_danceability = 0
            if 'energy' in self.wybrane_cechy:
                subt_energy = target[0]["energy"]-features[i]["energy"]
            else:
                subt_energy = 0
            if 'key' in self.wybrane_cechy:
                subt_key = target[0]["key"]-features[i]["key"]
            else:
                subt_key = 0
            if 'acousticness' in self.wybrane_cechy:
                subt_acousticness = target[0]["acousticness"]-features[i]["acousticness"]
            else:
                subt_acousticness = 0
            if 'instrumentalness' in self.wybrane_cechy:
                subt_instrumentalness = target[0]["instrumentalness"]-features[i]["instrumentalness"]
            else:
                subt_instrumentalness = 0
            if 'liveness' in self.wybrane_cechy:
                subt_liveness = target[0]["liveness"]-features[i]["liveness"]
            else:
                subt_liveness = 0
            if 'loudness' in self.wybrane_cechy:
                subt_loudness = target[0]["loudness"]-features[i]["loudness"]
            else:
                subt_loudness = 0
            if 'mode' in self.wybrane_cechy:
                subt_mode = target[0]["mode"]-features[i]["mode"]
            else:
                subt_mode = 0
            if 'speechiness' in self.wybrane_cechy:
                subt_speechiness = target[0]["speechiness"]-features[i]["speechiness"]
            else:
                subt_speechiness = 0
            if 'tempo' in self.wybrane_cechy:
                subt_tempo = target[0]["tempo"]-features[i]["tempo"]
            else:
                subt_tempo = 0
            if 'valence' in self.wybrane_cechy:
                subt_valence = target[0]["valence"]-features[i]["valence"]
            else:
                subt_valence = 0

            odległość = math.sqrt(subt_danceability**2+subt_energy**2+subt_key**2+subt_acousticness**2+subt_instrumentalness**2+subt_liveness**2+subt_loudness**2
                                  +subt_mode**2+subt_speechiness**2+subt_tempo**2+subt_valence**2)
            self.odległości.append([round(odległość,2), features[i]["id"], titles[i], artists[i][0]["name"]])
        self.odległości.sort()

    def potwierdzenie(self):
        self.obliczanie_odleglosci()
        k = int(self.pole_tekstowe.get())
        self.pole_tekstowe.delete(0, 'end')
        print("Posortowane odległości:", self.odległości)
        for i in range(k):
            self.proponowane.append(self.odległości[i])
        print("\nOto proponowane piosenki: \n")
        for utwor in self.proponowane:
            print("\n", utwor)
        self.odległości.clear()     # trzeba wyczyścić odległości, żeby przy wpisaniu innej liczby sąsiadów się nie nadpisało

    def button1_action(self):
        if self.licznik_cech < 3:
            self.button1.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('danceability')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")
    def button2_action(self):
        if self.licznik_cech < 3:
            self.button2.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('energy')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button3_action(self):
        if self.licznik_cech < 3:
            self.button3.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('key')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button4_action(self):
        if self.licznik_cech < 3:
            self.button4.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('acousticness')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button5_action(self):
        if self.licznik_cech < 3:
            self.button5.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('instrumentalness')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button6_action(self):
        if self.licznik_cech < 3:
            self.button6.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('liveness')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button7_action(self):
        if self.licznik_cech < 3:
            self.button7.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('loudness')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button8_action(self):
        if self.licznik_cech < 3:
            self.button8.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('mode')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button9_action(self):
        if self.licznik_cech < 3:
            self.button9.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('speechiness')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button10_action(self):
        if self.licznik_cech < 3:
            self.button10.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('tempo')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def button11_action(self):
        if self.licznik_cech < 3:
            self.button11.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('valence')
            self.licznik_cech += 1
            self.wizualizuj_dane()
        else:
            print("wybrałeś już 3 cechy ")

    def reset(self):
        self.button1.config(relief=RAISED, state=NORMAL)
        self.button2.config(relief=RAISED, state=NORMAL)
        self.button3.config(relief=RAISED, state=NORMAL)
        self.button4.config(relief=RAISED, state=NORMAL)
        self.button5.config(relief=RAISED, state=NORMAL)
        self.button6.config(relief=RAISED, state=NORMAL)
        self.button7.config(relief=RAISED, state=NORMAL)
        self.button8.config(relief=RAISED, state=NORMAL)
        self.button9.config(relief=RAISED, state=NORMAL)
        self.button10.config(relief=RAISED, state=NORMAL)
        self.button11.config(relief=RAISED, state=NORMAL)
        self.wybrane_cechy.clear()
        self.proponowane.clear()
        self.button_submit.config(relief=SUNKEN, state=DISABLED)
        self.odległości.clear()
        self.licznik_cech = 0
        self.canvas.get_tk_widget().pack_forget()
        # self.toolbar.pack_forget()
ids = []
titles = []
artists = []
target_id = "3cyHz6vzksSQ92KEkr0wu3"
target = sp.audio_features(target_id)
# wybrane_cechy = []

app = SampleApp()
app.mainloop()
