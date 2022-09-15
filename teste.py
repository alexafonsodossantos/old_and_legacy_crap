import time
from datetime import datetime
def writelog(n, c):
    now = datetime.now()
    log = open("log.txt", "a")
    log.write(str(now) + " - " + str(n) + " finished with " + str(c) + " iterations. " + "\n")
    log.close()

n = 12725
running = True
c = 0
while running:
    if (n % 2) == 0:
        d = n
        n = n / 2
        print(n)
        c += 1
        
    else:
        d = n
        n = (n * 3) + 1
        print(n)
        c += 1
    
    if n == 1:
        running = False
        print("-----------------------")
        print(str(c) + " iterations.")
        writelog(n,c)
        c = 0