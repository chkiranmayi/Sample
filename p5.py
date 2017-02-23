from collections import Counter
s = open("p4.txt")
wordcount = Counter(s.read().split())
print wordcount
