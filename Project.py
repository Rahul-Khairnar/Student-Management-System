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

greet = ""
weather_greet = "Weather:"
today = datetime.now()
hours = today.hour
if(hours<12):
	print("Good Morning!")
	greet = greet+"Good Morning! You are at"
elif(hours>12) & (hours<17):
	print("Good Afternoon!")
	greet = greet+"Good Afternoon! You are at"
elif(hours>17) &(hours<24):
	print("Good Evening!")
	greet = greet+"Good Evening! You are at"

stu_name = []
stu_roll = []
stu_marks = []


try:
	socket.create_connection( ("www.google.com", 80) )
	res = requests.get("https://ipinfo.io")
	data = res.json()
	loc1 = data["city"]
	
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
	weather_greet = weather_greet+weather

	res = requests.get("https://www.brainyquote.com/quote_of_the_day")
	soup = bs4.BeautifulSoup(res.text,"lxml")
	data = soup.find("img",{"class":"p-qotd"})
	thought = data["alt"]

except OSError as e:
	print("Connection Error!! ",e)


def name(Exception):
	def __init__(self,message):
		self.message = message

def roll(Exception):
	def __init__(self,message):
		self.message = message

def marks(Exception):
	def __init__(self,message):
		self.message = message


def f2():
	root.deiconify()
	viewstu.withdraw()

def f4():
	root.withdraw()
	addstu.deiconify()

def f5():
	addstu.withdraw()
	root.deiconify()

def f6():
	root.withdraw()
	delstu.deiconify()

def f7():
	root.withdraw()
	updatestu.deiconify()

def f8():
	root.deiconify()
	updatestu.withdraw()


def weather():
	pass




def add_record():
	Name = name_text.get()
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
					print(con)
					cursor = con.cursor()
					sql = "insert into students_rec values('%d','%s','%d')"
					args = (Roll,Name,Marks)
					cursor.execute(sql %args)
					con.commit()
	
					
				except Exception as e:
					con.rollback()
					showerror("Error","Record creation erorr! Roll No. Already exists!!")

				finally:
					if con is not None:
						con.close()
						showinfo("Status","Connection Closed")
			else:
				showerror("Error","Invalid Marks. Please insert marks between 0-100")
		else:			
			showerror("Error","Enter a valid Roll No. It cannot be negative!")
	else:
		showerror("Error","Name has to be minimum two alphabets long!!")


def view():
	root.withdraw()
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
		length_labl = Label(viewstu,text = ln, font = ("Courier",14), background = "pale turquoise") ## WINDOW HEADING
		length_labl.place(x = 400, y = 90)

	except Exception as e:
		con.rollback()
		showerror("Error","Unable to fetch data!!")


def update():
	con = None
	r = enterRoll.get()
	try:
		rno = int(r)
	except Exception as e:
		showerror("Error","Invalid Roll no! Please Enter a valid roll no!!")
	if(rno>0):
		name = enterName.get()
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
						showinfo("Status","Connection Closed")
			else:
				showerror("Error","Invalid Marks! Please enter marks in the range of 0-100 only!!")	
		else:
			showerror("Error!","Name should be atleast two alphabets long!!")		
	else:
		showerror("Error!","Roll Number cannot be negative!! Please enter a valid roll number!!")
		
def delete():
	con = None
	try:
		rno = int(rol_delete.get())
	except exception as e:
		showerror("Error","Invalid Roll no! Please insert an integer!!")
	if(rno>0):
		try:
			con = connect("student_rec.db")
			print("connected")
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
				showinfo("Status","Connection Closed")
	else:
		showerror("Error","Invalid Roll No!! Please enter a positive value!!")

def explore():
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
		print(stu_name)
		print(stu_marks)
		ln = len(stu_name)
		print(ln)

	except Exception as e:
		con.rollback()
		showerror("Error","Unable to fetch data!!")


	plt.bar(stu_name,stu_marks, color = "blue",width = 0.25)
	plt.xticks(stu_name, rotation = "vertical")
	plt.xlabel("NAMES")
	plt.ylabel("MARKS")
	plt.title("Marks Distribution")
	plt.show()


