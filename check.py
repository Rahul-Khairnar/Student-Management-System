string = "Rahul Sunil Khairnar"
if all(x.isalpha() or x.isspace() for x in string):
	print("Alphabets only")
else:
	print("Invalid")