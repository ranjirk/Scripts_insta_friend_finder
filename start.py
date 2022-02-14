import instaloader, time, os, json, cv2, logging
import tkinter as ttk
# import matchface
# from matchface import matcher

from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
from datetime import datetime

class UI :
	def __init__(self):
		self.jDic, self.flag = self.load_json()
		if self.flag:
			self.instaObj = instaloader.Instaloader()
			self.val_dict = { "authImage" : self.jDic["wrong"]}
			self.flagVals = {"cred":False, "getFollowers":False, "followersDp":False, "resize":False }
			self.userdata = { "username":"", "uploadImagePath":"", "followers":[], "cred":"" }
			self.cur_path = os.getcwd()
			logging.basicConfig(level=logging.INFO)
			self.top = ttk.Tk()
			self.screen_width, self.screen_height  = self.top.winfo_screenwidth(), self.top.winfo_screenheight()
			self.width, self.height  = 650, int(self.screen_height - 50)
			self.resize_images()
			self.top.geometry(f"{self.width}x{self.height}")

			self.username_var, self.password_var = ttk.StringVar(), ttk.StringVar()
			self.rain_Frame = (self.top)
			self.rain_Frame.grid()
			self.loginPage()
			# self.top.wm_attributes('-transparentcolor', '#ab23ff')
			self.top.mainloop()

	def loginPage(self):

		self.bgImage 	 = ImageTk.PhotoImage(Image.open(self.jDic["bg_image"]))
		self.loginImage  = ImageTk.PhotoImage(Image.open(self.jDic["login_button_image"]))
		self.labelImage1 = ImageTk.PhotoImage(Image.open(self.jDic["username_button_image"]))
		self.labelImage2 = ImageTk.PhotoImage(Image.open(self.jDic["password_button_image"]))

		self.canvas = ttk.Canvas(self.rain_Frame, width=self.width, height=self.height)
		self.canvas.grid(row=0, column=0, columnspan=2, rowspan=4)
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
		self.loginButton.grid(column=0, row=2, columnspan=2)

	def options(self):
		# __________________________ Login page __________________________ {
		self.username = str(self.usernameField.get())
		self.password = str(self.passwordField.get())
		logging.info(f"Username \'{self.username}\' entered in text field.")
		self.userdata["username"] = self.username
		try :
			logging.info(f"Logging {self.userdata['username']} in ...")
			self.instaObj.login(self.username, self.password)
			self.userdata["cred"] = self.password
			self.profile = instaloader.Profile.from_username(self.instaObj.context, self.username)
			self.val_dict["authImage"] = self.jDic["correct"]
			self.flagVals["cred"] = True
			logging.info("\nLogin in successful |\n")
			if self.wrongLabel.winfo_exists():
				self.wrongLabel.destroy()
		except Exception as e:
			logging.info("\n*** Login unsuccessful ! ***\n")
			self.error_logger("Exception at Credentials ", e)
			self.wrongimage = ImageTk.PhotoImage(Image.open(self.jDic["wrong"]))
			self.wrongLabel = ttk.Label(self.top, image=self.wrongimage)
			self.wrongLabel.grid(column=0, row=3, columnspan=2)
		# self.msgDisplay()
		# __________________________ Login page __________________________ }
		# ________________________________________________________________
		# _______________________ Successful login _______________________ {
		else :
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

			self.option1.grid(column=0, row=1, columnspan=2)
			self.option2.grid(column=0, row=2, columnspan=2)
			self.option3.grid(column=0, row=3, columnspan=2)
		# _______________________ Successful login _______________________ }	

# ________________________________________________________________________________________________
	def getFollowers(self): # Option 1
		logging.info("\nListing Followers ...")
		if not os.path.exists(f"followersList_{self.userdata['username']}.txt"):
			self.flagVals["getFollowers"] = True
			self.userdata["followers"] = [ self.followee.username for self.followee in self.profile.get_followers() ]
			self.f = open(f"followersList_{self.userdata['username']}.txt", 'w')
			[self.f.write(self.followerUsername+'\n') for self.followerUsername in self.userdata["followers"]]
			self.f.close()
		else:
			logging.info(f"Followers list\'s text file already exist for {self.userdata['username']}")
			logging.info(f"Delete followersList_{self.userdata['username']}.txt file & rerun the program to get updated list of followers")
			self.ff = open(f"followersList_{self.userdata['username']}.txt", "r")
			self.txtData = self.ff.read()
			self.ff.close()
			self.userdata["followers"] = " ".join(self.txtData.split("\n")).split()
			self.flagVals["getFollowers"] = True
		logging.info("\nFollowers listed\n")

	def matchFollowerface(self): # Option 2
		self.option1.destroy()
		self.option2.destroy()
		self.option3.destroy()

		self.tempPath = str(filedialog.askopenfilename())
		self.userdata["uploadImagePath"] = self.tempPath.replace("/", "\\")

		self.localImage = ImageTk.PhotoImage(Image.open(self.userdata["uploadImagePath"]))
		self.proceedImage = ImageTk.PhotoImage(Image.open(self.jDic["proceed"]))
		self.imageLabel = ttk.Label(self.top, image=self.localImage)
		# self.proceedButton = ttk.Button(self.top, image=self.proceedImage, command=self.matchIt)
		self.proceedButton = ttk.Button(self.top, image=self.proceedImage)
		self.imageLabel.grid(column=0, row=1, columnspan=2)
		self.proceedButton.grid(column=0, row=2, columnspan=2)
	def matchPosts(self): # Option 3
		logging.info("Match Posts selected")
		pass
	def existingMatch(self): # Option 4
		logging.info("Existing Match selected")
		pass
