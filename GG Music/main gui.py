import math, sys, copy, time
from tkinter import *
import tkinter as tk
from tkinter.ttk import *
from tkinter.filedialog import *
from music import MusicSystem
from threading import Thread

### CONTROL LOGIC ###
def SetFolder(): # Changes library location
    path = askdirectory()
    player.setFolderPath(path)
    
    # check for playlist. and all songs.txt
    cboxPlaylist.config(values = reloadList())

def AddSong(): # Adds new song to library, get song name/artist and adds to library folder
    # Create new window
    t = tk.Toplevel()
    t.wm_title("Add Song")
    l = tk.Label(t, text="ree")
    l.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    
    buttonSelectSong = tk.Button(t, text = 'Select Song', width = 9, command = selectSong)
    buttonSelectSong.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    
    
    lbPL = Listbox(root, selectmode = "single", width = 40)
    lbPL.bind('<<ListboxSelect>>',plselect)
    lbPL.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    list1 = player.getAllPlaylist()
    for v in range (len(list1)):
        lbPL.insert(v, list1[v])
    
    buttonAdd= tk.Button(t, text = 'Add Song', width = 9, command = selectAdd)
    buttonAdd.pack(side="top", fill="both", expand=True, padx=5, pady=5)
    # 
    # Create new window to select playlist to add to (except All Songs, since its going there anyways)

    #player.newSong(playlist, name1)
    
def selectSong():
    name1 = askopenfilename(initialdir = "/",title = "Select Song",filetypes = (("mp3 files","*.mp3"),))
    print(name1)
def plselect(evt):
    print("re")
def selectAdd():
    #player.newSong(playlist, name1)
    print("re")
    
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
    
    # check if playlist exist
        # if playlist exist, open file, and make new playlist node, then add to label
        # if not choose from list of existing playlists
    
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

def thread2(): # This thread handles changing the labels
    while True:
        time.sleep(0.5)
        label2.config(text = player.playingSong)
   
# Start Here #   
# Initialize #
addSong = ""
addPlaylist = ""

selected = "Nothing"
playlistSelected = ""
list1 = []
firstClick = True
player = MusicSystem()

# GUI #
root = tk.Tk()
menu = Menu(root)
root.config(menu = menu)
root.title("GG Music Player")
root.resizable(width = False, height = False)
root.geometry('550x300')

# Navigation bar
filemenu = Menu(menu, tearoff = 0)
menu.add_cascade(label = "File", menu = filemenu)
filemenu.add_command(label = "Set Folder", command = SetFolder)
filemenu.add_command(label = "Add Song To Library", command = AddSong)
filemenu.add_command(label = "New Playlist", command = NewPlaylist)
filemenu.add_separator()
filemenu.add_command(label = "Exit", command = Quit)
helpmenu = Menu(menu, tearoff = 0)
menu.add_cascade(label = "Help", menu = helpmenu)
helpmenu.add_command(label = "About...", command = About)

# Song playing label
label1 = Label(root, text = "Playing:")
label1.grid(column = 0, row = 0, sticky = E)
label2 = Label(root, text = "")
label2.grid(column = 1, row = 0, sticky = W)
thread2 = Thread(target=thread2, args=())
thread2.start()          

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

<<<<<<< HEAD
# Check for when song is finished (use player.playStatus())

mainloop()
=======
mainloop()
>>>>>>> 223dff1621fc52d5a03a252031dd563667a1887e
