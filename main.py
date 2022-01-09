import google_auth_oauthlib.flow, googleapiclient.discovery, googleapiclient.errors
import webbrowser, shutil, json, os, random, pyglet, time, threading
from pathlib import Path
from pytube import YouTube
from tkinter import *
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
helv = ('Helvetica', 15)


def search(query, youtube=None):
    request = youtube.search().list(
        part="snippet",
        maxResults=25,
        q=query
    )
    response = request.execute()

    videos = []
    for i in range(len(response.get('items'))):
        title = response.get('items')[i].get('snippet').get('title')
        video_id = response.get('items')[i].get('id').get('videoId')
        video_link = 'https://www.youtube.com/watch?v={}'.format(video_id)
        share_link = 'https://youtu.be/{}'.format(video_id)
        videos.append(
            {'title': title, 'video_id': video_id, 'video_link': video_link, 'share_link': share_link, 'numberID': i})
    return videos


class App(Tk):
    def __init__(self, playerOBJ=pyglet.media.Player()):
        super().__init__()
        self.title('Spotify')
        self.iconbitmap('spotify_app.ico')

        self.state('zoomed')

        self.player = playerOBJ
        self.player.source_paths = []
        self.player.current_volume = 100

        @playerOBJ.event
        def on_player_next_source():
            # remove finished song
            self.player.source_paths = self.player.source_paths[1:]
            self.setup_playscreen()

            # if exists, remove 'player' frame
            try:
                self.nf.destroy()
            except:
                pass

            os.system('cls')

        def on_enter(event):
            widget = event.widget
            to_query = widget.get()
            widget.delete(0, END)
            self.sclear()
            self.init()
            results = search(query=to_query, youtube=youtube_credentials)

            with open('results.json', 'w') as f:
                f.write(json.dumps(results))
            self.process_results(results)

        def on_back(event):
            widget = event.widget
            search = widget.get().split()
            for i in range(len(search)):
                search[i] = f'{search[i]} '
            widget.delete(0, END)
            widget.insert(0, f"{''.join(search[:-1])} ")

        self.label = Label(self, text="").grid(row=0, column=0, pady=(30, 0))
        self.show_playlists_button = Button(self, text='Show Playlists', font=('Helvetica', 15, 'bold'),
                                            command=lambda results=os.listdir('C:/spotify_app/playlists'),
                                                           result_type='DIRS': [self.sclear(), self.init(),
                                                                                self.display_results(results,
                                                                                                     result_type)])
        self.show_playlists_button.grid(row=1, column=0, ipadx=10, ipady=15, padx=(50, 0))
        self.hide_playlists_button = Button(self, text="Hide Playlists", font=('Helvetica', 15, 'bold'),
                                            command=lambda: [self.sclear(), self.init()])
        self.hide_playlists_button.grid(ipadx=10, padx=(50, 0), ipady=15, row=1, column=1)
        self.label = Label(self, text='Search: ', font=('Helvetica', 20, 'bold')).grid(row=1, column=2, padx=(150, 0))
        self.searchbox = Entry(self, font=helv)
        self.searchbox.grid(row=1, column=3, ipadx=450, ipady=15)
        self.searchbox.focus()
        self.searchbox.bind('<Return>', on_enter)
        self.searchbox.bind('<Control-BackSpace>', on_back)
        self.resultsbox = LabelFrame(self, text='Results', font=('Helvetica', 20))
        self.resultsbox.grid(row=2, column=0, pady=25, columnspan=5)

    def process_results(self, results):
        videos = [
            [
                video.get('numberID'),
                video.get('title'),
                video.get('share_link'),
                video.get('video_link'),
                video.get('video_id'),
            ]
            for video in results
        ]

        self.display_results(videos)

    def init(self, event=None):
        self.sclear()

        def on_enter(event):
            widget = event.widget
            to_query = widget.get()
            widget.delete(0, END)
            self.sclear()
            self.init()
            results = search(query=to_query, youtube=youtube_credentials)

            with open('results.json', 'w') as f:
                f.write(json.dumps(results))
            self.process_results(results)

        def on_back(event):
            widget = event.widget
            search = widget.get().split()
            for i in range(len(search)):
                search[i] = f'{search[i]} '
            widget.delete(0, END)
            widget.insert(0, f"{''.join(search[:-1])} ")

        self.label = Label(self, text="").grid(row=0, column=0, pady=(30, 0))
        self.show_playlists_button = Button(self, text='Show Playlists', font=('Helvetica', 15, 'bold'),
                                            command=lambda results=os.listdir('C:/spotify_app/playlists'),
                                                           result_type='DIRS': [self.sclear(), self.init(),
                                                                                self.display_results(results,
                                                                                                     result_type)])
        self.show_playlists_button.grid(row=1, column=0, ipadx=10, ipady=15, padx=(50, 0))
        self.hide_playlists_button = Button(self, text="Hide Playlists", font=('Helvetica', 15, 'bold'),
                                            command=lambda: [self.sclear(), self.init()])
        self.hide_playlists_button.grid(ipadx=10, padx=(50, 0), ipady=15, row=1, column=1)
        self.label = Label(self, text='Search: ', font=('Helvetica', 20, 'bold')).grid(row=1, column=2, padx=(150, 0))
        self.searchbox = Entry(self, font=helv)
        self.searchbox.grid(row=1, column=3, ipadx=450, ipady=15)
        self.searchbox.focus()
        self.searchbox.bind('<Return>', on_enter)
        self.searchbox.bind('<Control-BackSpace>', on_back)
        self.resultsbox = LabelFrame(self, text='Results', font=('Helvetica', 20))
        self.resultsbox.grid(row=2, column=0, pady=(25, 0), columnspan=5)

    def clicked1(self, event=None, result=None):
        self.sclear()
        self.init()
        self.main_frame = LabelFrame(self, text='Playlist: ', font=('Helvetica', 20, 'underline', 'bold'))
        self.main_frame.grid(row=2, column=0, pady=(25, 50), columnspan=5)
        self.label = Label(self.main_frame, text=result, fg='red', font=('Helvetica', 18, 'bold')).grid(row=0, column=0,
                                                                                                        columnspan=5)
        self.btn = Button(self.main_frame, text="Play", font=('Helvetica', 15, 'bold'),
                          command=lambda playlist_name=result: self.play(play_by_playlist_name=playlist_name)).grid(
            row=1,
            column=0)

        self.btn = Button(self.main_frame, text="Shuffle", font=('Helvetica', 15, 'bold'),
                          command=lambda playlist_name=result: self.shuffle(playlist_name)).grid(row=1, column=1)

        self.btn = Button(self.main_frame, text="Choose", font=('Helvetica', 15, 'bold'),
                          command=lambda playlist_name=result: self.choose_song(playlist_name))
        self.btn.grid(row=1, column=2)
        self.btn = Button(self.main_frame, text="Edit", font=('Helvetica', 15, 'bold'),
                          command=lambda playlist_name=result: self.edit_playlist(playlist_name)).grid(row=1, column=3)
        self.btn = Button(self.main_frame, text="Delete", font=('Helvetica', 15, 'bold'),
                          command=lambda playlist_name=result: self.remove_playlist(playlist_name)).grid(row=1,
                                                                                                         column=4)

    def clicked(self, event=None, result=None):
        self.sclear()
        self.init()
        self.main_frame = LabelFrame(self, text='Song: ', font=('Helvetica', 20))
        self.main_frame.grid(row=2, column=0, pady=25, columnspan=5)
        self.label = Label(self.main_frame, text=result[1], fg='red', font=('Helvetica', 14, 'bold')).grid(row=0,
                                                                                                           column=0,
                                                                                                           columnspan=3)
        self.btn = Button(self.main_frame, text="Add to Playlist", font=helv,
                          command=lambda share_link=result[2]: self.add_to_playlist(share_link)).grid(row=1, column=0)
        self.btn = Button(self.main_frame, text="Listen on YouTube", font=helv,
                          command=lambda watch_link=result[2]: self.listen_on_youtube(watch_link)).grid(row=1,
                                                                                                        column=2)

    def display_results(self, results, result_type='SEARCH'):
        for widget in self.resultsbox.winfo_children():
            widget.destroy()
        while len(results) < 25:
            results.append('')
        if result_type == 'SEARCH':
            i = 0
            self.one = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                             cursor="hand2")
            self.one.grid(row=i, column=0, pady=(0, 50))
            self.one.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.two = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                             cursor="hand2")
            self.two.grid(row=i, column=0, pady=(0, 50))
            self.two.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.three = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.three.grid(row=i, column=0, pady=(0, 50))
            self.three.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.four = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.four.grid(row=i, column=0, pady=(0, 50))
            self.four.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.five = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.five.grid(row=i, column=0, pady=(0, 50))
            self.five.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.six = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                             cursor="hand2")
            self.six.grid(row=i, column=0, pady=(0, 50))
            self.six.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.seven = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.seven.grid(row=i, column=0, pady=(0, 50))
            self.seven.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i += 1
            self.eight = Label(self.resultsbox, text=results[i][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.eight.grid(row=i, column=0, pady=(0, 50))
            self.eight.bind('<Button-1>', lambda event, x=results[i]: self.clicked(result=x))
            i = 0
            self.one1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.one1.grid(row=i, column=1, pady=(0, 50))
            self.one1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.two1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.two1.grid(row=i, column=1, pady=(0, 50))
            self.two1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.three1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                                cursor="hand2")
            self.three1.grid(row=i, column=1, pady=(0, 50))
            self.three1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.four1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.four1.grid(row=i, column=1, pady=(0, 50))
            self.four1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.five1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.five1.grid(row=i, column=1, pady=(0, 50))
            self.five1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.six1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.six1.grid(row=i, column=1, pady=(0, 50))
            self.six1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.seven1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                                cursor="hand2")
            self.seven1.grid(row=i, column=1, pady=(0, 50))
            self.seven1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.eight1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                                cursor="hand2")
            self.eight1.grid(row=i, column=1, pady=(0, 50))
            self.eight1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i += 1
            self.nine1 = Label(self.resultsbox, text=results[i + 8][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.nine1.grid(row=i, column=1, pady=(0, 50))
            self.nine1.bind('<Button-1>', lambda event, x=results[i + 8]: self.clicked(result=x))
            i = 0
            self.one2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.one2.grid(row=i, column=2, pady=(0, 50))
            self.one2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.two2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.two2.grid(row=i, column=2, pady=(0, 50))
            self.two2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.three2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'),
                                fg='blue',
                                cursor="hand2")
            self.three2.grid(row=i, column=2, pady=(0, 50))
            self.three2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.four2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.four2.grid(row=i, column=2, pady=(0, 50))
            self.four2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.five2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'), fg='blue',
                               cursor="hand2")
            self.five2.grid(row=i, column=2, pady=(0, 50))
            self.five2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.six2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'), fg='blue',
                              cursor="hand2")
            self.six2.grid(row=i, column=2, pady=(0, 50))
            self.six2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.seven2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'),
                                fg='blue',
                                cursor="hand2")
            self.seven2.grid(row=i, column=2, pady=(0, 50))
            self.seven2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
            i += 1
            self.eight2 = Label(self.resultsbox, text=results[i + 17][1], font=('Helvetica', 10, 'underline'),
                                fg='blue',
                                cursor="hand2")
            self.eight2.grid(row=i, column=2, pady=(0, 50))
            self.eight2.bind('<Button-1>', lambda event, x=results[i + 17]: self.clicked(result=x))
        elif result_type == 'DIRS':
            self.sclear()
            self.init()

            # setup listbox with scrollbar
            frame = Frame(self)
            frame.grid(row=2, column=0, pady=(25, 5), columnspan=5)

            playlists = Listbox(frame, width=30, height=20, font=("Helvetica", 12))
            playlists.pack(side="left", fill="y")

            scrollbar = Scrollbar(frame, orient="vertical")
            scrollbar.config(command=playlists.yview)
            scrollbar.pack(side="right", fill="y")

            playlists.config(yscrollcommand=scrollbar.set)

            # add all playlists to listbox
            for playlist_name in os.listdir('C:/spotify_app/playlists'):
                playlists.insert(END, playlist_name)

            def on_enter():
                result = playlists.get(ANCHOR)
                if result in os.listdir('C:/spotify_app/playlists'):
                    self.clicked1(result=result)

            # Add 'enter' button
            enter = Button(self, text="Select", padx=95, borderwidth=2, font=('Helvetica', 20, 'bold'),
                           command=on_enter, bg='#a6a6a6')
            enter.grid(row=3, column=0, columnspan=5, pady=(0, 25))

            # give color to items in listbox
            for i in reversed(range(playlists.size())):
                playlists.itemconfig(i, fg="red" if (i % 2) == 0 else "green")

    def add_to_playlist(self, link):
        def on_back1(event):
            widget = event.widget
            search = widget.get().split()
            for i in range(len(search)):
                search[i] = f'{search[i]} '
            widget.delete(0, END)
            widget.insert(0, f"{''.join(search[:-1])} ")

        self.file_name = Entry(self, font=helv)
        self.file_name.grid(row=5, column=0, columnspan=5, ipadx=100, ipady=15)
        self.file_name.bind('<Control-BackSpace>', on_back1)

        def get_name(event=None):
            with open('name.txt', 'w') as f:
                f.write(self.file_name.get())
                f.write('\n')
            self.file_name.delete(0, END)
            self.file_name.destroy()

            def get_playlist(event):
                widget = event.widget
                CONTENTS = widget.get()
                with open('name.txt', 'a') as f:
                    f.write(CONTENTS)
                with open('name.txt', 'r') as f:
                    lines = f.read().splitlines()
                    playlist_name = lines[-1]
                    song_name = lines[0]
                    if playlist_name != '' and playlist_name != ' ':
                        while playlist_name[-1] == ' ':
                            playlist_name = playlist_name[:-1]
                    elif song_name != '' and song_name != ' ':
                        while song_name[-1] == ' ':
                            song_name = song_name[:-1]

                    if playlist_name == 'fav' or playlist_name == 'favs':
                        playlist_name = 'favorites'

                with open('name.txt', 'w') as f:
                    f.write(playlist_name)
                    f.write('\n')
                    f.write(song_name)
                path = 'C:/spotify_app/playlists/{}'.format(playlist_name)
                if CONTENTS != '' and CONTENTS != ' ' and CONTENTS != 'Playlist Name' and CONTENTS != 'Playlist Name ' and self.check_playlist(
                        CONTENTS):
                    if not os.path.isdir(path):
                        os.mkdir(path)
                widget.delete(0, END)
                widget.destroy()

                # show error if video could not download
                def clicked_OnError():
                    self.sclear()
                    self.init()

                for w in self.winfo_children():
                    w.destroy()
                self.label = Label(self, text="Possible Error...", font=('Helvetica', 64, 'bold', 'underline'),
                                   fg='blue', cursor='hand2')
                self.label.pack(pady=400)
                self.label.bind('<Button-1>', clicked_OnError)

                def download(link, path, song_name):
                    url = YouTube(link)
                    video = url.streams.filter(only_audio=True).first()
                    path_to_download_folder = str(os.path.join(path))
                    if path == 'Playlist Name' or path == 'Playlist Name ' or path == '' or path == ' ' or not self.check_playlist(
                            CONTENTS):
                        DEFAULT_PATH = str(Path.home() / "Downloads")
                        video.download(DEFAULT_PATH, filename=f'{song_name}.mp3')
                        self.success(mb_notification=True)
                        return None
                    video.download(path_to_download_folder, filename=f'{song_name}.mp3')
                    self.success()

                download(link=link, path=path, song_name=song_name)

            def list_playlists():
                pl_win = Toplevel()
                pl_win.title('Playlists')
                pl_win.iconbitmap('spotify_app.ico')

                # setup listbox with scrollbar
                frame = Frame(pl_win)
                frame.pack()

                playlists = Listbox(frame, width=20, height=20, font=("Helvetica", 12))
                playlists.pack(side="left", fill="y")

                scrollbar = Scrollbar(frame, orient="vertical")
                scrollbar.config(command=playlists.yview)
                scrollbar.pack(side="right", fill="y")

                playlists.config(yscrollcommand=scrollbar.set)

                # TODO: fix this scrollbar shit

                # when an anchor is clicked, insert that into the playlist_name box and close the toplevel window
                def clickEvent(event):
                    w = event.widget
                    self.playlist_name.delete(0, END)
                    self.playlist_name.insert(0, w.get(int(w.curselection()[0])))
                    pl_win.destroy()

                # add all playlists to listbox
                for playlist_name in os.listdir('C:/spotify_app/playlists'):
                    playlists.insert(END, playlist_name)
                playlists.bind('<<ListboxSelect>>', clickEvent)

                # give color to items in listbox
                for i in reversed(range(playlists.size())):
                    playlists.itemconfig(i, fg="red" if (i % 2) == 0 else "green")

            self.playlist_name = Entry(self, font=helv)
            self.playlist_name.grid(row=5, column=0, columnspan=5, ipadx=100, ipady=15)
            self.playlist_name.bind('<Return>', get_playlist)
            self.playlist_name.insert(0, 'Playlist Name')
            self.playlist_name.focus()

            self.list_playlists_button = Button(self, text='List Playlists', command=list_playlists,
                                                font=('Helvetica', 20, 'bold'), bg='green')
            self.list_playlists_button.grid(row=6, column=0, columnspan=5, ipadx=116, ipady=1)

            def on_back2(event):
                widget = event.widget
                search = widget.get().split()
                for i in range(len(search)):
                    search[i] = f'{search[i]}'
                widget.delete(0, END)
                widget.insert(0, f"{''.join(search[:-1])} ")

            self.playlist_name.bind('<Control-BackSpace>', on_back2)

        self.file_name.bind('<Return>', get_name)
        self.file_name.insert(0, 'Song Name')
        self.file_name.focus()

    def listen_on_youtube(self, URL):
        webbrowser.open_new_tab(URL)

    def sclear(self):
        for w in self.winfo_children():
            w.destroy()

    def success(self, mb_notification=False):
        def success_body_func():
            self.sclear()
            self.label = Label(self, text="Success", font=('Helvetica', 64, 'bold', 'underline'), fg='green',
                               cursor='hand2')
            self.label.pack(pady=400, ipady=1000, ipadx=1000)
            return self.label

        if not mb_notification:
            self.label = success_body_func()
            self.label.bind('<Button-1>', self.init)
        else:
            def show_notification(event=None):
                mb.showwarning('Notice',
                               "Your song has been downloaded to your 'Downloads' folder due to having one of the following names:\n\tPlaylist Name\n\t<empty>")
                self.sclear()
                self.init()

            self.label = success_body_func()
            self.label.bind('<Button-1>', self.init)
            self.label.bind('<Button-1>', show_notification)

    def play(self, play_by_playlist_name=None, play_by_view=None, randomize=False):
        try:
            self.nf.destroy()
        except:
            pass
        if play_by_view != None:
            if self.player.playing:
                self.player.pause()
                self.player.source_paths = []
                for _ in range(len(self.player.source_paths) + 1):
                    self.player.next_source()
                media = pyglet.media.load(play_by_view)
                self.player.queue(media)

                # restart func to get song to play and add song to player.source_paths
                self.play(play_by_view=play_by_view)
                single_song = True
            else:
                media = pyglet.media.load(play_by_view)
                self.player.queue(media)
                # add source_path to list
                self.player.source_paths.append(play_by_view)
                single_song = True
            self.player.play()
        elif play_by_playlist_name != None:
            single_song = False
            if not randomize:
                # add all songs to queue
                def add_playlist_queue():
                    for song in os.listdir('C:/spotify_app/playlists/{}'.format(play_by_playlist_name)):
                        if song.endswith(".mp3"):
                            formatted_song = 'C:/spotify_app/playlists/{}/{}'.format(play_by_playlist_name, song)
                            self.player.queue(pyglet.media.load(formatted_song))
                            # add source_path to list
                            self.player.source_paths.append(formatted_song)

                if (self.player.playing == True and self.player.source_paths != []) or (
                        self.player.playing == False and self.player.source_paths != []):
                    self.player.pause()
                    for _ in range(len(self.player.source_paths)):
                        self.player.next_source()
                    self.player.source_paths = []
                    add_playlist_queue()
                else:
                    add_playlist_queue()
            else:
                def add_playlist_queue1():
                    # add all songs to temp playlists, next step is randomizing
                    all_songs = []
                    for song in os.listdir('C:/spotify_app/playlists/{}'.format(play_by_playlist_name)):
                        if song.endswith(".mp3"):
                            all_songs.append('C:/spotify_app/playlists/{}/{}'.format(play_by_playlist_name, song))

                    # add all songs to source_paths using randint
                    for _ in range(len(all_songs)):
                        num = random.randint(1, len(all_songs))

                        self.player.source_paths.append(all_songs[num - 1])
                        all_songs.remove(all_songs[num - 1])

                    # queue and play music
                    for song in self.player.source_paths:
                        self.player.queue(pyglet.media.load(song))

                    self.setup_playscreen()

                if (self.player.playing and self.player.source_paths != []) or (
                        not self.player.playing and self.player.source_paths != []):
                    # clear queue
                    self.player.pause()
                    for _ in range(len(self.player.source_paths)):
                        self.player.next_source()
                    self.player.source_paths = []
                    add_playlist_queue1()
                else:
                    add_playlist_queue1()
            with open('single_song_bool.json', 'w') as f:
                single_song_dict = {'single_song': single_song, 'run_permission': False}
                json.dump(single_song_dict, f)
            self.player.play()

        if not single_song:
            self.setup_playscreen(single_song=False)
        else:
            self.setup_playscreen(single_song=True)

    def setup_playscreen(self, single_song=False):
        try:
            if self.current.winfo_exists() == 1:
                self.current.destroy()
            if self.upcoming.winfo_exists() == 1:
                self.upcoming.destroy()
            if self.cpf.winfo_exists() == 1:
                self.cpf.destroy()
        except:
            pass
        self.cpf = LabelFrame(self, text="Commands: ", font=('Helvetica', 32, 'bold', 'underline'))
        self.current = LabelFrame(self, text='Currently Playing: ', font=('Helvetica', 40, 'bold', 'underline'))
        self.upcoming = LabelFrame(self, text='Queue: ', font=('Helvetica', 32, 'bold', 'underline'))
        self.cpf.grid(row=5, column=0, columnspan=5)
        self.current.grid(row=6, column=0, columnspan=5, pady=50)
        self.upcoming.grid(row=7, column=0, columnspan=5)

        try:
            # display current song
            song_name = os.path.split(self.player.source_paths[0])[-1][:-4]
            self.label = Label(self.current, text="{} - {}".format(song_name, '0:00'), fg='red',
                               font=('Helvetica', 28, 'bold')).pack()
            with open('current_song.txt', 'w') as f:
                f.write(song_name)

        except IndexError:
            # if IndexError, clear queue because there should be no songs
            self.player.next_source()
            self.player.next_source()
            self.player.source_paths = []

        # display queue, up to 4 songs
        for i in range(len(self.player.source_paths[1:])):
            new = self.player.source_paths[1:]
            if i < 4:
                if (i % 2) == 0:
                    self.label = Label(self.upcoming, text=os.path.split(new[i])[-1][:-4],
                                       font=('Helvetica', 20, 'bold'), fg='green').pack()
                elif (i % 2) == 1:
                    self.label = Label(self.upcoming, text=os.path.split(new[i])[-1][:-4],
                                       font=('Helvetica', 20, 'bold'), fg='red').pack()

        # cpf frame
        def play1():
            self.player.play()

        def pause():
            self.player.pause()

        def skip(single_song=False):
            if not single_song:
                current = self.player.source
                # add source_path to list
                self.player.source_paths.append(self.player.source_paths[0])
                self.player.next_source()
                self.player.play()
                self.player.queue(current)
            else:
                self.player.next_source()
                self.player.play()

        def back15():
            current_time = self.player.time
            self.player.seek(int(current_time) - 15)

        def forward15():
            current_time = self.player.time
            self.player.seek(int(current_time) + 15)

        def adjust_volume(event=None):
            # set volume to value based on slider position
            self.player.current_volume = self.volume.get()
            self.player.volume = float((self.volume.get()) / 100)

        self.resume = Button(self.cpf, text="Play", font=('Helvetica', 17, 'bold'), command=play1, bg='green', padx=132)
        self.resume.grid(row=0, column=0, columnspan=3)
        self.backward = Button(self.cpf, text="<<15", font=('Helvetica', 17, 'bold'), command=back15, bg='orange')
        self.backward.grid(row=1, column=0)
        self.pause = Button(self.cpf, text='Pause', font=('Helvetica', 17, 'bold'), command=pause, bg='yellow', padx=47)
        self.pause.grid(row=1, column=1)
        self.forward = Button(self.cpf, text='15>>', font=('Helvetica', 17, 'bold'), command=forward15, bg='orange')
        self.forward.grid(row=1, column=2)
        self.skip = Button(self.cpf, text='Skip', font=('Helvetica', 17, 'bold'),
                           command=lambda boolean=single_song: skip(boolean),
                           bg='red', padx=130)
        self.skip.grid(row=2, column=0, columnspan=3)

        self.volume = Scale(self.cpf, from_=0, to=100, orient='horizontal', bg='green', command=adjust_volume)
        self.volume.grid(row=3, column=0, columnspan=3, ipadx=112)
        self.volume.set(self.player.current_volume)

    def shuffle(self, name):
        self.play(randomize=True, play_by_playlist_name=name)

    def choose_song(self, name):
        path = 'C:/spotify_app/playlists/{}'.format(name)
        self.filename = askopenfilename(initialdir=path,
                                        title="Select Song")
        if not self.filename == '':
            self.play(play_by_view=self.filename)

    def edit_playlist(self, name):
        try:
            path = 'C:/spotify_app/playlists/{}'.format(name)
            askopenfilename(initialdir=path,
                            title="Edit Playlist")
        except:
            pass

    def show_mframes(self):
        try:
            # get single_song from file
            with open('single_song_bool.json', 'r') as f:
                file = json.load(f)
                single_song = file['single_song']

            exists = [self.cpf.winfo_exists(), self.current.winfo_exists()]

            # if widgets exists, do not run below code
            if exists[0] and exists[1]:
                run_permission = False
            elif (not exists[0] and not exists[1]) or (exists[0] and not exists[1]) or (not exists[0] and exists[1]):
                run_permission = True

            if run_permission:
                try:
                    # new frame for cpf and current
                    self.nf = LabelFrame(self)
                    self.nf.grid(row=16, column=0, columnspan=10)

                    self.cpf = LabelFrame(self.nf, text="Commands: ", font=('Helvetica', 32, 'bold', 'underline'))
                    self.current = LabelFrame(self.nf, text='Currently Playing: ',
                                              font=('Helvetica', 40, 'bold', 'underline'))

                    # place frames in new frame at screen bottom on same row
                    self.cpf.grid(row=0, column=0, padx=(10, 0))
                    self.current.grid(row=0, column=1, padx=(50, 10))

                    # note: self.current is set up with f_run

                    # setup self.cpf
                    def play1():
                        self.player.play()

                    def pause():
                        self.player.pause()

                    def skip(single_song=False):
                        if not single_song:
                            current = self.player.source
                            # add source_path to list
                            self.player.source_paths.append(self.player.source_paths[0])
                            self.player.next_source()
                            self.player.play()
                            self.player.queue(current)
                        else:
                            self.player.next_source()
                            self.player.play()

                    def back15():
                        current_time = self.player.time
                        self.player.seek(int(current_time) - 15)

                    def forward15():
                        current_time = self.player.time
                        self.player.seek(int(current_time) + 15)

                    def adjust_volume(event=None):
                        # set volume to value based on slider position
                        self.player.current_volume = self.volume.get()
                        self.player.volume = float((self.volume.get()) / 100)

                    self.resume = Button(self.cpf, text="Play", font=('Helvetica', 17, 'bold'), command=play1,
                                         bg='green',
                                         padx=132)
                    self.resume.grid(row=0, column=0, columnspan=3)
                    self.backward = Button(self.cpf, text="<<15", font=('Helvetica', 17, 'bold'), command=back15,
                                           bg='orange')
                    self.backward.grid(row=1, column=0)
                    self.pause = Button(self.cpf, text='Pause', font=('Helvetica', 17, 'bold'), command=pause,
                                        bg='yellow',
                                        padx=47)
                    self.pause.grid(row=1, column=1)
                    self.forward = Button(self.cpf, text='15>>', font=('Helvetica', 17, 'bold'), command=forward15,
                                          bg='orange')
                    self.forward.grid(row=1, column=2)
                    self.skip = Button(self.cpf, text='Skip', font=('Helvetica', 17, 'bold'),
                                       command=lambda boolean=single_song: skip(boolean),
                                       bg='red', padx=130)
                    self.skip.grid(row=2, column=0, columnspan=3)

                    self.volume = Scale(self.cpf, from_=0, to=100, orient='horizontal', bg='green',
                                        command=adjust_volume)
                    self.volume.grid(row=3, column=0, columnspan=3, ipadx=112)
                    self.volume.set(self.player.current_volume)
                except:
                    pass
        except:
            pass

    def remove_playlist(self, name):
        path = 'C:/spotify_app/playlists/{}'.format(name)
        if os.path.isdir(path):
            if name != 'favorites':
                # asks for confirmation
                user_response = mb.askokcancel('Warning',
                                               "Pressing 'OK' will permanently remove this playlist and its contents.")
                # removes dir and its contents
                if user_response:
                    shutil.rmtree(path)
                    self.success()
                else:
                    return None
            else:
                self.sclear()
                self.label = Label(self, text="'Favorites' playlist cannot be removed",
                                   font=('Helvetica', 64, 'bold', 'underline'), fg='red',
                                   cursor='hand2', pady=1000, padx=1000)
                self.label.pack(pady=400)
                self.label.bind('<Button-1>', self.init)
        else:
            self.sclear()
            self.label = Label(self, text="Playlist does not exist",
                               font=('Helvetica', 64, 'bold', 'underline'), fg='red',
                               cursor='hand2', pady=1000, padx=1000)
            self.label.pack(pady=400)
            self.label.bind('<Button-1>', self.init)

    def check_playlist(self, name):
        for i in name:
            if i.lower() not in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q',
                                 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '1', '2', '3', '4', '5', '6', '7', '8',
                                 '9', '0', '_']:
                mb.showerror('Name Error', 'File name must be alpha-numeric')
                return False
        return True


