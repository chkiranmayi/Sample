num = int(raw_input("Enter number: "))
if num > 1:
    for i in range(2,num):
        if num % 2 == 0 :
            print("The number is not prime number")
            break
    else :
        print(num,"is a prime number")

