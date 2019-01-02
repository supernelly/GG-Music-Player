import math, sys, copy, random
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter import filedialog
from music import MusicSystem
   
### CONTROL LOGIC ###
def AddSong():
    name1 = askopenfilename()
    print(name1)

def NewPlaylist():
    name2 = asksaveasfilename()
    print(name2)

def Quit():
    global root
    root.destroy()
    sys.exit()

def About():
    print("This is a music program.")
    
def play():
    global selected
    global playClick
    global songPause
    global currentlyPlaying
    
    if selected == "":
        print("Nothing selected")
        
    else: 
        if playClick == True:
            playClick = False
            player.play(selected)
            label2.config(text = selected)
            currentlyPlaying = selected
            
        if currentlyPlaying == selected and songPause == True:
            songPause = False
            player.pause()
            label2.config(text = selected)
            currentlyPlaying = selected
            
        if currentlyPlaying != selected:
            player.stop()
            player.play(selected)
            label2.config(text = selected)
            currentlyPlaying = selected    
   
def pause():
    global songPause   
    songPause = True
    player.pause() 
    
def forward():
    global currentlyPlaying
    global currentlyPlayingPlaylist
    global list2
    
    if selected == "" or currentlyPlayingPlaylist == "":
        print("Nothing selected") 
    else:
        file = open(currentlyPlayingPlaylist,"r").readlines()
        list2 = []
        row = 0
        for line in file:
            list2.append(str(line))
        list2 = [word.strip() for word in list1]    
        
        currentSongIndex = currentSongIndexNumber(currentlyPlaying)
        
        if currentSongIndex < len(list2) - 1:
            player.stop()
            player.play(list2[currentSongIndex + 1])
            label2.config(text = list2[currentSongIndex + 1])
            currentlyPlaying = list2[currentSongIndex + 1]
        if currentSongIndex == len(list2) - 1:
            player.stop()
            player.play(list2[0])
            label2.config(text = list2[0])
            currentlyPlaying = list2[0]  
    
def backward():
    global currentlyPlaying
    global currentlyPlayingPlaylist
    global list2
    
    if selected == "" or currentlyPlayingPlaylist == "":
        print("Nothing selected") 
    else:
        file = open(currentlyPlayingPlaylist,"r").readlines()
        list2 = []
        row = 0
        for line in file:
            list2.append(str(line))
        list2 = [word.strip() for word in list1]    
        
        currentSongIndex = currentSongIndexNumber(currentlyPlaying)
        
        if currentSongIndex > -1:
            player.stop()
            player.play(list2[currentSongIndex - 1])
            label2.config(text = list2[currentSongIndex - 1])
            currentlyPlaying = list2[currentSongIndex - 1] 

def cboxselect(evt): # Selecting playlist from combo box
    global firstClick
    global list1
    global playlistSelected
    firstClick = False
    
    # check if playlist exist
        # if playlist exist, open file, and make new playlist node, then add to label
        # if not choose from list of existing playlists
    
    
    
    # Tkinter passes an event object to cboxselect()
    lb.delete(0, END)
    u = cboxPlaylist.get()
    file = open(u,"r").readlines()
    playlistSelected = u
    list1 = []
    
    for line in file:
        list1.append(str(line))

    list1 = [word.strip() for word in list1]

    for v in range (len(list1)):
        lb.insert(v, list1[v])
    # cboxPlaylist.current(0) sets the selected item
    # cboxPlaylist.get() gets the selected item
    
def lbselect(evt): # Selecting song from playlist
    global selected
    global currentlyPlayingPlaylist
    global playlistSelected
    
    # Tkinter passes an event object to lbselect()
    if firstClick == False:
        try:
            selected = lb.get(lb.curselection())
            label4.config(text = selected)
            if selected == currentlyPlaying or currentlyPlaying == "Nothing":
                currentlyPlayingPlaylist = playlistSelected
        except:
            print("error: lbselect")
            
def reloadList(): # Used once at start
    global list1
    global playlistSelected
    
    file = open("All Playlist.txt","r").readlines()
    playlistSelected = "All Playlist.txt"
    list1 = []
    
    for line in file:
        list1.append(str(line))

    list1 = [word.strip() for word in list1]
    return list1
 
def currentSongIndexNumber(songPlaying): # Gets index value for playing song, returns -1 otherwise
    global list2
    
    if currentlyPlaying != "Nothing":
        i = 0
        for song in list2:
            if songPlaying == song:
                break
            else:
                i += 1
        return i
    else:
        return -1      
        

    
# Start Here #   
# Initialize #
currentSongIndex = 0 # Index number for currently playing song
currentlyPlaying = "Nothing" # Name for currently playing song
currentlyPlayingPlaylist = "" # Playlist for currently playing song
playlistSelected = ""

list1 = []
list2 = []
plSelectedDifferent = False
firstClick = True
playClick = True
songPause = False
selected = ""
player = BindVLC()

### GUI ###
root = tk.Tk()
menu = Menu(root)
root.config(menu = menu)
root.title("GG Music Player")
root.resizable(width = False, height = False)
root.geometry('550x300')

# Navigation bar
filemenu = Menu(menu, tearoff = 0)
menu.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Add Song", command = AddSong)
filemenu.add_command(label = "New Playlist", command = NewPlaylist)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = Quit)
helpmenu = Menu(menu, tearoff = 0)
menu.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "About...", command = About)

# Song playing label
label1 = Label(root, text = "Playing:")
label1.grid(column = 0, row = 0, sticky = E)
label2 = Label(root, text = "Nothing")
label2.grid(column = 1, row = 0, sticky = W)

# Play, Pause, Backward, Forward Buttons
buttonPlay = Button(root, text = 'Play', width = 9, command = play)
buttonPlay.grid(column = 2, row = 0)
buttonPause = Button(root, text = 'Pause', width = 9, command = pause)
buttonPause.grid(column = 3, row = 0)
buttonBackward = Button(root, text = 'Backward', width = 9, command = backward)
buttonBackward.grid(column = 4, row = 0)
buttonForward = Button(root, text = 'Forward', width = 9, command = forward)
buttonForward.grid(column = 5, row = 0)

# Combo Box
cboxLabel = Label(root, text = "Playlist:")
cboxLabel.grid(column = 0, row = 1, sticky = E)
cboxPlaylist = Combobox(root, state = "readonly", values = reloadList())
cboxPlaylist.bind("<<ComboboxSelected>>",cboxselect)
cboxPlaylist.grid(column = 1, row = 1, sticky = W)

# List Box
lb = Listbox(root, selectmode = "single", width = 40)
lb.bind('<<ListboxSelect>>',lbselect)
lb.grid(column = 0, row = 2, columnspan = 2)

# Song selected label
label3 = Label(root, text = "Selected:")
label3.grid(column = 2, row = 1)
label4 = Label(root, text = "Nothing")
label4.grid(column = 3, row = 1, columnspan = 4, sticky = W)

# Check for when song is finished (use player.playStatus())

mainloop()
