# -*- coding: utf-8 -*-
"""
Created on Mon Nov 03 01:52:22 2020

@author: serkan
"""
# Import Libraries

from tkinter import *
from tkinter.messagebox import showerror, showinfo, askquestion
from tkinter.ttk import Combobox
from keyboard import is_pressed
from playsound import playsound
from datetime import datetime
from gtts import gTTS
from os import remove

# Classes

class Window(object):
    def __init__(self, title = "tk", size = (200, 200), backgroundColor = "#212F3C"):
        self.title = title
        self.size = size
        self.windowState = "normal"
        self.backgroundColor = backgroundColor
        self.windowTransparency = 1.00

        self.form = Tk()
        self.form.title(self.title)
        self.form.geometry(
            "{}x{}+{}+{}".format(
                self.size[0],
                self.size[1],
                int(self.form.winfo_screenwidth() / 2 - self.size[0] / 2),
                int(self.form.winfo_screenheight() / 2 - self.size[1] / 2),
            )
        )
        self.form.iconbitmap("Power House.ico")
        self.form.overrideredirect(True)
        self.form.attributes("-topmost", True)

        Frame(self.form, width = self.size[0], height = self.size[1], bg = self.backgroundColor).place(x = 0, y = 0)
        self.titleBar = Frame(self.form, width = self.size[0], height = 35, bg = "#17202a").place(x = 0, y = 0)

        title = Label(self.form, text = self.title, bg = "#17202a", fg = "White", font = "Calibri 12 normal")
        title.place(x = 15, y = 5)

        self.exitButton = Frame(self.form, width = 45, height = 35, bg = "#17202a")
        self.exitButton.place(x = self.size[0] - self.exitButton["width"], y = 0)
        self.xLabel = Label(self.form, text = "X", fg = "White", bg = "#17202a", font = "Verdana 15 bold")
        self.xLabel.place(x = self.size[0] - 33, y = 2)

        self.loop()

    def summonWindow(self):
        self.form.mainloop()

    def hide(self):
        self.windowState = "withdrawn"
        self.form.state(self.windowState)
        self.form.update()

    def show(self):
        self.windowState = "normal"
        self.form.state(self.windowState)
        self.form.update()

    def loop(self):
        self.mouseXOnWindow = self.form.winfo_pointerx() - int(self.form.winfo_screenwidth() / 2 - self.size[0] / 2)
        self.mouseYOnWindow = self.form.winfo_pointery() - int(self.form.winfo_screenheight() / 2 - self.size[1] / 2)

        def destroyWindow(event):
            try:
                def destroy():
                    self.windowTransparency -= 0.01
                    self.form.wm_attributes("-alpha", self.windowTransparency)
                    self.form.update()
                    if self.windowTransparency < 0:
                        self.form.destroy()
                    self.form.after(20, destroy)
                destroy()
            except:
                pass

        if is_pressed("shift") and is_pressed("ctrl"):
            if self.windowState != "normal":
                self.show()

        if self.size[0] - self.exitButton["width"] < self.mouseXOnWindow < self.size[0] and 0 < self.mouseYOnWindow < 35:
            self.exitButton["bg"] = "#CB4335"
            self.exitButton.update()
            self.xLabel["bg"] = "#CB4335"
            self.xLabel.update()
            self.exitButton.bind("<Button-1>", destroyWindow)
            self.xLabel.bind("<Button-1>", destroyWindow)
        else:
            self.exitButton["bg"] = "#17202a"
            self.exitButton.update()
            self.xLabel["bg"] = "#17202a"
            self.xLabel.update()

        if is_pressed("ğ"):
            print("x : {} - y : {}".format(self.mouseXOnWindow, self.mouseYOnWindow))

        self.form.after(10, self.loop)

