from datetime import datetime

import serial
import threading
import tkinter, win32api, win32con, pywintypes

port = input("Podaj COM i numer portu")

def thread_function(label):
    ser = serial.Serial(port, 115200)  # open serial port,
    print("connected")
    print(ser.name)
    stopped = True
    ms = 0
    lastTime = datetime.now()
    timeDelta = 0
    while True:
        currentTime = datetime.now()
        timeDelta = (currentTime-lastTime).microseconds
        if stopped == False:
            ms += timeDelta
        while ser.in_waiting:
            action = ser.read(1)
            if action == b's':
                stopped = not stopped
            elif action == b'r':
                if stopped == True:
                    ms = 0
        millis = ms/10000
        seconds = (millis / 100) % 60
        seconds = int(seconds)
        minutes = (millis / (100 * 60)) % 60
        minutes = int(minutes)
        ss = str(seconds)
        mm = str(minutes)
        mss = str(int(millis)%100)
        if(seconds<10):
            ss = '0'+ss
        if(minutes<10):
            mm = '0'+mm
        if(int(millis)%100<10):
            mss = '0'+mss

        label.configure(text=mm+':'+ss +':' + mss)
        label.update()
        lastTime = currentTime



label = tkinter.Label(text='0', font=('Times New Roman','80'), fg='yellow', bg='white')
label.master.overrideredirect(True)
label.master.geometry("+0+0")
label.master.lift()
label.master.wm_attributes("-topmost", True)
label.master.wm_attributes("-disabled", True)
label.master.wm_attributes("-transparentcolor", "white")
x = threading.Thread(target=thread_function, args=(label,))
x.start()

hWindow = pywintypes.HANDLE(int(label.master.frame(), 16))
# http://msdn.microsoft.com/en-us/library/windows/desktop/ff700543(v=vs.85).aspx
# The WS_EX_TRANSPARENT flag makes events (like mouse clicks) fall through the window.
exStyle = win32con.WS_EX_COMPOSITED | win32con.WS_EX_LAYERED | win32con.WS_EX_NOACTIVATE | win32con.WS_EX_TOPMOST | win32con.WS_EX_TRANSPARENT
win32api.SetWindowLong(hWindow, win32con.GWL_EXSTYLE, exStyle)

label.pack()
label.mainloop()