## PRIMARY WINDOW WITH ADD AND VIEW AND EXIT BUTTONS
root = Tk()
root.geometry("700x500+450+40")
root.title("Student Management System")
root.resizable(False,False)
head_lbl = Label(root,text = "Student Management System", font = ("Courier",28), background = "pale turquoise") ## WINDOW HEADING
head_lbl.place(x = 60, y = 5)

root.configure(background = "pale turquoise")



## LOCATION TEMPERATURE AND GREETING

head_lbl = Label(root,text = greet, font = ("Courier",12), background = "pale turquoise") ## WINDOW HEADING
head_lbl.place(x = 60, y = 70)

loc_lbl = Label(root,text = loc1, font = ("Courier",12), background = "pale turquoise") ## WINDOW HEADING
loc_lbl.place(x = 310, y = 70)
root.configure(background = "pale turquoise") 

head_lbl = Label(root,text = "Temperature is ", font = ("Courier",12), background = "pale turquoise") ## WINDOW HEADING
head_lbl.place(x = 400, y = 70)
root.configure(background = "pale turquoise") ## FOR TEMPERATURE

head_lbl = Label(root,text = temperature, font = ("Courier",12), background = "pale turquoise") ## WINDOW HEADING
head_lbl.place(x = 549, y = 70)
root.configure(background = "pale turquoise") ## FOR LOCATION

head_lbl = Label(root,text = weather_greet, font = ("Courier",12), background = "pale turquoise") ## WINDOW HEADING
head_lbl.place(x = 70, y = 130)
root.configure(background = "pale turquoise")## FOR QUOTE OF THE DAY




## BUTTONS TO ADD AND VIEW
btnAdd = Button(root,text="Add new Record",font = ("courier",15), background = "tan", command = f4)
btnView = Button(root,text = "View Existing Record",font= ("courier",15), background = "tan", command = view)
btnDelete = Button(root,text = "Delete Existing Record",font= ("courier",15), background = "tan", command = f6)


btnUpdate = Button(root,text="Update a record",font = ("courier",15), background = "tan", command = f7)
btnCharts = Button(root,text="Explore the Data",font = ("courier",15), background = "tan", command = explore)

btnExit = Button(root,text="Exit",font = ("courier",15), command = exit, background = "tan")

btnAdd.place(x = 90, y = 180)
btnView.place(x = 330, y = 180)

btnDelete.place(x = 90, y = 250)
btnUpdate.place(x = 390, y = 250)

btnCharts.place(x = 240, y = 350)
btnExit.place(x = 400, y = 500)

## WINDOW 1 ENDS HERE






addstu = Toplevel(root)
addstu.geometry("500x600+450+40")
addstu.configure(background = "pale turquoise")
addstu.title("New Record")
addstu.resizable(False,False)
## WINDOW HEADING
head_labl = Label(addstu,text = "Add a new Record", font = ("Courier",30), background = "pale turquoise")
head_labl.place(x = 45, y = 5)

## LABELS
roll_labl = Label(addstu, text = "Roll No.", font = ("Courier",15),background = "Pale turquoise")
roll_labl.place(x = 30, y = 140)
roll_text = Entry(addstu, bd = 5, font = ("Courier",15))
roll_text.place(x = 170, y =140)

name_labl = Label(addstu, text = "Name",font = ("Courier",15), background = "pale turquoise")
name_labl.place(x = 30, y = 180)
name_text = Entry(addstu,bd = 5, font = ("Courier",15))
name_text.place(x = 170, y = 180)

marks_labl = Label(addstu, text = "Marks", font = ("Courier", 15), background = "pale turquoise")
marks_labl.place(x = 30, y = 220)
marks_text = Entry(addstu, bd = 5, font = ("Courier",15))
marks_text.place(x = 170,y=220)


btnAdd = Button(addstu,text = "Add Record", font= ("courier",15), background = "tan", command = add_record)
btnAdd.place(x = 150, y = 530)

btnBack = Button(addstu,text = "Back", font= ("courier",15), background = "tan", command = f5)
btnBack.place(x = 350, y = 530)