class Init:
    def __init__(self):
        # create dirs if not exists
        if not os.path.isdir('C:/spotify_app'):
            os.mkdir('C:/spotify_app')
        if not os.path.isdir('C:/spotify_app/playlists'):
            os.mkdir('C:/spotify_app/playlists')
        if not os.path.isdir('C:/spotify_app/playlists/favorites'):
            os.mkdir('C:/spotify_app/playlists/favorites')

    def create_ssf(self):
        if not os.path.exists('single_song_bool.json'):
            with open('single_song_bool.json', 'w') as f:
                single_song_dict = {'single_song': None, 'run_permission': False}
                json.dump(single_song_dict, f)

    def sign_in(self):
        os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
        api_service_name, api_version = "youtube", "v3"
        client_secrets_file = "token.json"

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            client_secrets_file, scopes)
        credentials = flow.run_local_server()
        return googleapiclient.discovery.build(
            api_service_name, api_version, credentials=credentials)


def pyglet_mainloop():
    try:
        pyglet.app.run()
    except:
        mb.showerror('Application Crash',
                     'This player has stopped working for unknown reasons\nPlease: Refresh your playlist/select another and continue without the seek buttons\nOr\nRestart the application')


def pyglet_mainloop_threader():
    global thread
    thread = threading.Thread(target=pyglet_mainloop)
    thread.start()