# ________________________________________________________________________________________________
	def matchIt(self):
		self.dpFlag = self.downloadFollowersDp()
		if self.dpFlag :
			self.FR = matcher(self.userdata, self.instaObj)
			self.returnValus = self.FR.f1()
			if self.returnValus["result"]:
				logging.info("Results\n___________________\n", self.returnValus["follower"], "___________________")
				self.foundMatch(self.returnValus)
		else :
			logging.info("\n|Exception at creating username folder|\n")
	def downloadFollowersDp(self):
		if not self.flagVals["getFollowers"]:
			self.getFollowers()
		try :
			logging.info("Downloading follower's Display pictures...")
			if not os.path.exists(f"{self.cur_path}\\{self.userdata['username']}"):
				os.mkdir(f"{self.cur_path}\\{self.userdata['username']}")
				os.chdir(f"{self.userdata['username']}\\")
				for self.username in self.userdata["followers"] :
					logging.info(f"Downloading {self.username} 's display picture")
					self.instaObj.download_profile(self.username ,profile_pic_only=True)
				os.chdir("..")
			else :
				self.flagVals["followersDp"] = True
		except Exception as e:
			logging.info("Error in downloading followers display picture!\n Check downloadFollowersDp()")
			self.error_logger("Exception at creating username folder", e)
			return False
		else:
			logging.info("Followers Display pictures downloaded successfully")
		return True
	def foundMatch(self, data):
		self.imagepath, self.ID = data["file"], data["follower"]
		# logging.info(f"\nPath of match image {self.imagepath}\n")
		self.mf = ImageTk.PhotoImage(Image.open(self.imagepath))
		self.foundimage = ttk.Label(self.top, image=self.mf)
		self.foundText  = ttk.Label(self.top, text="Match found")
		self.foundimage.grid(column=1, row=1)
		self.foundText.grid(column=1, row=1)
# ________________________________________________________________________________________________
	def load_json(self):
		try :
			logging.info("Opening \'values.json\' file")
			with open('values.json', 'r') as self.f :
				self.data_json = json.load(self.f)
				return self.data_json, True
		except Exception as e :
			logging.info(f"Could not load \'values.json\' file at load_json()\n{e}")
			self.error_logger("Exception at reading data.json file", e)
			return False, False
# ________________________________________________________________________________________________
	def error_logger(self, txt, exceptioN):
		try :
			self.txt, self.excpn,self.valuesList = txt, str(type(exceptioN)), []
			self.valuesList = [	'\n\n| ' + self.txt, "\n| " + str(datetime.now()), "\n| " + self.excpn]
			self.f2 = open('ErrorLog.txt', 'a+')
			for self.line in range(len(self.valuesList)) :
				self.f2.write(self.valuesList[self.line])
			self.f2.close()
		except Exception as e:
			logging.info("||| Error !!!\n Exception in data at error_logger() |||")
# ________________________________________________________________________________________________
	def resize_images(self):
		logging.info("Background image resizing...")
		try :
			self.image_org = cv2.imread(self.jDic['vector_path'])
			self.resized = cv2.resize(self.image_org, (self.width, self.height))
			cv2.imwrite(self.jDic['bg_image'], self.resized)
		except Exception as e:
			logging.info("Error at resizing Background image\n Check resize_images()")
			pass
		else:
			logging.info("Background image resized")

# ________________________________________________________________________________________________
	# def msgDisplay(self):
	# 	self.msgImage = ImageTk.PhotoImage(Image.open(self.val_dict["authImage"]))
	# 	self.message = ttk.Label(self.top, image=self.msgImage)
	# 	self.message.grid(column=1, row=1)
	# 	time.sleep(3)
	# 	if not self.flagVals["cred"] :
	# 		print("\n Problem in credentials...\n")
	# 		self.top.destroy()
# ________________________________________________________________________________________________

obj = UI()