class ButtonWidget(object):
    def __init__(self, location = None, text = None, command = None, width = 1, height = 1, font = "Verdana 16 bold"):
        self.location = location
        self.text = text
        self.command = command
        self.width, self.height = width, height
        self.font = font
        self.button = Button(
            self.location,
            text = self.text,
            bg = "#17202A",
            fg = "White",
            bd = 0,
            command = self.command,
            font = self.font,
            width = self.width,
            height = self.height,
            activebackground = "#2E4053",
            activeforeground = "White",
        )

    def summonButton(self, x = 0, y = 0):
        self.button.place(x = x, y = y)

# Basic Variables and My Class Objects

mainWindow = Window(title = "Power House Announce", size = (600, 400))
setWindowState = False
minute = 30
second = 0
hoursToClose = None
minutesToClose = None
secondsToClose = None
weekday = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
]
weekend = ["Saturday", "Sunday"]
weekdayClosingTime = "22:0"
weekendClosingTime = "20:0"
list_ = []
for min in range(23, -1, -1):
    for sec in range(59 , -1, -1):
        list_.append(str(min) + ":" + str(sec))
timeStatus = False
warningAnnounceWorkingStatus = "on"
closingAnnounceWorkingStatus = "on"

# Button Functions

def stop():
    global timeStatus
    timeStatus = False

    stopButton.button["fg"] = "Red"
    stopButton.button.update()
    startButton.button["fg"] = "#ffffff"
    startButton.button.update()

def start():
    global timeStatus
    timeStatus = True

    startButton.button["fg"] = "Green"
    startButton.button.update()
    stopButton.button["fg"] = "#ffffff"
    stopButton.button.update()

def save():
    global minute, second
    global weekendClosingTime
    global weekdayClosingTime

    try:
        if 1 <= int(selectMinuteSpinBox.get()) <= 59:
            minute = int(selectMinuteSpinBox.get())
            second = 0
            timeLabel.configure(text="{}:{}".format(minute, second))
        else:
            showerror("Hata", "Lütfen anons süresini 1-59 dakika aralığında seçiniz.\n1-59 dışında değer girilemez!")
    except ValueError:
        showerror("Hata", "Lütfen anons süresini 1-59 dakika aralığında seçiniz.")

    if weekendClosingCombobox.get() in list_:
        weekendClosingTime = weekendClosingCombobox.get()
    else:
        showerror("Hata", "Lütfen kapanış zamanlarına bir saat değeri seçiniz.")
    if weekdayClosingCombobox.get() in list_:
        weekdayClosingTime = weekdayClosingCombobox.get()
    else:
        showerror("Hata", "Lütfen kapanış zamanlarına bir saat değeri seçiniz.")


    showinfo("Bilgi", "Ayarlar kaydedildi.")

def onWarningAnnounce():
    global warningAnnounceWorkingStatus

    warningAnnounceButton["fg"] = "Green"
    warningAnnounceButton["text"] = "AÇIK"
    warningAnnounceButton["command"] = offWarningAnnounce
    warningAnnounceWorkingStatus = "on"
    warningAnnounceOffLabel["text"] = ""

    warningAnnounceButton.update()

def offWarningAnnounce():
    global warningAnnounceWorkingStatus

    warningAnnounceButton["fg"] = "Red"
    warningAnnounceButton["text"] = "KAPALI"
    warningAnnounceButton["command"] = onWarningAnnounce
    warningAnnounceWorkingStatus = "off"
    warningAnnounceOffLabel["text"] = "Uyarı anonsu yapılmayacaktır! ayarlardan aktif ediniz..."

    warningAnnounceButton.update()

def onClosingAnnounce():
    global closingAnnounceWorkingStatus

    closingAnnounceButton["fg"] = "Green"
    closingAnnounceButton["text"] = "AÇIK"
    closingAnnounceButton["command"] = offClosingAnnounce
    closingAnnounceWorkingStatus = "on"

    closingAnnounceButton.update()

def offClosingAnnounce():
    global closingAnnounceWorkingStatus

    closingAnnounceButton["fg"] = "Red"
    closingAnnounceButton["text"] = "KAPALI"
    closingAnnounceButton["command"] = onClosingAnnounce
    closingAnnounceWorkingStatus = "off"

    closingAnnounceButton.update()

