##IMPORTING ALL THE MODULES REQUIRED
from tkinter import *
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from tkinter.messagebox import *
from tkinter.scrolledtext import *
from sqlite3 import *
import requests
import socket
import bs4
from datetime import *
from webbrowser import *


greet = ""
weather_greet = "Weather is"
today = datetime.now()
hours = today.hour

#CURRENT TIME FOR GREETING 
if(hours<=11):
	greet = greet+"Good Morning! You are at"
elif(hours>=12) & (hours<=17):
	greet = greet+"Good Afternoon! You are at"
elif(hours>=18) &(hours<=24):
	greet = greet+"Good Evening! You are at"

#INITIALIZAION OF EMPTY LISTS REQUIRED FOR EXPLORING DATA
stu_name = []
stu_roll = []
stu_marks = []

#COMMUNICATIONG WITH WEBSITES FOR WEATHER, QUOTE OF THE DAY, LOCATION AND ARTICLE OF THE DAY(NY TIMES)
try:
	socket.create_connection( ("www.google.com", 80) )
	res = requests.get("https://ipinfo.io")
	data = res.json()
	loc1 = data["city"]
	
	## FOR WEATHER RELATED INFO ##
	socket.create_connection( ("www.google.com", 80))
	city = "Thane"
	a1 = "http://api.openweathermap.org/data/2.5/weather?units=metric"
	a2 = "&q=" + city 
	a3 = "&appid=c6e315d09197cec231495138183954bd"
	api_address =  a1 + a2  + a3 		
	res = requests.get(api_address)
	data = res.json()
	main_data = data["main"]
	temp = main_data["temp"]
	temperature = str(temp)+"°"

	main_weather = data["weather"]
	for d in main_weather:
		weather = (d["main"])

	## FOR QUOTE OF THE DAY ##
	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,"lxml")
	data = soup.find("img",{"class":"p-qotd"})
	th = data["alt"]
	thou = th.split("-")
	thought = '"'+thou[0]+'"'+" -"+thou[1]
	
	## FOR NYTIMES ARTICLE OF THE WEEK ## 
	resp = requests.get("https://www.nytimes.com/section/education")
	soup = bs4.BeautifulSoup(resp.text,"lxml")
	data = soup.find("div",{"class":"css-xbztij"})
	f = data.find("a")
	a = (f["href"])
	url = "https://www.nytimes.com"+a
	f = data.find_all("a")
	news = f[1].contents[0]
	
except OSError as e:
	showerror("Error","Connection Error!! ")

# FUNCTIONS FOR UI
def f2():
	main_win.deiconify()
	viewstu.withdraw()

def f4():
	roll_text.delete(0,END)
	name_text.delete(0,END)
	marks_text.delete(0,END)
	main_win.withdraw()
	addstu.deiconify()


def f5():
	addstu.withdraw()
	main_win.deiconify()

def f6():
	main_win.withdraw()
	delstu.deiconify()

def f7():
	main_win.withdraw()
	updatestu.deiconify()

def f8():
	main_win.deiconify()
	delstu.withdraw()

def f9():
	updatestu.withdraw()
	main_win.deiconify()

# FUNCTION TO ADD NEW RECORD TO THE DB
def add_record():
	Name = name_text.get()
	if all(x.isalpha() or x.isspace() for x in Name):
		if(len(Name)>=2):
			R = roll_text.get()
			try:
				Roll = int(R)
			except Exception as e:
				showerror("Error","Invalid Roll No.!! Please Insert Integer only!!")	
			if(Roll>0):
				M = marks_text.get()
				try:
					Marks = int(M)
				except Exception as e:
					showerror("Error","Invalid marks! Please enter integers between 0-100 only")	
				if(Marks<=100)&(Marks>=0):
					con = None
					try:
						con = connect("student_rec.db")
						cursor = con.cursor()
						sql = "insert into students_rec values('%d','%s','%d')"
						args = (Roll,Name,Marks)
						cursor.execute(sql %args)
						con.commit()
						showinfo("Success","Data Inserted")
		
						
					except Exception as e:
						con.rollback()
						showerror("Error","Record creation erorr! Roll No. Already exists!!")

					finally:
						if con is not None:
							con.close()
				else:
					roll_text.delete(0,END)
					name_text.delete(0,END)
					marks_text.delete(0,END)
					showerror("Error","Invalid Marks. Please insert marks between 0-100")
			else:
				roll_text.delete(0,END)
				name_text.delete(0,END)
				marks_text.delete(0,END)			
				showerror("Error","Enter a valid Roll No. It cannot be negative!")
		else:
			roll_text.delete(0,END)
			name_text.delete(0,END)
			marks_text.delete(0,END)
			showerror("Error","Name has to be minimum two alphabets long!!")
	else:
		roll_text.delete(0,END)
		name_text.delete(0,END)
		marks_text.delete(0,END)
		showerror("Error","Special Charecters not allowed in the name!")
	roll_text.delete(0,END)
	name_text.delete(0,END)
	marks_text.delete(0,END)

