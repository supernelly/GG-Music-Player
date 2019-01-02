from music import MusicSystem

m = MusicSystem()
programRunning = True
while programRunning:
    cmd = raw_input()
        
    if cmd == "quit":
        programRunning = False
        
    elif cmd == "help":
    
    elif cmd == "print": # Prints song library
    
    elif cmd == "play": # Plays song
        print("Select playlist")
        playlistSelect = raw_input()
    
    else:    