def useDefaultSettings():
    onClosingAnnounce()
    onWarningAnnounce()
    selectMinuteSpinBox.delete(0, "end")
    selectMinuteSpinBox.insert(0, 30)
    weekdayClosingCombobox.delete(0, "end")
    weekdayClosingCombobox.insert(0, "22:0")
    weekendClosingCombobox.delete(0, "end")
    weekendClosingCombobox.insert(0, "20:0")

def hide(event):
    mainWindow.hide()

def openInfoWindow():
    mainWindowWidgetList = [
        startButton.button,
        timeLabel,
        clockLabel,
        closingLabel,
        stopButton.button,
        f1, f2,
        fastAnnounceButton.button,
        warningAnnounceOffLabel,
        infoButton,
    ]
    for widget in mainWindowWidgetList:
        widget.place(x=3000, y=-1000)

    widgetsPack_Info()

def openSetWindow(event):
    global setWindowState
    setWindowState = True

    mainWindowWidgetList = [
        startButton.button,
        timeLabel,
        clockLabel,
        closingLabel,
        stopButton.button,
        f1,
        f2,
        fastAnnounceButton.button,
        warningAnnounceOffLabel,
        backButton.button,
        setFrame,
        playFastWarningAnnounceButton.button,
        playFastText,
        playFastTextButton.button,
        infoButton,
        infoContentLabel,
        phImageLabel,
        masterDevLabel,
    ]
    for i in mainWindowWidgetList:
        i.place(x = 3000, y = -1000)

    widgetsPack_Set()

def openFastAnnounceWindow():
    mainWindowWidgetList = [
        startButton.button,
        timeLabel,
        clockLabel,
        closingLabel,
        stopButton.button,
        f1, f2,
        fastAnnounceButton.button,
        warningAnnounceOffLabel,
        infoButton,
    ]
    for widget in mainWindowWidgetList:
        widget.place(x=3000, y=-1000)

    widgetsPack_Fast()

def backMainWindow():
    global setWindowState
    setWindowState = False

    setWindowWidgetList = [
        backButton.button,
        selectMinuteSpinBox,
        setFrame,
        selectMinuteLabel,
        saveButton.button,
        weekdayClosingCombobox,
        weekendClosingCombobox,
        weekdayClosingLabel,
        weekendClosingLabel,
        closingAnnounceLabel,
        warningAnnounceLabel,
        warningAnnounceButton,
        closingAnnounceButton,
        useDefaultSettingsButton.button,
        playFastWarningAnnounceButton.button,
        playFastText,
        playFastTextButton.button,
        infoContentLabel,
        phImageLabel,
        f1,
        masterDevLabel,
    ]
    for j in setWindowWidgetList:
        j.place(x = 3000, y = -1000)

    widgetsPack_Main()

def widgetsPack_Main():
    startButton.summonButton(
        x = (mainWindow.size[0] - 224) / 2 - 1,
        y = int(mainWindow.size[1] - startButton.button["height"] - 80),
    )
    stopButton.summonButton(
        x= 1 + (mainWindow.size[0]) / 2,
        y= int(mainWindow.size[1] - stopButton.button["height"] - 80),
    )
    f1.pack(side = TOP)
    f2.pack(side = TOP)
    timeLabel.pack(side = TOP)
    clockLabel.place(x = 166, y = 240)
    closingLabel.place(x = 333, y = 248)
    fastAnnounceButton.button.pack(side = TOP) # summonButton(x = (mainWindow.size[0] - 224) / 2 - 1, y = 275)
    warningAnnounceOffLabel.pack()
    infoButton.place(x = 15, y = 50)