def auto_update_time_and_check_mframe_display_threader():
    global thread1
    thread1 = threading.Thread(target=f_run(threading.Event()))
    thread1.start()


def auto_update_time():
    try:
        with open('current_song.txt', 'r') as f:
            song_name = f.read()
        for w in app.current.winfo_children():
            w.destroy()
        app.label = Label(app.current, text="{} - {}".format(song_name, time.strftime('%M:%S', time.gmtime(
            int(round(app.player.time))))), fg='red',
                          font=('Helvetica', 28, 'bold')).pack()
    except:
        pass


# check for displayed music frames every half second
# run auto_update_time every half_second
def f_run(f_stop):
    auto_update_time()
    # check
    if app.player.playing:
        app.show_mframes()

    # loop
    if not f_stop.is_set():
        threading.Timer(0.5, f_run, [f_stop]).start()

def on_closing():
    app.destroy()
    try:
        import sys
        sys.exit()
    except:
        try:
            os._exit(0)
        except:
            pass
    quit()

if __name__ == "__main__":
    # initialize application
    init = Init()
    init.create_ssf()

    youtube_credentials = init.sign_in()
    app = App()

    # prevent screen from resizing
    app.resizable(False, False)

    # bring screen to front
    app.attributes('-topmost', 1)
    app.update()
    app.attributes('-topmost', 0)

    # run auto_update_time and check_mframe_display
    auto_update_time_and_check_mframe_display_threader()


    # make sure app closes on exit
    app.protocol("WM_DELETE_WINDOW", on_closing)

    # run loops on separate threads
    pyglet_mainloop_threader()
    app.mainloop()
