from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


class Normal_Behavior():
	def __init__(self):
		self.driver = webdriver.Chrome("/home/vincent/Desktop/chromedriver")
		self.driver.get("http:localhost:8080")
		self.is_login = False

	def run(self):
		self.login(uname="pigman0315",pwd="04383129")
		self.play_video(sec=2)
		self.logout()
		time.sleep(100)
		#self.download_file(file_num=1)
		#self.download_file(file_num=2)
		#self.download_file(file_num=3)
		self.driver.close()

	def play_video(self,sec):
		# redirect to videos.jsp & check login status
		if(self.is_login == True):
			self.driver.get("http:localhost:8080/videos.jsp")
		else:
			self.login(uname="pigman0315",pwd="04383129")

		# click play button in iframe
		player = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/iframe"))
		)
		player.click()
		time.sleep(sec)

	def download_file(self,file_num):
		# redirect to files.jsp & check login status
		if(self.is_login == True):
			self.driver.get("http:localhost:8080/files.jsp")
		else:
			self.login(uname="pigman0315",pwd="04383129")

		# determine to download which file
		if(file_num <= 3):
			link = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "/html/body/a["+str(file_num)+"]"))
			)
			link.click()

			# make sure the file is downloaded
			full_path = "/home/vincent/Downloads/"+link.text
			while(True):
				if(os.path.exists(full_path)):
					os.remove(full_path)
					break
				else:
					time.sleep(2)

	def login(self,uname,pwd):	
		self.driver.get("http:localhost:8080/login.jsp")
		username = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.NAME, "username"))
		)
		password = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.NAME, "password"))
		)
		login_button = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/form/input[3]"))
		)
		username.clear()
		password.clear()
		username.send_keys(uname)
		password.send_keys(pwd)
		login_button.click()

		if(uname=="pigman0315" and pwd=="04383129"):
			self.is_login = True
		else:
			self.is_login = False

	def logout(self):
		if(self.is_login == True):
			self.driver.get("http:localhost:8080/welcome.jsp")
			logout_button = WebDriverWait(self.driver, 10).until(
				EC.presence_of_element_located((By.XPATH, "/html/body/form/input"))
			)
			logout_button.click()
			is_login = False

		else:
			self.driver.get("http:localhost:8080/login.jsp")

	def backward(self):
		self.driver.back()

	def forward(self):
		self.driver.forward()

if(__name__ == '__main__'):
	nm = Normal_Behavior()
	nm.run()