def widgetsPack_Set():
    backButton.summonButton(x = 18, y = 52)
    setFrame.place(x = 100, y = 50 + 35)
    saveButton.summonButton(x = (mainWindow.size[0] - 77) / 2, y = 310)

    warningAnnounceLabel.place(x = 130, y = 110)
    warningAnnounceButton.place(x = 305, y = 110)

    closingAnnounceLabel.place(x=130, y=140)
    closingAnnounceButton.place(x=305, y=140)

    selectMinuteSpinBox.place(x=305, y=170)
    selectMinuteLabel.place(x=130, y=170)

    weekdayClosingCombobox.place(x = 305, y = 200)
    weekdayClosingLabel.place(x = 130, y = 200)

    weekendClosingCombobox.place(x = 305, y = 230)
    weekendClosingLabel.place(x = 130, y = 230)

    useDefaultSettingsButton.button.place(x = 410, y = 315)

def widgetsPack_Fast():
    setFrame.place(x = 100, y = 50 + 35)
    backButton.summonButton(x = 18, y = 52)
    playFastWarningAnnounceButton.summonButton(x = (mainWindow.size[0] - 172) / 2, y = 100)
    playFastText.place(x = 130, y = 175)
    playFastTextButton.summonButton(x = 435, y = 175)

def widgetsPack_Info():
    f1.pack(side = TOP)
    phImageLabel.pack(side = TOP)
    backButton.summonButton(x = 18, y = 52)
    infoContentLabel.pack(side = TOP)
    masterDevLabel.pack(side = TOP)

def playFastWarningAnnounce():
     playsound("sounds/announce.mp3")

def playTheText():
    # print(playFastText.get(1.0, END))
    try:
        ask = askquestion("Dikkat", "Yazılanlarda yanlışlık olmadığına emin misiniz?", icon = "warning")
        if ask == "yes":
            sound = gTTS(text = playFastText.get(1.0, END), lang = "tr")
            remove("sounds/sound.mp3")
            sound.save("sounds/sound.mp3")
            playsound("sounds/sound.mp3")
        else:
            pass
    except AssertionError:
        showerror("Hata", "Bu olayı gerçekleştirmeniz için kutucuğa bir şeyler yazınız.")

# Window Design

iButton = Frame(mainWindow.form, width = 45, height = 35, bg = "#17202a")
iButton.place(x = mainWindow.size[0] - mainWindow.exitButton["width"] * 2, y = 0)
_Label = Label(mainWindow.form, text = "-", fg = "White", bg = "#17202a", font = "Verdana 15 bold")
_Label.place(x = mainWindow.size[0] - iButton["width"] - 30, y = 2)
setButton = Frame(mainWindow.form, width = 45, height = 35, bg = "#17202a")
setButton.place(x = mainWindow.size[0] - mainWindow.exitButton["width"] * 3, y = 0)
setLabel = Label(mainWindow.form, text = "SET", fg = "#ffffff", bg = "#17202a", font = "Verdana 13 bold")
setLabel.place(x = mainWindow.size[0] - iButton["width"] - setButton["width"] - 43, y = 3)

#____________________________________________________________________________________________________________________________________________________

f1 = Frame(mainWindow.form, bg = "#17202a", height = 35, width = 1)
f2 = Frame(mainWindow.form, bg = "#212F3C", height = 35, width = 1)
timeLabel = Label(mainWindow.form, text = "{}:{}".format(minute, second), font = "Verdana 70 bold", bg = "#212F3C",fg = "#ffffff")
clockLabel = Label(mainWindow.form, font = "Calibri 25 normal", bg = "#212F3C", fg = "#ffffff")
closingLabel = Label(mainWindow.form, text = weekdayClosingTime, font = "Calibri 12 normal", bg = "#212f3c", fg = "Yellow")
warningAnnounceOffLabel = Label(mainWindow.form, text = "", bg = "#212F3C", fg = "Red")
startButton = ButtonWidget(
    location = mainWindow.form,
    text = "Başlat",
    command = start,
    width = 7,
    height = 2,
)
stopButton = ButtonWidget(
    location = mainWindow.form,
    text = "Durdur",
    command = stop,
    width = 7,
    height = 2
)
fastAnnounceButton = ButtonWidget(
    location = mainWindow.form,
    text = "Hızlı Anons",
    width = 22,
    height = 1,
    font = "Montserrat 12 underline",
    command = openFastAnnounceWindow,
)
infoButton = Button(mainWindow.form, text = "İ", font = "Verdana 15 bold", height = 1, fg = "#ffffff", bg = "#000000", bd = 0, command = openInfoWindow)