addstu.withdraw()
## WINDOW 2 ENDS HERE

## WINDOW 3 BEGINS VIEWING DATA

viewstu = Toplevel(root)
viewstu.geometry("500x600+450+40")
viewstu.configure(background = "pale turquoise")
viewstu.title("View Records")
viewstu.resizable(False,False)
head_labl = Label(viewstu,text = "View Records", font = ("Courier",30), background = "pale turquoise") ## WINDOW HEADING
head_labl.place(x = 100, y = 5)

count_labl = Label(viewstu,text = "Total count of students is: ", font = ("Courier",14), background = "pale turquoise") ## WINDOW HEADING
count_labl.place(x = 90, y = 90)

## SCROLLING WIDGET
scroller = ScrolledText(viewstu, width = 35, height = 20, font = ("Courier",15), background = "light cyan")
scroller.pack(pady = 140)

btnBack = Button(viewstu,text = "Back", font= ("courier",15), background = "tan", command = f2)
btnBack.place(x = 350, y = 530)

btnExplore = Button(viewstu,text = "Explore the Records", font= ("courier",15), background = "tan", command = explore)
btnExplore.place(x = 70, y = 530)
viewstu.withdraw()


## WINDOW 5 STARTS HERE UPDATE TAB MAIN


updatestu = Toplevel(root)
updatestu.geometry("500x600+450+40")
updatestu.configure(background = "pale turquoise")
updatestu.title("Update Record")
updatestu.resizable(False,False)
## WINDOW HEADING
head_labl = Label(updatestu,text = "Update Record", font = ("Courier",30), background = "pale turquoise")
head_labl.place(x = 80, y = 5)


roll_labl = Label(updatestu,text = "Roll No.", font = ("Courier",15), background = "pale turquoise")
roll_labl.place(x = 30, y = 140)

enterRoll = Entry(updatestu,bd = 5, font = ("Courier",15))
enterRoll.place(x = 170, y = 140)


name_labl = Label(updatestu,text = "Name", font = ("Courier",15), background = "pale turquoise")
name_labl.place(x = 30, y = 190)
enterName = Entry(updatestu,bd = 5, font = ("Courier",15))
enterName.place(x = 170, y = 190)



enterMarks = Entry(updatestu,bd = 5, font = ("Courier",15))
enterMarks.place(x = 170, y = 240)
marks_labl = Label(updatestu,text = "Marks", font = ("Courier",15), background = "pale turquoise")
marks_labl.place(x = 30, y = 240)



btnUpdate = Button(updatestu,text = "Update Record", font= ("courier",12), background = "tan",command = update)
btnUpdate.place(x = 120, y = 360)

btnBack = Button(updatestu,text = "Back", font= ("courier",12), background = "tan", command = f8)
btnBack.place(x = 350, y = 360)
updatestu.withdraw()




## WINDOW 6 STARTS HERE


delstu = Toplevel(root)
delstu.geometry("500x600+450+40")
delstu.configure(background = "pale turquoise")
delstu.title("Delete Record")
delstu.resizable(False,False)
## WINDOW HEADING
head_labl = Label(delstu,text = "Delete Records", font = ("Courier",30), background = "pale turquoise")
head_labl.place(x = 80, y = 5)


roll_labl = Label(delstu,text = "Enter Roll No. to delete record: ", font = ("Courier",15), background = "pale turquoise")
roll_labl.place(x = 40, y = 160)


roll_labl = Label(delstu,text = "Roll No.", font = ("Courier",15), background = "pale turquoise")
roll_labl.place(x = 30, y = 240)

rol_delete = Entry(delstu,bd = 5, font = ("Courier",15))
rol_delete.place(x = 170, y = 240)

btnDelete = Button(delstu,text = "Delete Record", font= ("courier",12), background = "tan", command = delete)
btnDelete.place(x = 120, y = 360)

btnBack = Button(delstu,text = "Back", font= ("courier",12), background = "tan", command = f8)
btnBack.place(x = 350, y = 360)
delstu.withdraw()


root.mainloop()