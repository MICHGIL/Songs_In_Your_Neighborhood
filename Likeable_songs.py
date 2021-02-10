import pandas as pd
import spotipy
import math
from tkinter import *
from tkinter import messagebox
from spotipy.oauth2 import SpotifyClientCredentials
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
from mpl_toolkits.mplot3d import proj3d
from statistics import mode

client_id = "2414011f2fab4d93ab24db4093524758"
client_secret = "b4b85483ecac42cfa2d9e8b255137757"
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id, client_secret))

class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.state("zoomed")
        self.title("Likeable songs")
        self.config(bg="seashell2")
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
        Frame.__init__(self, master, width=1920, height=1080, bg="seashell2")
        self.stworzWidgety()

    def stworzWidgety(self):
        start_frame = Frame(self, width=1150, height=580, bg="powderblue")
        start_frame.place(x=200, y=100)
        ID_playlisty = Label(start_frame, text="Podaj łącze do playlisty", bg="slateblue", font=("Arial", 14),
                             width=40, height=2)
        ID_playlisty.place(x=360, y=225)
        self.entry_ID_playlisty = Entry(start_frame, font=("Arial", 12))
        self.entry_ID_playlisty.place(x=400, y=280, width=360, height=30)
        Button(start_frame, text="Zatwierdź", command=self.playlista, height=2, width=20, font=("Arial", 12)).place(x=475, y=350)
        self.dalej = Button(start_frame, text="Dalej", command=lambda: self.master.switch_frame(PageOne), height=2, width=20, font=("Arial", 12))
        self.dalej.config(relief=SUNKEN, state=DISABLED)
        self.dalej.place(x=475, y=500)


    def playlista(self):
        global songs
        global features
        global titles
        global artists
        artists = []
        titles = []
        ids = []
        playlistID = self.entry_ID_playlisty.get()      # ID playlisty to ten fragment linku po ukośniku i pytajnikiem
        if playlistID.startswith('https://open.spotify.com/playlist/'):
            playlistID = playlistID[34:].split("?")[0]
        else:
            messagebox.showerror("Błąd", "Błędny link. Podaj łącze do playlisty.\n\nW oknie Spotify wybierz playlistę, znajdź zakładkę 'Udostępnij', a następnie wybierz opcję 'skopiuj łącze do playlisty'")
            self.entry_ID_playlisty.delete(0, 'end')
        playlist = sp.playlist(playlistID)
        songs = playlist["tracks"]["items"]
        print("Liczba piosenek: ", len(songs))    # niestety w tym API jest ograniczenie do 100 piosenek
        for i in range(len(songs)):                 # zastanawiam się, czy nie przenieść tego do funkcji "przygotuj_dane "
            ids.append(songs[i]["track"]["id"])
            titles.append(songs[i]["track"]["name"])
            artists.append(songs[i]["track"]["artists"])
        features = sp.audio_features(ids)
        self.entry_ID_playlisty.delete(0, 'end')
        self.dalej.config(relief=RAISED, state=NORMAL)


