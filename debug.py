import time

def myfunc():
    now=time.time()
    timer = 0
    while timer != 10:
        end = time.time()
        timer = round(end-now)

def mynextfunc():
    now=time.time()
    timer = 0
    while timer != 5:
        end = time.time()
        timer = round(end-now)


myfunc()
print("myfunc() exited after 10 seconds")

mynextfunc()
print("mynextfunc() exited after 5 seconds")