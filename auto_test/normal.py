from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import random


class Normal_Behavior():
	def __init__(self):
		self.driver = webdriver.Chrome(os.getcwd()+"/chromedriver")
		self.driver.get("http:localhost:8080")
		self.is_login = False

	def run(self):
		for i in range(10):
			rand = random.randint(0,5)
			print(i,rand)
			if(rand == 0):
				self.login(True)
			elif(rand == 1):
				self.login(False)
			elif(rand == 2):
				self.play_video(2)
			elif(rand == 3):
				self.logout()
			elif(rand == 4):
				self.download_file(1)
			elif(rand == 5):
				self.download_file(2)
			time.sleep(1)

		self.driver.close()

	def play_video(self,sec):
		# redirect to videos.jsp & check login status
		if(self.is_login == False):
			self.login(is_success=True)
		self.driver.get("http:localhost:8080/videos.jsp")	

		# click play button in iframe
		player = WebDriverWait(self.driver, 10).until(
			EC.presence_of_element_located((By.XPATH, "/html/body/iframe"))
		)
		player.click()
		time.sleep(sec)

	def download_file(self,file_num):
		# redirect to files.jsp & check login status
		if(self.is_login == False):
			self.login(is_success=True)
		self.driver.get("http:localhost:8080/files.jsp")

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

	def login(self,is_success):
		# if login, logout first
		if(self.is_login == True):
			self.logout()

		if(is_success == True):
			uname = "pigman0315"
			pwd = "04383129"
		else:
			uname = "anonymous"
			pwd = "123456"

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
		time.sleep(1)
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
			self.is_login = False

		else:
			self.driver.get("http:localhost:8080/login.jsp")

	def backward(self):
		self.driver.back()

	def forward(self):
		self.driver.forward()

if(__name__ == '__main__'):
	nm = Normal_Behavior()
	nm.run()

