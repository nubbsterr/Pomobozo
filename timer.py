# Libraries
import tkinter as tk # GUI setup by tkinter
from tkinter import messagebox # used to create messageboxes to display on screen when break time expires

from PIL import Image, ImageTk # image resizing, that's literally it

import pygame # soley for playing audio, playsound couldn't work :c
import random as rand # used for creating random usernames if no username is given on login screen
import time # used for creating 1 second interval between timer update on screen and decrementing time
import os # allows specified file permissions (read-only login details)

# window setup
root = tk.Tk() # create new window
root.title("Pomobozo Timer") # window title

# font styles
titleFont = ("DejaVu Sans Mono", 15)
headingFont = ("DejaVu Sans Mono", 10)
normaltextFont = ("DejaVu Sans Mono", 8)

# bg colour and font colour setup
global bgColour
bgColour = "white"
global fontColour
fontColour = "#040406"

# final window setup
WIDTH = 250
HEIGHT = 200
root.geometry(f"{WIDTH}x{HEIGHT}")
root.configure(background=bgColour)

# "Backend" functionality (before main timer GUI loads)
def LoadAbsolutePath(filename):
	"""
	Loads absolute path of file with added filename. Uses executables' absolute path.
	"""
	script_dir = os.path.dirname(os.path.abspath(__file__)) # absolute path of script

	parent_dir = os.path.dirname(script_dir) # navigate back one directory to Drive:\Users\user\InstallLocationOfEXE\timer
	internals_dir = os.path.join(parent_dir, "_internal") # navigates to internal file to grab images

	filePATH = str(os.path.join(internals_dir, f"{filename}")) # tags described filename from function input

	return filePATH

def SaveLogin(username):
	"""
	Saves username for future logins. Read-only permissions on file.
	"""

	loginDetailLocation = LoadAbsolutePath("logindetails.txt")

	with open(loginDetailLocation, "w") as file:
		if (username == "Enter your name :)") or (username == ""):
			file.write(f"Guest\n1")
			ChooseTime("Guest")
		else:
			file.write(f"{username}\n1") # 1 is a special identifier to bypass the basic login screen on startup for future sessions
			ChooseTime(username)
	os.chmod(loginDetailLocation, 0o444) # read-only permissions active after writing to file, using octal integer mode
	
	stat_info = os.stat(loginDetailLocation)
	print(f"Saved login details with permissions: {stat_info.st_mode}.")

def StartPygame():
	"""
	Initializes pygame for later use with playing audio.
	"""
	pygame.init()

