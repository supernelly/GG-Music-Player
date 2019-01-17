import math, sys, copy, random, vlc, os, time
from threading import Thread
from queue import Queue
# Interface only needs to import MusicSystem from this file
# Interface only needs to use MusicSystem.

class Song: # Holds song name and artist
    def __init__(self, Name, Artist):
        self.songName = Name
        self.songArtist = Artist

class Node:
    def __init__(self):
        self.Data = None
        self.Next = None
        
class Playlist: # Holds songs as nodes
    def __init__(self, Name):
        self.playListName = Name
        self.current = None
        self.size = 0
        
    def addSong(self, song):
        newNode = Node() # Create new node
        newNode.Data = song
        newNode.Next = self.current # Link new node to previous node
        self.current = newNode # Set current node to new node
        self.size += 1
    
    def printList(self):
        node = self.current
        print(self.playListName)
        while node:
            print("    " + node.Data.songArtist + " - " + node.Data.songName)
            node = node.Next
    
    def checkSong(self, song):
        node = self.current
        while node:
            if (node.Data.songArtist + " - " + node.Data.songName) == song:
                return True
            node = node.Next
        return False
        
    def getSongs(self): # Returns songs in playlist in a list
        node = self.current
        list1 = []
        while node:
            list1.append(node.Data.songArtist + " - " + node.Data.songName)
            node = node.Next
        return list1
    
    def removeHead(self):      
        while self.current:
            self.current = None
            self.playListName = None
            self.size = 0
            self.current = self.current.Next
    
class ListPlaylist: # Holds playlists as nodes
    def __init__(self):
        self.current = None
        self.size = 0
        
    def addPlaylist(self, playlist):
        newNode1 = Node() # Create new node
        newNode1.Data = playlist
        newNode1.Next = self.current # Link new node to previous node
        self.current = newNode1 # Set current node to new node
        self.size += 1
    
    def printList(self):
        node = self.current
        while node:
            node.Data.printList()
            node = node.Next
    
    def checkPlaylist(self, playlist): # Accepts string. Returns True if exists, returns False otherwise
        node = self.current
        while node:
            if node.Data.playListName == playlist:
                return True
            node = node.Next
        return False
        
    def checkPlaylistSong(self, playlist, song): # Accepts string. Returns True if song exists, returns False otherwise
        node = self.current
        while node:
            if node.Data.playListName == playlist:
                return node.Data.checkSong(song)
            node = node.Next
        return False
        
    def getAllPlaylist(self): # Returns all playlist names in a list
        node = self.current
        list1 = []
        while node:
            list1.append(node.Data.playListName)
            node = node.Next
        return list1

    def getSongList(self, playlist): # Returns songs in playlist in a list
        node = self.current
        while node:
            if node.Data.playListName == playlist:
                return node.Data.getSongs()
            node = node.Next
        return []
        
    def removeHead(self): # Removes reference to first node
        while self.current:
            self.current = None
            self.size = 0
            self.current.Data.removeHead()
            self.current = self.current.Next
    
