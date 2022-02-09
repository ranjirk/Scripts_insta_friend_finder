import os, face_recognition, glob, time, instaloader
from datetime import datetime
# https://pythonhosted.org/face_recognition/readme.html
# pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f
class matcher:
	def __init__(self, userDic, cred):
		self.userData, self.cred = userDic, cred
		self.current_Path = os.getcwd()
		self.user_name, self.cred = self.userData['username'], self.userData['cred']
		self.uploadimgpath, self.followerList = self.userData["uploadImagePath"], self.userData["followers"]
		self.objInsta = instaloader.Instaloader()
		self.objInsta.login(self.user_name, self.cred)
		self.returnValues = {"result":False, "file":"", "follower":""}

	def f1(self):
		try :
			self.uploadImgEncoding  = self.faceLoad(self.uploadimgpath)
		except Exception as e:
			print("No face found in uploaded image")
		self.count = 1
		for self.follower in self.followerList :
			print(f"\nFollower count searching {self.count}")
			print("Current follower : ", self.follower)
			self.count += 1
			self.searchPath = f"{self.current_Path}\\{self.user_name}\\{self.follower}\\"
			if os.path.isdir(self.searchPath):
				self.result = self.jpgAndFace(self.searchPath)
				print("Result in face match is ", self.result)
				if True in self.result:
					self.returnValues["result"] = self.result
					self.returnValues["file"] = self.jpgFiles[0]
					self.returnValues["follower"] = self.follower
					break
				else:
					self.error_logger("Face not found", "!")
			else:
				print(f"Data for {self.follower} does not exist")
				print(f"Hence downloading data for {self.follower} profile ...")
				if self.downloadProf(self.follower):
					self.result = self.jpgAndFace(self.searchPath)
					if True in self.result:
						self.returnValues["result"] = self.result
						self.returnValues["file"] = self.jpgFiles[0]
						self.returnValues["follower"] = self.follower
						break
					else:
						print("Face not found")
						self.error_logger("Face not found", "NO")
		return self.returnValues

	def jpgAndFace(self, searchPath):
		self.path = searchPath
		self.jpgFiles = glob.glob(f'{self.path}*.jpg')
		print("JPG FILES\n\n", self.jpgFiles,"\n\n")
		if self.jpgFiles:
			self.followerimgpath = self.jpgFiles[0]
			self.followerImgEnoding = self.faceLoad(self.followerimgpath)
			return face_recognition.compare_faces([self.uploadImgEncoding], self.followerImgEnoding)
		else:
			return False

	def downloadProf(self, follower_user_name):
		self.follower_user_name = follower_user_name
		try:
			if not os.path.exists(f"{self.current_Path}\\{self.user_name}\\{self.follower_user_name}"):
				os.chdir(f"{self.user_name}\\")
				print(f"Downloading profile for {self.follower_user_name}   ...")
				self.objInsta.download_profile(self.follower_user_name ,profile_pic_only=True)
				print(f"						Downloaded")				
				os.chdir("..")
				return True
			else:
				print("\n\nElse triggered\n\n")
				self.error_logger("Delete this folder  in  and try running program again.", "Unknown Error")
				print(f"{self.current_Path}\\{self.user_name}\\{self.follower_user_name}")
				return False
		except Exception as e:
			self.error_logger(f"Could not download {self.follower_user_name} profile", e)
			return False

	def faceLoad(self, path):
		print("\nfaceLoad() started\n")
		self.path = path
		self.image = face_recognition.load_image_file(self.path)
		self.encoding = face_recognition.face_encodings(self.image)[0]
		print("\nfaceLoad() ended\n")
		return self.encoding

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