def StartApp():
	"""
 	Creates login screen if no stored username can be found.
	"""
	# globalling vars into function to access them
	global fontColour
	global bgColour

	# random sentence on startup for some flair
	startsentences = ['how have you been?', 'get to work bozo.', 'enter your name to get started.', 'revving up those fryers...', 'completing domain...', 'trying to acquire Rigidbody...', 'adding force to rb...', 'instantiating...', 'particles systems...', 'maximum productivity!']
	
	# light mode by default, no dark mode integration since that'd require way too much tinkering
	bgColour = "white"
	fontColour = "#040406"
	root.configure(background="white")
	ryoThumbs_img = Image.open(LoadAbsolutePath("ryoThumbs_white.png"))

	# icon setup (definitely didn't take 2 days to complete)
	photo = tk.PhotoImage(file = LoadAbsolutePath("ryoyamada.png")) # we love ryo
	root.iconphoto(False, photo)
	
	# text setup
	mainText = tk.Label(root, text="Welcome back.", bg=bgColour, foreground= fontColour, font = titleFont)
	secondaryText = tk.Label(root, text= rand.choice(startsentences), bg = bgColour, foreground= fontColour, font = normaltextFont)
	nameEntry = tk.Entry(root, bg=bgColour, foreground= fontColour, font = normaltextFont, width = 19)
	versionText = tk.Label(root, text="Pomobozo Timer v1.0.0-alpha", bg=bgColour, foreground= "#c2c0c0", font = normaltextFont)

	# thumbs up img next to name entry (we love ryo)
	resized_image = ryoThumbs_img.resize((31, 25))
	img = ImageTk.PhotoImage(resized_image)

	ryoThumbs = tk.Label(image=img)
	ryoThumbs.image = img
	ryoThumbs.pack()
	ryoThumbs.place(x=WIDTH/2-40, y=HEIGHT/2 + 60, anchor= "center")
	continueButton = tk.Button(root, text="Ready?", bg=bgColour, foreground= fontColour, font = normaltextFont, command= lambda: [SaveLogin(nameEntry.get()), ryoThumbs.destroy(),mainText.destroy(), secondaryText.destroy(), continueButton.destroy(), infoButton.destroy(), nameEntry.destroy()]) # clear the screen basically, then continue to the next program phase
	infoButton = tk.Button(root, text= "Program Info", bg=bgColour, foreground= fontColour, font = normaltextFont, command = lambda: [messagebox.showinfo("We're here to help :D", "This is the login page which contains a small box to enter your username for future sessions.\n\nBe warned that if it is too long it will be sliced to fit the UI.\n\nIt's also worth noting that once the break timer is over, you'll promptly exit the program.\n\nYou'll need to restart the program again (loop functionality makes rerunning everything a pain, sorry)\n\nResizing the window is not recommended as widgets do not stretch to fit, so don't go insane when things don't look right.\n\nPast that, there isn't much else to assist with here. If you wish to end the work or break timers while running, you can always close the window (no you cannot skip to breaks, keep working!!)")])

	# packing area
	mainText.pack()
	secondaryText.pack()
	nameEntry.pack()
	versionText.pack()
	infoButton.pack()
	continueButton.pack()

	# placement area
	mainText.place(x=WIDTH/2, y=HEIGHT/2-30, anchor= "center")
	secondaryText.place(x=WIDTH/2, y=HEIGHT/2 - 5, anchor= "center")
	nameEntry.place(x=WIDTH/2, y=HEIGHT/2 + 25, anchor= "center")
	nameEntry.insert(0,"Enter your name :)")
	versionText.place(x=5, y=HEIGHT-10, anchor="w")
	infoButton.place(x=WIDTH/2, y=30, anchor = "center")
	continueButton.place(x=WIDTH/2+10, y=HEIGHT/2 + 60, anchor= "center")

def AuthUser():
	"""
	Find user login details before going to login page.
	Otherwise goes straight to ChooseTime page.
	"""
	try:
		loginDetailLocation = LoadAbsolutePath("logindetails.txt")
		print(loginDetailLocation)
		with open(loginDetailLocation, "r") as file:
			fileContent = file.readlines()
			if fileContent[1] == "1":
				ChooseTime(fileContent[0]) # immediately go to choosing time screen with stored username
	except FileNotFoundError:
		print("No saved login details. Login started")
		StartApp()

# GUI runtime functions
def PlayTimerEndSFX():
	"""
	Plays a digital alarm clock SFX when the break and work timers end respectively.
	"""
	timerSFXpath = (LoadAbsolutePath("timerEnd.mp3"))
	pygame.mixer.music.load(timerSFXpath)
	pygame.mixer.music.play()

def FreeApp():
	"""
	Free up system resources of application by killing GUI and ending pygame process. Runs on attempted force close.
	"""
	print("Force close detected, exiting.\n\n== Tkinter Callback may occur due to widget destruction. Please ignore. ==\n\n")
	root.destroy()
	pygame.quit()