class LoadMusic:
    def __init__(self):
        self.folderPath = "C:/Users/nelso/Documents/GitHub/GG-Music-Player/GG Music"
        self.reloadMusic()
        
    def setFolderPath(self, path):
        self.folderPath = path
        #self.mainList.removeHead()
        del self.mainList
        self.reloadMusic()
    
    def getFolderPath(self):
        return self.folderPath
        
    def reloadMusic(self): # Use at start and everytime new playlist or song is added
        self.mainList = ListPlaylist() # Create ListPlaylist object
        
        # Parse all playlists
        file = open(self.folderPath + "/" + "All Playlist.txt", "r").readlines()
        list1 = [] # List that holds names of playlists
        for line in file:
            list1.append(str(line))
        list1 = [word.strip() for word in list1]
        list1 = list1[::-1] # Reverse list
        
        # Parse all songs
        for plName in list1:
            self.mainPlaylist = Playlist(plName.replace(".txt", "")) # Create playlist object
            
            list2 = [] # List that holds song names
            file = open(self.folderPath + "/" + plName, "r").readlines()
            for line1 in file:
                list2.append(str(line1))
            list2 = [word.strip() for word in list2]
            list2 = list2[::-1] # Reverse list
            
            # Parse song name and artist
            for x in list2:
                list3 = x.split(" - ")

                # Create song object
                self.mainSong = Song(list3[1].replace(".mp3", ""), list3[0])
      
                # Add songs to playlist
                self.mainPlaylist.addSong(self.mainSong)
            
            # Add playlist to mainList
            self.mainList.addPlaylist(self.mainPlaylist)   
       
    def checkPlaylist(self, playlist): # Accepts string. Returns True if playlist exists, returns False otherwise
        return self.mainList.checkPlaylist(playlist)
        
    def checkPlaylistSong(self, playlist, song): # Accepts string. Returns True if song exists, returns False otherwise
        return self.mainList.checkPlaylistSong(playlist, song)
   
    def getAllPlaylist(self): # Returns all playlist names in a list
        return self.mainList.getAllPlaylist()

    def getSongList(self, playlist): # Returns songs in playlist in a list
        return self.mainList.getSongList(playlist)
    
    def printList(self):
        self.mainList.printList()

