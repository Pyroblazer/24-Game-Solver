import sys
import time

def hitung(a,operator,b):
#fungsi untuk mengembalikan hasil dari operasi a dan b yang sesuai dengan operatornya
#operator terdiri dari +,-,*,/
	if (operator == "+"):
		return a+b
	elif (operator == "-"):
		return a-b
	elif (operator == "*"):
		return a*b
	else:
		return a/b

def pick_operator(a,b):
#fungsi untuk mengembalikan operator yang sesuai sehingga operasi a b mendekati 24
#operator yang digunakan adalah +,-,*,/
	if (a < 24):
		op = '+'
		pembanding = abs(a+b-24)
		if(abs(a*b-24) < pembanding):
			op = '*'
	elif (a > 24):
		op = '-'
		pembanding = abs(a-b-24)
		if(abs(a/b-24) < pembanding):
			op = '/'
	else:
		op = '+'
		pembanding = abs(a+b-24)
		if(abs(a-b-24) < pembanding):
			pembanding = abs(a-b-24)
			op  = '-'
		if(abs(a*b-24) < pembanding):
			pembanding = abs(a*b-24)
			op = '*'
		if(abs(a/b-24) < pembanding):
			pembanding = abs(a/b-24)
			op = '/'
	return op

def sort(arr):
#prosedur untuk sort 3 buah bilangan dari besar ke kecil
#menggunakan bubble sort
	for i in range (4):
		for j in range (0, 3-i):
			if arr[j] < arr[j+1]:
				arr[j],arr[j+1] = arr[j+1],arr[j]

def hitung_all(a,b,c,d):
#mengembalikan hasil dari operasi a,b,c,d dengan operator yang sesuai agar mendekati 24
#menggunakan algoritma greedy
	op1 = pick_operator(a,b)
	op2 = pick_operator(hitung(a,op1,b),c)
	op3 = pick_operator(hitung(hitung(a,op1,b),op2,c),d)
	return hitung(hitung(hitung(a,op1,b),op2,c),op3,d)

def solve(a,op1,b,op2,c,op3,d):
#mengembalikan output dari hasil operasi dengan tempat kurung yang sesuai
	if (((op2 == '+') or (op2 == '-')) and ((op3 == '*') or (op3 == '/'))):
		return("(" + str(a) + op1 + str(b) + op2 + str(c) + ")" + op3 + str(d) + "=" + str(hitung_all(a,b,c,d)))
	elif (((op1 == '+') or (op1 == '-')) and ((op2 == '*') or (op2 == '/'))):
		return("(" + str(a) + op1 + str(b) + ")" + op2 + str(c) + op3 + str(d) + "=" + str(hitung_all(a,b,c,d)))
	else:
		return(str(a) + op1 + str(b) + op2 + str(c) + op3 + str(d) + "=" + str(hitung_all(a,b,c,d)))

#main program
fin = open(sys.argv[1],"r")
nums = []
for line in fin:
    for num in line.split():
        nums.append(int(num))
sort(nums)
op1 = pick_operator(nums[0],nums[1])
op2 = pick_operator(hitung(nums[0],op1,nums[1]),nums[2])
op3 = pick_operator(hitung(hitung(nums[0],op1,nums[1]),op2,nums[2]),nums[3])
fout = open(sys.argv[2],"w")
fout.write(solve(nums[0],op1,nums[1],op2,nums[2],op3,nums[3]))