#____________________________________________________________________________________________________________________________________________________

backButton = ButtonWidget(location = mainWindow.form, text = "Geri", command = backMainWindow, width = 5, height = 1, font = "Montserrat 12 normal")
setFrame = Frame(mainWindow.form, bg = "#283747", width = mainWindow.size[0] - 200, height = mainWindow.size[1] - 100 - 35)
selectMinuteLabel = Label(mainWindow.form, text = "Anons süresi : ", font = "Montserrat 10 normal", bg = "#283747", fg = "#ffffff")
selectMinuteSpinBox = Spinbox(mainWindow.form, width = 5, from_ = 1, to = 59, font = "Montserrat 10 normal")
selectMinuteSpinBox.delete(0, "end")
selectMinuteSpinBox.insert(0, minute)
lineFrame = Frame(mainWindow.form, bg = "#ffffff", height = 1, width = 260)
weekdayClosingLabel = Label(mainWindow.form, text = "Hafta içi kapanış : ", font = "Montserrat 10 normal", bg = "#283747", fg = "#ffffff")
weekendClosingLabel = Label(mainWindow.form, text = "Hafta sonu kapanış : ", font = "Montserrat 10 normal", bg = "#283747", fg = "#ffffff")
weekdayClosingCombobox = Combobox(mainWindow.form, width = 5, value = list_, font = "Montserrat 10 normal")
weekdayClosingCombobox.insert(0, weekdayClosingTime)
weekendClosingCombobox = Combobox(mainWindow.form, width = 5, value = list_, font = "Montserrat 10 normal")
weekendClosingCombobox.insert(0, weekendClosingTime)
saveButton = ButtonWidget(location = mainWindow.form, text = "Kaydet", command = save, width = 7, font = "Montserrat 13 bold")
warningAnnounceLabel = Label(mainWindow.form, text = "Uyarı anonsu : ", font = "Montserrat 10 normal", bg = "#283747", fg = "#ffffff")
closingAnnounceLabel = Label(mainWindow.form, text = "Kapanış anonsu : ", font = "Montserrat 10 normal", bg = "#283747", fg = "#ffffff")
warningAnnounceButton = Button(
    mainWindow.form,
    bd = 3,
    text = "AÇIK",
    font = "Montserrat 8 normal",
    width = 8,
    fg = "Green",
    bg = "Light gray",
    command = offWarningAnnounce,
)
closingAnnounceButton = Button(
    mainWindow.form,
    bd = 3,
    text = "AÇIK",
    font = "Montserrat 8 normal",
    width = 8,
    fg = "Green",
    bg = "Light gray",
    command = offClosingAnnounce
)
useDefaultSettingsButton = ButtonWidget(
    location = mainWindow.form,
    text = "Varsayılan",
    width = 10,
    height = 1,
    command = useDefaultSettings,
    font = "Montserrat 8 italic"
)

#____________________________________________________________________________________________________________________________________________________

playFastWarningAnnounceButton = ButtonWidget(location = mainWindow.form, text = "Uyarı Anonsu", width = 15, height = 2, font = "Montserrat 12 bold", command = playFastWarningAnnounce)
playFastText = Text(mainWindow.form, width = 32, height = 8, font = "12")
playFastTextButton = ButtonWidget(location = mainWindow.form, text = "Anons\nyap", height = 6, width = 5, font = "10", command = playTheText)

#____________________________________________________________________________________________________________________________________________________

phImage = PhotoImage(file = "Power.gif")
phImageLabel = Label(mainWindow.form, image = phImage, bg = "#212F3C")
infoContentLabel = Label(
    mainWindow.form,
    text = """
    1- Program anons yapılırken kendini durdurur, bu normal bir durumdur.
    2- Sağ üstteki "SET" butonundan programın ayarlarına ulaşabilirsiniz. 
    3- Sağ üstteki "-" butonu ile pencere görünmez yapılabilir, tekrar görünür yapmak için CTRL+Shift yapınız.
            """,
    fg = "#ffffff",
    bg = "#212F3C",
)
masterDevLabel = Label(mainWindow.form, text = "Programming by Serkan Seğmenoğlu", bg = "#212F3C", fg = "Yellow")

