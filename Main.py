from bs4 import BeautifulSoup
import pandas
import requests
import re
import time

		

class Scrape:
	
	
	
	def __init__(self):
		#color
		self.default = '\033[0m'
		self.red = '\033[91m'
		self.blue = '\033[94m'
		self.gren = '\033[92m'
		self.yellow = '\033[93m'
		
		self.x = "________________________________________"
		self.index=0
		#menyiapkan array kosong untuk menyimpan data
		self.array  = []
		
		self.file_list()
	
		
		
	def file_list(self):
		#mengambil data file list
		print(self.default+"""Pilih jenis file list yang digunakan
			[1] excel 
			[2] csv
			[3] txt""")
	
		file_list = input("masukan pilihan : ")
		print(self.x)
		self.path_file = input("masukan path file : ")
		if(str(file_list) == "1"):
				self.read_excel()
		elif(str(file_list) == "2"):
				self.read_csv()
		elif(str(file_list) == "3"):
				self.read_txt()
		else:
				print("menu salah")
		
				
	
	#fungsi untuk membaca file excel			
	def read_excel(self):
		try:
			
			with pandas.ExcelFile(self.path_file) as file:
				self.list = pandas.read_excel(file)
				print("Path file : "+str(self.list))
				print("Total baris : "+str(len(self.list)))
				
				self.page()
				
		except:
			#jika file error maka kembali ke file_list()
			print(self.yellow+"file excel tidak di temikan")
			self.file_list()
			
			
		
	def page(self):
		
		#self.col = col
		
		if(self.index == 0):
			print(self.default+self.x)
			self.col = input("masukan nama kolom url : ")
			print(self.x)
			print("pilih html yang ingin di ambil")
			print("[1] Alamat link")
			print("[2] String")
			self.sf = input("masukan pilihan : ")
		else:
			pass
		
	#	while (index < len(self.list)):
		try:
			url = self.list.loc[self.index][self.col]
		except:
			print(self.yellow+"alamat link error cek apakah nama kolom sudah benar")
			self.page()
			
		try:
					
			print(self.default+"\n============================================\n")
			print("mencoba koneksi index ke : "+str(self.index))
			print("addres : "+str(url))
			get = requests.get(url)
			print("status url : "+self.gren+str(get.status_code)+" ok")
			self.content = BeautifulSoup(get.content, "html.parser")
				
		except:
			print(self.red+"internet error! silahkan cek koneksi internet anda")
			time.sleep(3)
			self.page()
				
				
		
		if(str(self.sf) == "1"):
			
			self.find_link()
			
		elif(str(self.sf) == "2"):
			
			self.find_string()
			
		else:
			
			print("menu salah")
	
	
	#fungsi scrap alamat link
	def find_link(self):
		if(str(self.index)=="0"):
			print(self.default+self.x)
			self.cls = input("masukan attr class : ")
			print("==== masukan base url link agar pencarian lebih akurat =====")
			self.link = input("masukan base url : ")
		
		else:
			pass
			
		self.data = self.content.find_all(href=re.compile(str(self.link)), class_=re.compile(str(self.cls)))
		
		for data in self.data:
			#print(data)
			self.array.append(data["href"])
			
		self.index = self.index+1
		if(self.index < len(self.list)):
			self.page()
		else:
			self.dataframe()
	
			
	#fhngsi scrap string		
	def find_string(self):
		if(str(self.index)=="0"):
			print(self.default+self.x)
			self.tag = input("masukan tag html : ")
			self.cls = input("masukan attr class : ")
		else:
			pass
		
		self.data = self.content.find_all(str(self.tag) , class_=re.compile(str(self.cls)))
	
		for data in self.data:
			#print(data)
			self.array.append(data.text)
		
		
		self.index = self.index+1
		if(self.index < len(self.list)):
			self.page()
		else:
			self.dataframe()


	#membuat data frame
	def dataframe(self):
	
		data_array = {"Scrape data" : self.array}
		self.df = pandas.DataFrame(data_array)
		print(self.df)	

	
if(__name__ == "__main__"):
	Scrape()

