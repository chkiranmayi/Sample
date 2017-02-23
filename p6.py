n1 = int(raw_input("enter your number"))
rev = 0
while (n1 > 0):
    x = n1 % 10
    rev = (rev * 10)+ x
    n1 = n1 //10
print rev