class PageOne(Frame):
    def __init__(self, master):
        Frame.__init__(self, master, width=1920, height=1080, bg="seashell2")
        self.stworzWidgety()
        self.df = pd.DataFrame()
        self.wybrane_cechy = []
        self.odległości = []
        self.proponowane = []
        self.proponowane_ids = []
        self.indeksy = []
        self.licznik_cech = 0
        self.fig = Figure(figsize=(6, 5.5), dpi=100, facecolor="powderblue")

    def stworzWidgety(self):
        global home_image       # jak nie jest globalna, to obrazek się nie wyświetla
        home_image = PhotoImage(file="home_button2.png")
        left_frame1 = Frame(self, width=160, height=160, bg="powderblue")
        left_frame1.grid(row=0, column=0, padx=70, pady=10)
        left_frame2 = Frame(self, width=200, height=400, bg="powderblue")
        left_frame2.grid(row=1, column=0, padx=25)
        mid_frame_up = Frame(self, width=200, height=100, bg="powderblue")
        mid_frame_up.grid(row=0, column=1, pady=10, ipadx=8)
        self.mid_frame2 = Frame(self, width=800, height=550, bg="powderblue")
        self.mid_frame2.grid(row=1, column=1, pady=10)
        # right_frame1 = Frame(self, width=500, height=200, bg="powderblue")
        # right_frame1.grid(row=0, column=3, padx=20)
        self.resultbox = Text(self, bg="powderblue", width=40, height=30, bd=0, font=("Arial", 12), wrap=WORD, padx=10, pady=10,
                              state=DISABLED)
        self.resultbox.grid(row=1, column=3, padx=25)
        wybor_piosenki = Label(mid_frame_up, text="Podaj łącze do utworu", bg="slateblue", width=25, height=2, font=("Arial", 12))
        wybor_piosenki.grid(row=0, column=1, padx=10, pady=5)
        cechy = Label(left_frame2, text="Cechy", relief=RAISED, bg="slateblue", width=15, height=2, font=("Arial", 14))
        cechy.grid(row=0, column=0, pady=25)
        wybor_knn = Label(mid_frame_up, text="Ile piosenek zaproponować?", bg="slateblue",  height=2, width=25, font=("Arial", 12))
        wybor_knn.grid(row=1, column=1, padx=25, pady=5)
        self.entry_wybor_piosenki = Entry(mid_frame_up, font=("Arial", 12))
        self.entry_wybor_piosenki.grid(row=0, column=2, padx=10, pady=5, ipady=10, ipadx=50)
        self.pole_tekstowe = Entry(mid_frame_up, font=("Arial", 12))
        self.pole_tekstowe.grid(row=1, column=2, padx=10, pady=5, ipady=10, ipadx=2)

        self.button_submit = Button(mid_frame_up, text="Zatwierdź", command=self.potwierdzenie, height=2, width=20, font=("Arial", 12))
        self.button_submit.grid(row=2, column=2, pady=5, padx=5)
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
        home_button = Button(self, image=home_image, command=lambda: self.master.switch_frame(StartPage))
        home_button.grid(row=0, column=0)

    def przygotuj_dane(self):
        self.df = pd.DataFrame(features)
        names = []
        for i in range(len(songs)):
            names.append(artists[i][0]["name"])
        self.df["title"] = titles
        self.df["artist"] = names

    def wizualizuj_dane(self):
        self.canvas.get_tk_widget().pack_forget()
        self.chart.set_title("Przestrzeń najbliższych sąsiadów")

        if self.licznik_cech == 1:
            self.chart.barh(self.df.loc[self.indeksy, "title"], self.df.loc[self.indeksy, self.wybrane_cechy[0]])
            self.chart.barh(self.target_title, self.target[0][self.wybrane_cechy[0]], color="orange")
            self.scatter = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)
            self.scatter.get_tk_widget().pack()
        elif self.licznik_cech == 2:
            data_x = self.df.loc[self.indeksy, self.wybrane_cechy[0]]
            data_y = self.df.loc[self.indeksy, self.wybrane_cechy[1]]
            i = 0
            for x, y in zip(data_x, data_y):
                label = self.df.loc[self.indeksy[i], "title"]
                self.chart.annotate(label, (x, y), textcoords="offset points", xytext=(0, 5), ha="center")
                i += 1
            self.chart.annotate(self.target_title, (self.target[0][self.wybrane_cechy[0]], self.target[0][self.wybrane_cechy[1]]),
                                textcoords="offset points", xytext=(0, 5), ha="center")
            self.chart.scatter(data_x, data_y, color='b')
            self.chart.scatter(self.target[0][self.wybrane_cechy[0]], self.target[0][self.wybrane_cechy[1]], color="orange")
            self.scatter = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)
            self.scatter.get_tk_widget().pack()
        elif self.licznik_cech == 3:
            data_x = self.df.loc[self.indeksy, self.wybrane_cechy[0]]
            data_y = self.df.loc[self.indeksy, self.wybrane_cechy[1]]
            data_z = self.df.loc[self.indeksy, self.wybrane_cechy[2]]
            i = 0
            for x, y, z in zip(data_x, data_y, data_z):
                x3D, y3D, _ = proj3d.proj_transform(x, y, z, self.chart.get_proj())
                label = self.df.loc[self.indeksy[i], "title"]
                self.chart.annotate(label, (x3D, y3D), textcoords="offset points", xytext=(0, 5), ha="center")
                i += 1
            self.chart.scatter(data_x, data_y, data_z, color='b')
            self.chart.scatter(self.target[0][self.wybrane_cechy[0]], self.target[0][self.wybrane_cechy[1]], self.target[0][self.wybrane_cechy[2]], color="orange")
            self.scatter = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)
            self.scatter.get_tk_widget().pack()

    def rysuj_osie(self):
        if self.licznik_cech == 1:
            self.fig = Figure(figsize=(8, 5.5), dpi=100, facecolor="powderblue")
            self.chart = self.fig.add_subplot(111)
            self.chart.set_xlabel(self.wybrane_cechy[0])

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
        elif self.licznik_cech == 2:
            self.canvas.get_tk_widget().pack_forget()
            self.fig = Figure(figsize=(8, 5.5), dpi=100, facecolor="powderblue")
            self.chart = self.fig.add_subplot(111)
            self.chart.set_xlabel(self.wybrane_cechy[0])
            self.chart.set_ylabel(self.wybrane_cechy[1])

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()
        elif self.licznik_cech == 3:
            self.canvas.get_tk_widget().pack_forget()
            self.fig = Figure(figsize=(8, 5.5), dpi=100, facecolor="powderblue")
            self.chart = self.fig.add_subplot(111, projection="3d")
            self.chart.set_xlabel(self.wybrane_cechy[0])
            self.chart.set_ylabel(self.wybrane_cechy[1])
            self.chart.set_zlabel(self.wybrane_cechy[2])

            self.canvas = FigureCanvasTkAgg(self.fig, master=self.mid_frame2)  # A tk.DrawingArea.
            self.canvas.draw()
            self.canvas.get_tk_widget().pack()

    def obliczanie_odleglosci(self):
        for i in range(len(songs)):
            if 'danceability' in self.wybrane_cechy:
                subt_danceability = self.target[0]["danceability"]-features[i]["danceability"]
            else:
                subt_danceability = 0
            if 'energy' in self.wybrane_cechy:
                subt_energy = self.target[0]["energy"]-features[i]["energy"]
            else:
                subt_energy = 0
            if 'key' in self.wybrane_cechy:
                subt_key = self.target[0]["key"]-features[i]["key"]
            else:
                subt_key = 0
            if 'acousticness' in self.wybrane_cechy:
                subt_acousticness = self.target[0]["acousticness"]-features[i]["acousticness"]
            else:
                subt_acousticness = 0
            if 'instrumentalness' in self.wybrane_cechy:
                subt_instrumentalness = self.target[0]["instrumentalness"]-features[i]["instrumentalness"]
            else:
                subt_instrumentalness = 0
            if 'liveness' in self.wybrane_cechy:
                subt_liveness = self.target[0]["liveness"]-features[i]["liveness"]
            else:
                subt_liveness = 0
            if 'loudness' in self.wybrane_cechy:
                subt_loudness = self.target[0]["loudness"]-features[i]["loudness"]
            else:
                subt_loudness = 0
            if 'mode' in self.wybrane_cechy:
                subt_mode = self.target[0]["mode"]-features[i]["mode"]
            else:
                subt_mode = 0
            if 'speechiness' in self.wybrane_cechy:
                subt_speechiness = self.target[0]["speechiness"]-features[i]["speechiness"]
            else:
                subt_speechiness = 0
            if 'tempo' in self.wybrane_cechy:
                subt_tempo = self.target[0]["tempo"]-features[i]["tempo"]
            else:
                subt_tempo = 0
            if 'valence' in self.wybrane_cechy:
                subt_valence = self.target[0]["valence"]-features[i]["valence"]
            else:
                subt_valence = 0

            odległość = math.sqrt(subt_danceability**2+subt_energy**2+subt_key**2+subt_acousticness**2+subt_instrumentalness**2+subt_liveness**2+subt_loudness**2
                                  + subt_mode**2+subt_speechiness**2+subt_tempo**2+subt_valence**2)
            self.odległości.append([round(odległość, 2), features[i]["id"], titles[i], artists[i][0]["name"], features[i]["uri"]])
        self.odległości.sort()

    def potwierdzenie(self):
        self.przygotuj_dane()
        self.canvas.get_tk_widget().pack_forget()
        target_id = str(self.entry_wybor_piosenki.get())
        if target_id.startswith('https://open.spotify.com/track/'):
            target_id = target_id[31:].split("?")[0]
            self.target_title = sp.track(target_id)["name"]
            self.target_artist = sp.track(target_id)["artists"][0]["name"]
            self.target = sp.audio_features(target_id)
            self.obliczanie_odleglosci()
            k = int(self.pole_tekstowe.get())
            self.pole_tekstowe.delete(0, 'end')
            print("Posortowane odległości:", self.odległości)
            for i in range(k):
                self.proponowane.append(self.odległości[i])
                self.proponowane_ids.append(self.odległości[i][1])
            for id in self.proponowane_ids:
                self.indeksy.append(self.df[self.df['id'] == id].index.item())
            self.wizualizuj_dane()
            print("\nOto proponowane piosenki: \n")
            for i in range(len(self.proponowane)):
                tytuł = self.proponowane[i][2]
                wykonawca = self.proponowane[i][3]
                URI = self.proponowane[i][4]
                self.resultbox.config(state=NORMAL)
                self.resultbox.insert(END, (str(i+1)+". "+tytuł+" - "+wykonawca+"\n"+URI+"\n\n"))
            self.resultbox.config(state=DISABLED)
            self.odległości.clear()     # trzeba wyczyścić odległości, żeby przy wpisaniu innej liczby sąsiadów się nie nadpisało
            self.button_submit.config(state=DISABLED)
        else:
            messagebox.showerror("Błąd", "Błędny link. Podaj łącze do utworu.\n\nW oknie Spotify wybierz utwór, znajdź zakładkę 'Udostępnij', a następnie wybierz opcję 'skopiuj łącze do utworu'")
            self.entry_wybor_piosenki.delete(0, 'end')

    def button1_action(self):
        if self.licznik_cech < 3:
            self.button1.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('danceability')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button2_action(self):
        if self.licznik_cech < 3:
            self.button2.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('energy')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button3_action(self):
        if self.licznik_cech < 3:
            self.button3.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('key')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button4_action(self):
        if self.licznik_cech < 3:
            self.button4.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('acousticness')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button5_action(self):
        if self.licznik_cech < 3:
            self.button5.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('instrumentalness')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button6_action(self):
        if self.licznik_cech < 3:
            self.button6.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('liveness')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button7_action(self):
        if self.licznik_cech < 3:
            self.button7.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('loudness')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button8_action(self):
        if self.licznik_cech < 3:
            self.button8.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('mode')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button9_action(self):
        if self.licznik_cech < 3:
            self.button9.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('speechiness')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button10_action(self):
        if self.licznik_cech < 3:
            self.button10.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('tempo')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

    def button11_action(self):
        if self.licznik_cech < 3:
            self.button11.config(relief=SUNKEN, state=DISABLED)
            self.button_submit.config(relief=RAISED, state=NORMAL)
            self.wybrane_cechy.append('valence')
            self.licznik_cech += 1
            self.rysuj_osie()
        else:
            messagebox.showwarning("Wskazówka", "Możesz wybrać maksymalnie 3 cechy! Tylko tyle zmieści się na wykresie.")

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
        self.proponowane_ids.clear()
        self.indeksy.clear()
        self.button_submit.config(relief=SUNKEN, state=DISABLED)
        self.odległości.clear()
        self.licznik_cech = 0
        if self.resultbox['state'] == DISABLED:
            self.resultbox.config(state=NORMAL)
            self.resultbox.delete("1.0", END)
        self.resultbox.config(state=DISABLED)
        self.canvas.get_tk_widget().pack_forget()
        try:
            self.scatter.get_tk_widget().pack_forget()
        except:
            self.barh.get_tk_widget().pack_forget()
        try:
            self.barh.get_tk_widget().pack_forget()
        except:
            self.scatter.get_tk_widget().pack_forget()

app = App()
app.mainloop()
