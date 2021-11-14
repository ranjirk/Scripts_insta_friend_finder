import os, face_recognition, glob
# https://pythonhosted.org/face_recognition/readme.html
# pip install https://pypi.python.org/packages/da/06/bd3e241c4eb0a662914b3b4875fc52dd176a9db0d4a2c915ac2ad8800e9e/dlib-19.7.0-cp36-cp36m-win_amd64.whl#md5=b7330a5b2d46420343fbed5df69e6a3f
class matcher:
	def __init__(self):
		self.returnValues = {"result":False, "file":"", "follower":""}
		pass
	def f1(self, userDic):
		self.userData = userDic
		self.followersImgFolder = f"{os.getcwd()}\\{self.userData['username']}\\"
		self.uploadimgpath = self.userData["uploadImagePath"]
		self.followerList = self.userData["followers"]
		try :
			self.uploadImgEncoding  = self.faceLoad(self.uploadimgpath)
		except Exception as e:
			print("No face found in uploaded image")
		self.count = 1
		print("Follower list :", self.followerList)
		for self.follower in self.followerList :
			print(f"\nFollower count searching {self.count}")
			self.count += 1
			self.searchPath = self.followersImgFolder + self.follower + "\\"
			self.jpgFiles = glob.glob(f'{self.searchPath}*.jpg')
			self.followerimgpath = self.jpgFiles[0]
			print(f"\nCurrent path searching : {self.followerimgpath}\n")

			self.followerImgEnoding = self.faceLoad(self.followerimgpath)
			self.result = face_recognition.compare_faces([self.uploadImgEncoding], self.followerImgEnoding)

			if self.result:
				print("________________________________")
				print("Match found   : ", self.follower)
				print("File location : ", self.jpgFiles[0])
				print("________________________________")
				self.returnValues["result"] = self.result
				self.returnValues["file"] = self.jpgFiles[0]
				self.returnValues["follower"] = self.follower
				break
		return self.returnValues

	def faceLoad(self, path):
		print("\nfaceLoad() started\n")
		self.path = path
		self.image = face_recognition.load_image_file(self.path)
		self.encoding = face_recognition.face_encodings(self.image)[0]
		print("\nfaceLoad() ended\n")
		return self.encoding

