import instaloader, time, os, json, matchface
import tkinter as ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
from datetime import datetime
from matchface import matcher

class UI :
	def __init__(self):
		self.jDic, self.flag = self.load_json()
		if self.flag:
			self.instaObj = instaloader.Instaloader()
			self.val_dict = { "authImage" : self.jDic["wrong"]}
			self.flagVals = {"cred":False, "getFollowers":False, "followersDp":False }
			self.userdata = { "username":"", "uploadImagePath":"", "followers":[] }
			self.cur_path = os.getcwd()

			self.top = ttk.Tk()
			self.top.geometry("1200x720")

			self.username_var = ttk.StringVar()
			self.password_var = ttk.StringVar()
			self.rain_Frame=(self.top)
			self.rain_Frame.grid()
			self.loginPage()
			# self.top.wm_attributes('-transparentcolor', '#ab23ff')
			self.top.mainloop()

	def loginPage(self):

		self.bgImage 	= ImageTk.PhotoImage(Image.open(self.jDic["bgimage"]))
		self.loginImage = ImageTk.PhotoImage(Image.open(self.jDic["login"]))
		self.labelImage1 = ImageTk.PhotoImage(Image.open(self.jDic["username"]))
		self.labelImage2 = ImageTk.PhotoImage(Image.open(self.jDic["password"]))

		self.canvas = ttk.Canvas(self.rain_Frame, width=1200, height=720)
		self.canvas.grid(row=0, column=0, columnspan=4, rowspan=4)
		self.canvas.create_image( 1, 1, image=self.bgImage, anchor="nw")

		self.usernameLabel = ttk.Label(self.top, image=self.labelImage1)
		self.passwordLabel = ttk.Label(self.top, image=self.labelImage2)
		self.usernameField = ttk.Entry(self.top, textvariable=self.username_var, font = Font(family='Consolas', slant='italic'), justify='center')
		self.passwordField = ttk.Entry(self.top, textvariable=self.password_var, font = Font(family='Consolas', slant='italic'), show="*", justify='center')
		self.loginButton = ttk.Button(self.top, image=self.loginImage, command=self.options)

		self.usernameLabel.grid(column=0, row=0)
		self.passwordLabel.grid(column=0, row=1)
		self.usernameField.grid(column=1, row=0)
		self.passwordField.grid(column=1, row=1)
		self.loginButton.grid(column=3, row=2)

	def options(self):
		self.username = str(self.usernameField.get())
		self.password = str(self.passwordField.get())
		self.userdata["username"] = self.username
		try :
			self.instaObj.login(self.username, self.password)
			self.profile = instaloader.Profile.from_username(self.instaObj.context, self.username)
			self.val_dict["authImage"] = self.jDic["correct"]
			self.flagVals["cred"] = True
			print(f"\nLogged in {self.userdata['username']}\n")
		except Exception as e:
			pass
		self.msgDisplay()

		self.usernameLabel.destroy()
		self.passwordLabel.destroy()
		self.usernameField.destroy()
		self.passwordField.destroy()
		self.loginButton.destroy()

		self.getfollowers = ImageTk.PhotoImage(Image.open(self.jDic["getFollowers"]))
		self.cmpfollowers = ImageTk.PhotoImage(Image.open(self.jDic["cmpFollowers"]))
		self.cmpprofile = ImageTk.PhotoImage(Image.open(self.jDic["cmpProfile"]))
		self.existMatch = ImageTk.PhotoImage(Image.open(self.jDic["existingMatch"]))

		self.option1 = ttk.Button(self.top, image=self.getfollowers, command=self.getFollowers)
		self.option2 = ttk.Button(self.top, image=self.cmpfollowers, command=self.matchFollowerface)
		self.option3 = ttk.Button(self.top, image=self.cmpprofile,   command=self.matchPosts)
		self.option4 = ttk.Button(self.top, image=self.existMatch,   command=self.existingMatch)

		self.option1.grid(column=1, row=1)
		self.option2.grid(column=1, row=2)
		self.option3.grid(column=1, row=3)

	def msgDisplay(self):
		self.msgImage = ImageTk.PhotoImage(Image.open(self.val_dict["authImage"]))
		self.message = ttk.Label(self.top, image=self.msgImage)
		time.sleep(3)
		if not self.flagVals["cred"] :
			print("\n Problem in credentials...\n")
			self.top.destroy()
