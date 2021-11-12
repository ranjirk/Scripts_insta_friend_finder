import os, face_recognition
# https://pythonhosted.org/face_recognition/readme.html
class matcher:
	def f1(self, userDic):
		self.userData = userDic
		self.followersImgFolder = f"{os.getcwd()}\\{self.userData["username"]}\\"
		self.uploadimgpath = self.userData["uploadImagePath"]
		self.followerList = self.userData["followersList"]
		try :
			self.uploadImgEncoding  = self.faceload(self.uploadimgath)
		except Exception as e:
			print("No face found in uploaded image")

		for self.follower in self.followerList :
			self.searchPath = self.followersImgFolder + self.follower + "\\"
			self.jpgFiles = glob.glob(f'{self.searchPath}*.jpg')
			self.followerimgpath = self.faceload(self.jpgFiles[0])

			self.followerImgEnoding = self.faceload(self.followerpath)
			self.result = face_recognition.compare_faces(self.uploadImgEncoding, self.followerImgEnoding)
			if self.result:
				break
		return self.result, self.followerimgpath, self.follower

	def faceLoad(self, path):
		self.path = path
		self.image = face_recognition.load_image_file(self.path)
		self.encoding = face_recognition.face_encodings(self.image)[0]
		return self.encoding

