import time

def waitUntil(condition, output): #defines function
    wU = True
    while wU == True:
        if condition: #checks the condition
            output
            wU = False
        time.sleep(60) #waits 60s for preformance