class MusicSystem: # Add new playlists and new songs using this class
    def __init__(self):
        self.m = LoadMusic()
        self.vlc = BindVLC()
        self.queue = Queue()
        self.playingPlaylist = ""
        self.playingSong = ""
        self.firstPlay = True
        self.playPressed = False
        self.songPaused = False
        self.pos = 0
            
    def setFolderPath(self, path):
        self.m.setFolderPath(path)
        
        # Reload LoadMusic()
        self.m.reloadMusic()
    
    def getFolderPath(self):
        return self.m.getFolderPath()
    
    def newPlaylist(self, playlist):
        # Create new file with playlist name
        file = open(self.m.getFolderPath() + "/" + playlist + ".txt", "w+")
        file.close()
        
        # Add to 'All Playlist.txt'
        file = open(self.m.getFolderPath() + "/" + "All Playlist.txt", "a+")
        file.write("\n" + playlist + ".txt")
        file.close()
        
        # Reload LoadMusic()
        self.m.reloadMusic()
        
    def newSong(self, playlist, name): # Accepts string. Adds song to playlist file
        if self.m.checkPlaylist(playlist) == True and self.m.checkPlaylistSong(playlist, name) == False and self.m.checkPlaylistSong("All Songs", name) == False: # If playlist exists and song doesn't exist in playlist and song doesn't exist in "All Songs"
            # Add file name to playlist txt file
            if os.path.getsize(self.m.getFolderPath() + "/" + playlist + ".txt") > 0: # If playlist isn't empty
                file = open(self.m.getFolderPath() + "/" + playlist + ".txt", "a+")
                file.write("\n" + name + ".mp3")
                file.close()
            else: # If playlist is empty
                file = open(self.m.getFolderPath() + "/" + playlist + ".txt", "a+")
                file.write(name + ".mp3")
                file.close()                
            
            if playlist != "All Songs.txt":
                # Add file name to "All Songs.txt"
                file = open(self.m.getFolderPath() + "/" + "All Songs.txt", "a+")
                file.write("\n" + name + ".mp3")
                file.close()
        
        if self.m.checkPlaylist(playlist) == False and self.m.checkPlaylistSong("All Songs", name) == False: # If playlist doesn't exists and song doesn't exists in "All Songs"
            # Add file name to "All Songs.txt"
            file = open(self.m.getFolderPath() + "/" + "All Songs.txt", "a+")
            file.write("\n" + name + ".mp3")
            file.close()
        
        if self.m.checkPlaylist(playlist) == True and self.m.checkPlaylistSong("All Songs", name) == True and self.m.checkPlaylistSong(playlist, name): # If playlist exists and song already exists in "All Songs" but isn't in playlist
            # Add file name to playlist txt file
            if os.path.getsize(self.m.getFolderPath() + "/" + playlist + ".txt") > 0: # If playlist isn't empty
                file = open(self.m.getFolderPath() + "/" + playlist + ".txt", "a+")
                file.write("\n" + name + ".mp3")
                file.close()
            else: # If playlist is empty
                file = open(self.m.getFolderPath() + "/" + playlist + ".txt", "a+")
                file.write(name + ".mp3")
                file.close()  
            
        # Reload LoadMusic()
        self.m.reloadMusic()
        
    def getAllPlaylist(self): # Returns all playlist names in a list
        return self.m.getAllPlaylist()
    
    def getSongList(self, playlist): # Returns songs in playlist in a list
        return self.m.getSongList(playlist)
  
    def addQueue(self, playlist, name): # Adds playlist to queue starting at song name
        while not self.queue.empty(): # Empty queue
            self.queue.get()

        list1 = self.getSongList(playlist)
        reachedName = False
        for a in list1:
            if a == name:
                reachedName = True
                self.queue.put(a)
            elif reachedName == True:
                self.queue.put(a)
        self.queue.put(None)
        self.playPressed = True
        
    def thread1(self):
        while True:
            #if a is None: return # Poison pill
            time.sleep(1)
            if self.vlc.playStatus() == 0: # If nothing is playing
                self.playPressed = False
                a = self.queue.get()
                if a is not None:
                    self.vlc.play(self.getFolderPath() + "/" + a + ".mp3")
                self.playingSong = a
                print(a)
                time.sleep(1)
            elif self.vlc.playStatus() == 1 and self.playPressed == True: # If something is playing and play has been pressed
                self.playPressed = False
                self.vlc.stop()
                a = self.queue.get()
                self.vlc.play(self.getFolderPath() + "/" + a + ".mp3")
                print(a)
                time.sleep(1)
            if self.queue.empty():
                self.playingSong = ""
                
    def play(self, playlist, name): # Example, playSong("All Songs", "Adele - Hello")
        if self.firstPlay == True: # First time playing
            self.firstPlay = False
            # Play song in new tread
            self.thread1 = Thread(target=self.thread1, args=())
            self.thread1.start()
            
        if self.playingSong == name and self.playingPlaylist == playlist: # If song is already playing
            print("Song already playing")
        else:
            self.playingPlaylist = playlist
            self.playingSong = name
            
            self.addQueue(playlist, name) # Adds playlist to queue starting at song
        
    def pause(self):
        self.vlc.pause()

    def forward(self):
        self.vlc.setPosition(1.0)
        
    def backward(self):
        list1 = self.getSongList(self.playingPlaylist)
        if self.playingSong == list1[0]: # Check if at beginning of song list
            self.addQueue(self.playingPlaylist, self.playingSong) # Adds playlist to queue starting at song
        else: # Play previous song
            list1.reverse()
            count = 0
            for x in list1:
                if x == self.playingSong:
                    count1 = count
                    break
                count += 1
            try:
                self.addQueue(self.playingPlaylist, list1[count1 + 1]) # Adds playlist to queue starting at song
                self.playingSong = list1[count1 + 1]
            except:
                print("No queue")
            
    def printList(self):
        self.m.printList()
        
class BindVLC:
    def __init__(self):
        self.player = vlc.MediaPlayer()
    
    def play(self, song): # Play song from beginning
        self.player = vlc.MediaPlayer(song)
        self.player.play()
        
    def pause(self): # Pause/Unpause song
        self.player.pause()
        
    def stop(self): # Stop song
        self.player.stop()
        
    def playStatus(self): # Returns 0 if nothing is playing, 1 if playing
        return self.player.is_playing()

    def getPosition(self): # Get song position as percentage between 0.0 and 1.0 (float)
        return self.player.get_position()
        
    def setPosition(self, pos): # Set song position as percentage between 0.0 and 1.0 (float)
        self.player.set_position(pos)
    
# Test #
#abc = MusicSystem()
#abc.SetFolder(a)
#abc.printList()