widgetsPack_Main()

# Loop and Functions

def Loop():
    global weekdayClosingTime
    global weekendClosingTime
    global closingAnnounceWorkingStatus

    if mainWindow.size[0] - iButton["width"] * 2 < mainWindow.mouseXOnWindow < mainWindow.size[0] - iButton[
        "width"] and 0 < mainWindow.mouseYOnWindow < 35:
        iButton["bg"] = "#CB4335"
        iButton.update()
        _Label["bg"] = "#CB4335"
        _Label.update()
        iButton.bind("<Button-1>", hide)
        _Label.bind("<Button-1>", hide)
    else:
        iButton["bg"] = "#17202a"
        iButton.update()
        _Label["bg"] = "#17202a"
        _Label.update()

    if mainWindow.size[0] - iButton["width"] * 3 < mainWindow.mouseXOnWindow < mainWindow.size[0] - setButton[
        "width"] * 2 and 0 < mainWindow.mouseYOnWindow < 35:
        setButton["bg"] = "#CB4335"
        setButton.update()
        setLabel["bg"] = "#CB4335"
        setLabel.update()
        setButton.bind("<Button-1>", openSetWindow)
        setLabel.bind("<Button-1>", openSetWindow)
    else:
        setButton["bg"] = "#17202a"
        setButton.update()
        setLabel["bg"] = "#17202a"
        setLabel.update()

    nowTime = datetime.now()
    nowDayName = datetime.strftime(nowTime, "%A")

    for day in weekday:
        if nowDayName == day:
            if setWindowState == False:
                # weekdayClosingTime = "22:00"
                closingLabel["text"] = "Kapanış: " + weekdayClosingTime
                closingLabel.update()
            if closingAnnounceWorkingStatus == "on":
                if nowTime.hour == 21 and nowTime.minute == 40 and nowTime.second == 0:
                    playsound("sounds/20minAnnounce.wav")
                elif nowTime.hour == 21 and nowTime.minute == 50 and nowTime.second == 0:
                    playsound("sounds/10minAnnounce.wav")
    if nowDayName == weekend[0]:
        if setWindowState == False:
            # weekendClosingTime = "20:00"
            closingLabel["text"] = "Kapanış: " + weekendClosingTime
            closingLabel.update()
        if closingAnnounceWorkingStatus == "on":
            if nowTime.hour == 19 and nowTime.minute == 40 and nowTime.second == 0:
                playsound("sounds/20minAnnounce.wav")
            elif nowTime.hour == 19 and nowTime.minute == 50 and nowTime.second == 0:
                playsound("sounds/10minAnnounce.wav")
    if nowDayName == weekend[1]:
        if setWindowState == False:
            weekendClosingTime = "Bugün Kapalıdır."
            closingLabel["text"] = "Kapanış: " + weekendClosingTime
            closingLabel.update()

    if setWindowState == False:
        clockLabel["text"] = "{}:{}:{}".format(nowTime.hour, nowTime.minute, nowTime.second)
        clockLabel.update()
    mainWindow.form.after(10, Loop)

Loop()

def timeLoop():
    global minute
    global second
    global timeStatus
    global warningAnnounceWorkingStatus

    if timeStatus == True:
        if second == 0:
            if minute == 0:
                if warningAnnounceWorkingStatus == "on":
                    playsound("sounds/announce.mp3")
                minute = int(selectMinuteSpinBox.get())
            minute -= 1
            second = 59

        second -= 1

        if setWindowState == False:
            timeLabel.configure(text="{}:{}".format(minute, second))

    mainWindow.form.after(1000, timeLoop)
timeLoop()
# 311
mainWindow.summonWindow()