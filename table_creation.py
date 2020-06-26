from sqlite3 import *
con = None
try:
	con = connect("student_rec.db")
	print("connected")
	cursor = con.cursor()
	sql = "create table students_rec(roll_no int primary key, name text, marks int)"
	cursor.execute(sql)
	print("table created!")
except Exception as e:
	print("table creation issue!",e)

finally:
	if con is not None:
		con.close()
		print("Connection Closed")