def TimerStart(workMins, breakMins):
	"""
 	Shows pomodoro timer on screen. When timer runs out, play an audio cue and allow start the break timer immediately. Exits program when break is over.
	"""
	# set up counting vars (second counting, mins decrementing, etc)
	isWorking = True # controls whether the break or work timer is operating
	onBreak = False # needed to exit out of break time loop
	currentWorkTime = 0 # work time in seconds, starts as 0 but is adjusted in accordance to value as it decrements
	currentBreakTime = 0 # same logic here

	# text setup before timer starts (so it appears on screen, packing and placing everything here)
	remainingTime = tk.Label(root, text= "Remaining work time.", font= ("DejaVu Sans Mono", 11), bg= bgColour, fg= fontColour)
	remainingTime.pack()
	remainingTime.place(x=WIDTH/2,y=HEIGHT/2-60,anchor="center")

	infoText = tk.Label(root, text= "You will be notified when the timer expires :)", font= normaltextFont, bg= bgColour, fg= fontColour,wraplength= WIDTH-30)
	infoText.pack()
	infoText.place(x=WIDTH/2,y=HEIGHT/2+10,anchor="center")

	infoText2 = tk.Label(root, text= "(get to work lol)", font= normaltextFont, bg= bgColour, fg= fontColour,wraplength= WIDTH-30)
	infoText2.pack()
	infoText2.place(x=WIDTH/2,y=HEIGHT/2+40,anchor="center")
	
	# protocal to catch window being force closed
	root.protocol("WM_DELETE_WINDOW", FreeApp)

	# work timer decrementing logic
	while isWorking and not onBreak:
		while True:
			if workMins == 0 and currentWorkTime <= 0:
				isWorking = False # needed to stop working timer and start break timer (!! does NOT break out of loop, that's why the break line below is needed !!)
				onBreak = True
				break # exit from the working time loop and go to break
			workTime_ = tk.Label(root, text= f"{workMins}:{currentWorkTime} mins left", font= ("DejaVu Sans Mono", 12, "bold"), bg= bgColour, fg= fontColour, padx=5)
			workTime_.pack()
			workTime_.place(x=WIDTH/2,y=HEIGHT/2-30,anchor="center")
			currentWorkTime-=1
			if currentWorkTime == -1:
				currentWorkTime = 59
				workMins -=1
			if currentWorkTime < 10: # just so there isn't a floating single digit past the colon; looks goofy without the zero
				workTime_ = tk.Label(root, text= f"{workMins}:0{currentWorkTime} mins left", font= ("DejaVu Sans Mono", 12, "bold"), bg= bgColour, fg= fontColour, padx=5)
				workTime_.pack()
				workTime_.place(x=WIDTH/2,y=HEIGHT/2-30,anchor="center")
			root.update()
			time.sleep(1)
			workTime_.destroy() # working timer decrementing logic

	# destroy work elements before transitioning to break time--creates breaktime text and stuff, also plays timer ending sfx
	PlayTimerEndSFX()

	workTime_.destroy()
	remainingTime.destroy()
	infoText.destroy()
	infoText2.destroy()

	remainingBreakTime = tk.Label(root, text= "Break Time!", font= ("DejaVu Sans Mono", 11), bg= bgColour, fg= fontColour)
	remainingBreakTime.pack()
	remainingBreakTime.place(x=WIDTH/2,y=HEIGHT/2-60,anchor="center")

	infoText_ = tk.Label(root, text= "You will be notified when your break's over :)", font= normaltextFont, bg= bgColour, fg= fontColour,wraplength= WIDTH-30)
	infoText_.pack()
	infoText_.place(x=WIDTH/2,y=HEIGHT/2+10,anchor="center")

	infoText2_ = tk.Label(root, text= "(go do something fun now!)", font= normaltextFont, bg= bgColour, fg= fontColour,wraplength= WIDTH-30)
	infoText2_.pack()
	infoText2_.place(x=WIDTH/2,y=HEIGHT/2+40,anchor="center")

	# break time logic, exits program once break is over
	while not isWorking and onBreak and (workMins == 0 and currentWorkTime <= 0):
		while True:
			if breakMins == 0 and currentBreakTime <= 0:
				onBreak = False 
				break # exit from the break time loop and notify the user that they're break is over and they can start a new session when they're ready through a button press
			breakTime_ = tk.Label(root, text= f"{breakMins}:{currentBreakTime} mins left", font= ("DejaVu Sans Mono", 12, "bold"), bg= bgColour, fg= fontColour, padx=5)
			breakTime_.pack()
			breakTime_.place(x=WIDTH/2,y=HEIGHT/2-30,anchor="center")
			currentBreakTime-=1
			if currentBreakTime == -1:
				currentBreakTime = 59
				breakMins -=1
			if currentBreakTime < 10: # just so there isn't a floating single digit past the colon; looks goofy without the zero
				breakTime_ = tk.Label(root, text= f"{breakMins}:0{currentBreakTime} mins left", font= ("DejaVu Sans Mono", 12, "bold"), bg= bgColour, fg= fontColour, padx=5)
				breakTime_.pack()
				breakTime_.place(x=WIDTH/2,y=HEIGHT/2-30,anchor="center")
			root.update()
			time.sleep(1)
			breakTime_.destroy() # working timer decrementing logic

	# message box appears after break time is over, also plays timer ending sfx
	PlayTimerEndSFX()

	messageboxsentences = ["Break's Over!", "Your work session is over.", "see u again soon :)", "were you productive today?", 'great job working today!', 'thanks for your time :)'] # added flair to the message box
	if messagebox.showinfo(rand.choice(messageboxsentences), "Your session will be closed once this pop-up is closed.\n\nYou can restart the app to start a new session :)", default= "ok",parent= root): # after closing out of the message box, everything below it will run (i.e. we'll return to the main menu again)
		FreeApp()