# FUNCTION TO VIEW THE RECORDS FROM DB
def view():
	main_win.withdraw()
	viewstu.deiconify()
	scroller.delete(1.0,END)
	con = None
	try:
		con = connect("student_rec.db")
		cursor = con.cursor()
		sql = "select * from students_rec";
		cursor.execute(sql)
		data = 	cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Roll No.= " +str(d[0]) + "\n" + "Name= " +str(d[1]) +"\n" + "Marks= "+str(d[2])+"\n"+"\n"
			if int(d[0]) not in stu_roll:
				stu_roll.append(int(d[0]))
				stu_name.append(str(d[1]))
				stu_marks.append(int(d[2]))
		scroller.insert(INSERT,info)
		ln = len(stu_name)
		length_labl = Label(viewstu,text = ln, font = ("Courier",14), background = "#D8D8F6") ## WINDOW HEADING
		length_labl.place(x = 400, y = 90)

	except Exception as e:
		con.rollback()
		showerror("Error","Unable to fetch data!!")

# FUNCTION TO UPDATE RECORDS INSIDE THE DB
def update():
	con = None
	r = enterRoll.get()
	try:
		rno = int(r)
	except Exception as e:
		showerror("Error","Invalid Roll no! Please Enter a valid roll no!!")
	if(rno>0):
		name = enterName.get()
		if all(x.isalpha() or x.isspace() for x in name):
			if(len(name)>=2):
				m = enterMarks.get()
				try:
					marks = int(m)
				except Exception as e:
					showerror("Error","Invalid marks! Please enter a valid number!")
			
				if(marks>=0) & (marks <=100):
					try:
						con = connect("student_rec.db")
						print("connected")
						cursor = con.cursor()
						sql = "update students_rec set name = '%s', marks = '%f' where roll_no = '%r'"	
						args = (name,marks,rno)
						cursor.execute(sql %args)
						if cursor.rowcount >= 1:
							con.commit()
							showinfo("Status","Record updated!")
						else:
							showerror("Status","Record not found!")

					except Exception as e:
						con.rollback()
						showerror("Error",e)

					finally:
						if con is not None:
							con.close()
				else:
					enterRoll.delete(0,END)
					enterName.delete(0,END)
					enterMarks.delete(0,END)
					showerror("Error","Invalid Marks! Please enter marks in the range of 0-100 only!!")	
			else:
				enterRoll.delete(0,END)
				enterName.delete(0,END)
				enterMarks.delete(0,END)
				showerror("Error!","Name should be atleast two alphabets long!!")	
		else:
			enterRoll.delete(0,END)
			enterName.delete(0,END)
			enterMarks.delete(0,END)
			showerror("Error","Name cannot contain Special Charcters! Please re-enter the details!")	
	else:
		enterRoll.delete(0,END)
		enterName.delete(0,END)
		enterMarks.delete(0,END)
		showerror("Error!","Roll Number cannot be negative!! Please enter a valid roll number!!")
	enterMarks.delete(0,END)
	enterName.delete(0,END)
	enterRoll.delete(0,END)
		
# FUNCTION TO DELETE THE RECORDS INSIDE THE DB
def delete():
	con = None
	try:
		rno = int(rol_delete.get())
	except exception as e:
		showerror("Error","Invalid Roll no! Please insert an integer!!")
	if(rno>0):
		try:
			con = connect("student_rec.db")
			cursor = con.cursor()
			sql = "delete from students_rec where roll_no = '%r'"
			args = (rno)
			cursor.execute(sql %args)
			if cursor.rowcount >= 1:
				con.commit()
				showinfo("Status","Record Deleted")

			else:
				showerror("Status","Record not found!")
				
		except Exception as e:
			con.rollback()
			showerror("Error",e)

		finally:
			if con is not None:
				con.close()
	else:
		rol_delete.delete(0,END)
		showerror("Error","Invalid Roll No!! Please enter a positive value!!")
	rol_delete.delete(0,END)