# ________________________________________________________________________________________________
	def getFollowers(self): # Option 1
		print("\ngetFollowers() Started\n")
		if not os.path.exists(f"followersList_{self.userdata['username']}.txt"):
			self.flagVals["getFollowers"] = True
			self.userdata["followers"] = [ self.followee.username for self.followee in self.profile.get_followers() ]
			self.f = open(f"followersList_{self.userdata['username']}.txt", 'w')
			[self.f.write(self.followerUsername+'\n') for self.followerUsername in self.userdata["followers"]]
			self.f.close()
		else:
			print(f"Followers list text file exist for {self.userdata['username']}")
			self.ff = open(f"followersList_{self.userdata['username']}.txt", "r")
			self.txtData = self.ff.read()
			self.ff.close()
			self.userdata["followers"] = " ".join(self.txtData.split("\n")).split()
			self.flagVals["getFollowers"] = True
		print("\ngetFollowers() ended\n")
	def matchFollowerface(self): # Option 2
		self.tempPath = str(filedialog.askopenfilename())
		self.userdata["uploadImagePath"] = self.tempPath.replace("/", "\\")

		self.localImage = ImageTk.PhotoImage(Image.open(self.userdata["uploadImagePath"]))
		self.proceedImage = ImageTk.PhotoImage(Image.open(self.jDic["proceed"]))
		self.imageLabel = ttk.Label(self.top, image=self.localImage)
		self.proceedButton = ttk.Button(self.top, image=self.proceedImage, command=self.matchIt)
		self.imageLabel.grid(column=1, row=1)
		self.proceedButton.grid(column=1, row=2)
	def matchPosts(self): # Option 3
		print("Match Posts selected")
		pass
	def existingMatch(self): # Option 4
		pass
# ________________________________________________________________________________________________
	def matchIt(self):
		self.dpFlag = self.downloadFollowersDp()
		if self.dpFlag :
			self.FR = matcher()
			print(f"\nUser data {self.userdata}\n")
			self.foundFace, self.foundFacePath, self.followerID = self.FR.f1(self.userdata)
		else :
			print("\n|Exception at creating username folder|\n")
	def downloadFollowersDp(self):
		if not self.flagVals["getFollowers"]:
			self.getFollowers()
		try :
			if not os.path.exists(f"{self.cur_path}\\{self.userdata['username']}"):
				os.mkdir(f"{self.cur_path}\\{self.userdata['username']}")
				os.chdir(f"{self.userdata['username']}\\")
				for self.username in self.userdata["followers"] :
					self.instaObj.download_profile(self.username ,profile_pic_only=True)
				os.chdir("..")
			else :
				self.flagVals["followersDp"] = True
		except Exception as e:
			self.error_logger("Exception at creating username folder", e)
			return False
		return True
# ________________________________________________________________________________________________
	def load_json(self):
		try :
			with open('values.json', 'r') as self.f :
				self.data_json = json.load(self.f)
				return self.data_json, True
		except Exception as e :
			print("Error !!! def load_json()")
			self.error_logger("Exception at reading data.json file", e)
			return False, False

	def error_logger(self, txt, exceptioN):
		try :
			self.txt, self.excpn,self.valuesList = txt, str(exceptioN), []
			self.valuesList.append('\n    Time | ' + str(datetime.now()) + ' |')
			self.valuesList.append('\n         | ' + self.txt + " |")
			self.valuesList.append('\n         | Type ' + str(type(self.excpn)) + ' |')
			self.valuesList.append('\n         | Exception ' + self.excpn + ' |')
			self.f2 = open('ErrorLog.txt')
			for self.line in len(self.valuesList) :
				self.f2.write(self.valuesList[self.line])
			self.f2.close()
		except Exception as e:
			print("||| Error !!!\n Exception in data at error_logger() |||")
# ________________________________________________________________________________________________
obj = UI()
