num = int(raw_input("enter the number of elements of series :"))
n1 = 0
n2 = 1
n3 = 2
if num <= 0:
    print ("Enter positive integer:")
elif num == 1 :
    print "Fibnocci series upto", num,":"
    print n1
else :
    print "Fibnocci series upto", num,":"
    print n1
    print n2
    while n3 < num :
        n4 = n2+n1
        print n4
        n1 = n2
        n2 = n4
        n3 = n3+1
