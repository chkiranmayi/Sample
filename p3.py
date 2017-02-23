num = int(raw_input("Enter number: "))
fac = 1
if num <  0 :
    print "factorial doesnot exists"
elif num == 0:
    print "factorial of number is 1"
else:
    for i in range(1,num+1):
        fac = fac*i
    print "factorial of number is", fac    