# FUNCTION FOR THE PLOTTING OF DATA FOR BETTER UNDERSTANDING
def explore():
	stu_fail = []
	stu_avg = []
	stu_good = []
	stu_ex = []	
	stu_total = []
	con = None
	try:
		con = connect("student_rec.db")
		cursor = con.cursor()
		sql = "select * from students_rec";
		cursor.execute(sql)
		data = 	cursor.fetchall()
		info = ""
		for d in data:
			info = info + "Roll No.= " +str(d[0]) + "\n" + "Name= " +str(d[1]) +"\n" + "Marks= "+str(d[2])+"\n"+"\n"
			if d not in stu_roll:
				stu_roll.append(int(d[0]))
				stu_name.append(str(d[1]))
				stu_marks.append(int(d[2]))
		scroller.insert(INSERT,info)
		ln = len(stu_name)

	except Exception as e:
		con.rollback()
		showerror("Error","Unable to fetch data!!")
	

	for marks in stu_marks:
		
		if(marks<40):
			stu_fail.append(marks)
		elif(marks>=40)&(marks<=60):
			stu_avg.append(marks)
		elif(marks>61)&(marks<=80):
			stu_good.append(marks)
		else:
			stu_ex.append(marks)
	stu_total.append(len(stu_fail))
	stu_total.append(len(stu_avg))
	stu_total.append(len(stu_good))
	stu_total.append(len(stu_ex))
	if(len(stu_marks) != 0):
		categories = ["Marks below 40-Fail","Marks between 41-60 Average","Marks between 61-80 Good","Marks greater than 100 Excellent"]
		plt.title("Distribution of students in various Grade Categories")
		colors = ["Orange","Green","#978897","Teal"]
		explode = [0.2,0,0,0]
		plt.pie(stu_total,radius = 0.9,labels = categories,autopct = "%.2f%%", shadow = True, startangle = 175, colors = colors, explode = explode)
		plt.show()

	else:
		showwarning('No Data',"No data to plot!")

# FUNCTION FOR CONTROLLING THE LOGIN PAGE
def login():
	user = enterUsername.get()
	passw = enterPassword.get()
	if(user == "Admin") & (passw == "Admin"):
		root.withdraw()
		main_win.deiconify() 
	elif(user != "Admin") | (passw != "Admin"):
		enterUsername.delete(0,END)
		enterPassword.delete(0,END)
		showerror("Error","Username or password incorrect!")

# FUNCTION FOR LOGGING OUT
def logout():
	enterUsername.delete(0,END)
	enterPassword.delete(0,END)
	main_win.withdraw()
	root.deiconify()
	showinfo("Connection Status","Connction Closed!")

# FUNCTION TO OPEN THE ARTICLE 
def article():
	open(url)


## PRIMARY WINDOW FOR LOGIN 
root = Tk()
root.geometry("450x300+430+170")
root.resizable(False,False)
root.configure(background = '#D8D8F6')
root.title("S.M.S. Login Page")

