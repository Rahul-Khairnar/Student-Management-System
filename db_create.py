from sqlite3 import *
con = None
try:
	con = connect("student_rec.db")
	print("connected")

except Exception as e:
	print("Connection issues",e)
	

finally:
	if con is not None:
		con.close()
		print("Connection Closed")