def EntryCheck(customWorkEntry, customBreakEntry, workButtonVal, breakButtonVal, username): # will take all parameters from before (intvars and entries)
	"""
 	Checks all entries and inputed radiobuttons before timer start. Takes entries if inputed, takes radiobuttons if left empty or as default entry.
	"""
	startTimesentences = ['Your work session.', 'Your work session today.', 'Your work session for today.', 'Ready to start?', 'dis good?', 'good to go?', 'ready?'] # more random sentences for added flair
	defaultWorkOpt = ["Work Time", "", "0"]
	defaultBreakOpt = ["Break Time", "", "0"]
	if customWorkEntry.strip() in defaultWorkOpt:
		workTime = workButtonVal
	elif customWorkEntry.strip() not in defaultWorkOpt:
		try: # take the entry as the value, but if they didn't type an integer, use the default value
			if not int(customWorkEntry) in range(121, 1001):
				workTime = int(customWorkEntry)
			else:
				workTime = workButtonVal
		except ValueError:
			workTime = workButtonVal
	
	if customBreakEntry.strip() in defaultBreakOpt:
		breakTime = breakButtonVal
	elif customBreakEntry.strip() not in defaultBreakOpt:
		try: # same thing as above but taking the default break time option
			if not int(customBreakEntry) in range(121, 1001):
				breakTime = int(customBreakEntry)
			else:
				breakTime = breakButtonVal
		except ValueError:
			breakTime = breakButtonVal
	
	# text setup
	warningText = tk.Label(root, text= rand.choice(startTimesentences), font= ("DejaVu Sans Mono", 10, "bold"), bg= bgColour, fg= fontColour)
	finalWorkText = tk.Label(root, text= f"Work Time: {workTime} minutes", font=normaltextFont, bg=bgColour, foreground=fontColour, padx= 6, pady= 3)
	finalBreakText = tk.Label(root, text= f"Break Time: {breakTime} minutes", font=normaltextFont, bg=bgColour, foreground=fontColour, padx=6, pady=3)

	# button setup to continue to main timer
	continueButton = tk.Button(root, text= "Continue to timer.", bg=bgColour, foreground= fontColour, font = normaltextFont, command= lambda: [warningText.destroy(), finalWorkText.destroy(), finalBreakText.destroy(),continueButton.destroy(),returnButton.destroy(), TimerStart(workTime, breakTime)], width= 20, height= 1)
	returnButton = tk.Button(root, text= "Change times?", bg=bgColour, foreground= fontColour, font = normaltextFont, command= lambda: [ChooseTime(username), warningText.destroy(), finalWorkText.destroy(), finalBreakText.destroy(),continueButton.destroy(), returnButton.destroy()], width= 20, height= 1)
	
	# packing area
	warningText.pack()
	finalWorkText.pack()
	finalBreakText.pack()
	continueButton.pack()
	returnButton.pack()
	
	# placement area
	warningText.place(x= WIDTH/2, y= HEIGHT/2-60, anchor = "center")
	finalWorkText.place(x= WIDTH/2, y= HEIGHT/2-30, anchor = "center")
	finalBreakText.place(x= WIDTH/2, y= HEIGHT/2-10, anchor = "center")
	continueButton.place(x= WIDTH/2, y= HEIGHT/2+30, anchor = "center")
	returnButton.place(x=WIDTH/2, y=HEIGHT/2+60, anchor = "center")

