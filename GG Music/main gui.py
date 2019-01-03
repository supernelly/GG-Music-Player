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
    global playlistSelected
    
    if selected == "Nothing":
        print("Nothing selected")  
    else: 
        currentlyPlaying = True
        player.play(playlistSelected, selected)
   
def pause():
    player.pause() 
    
def forward():
    # do nothing if nothing is playing
    player.forward()
    
def backward():
    # do nothing if nothing is playing
    player.backward()
    
def cboxselect(evt): # Selecting playlist from combo box
    global firstClick
    global list1
    global selected
    global playlistSelected
    firstClick = False
        
    # Tkinter passes an event object to cboxselect()
    lb.delete(0, END)
    list1 = player.getSongList(cboxPlaylist.get())
    playlistSelected = cboxPlaylist.get()
    
    for v in range (len(list1)):
        lb.insert(v, list1[v])
    
    try:
        selected = list1[0]
        label4.config(text = selected)
    except:
        selected = "Nothing"
        label4.config(text = "Nothing")
        
    # cboxPlaylist.current(0) sets the selected item
    # cboxPlaylist.get() gets the selected item
    
def lbselect(evt): # Selecting song from playlist
    global selected
    global firstClick
    global list1
    
    # Tkinter passes an event object to lbselect()
    if firstClick == False:
        try:
            selected = lb.get(lb.curselection())
            label4.config(text = selected)
        except:
            try:
                selected = list1[0]
                label4.config(text = selected)
            except:
                selected = "Nothing"
                label4.config(text = "Nothing")                
            
def reloadList(): # Used once at start
    list1 = player.getAllPlaylist()
    return list1      

    
# Start Here #   
# Initialize #
selected = "Nothing"
playlistSelected = ""
list1 = []
firstClick = True
currentlyPlaying = False
player = MusicSystem()

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
