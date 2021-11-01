import tkinter as ttk
from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
from tkinter.font import Font
import instaloader, time
# import dp
# from dp import disp

class UI1 :
	def __init__(self):

		self.val_dict = { "username" : "", "location" : "" }
		self.top = ttk.Tk()
		self.top.geometry("1200x720")
		self.username_var = ttk.StringVar()
		self.password_var = ttk.StringVar()
		self.rain_Frame=(self.top)
		self.rain_Frame.grid()

		self.canvas = ttk.Canvas(self.rain_Frame, width=1200, height=720)
		self.canvas.grid(row=0, column=0, columnspan=4, rowspan=4)

		self.canvas1 = ttk.Canvas(self.rain_Frame, width=1000, height=665)


		self.top.wm_attributes('-transparentcolor', '#ab23ff')

		self.bg_image = Image.open('.\\data\\assets\\bgimage.png')
		self.button_image = Image.open('.\\data\\assets\\button_image.png')
		self.label1_image = Image.open('.\\data\\assets\\label1.png')
		self.label2_image = Image.open('.\\data\\assets\\label2.png')
		self.loadimage = Image.open('.\\data\\assets\\loading.png')

		self.image1 = ImageTk.PhotoImage(self.bg_image)
		self.image2 = ImageTk.PhotoImage(self.button_image)
		self.image3 = ImageTk.PhotoImage(self.label1_image)
		self.image4 = ImageTk.PhotoImage(self.label2_image)
		self.image5 = ImageTk.PhotoImage(self.loadimage)

		self.canvas.create_image( 1, 1, image=self.image1, anchor="nw")

		self.label1 = ttk.Label(self.top, image=self.image3)
		self.label2 = ttk.Label(self.top, image=self.image4)
		self.usernameField = ttk.Entry(self.top, textvariable=self.username_var, font = Font(family='Consolas', slant='italic'), justify='center')
		self.passwordField = ttk.Entry(self.top, textvariable=self.password_var, font = Font(family='Consolas', slant='italic'), show="*", justify='center')
		self.button1 = ttk.Button(self.top, image=self.image2, command=self.profiling)

		self.label1.grid(column=0, row=0)
		self.label2.grid(column=0, row=1)
		self.usernameField.grid(column=1, row=0)
		self.passwordField.grid(column=1, row=1)
		self.button1.grid(column=3, row=2)

		self.top.mainloop()

	def profiling(self):
		self.username = str(self.usernameField.get())
		self.password = str(self.passwordField.get())
		self.location = str(filedialog.askopenfilename())
		self.label1.destroy()
		self.label2.destroy()
		self.usernameField.destroy()
		self.passwordField.destroy()
		self.button1.destroy()

		self.canvas1.grid(row=0, column=0, columnspan=4, rowspan=4)
		self.canvas1.create_image(0, 0, image=self.image5, anchor="nw")
		time.sleep(2)
		# ____________________________________________________________________


		self.loadObj = instaloader.Instaloader()
		self.loadObj.login(self.username, self.password)
		self.profile = instaloader.Profile.from_username(self.loadObj.context, self.username)
		self.followers_list = [ self.followee.username for self.followee in self.profile.get_followers() ]
		# self.canvas1.destroy()
		# self.top1.destroy()
		print("______________________________________________________________________")
		print(self.followers_list)
		print("______________________________________________________________________")
		print(len(self.followers_list))


class UI2:
	def __init__(self):
		self.top2 = ttk.Tk()
		self.top2.geometry("1550x700")




		# self.loadObj = instaloader.Instaloader()
		# self.loadObj.login(self.username, self.password)
		# self.profile = instaloader.Profile.from_username(self.loadObj.context, self.username)

		# self.followers_list = [ self.followee.username for self.followee in self.profile.get_followers() ]


		print(self.followers_list)
		print("__________________")
		print(len(self.followers_list))

obj = UI1()