def ChooseTime(username):
	"""
 	Time picking menu. Runs after login is complete. Takes input from user for work/break time.
	"""
	# shorten username if too long, otherwise keep original length
	if len(username) > 20:
		username = username[:20] # splice username to 10th character
	else:
		username = username
	
	# text setup
	WelcomeText = tk.Label(root, text= "Welcome back, ", bg=bgColour, foreground= fontColour, font = headingFont)
	name = tk.Label(root, text = username.lower().strip(), bg=bgColour, foreground= fontColour, font = ("DejaVu Sans Mono", 10, "bold"))
	workText = tk.Label(root, text= "Work Time (mins):", bg=bgColour, foreground= fontColour, font = normaltextFont)
	breakText = tk.Label(root, text= "Break Time (mins):", bg=bgColour, foreground= fontColour, font = normaltextFont)
	customText = tk.Label(root, text= "Custom Times (mins):", bg=bgColour,foreground= fontColour, font = normaltextFont)

	# intvars to control default selection, also to acquire work and break times before timer start
	workTime = tk.IntVar(value= 30)
	breakTime = tk.IntVar(value= 5)
	
	# radiobutton setup (time intervals)
	work10mins = tk.Radiobutton(root, text= "10", variable= workTime, value= 10, bg=bgColour, foreground= fontColour, font = normaltextFont)
	work20mins = tk.Radiobutton(root, text= "20", variable= workTime, value= 20, bg=bgColour, foreground= fontColour, font = normaltextFont)
	work30mins = tk.Radiobutton(root, text= "30", variable= workTime, value= 30, bg=bgColour, foreground= fontColour, font = normaltextFont)
	work45mins = tk.Radiobutton(root, text= "45", variable= workTime, value= 45, bg=bgColour, foreground= fontColour, font = normaltextFont)

	break5mins = tk.Radiobutton(root, text= "5", variable= breakTime, value= 5, bg=bgColour, foreground= fontColour, font = normaltextFont)
	break10mins = tk.Radiobutton(root, text= "10", variable= breakTime, value= 10, bg=bgColour, foreground= fontColour, font = normaltextFont)
	break15mins = tk.Radiobutton(root, text= "15", variable= breakTime, value= 15, bg=bgColour, foreground= fontColour, font = normaltextFont)
	
	# entry setup (custom time intervals)
	customTime = tk.Entry(root, bg=bgColour, foreground= fontColour, font = normaltextFont, width= 10)
	customTime.insert(0,"Work Time")
	customBreak = tk.Entry(root, bg=bgColour, foreground= fontColour, font = normaltextFont, width= 10)
	customBreak.insert(0, "Break Time")
	
	# button setup (start/pause timer)
	ReadyButton = tk.Button(root, text= "Start.", bg=bgColour, foreground= fontColour, font = normaltextFont, command= lambda: [EntryCheck(customTime.get(),customBreak.get(),workTime.get(), breakTime.get(), username), WelcomeText.destroy(), name.destroy(), workText.destroy(), breakText.destroy(), customText.destroy(), work10mins.destroy(), work20mins.destroy(), work30mins.destroy(), work45mins.destroy(), break5mins.destroy(), break10mins.destroy(), break15mins.destroy(), customTime.destroy(), customBreak.destroy(),ReadyButton.destroy()], width= 7, height= 1, activebackground= fontColour, activeforeground= bgColour) # this is a massive command, but we're basically taking all the user input out of the entry boxes and radiobuttons, then clearing the screen by destroying all the other on-screen widgets
	
	# packing area
	WelcomeText.pack()
	name.pack()
	workText.pack()
	breakText.pack()
	customText.pack()

	work10mins.pack()
	work20mins.pack()
	work30mins.pack()
	work45mins.pack()

	break5mins.pack()
	break10mins.pack()
	break15mins.pack()

	customTime.pack()
	customBreak.pack()

	ReadyButton.pack()
	
	# placemeant area
	WelcomeText.place(x= 5, y= 5)
	name.place(x= WIDTH/2-25, y= 5)
	workText.place(x= 5, y= 40)
	breakText.place(x= 5, y= 100)
	customText.place(x=5 , y= 150)

	work10mins.place(x= 5, y= 60)
	work20mins.place(x= 60, y= 60)
	work30mins.place(x= 115, y= 60)
	work45mins.place(x= 170, y= 60)

	break5mins.place(x=5, y= 120)
	break10mins.place(x=60, y= 120)
	break15mins.place(x=115, y= 120)

	customTime.place(x= 5, y= 170)
	customBreak.place(x= WIDTH/2-50, y= 170)

	ReadyButton.place(x=WIDTH/2+35, y=163)

AuthUser() # login detail check
StartPygame() # run pygame in background for music loading and playing

tk.mainloop() # keep the window running and updating until clossed