login_lbl = Label(root,text = "Login to S.M.S.", font = ("Courier",20),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
login_lbl.place(x = 100, y = 20)


head_lbl = Label(root,text = greet, font = ("Courier",12),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 55, y = 80)


loc_lbl = Label(root,text = loc1, font = ("Courier",16),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
loc_lbl.place(x = 305, y = 77)

user_labl = Label(root,text = "Username", font = ("Courier",12), fg = '#494850', background = "#D8D8F6")
user_labl.place(x = 70, y = 130)
enterUsername = Entry(root,bd = 1, font = ("Courier",12))
enterUsername.place(x = 160, y = 130)

pass_labl = Label(root,text = "Password", font = ("Courier",12),fg = '#494850', background = "#D8D8F6")
pass_labl.place(x = 70, y = 180)
enterPassword = Entry(root,bd = 1, font = ("Courier",12),show = "*")
enterPassword.place(x = 160, y = 180)

btnLogin = Button(root,text="Login",font = ("courier",12),fg = "#2C2C34",width = 9,command = login, background = "#978897")
btnLogin.place(x = 90, y = 230)

btnExit = Button(root,text="Exit",font = ("courier",12),width = 9,fg ="#2C2C34", command = exit, background = "#978897")
btnExit.place(x = 250, y = 230)


# WINDOW WITH CRUD OPERATION BUTTONS
main_win = Toplevel(root)
main_win.geometry("700x630+450+40")
main_win.title("Student Management System")
main_win.resizable(False,False)
head_lbl = Label(main_win,text = "Student Management System", font = ("Courier",30),fg = '#2C2C34', background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 40, y = 5)

main_win.configure(background = "#D8D8F6")

# THOUGHT OF THE DAY
head_lbl = Label(main_win,text = thought, font = ("Courier",12),fg = '#494850',wraplength = 610, background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 40, y = 70)

# TEMPERATURE
head_lbl = Label(main_win,text = "Temperature is ", font = ("Courier",12),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 182, y = 130)
head_lbl = Label(main_win,text = temperature, font = ("Courier",16), fg = '#494850',background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 332, y = 127)

# WEATHER
head_lbl = Label(main_win,text = weather_greet, font = ("Courier",12),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 302, y = 150)
head_lbl = Label(main_win,text = weather, font = ("Courier",16),fg = '#494850', background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 412, y = 147)

# ARTICLE
head_lbl = Label(main_win,text = "Article by NY Times", font = ("Courier",12),fg = '#494850', wraplength = 470, background = "#D8D8F6") ## WINDOW HEADING
head_lbl.place(x = 250, y = 530)



## BUTTONS FOR CRUD OPERATIONS
btnAdd = Button(main_win,text="New Record",font = ("courier",12),fg = "#2C2C34", background = "#978897",width = 18,command = f4)
btnView = Button(main_win,text = "View Records",font= ("courier",12),fg = "#2C2C34", background = "#978897",width = 18,command = view)
btnDelete = Button(main_win,text = "Delete Record",font= ("courier",12), fg = "#2C2C34",background = "#978897",width = 18,command = f6)
btnUpdate = Button(main_win,text="Update Record",font = ("courier",12),fg = "#2C2C34", background = "#978897",width = 18,command = f7)
btnCharts = Button(main_win,text="Explore Data",font = ("courier",12),fg = "#2C2C34", background = "#978897",width = 18,command = explore)
btnLogout = Button(main_win,text="Logout",font = ("courier",12),width = 18,command = logout,fg = "#2C2C34", background = "#B18FCF")
btnArticle = Button(main_win,text=news,font = ("courier",12),width = 60,wraplength = 300,fg = "#2C2C34",command = article, background = "#978897")

btnAdd.place(x = 250, y = 210)
btnView.place(x = 250, y = 260)
btnDelete.place(x = 250, y = 310)
btnUpdate.place(x = 250, y = 360)
btnCharts.place(x = 250, y = 410)
btnLogout.place(x = 250, y = 460)
btnArticle.place(x = 43, y = 560)

main_win.withdraw()
## WINDOW ENDS HERE


# WINDOW TO ADD NEW RECORDS
addstu = Toplevel(root)
addstu.geometry("500x600+450+40")
addstu.configure(background = "#D8D8F6")
addstu.title("New Record")
addstu.resizable(False,False)
## WINDOW HEADING
head_labl = Label(addstu,text = "Add a new Record", font = ("Courier",30),fg = "#2C2C34", background = "#D8D8F6")
head_labl.place(x = 45, y = 5)

## LABELS
roll_labl = Label(addstu, text = "Roll No.", font = ("Courier",15),fg = "#2C2C34",background = "#D8D8F6")
roll_labl.place(x = 30, y = 140)
roll_text = Entry(addstu, bd = 5, font = ("Courier",15),fg = "#2C2C34",)
roll_text.place(x = 170, y =140)

name_labl = Label(addstu, text = "Name",font = ("Courier",15),fg = "#2C2C34", background = "#D8D8F6")
name_labl.place(x = 30, y = 180)
name_text = Entry(addstu,bd = 5, font = ("Courier",15),fg = "#2C2C34",)	
name_text.place(x = 170, y = 180)

marks_labl = Label(addstu, text = "Marks", font = ("Courier", 15),fg = "#2C2C34", background = "#D8D8F6")
marks_labl.place(x = 30, y = 220)
marks_text = Entry(addstu, bd = 5, font = ("Courier",15),fg = "#2C2C34",)
marks_text.place(x = 170,y=220)

# WINDOW BUTTONS
btnAdd = Button(addstu,text = "Submit", font= ("courier",12),width = 9, background = "#978897",wraplength = 60,command = add_record)
btnAdd.place(x = 100, y = 530)
btnBack = Button(addstu,text = "Back", font= ("courier",12),width = 9, background = "#978897",wraplength = 60,command = f5)
btnBack.place(x = 300, y = 530)

addstu.withdraw()
## WINDOW ENDS HERE


## WINDOW FOR VIEWING DATA

viewstu = Toplevel(root)
viewstu.geometry("500x600+450+40")
viewstu.configure(background = "#D8D8F6")
viewstu.title("View Records")
viewstu.resizable(False,False)

# LABELS
head_labl = Label(viewstu,text = "View Records", font = ("Courier",30),fg = "#2C2C34", background = "#D8D8F6") ## WINDOW HEADING
head_labl.place(x = 100, y = 5)
count_labl = Label(viewstu,text = "Total count of students is: ", font = ("Courier",14),fg = "#2C2C34", background = "#D8D8F6") ## WINDOW HEADING
count_labl.place(x = 90, y = 90)

## SCROLLING WIDGET
scroller = ScrolledText(viewstu, width = 40, height = 20, font = ("Courier",13), fg = "white",background = "#978897")
scroller.pack(pady = 140)

# BUTTONS
btnBack = Button(viewstu,text = "Back", font= ("courier",12),width = 9, background = "#978897",wraplength = 60,command = f2)
btnBack.place(x = 100, y = 530)
btnExplore = Button(viewstu,text = "Explore", font= ("courier",12),width = 10, background = "#978897",wraplength = 70,command = explore)
btnExplore.place(x = 300, y = 530)

viewstu.withdraw()
# WINDOW ENDS HERE

## WINDOW FOR UPDATING RECORDS
updatestu = Toplevel(root)
updatestu.geometry("500x600+450+40")
updatestu.configure(background = "#D8D8F6")
updatestu.title("Update Record")
updatestu.resizable(False,False)

## WINDOW HEADING
head_labl = Label(updatestu,text = "Update Record", font = ("Courier",30),fg = "#2C2C34", background = "#D8D8F6")
head_labl.place(x = 80, y = 5)

# LABELS
roll_labl = Label(updatestu,text = "Roll No.", font = ("Courier",15), fg = "#2C2C34",background = "#D8D8F6")
roll_labl.place(x = 30, y = 140)
enterRoll = Entry(updatestu,bd = 5, font = ("Courier",15))
enterRoll.place(x = 170, y = 140)
name_labl = Label(updatestu,text = "Name", font = ("Courier",15), fg = "#2C2C34",background = "#D8D8F6")
name_labl.place(x = 30, y = 190)
marks_labl = Label(updatestu,text = "Marks", font = ("Courier",15),fg = "#2C2C34", background = "#D8D8F6")
marks_labl.place(x = 30, y = 240)

# ENTRY WIDGETS
enterName = Entry(updatestu,bd = 5, font = ("Courier",15))
enterName.place(x = 170, y = 190)
enterMarks = Entry(updatestu,bd = 5, font = ("Courier",15))
enterMarks.place(x = 170, y = 240)

#BUTTONS
btnUpdate = Button(updatestu,text = "Submit", font= ("courier",12),width = 9, background = "#978897",wraplength = 60,command = update)
btnUpdate.place(x = 100, y = 530)
btnBack = Button(updatestu,text = "Back", font= ("courier",12),width = 10, background = "#978897",wraplength = 70,command = f9)
btnBack.place(x = 300, y = 530)

updatestu.withdraw()
# WINDOW ENDS HERE


## WINDOW FOR DELETING STUDENTS

delstu = Toplevel(root)
delstu.geometry("500x600+450+40")
delstu.configure(background = "#D8D8F6")
delstu.title("Delete Record")
delstu.resizable(False,False)

## WINDOW HEADING

# LABELS
head_labl = Label(delstu,text = "Delete Records", font = ("Courier",30),fg = "#2C2C34", background = "#D8D8F6")
head_labl.place(x = 80, y = 5)
roll_labl = Label(delstu,text = "Enter Roll No. to delete record: ",fg = "#2C2C34", font = ("Courier",15), background = "#D8D8F6")
roll_labl.place(x = 40, y = 160)
roll_labl = Label(delstu,text = "Roll No.", font = ("Courier",15), fg = "#2C2C34",background = "#D8D8F6")
roll_labl.place(x = 30, y = 240)

#ENTRY WIDGETS
rol_delete = Entry(delstu,bd = 5, font = ("Courier",15),fg = "#2C2C34",)
rol_delete.place(x = 170, y = 240)
btnDelete = Button(delstu,text = "Delete", font= ("courier",12),width = 9, background = "#978897",wraplength = 60,command = delete)
btnDelete.place(x = 100, y = 530)
btnBack = Button(delstu,text = "Back", font= ("courier",12),width = 10, background = "#978897",wraplength = 70,command = f8)
btnBack.place(x = 300, y = 530)


delstu.withdraw()


root.mainloop()