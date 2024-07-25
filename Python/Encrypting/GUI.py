import tkinter.filedialog
import EncryptCore
import os
import sys

import tkinter
from tkinter import filedialog

subWindows = { "GenerateKey": None,
               "EncryptFile": None,
               "DecryptFile": None }
selectedDir = ""
publicKey = None
privateKey = None
strVar = None

def FindDirectory():
    global selectedDir
    selectedDir = filedialog.askdirectory()
    OnGenerateKeyButtonClicked()
    
def SubWindowClose(type):
    global subWindows
    if subWindows[type] is not None :
        subWindows[type].destroy()
        subWindows[type] = None

def GenerateKey():
    global selectedDir
    global strVar
    fileName = strVar.get()
    if selectedDir == "":
        return
    if fileName == "":
        fileName = "RSA"
    
    os.chdir(selectedDir)
    global publicKey
    global privateKey
    publicKey, privateKey = EncryptCore.RSAInitialize(True, fileName)

def OnGenerateKeyButtonClicked():
    global subWindows
    if subWindows["GenerateKey"] == None:
        subWindows["GenerateKey"] = tkinter.Tk(className=" Generate Key")
    
    window = subWindows["GenerateKey"]
    window.geometry('320x240')
    window.wm_resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", lambda:SubWindowClose("GenerateKey"))

    label = tkinter.Label(window, text="Selected Directory:", padx=3, pady=10)
    label.grid(row=1, column=1)

    global selectedDir
    dirTextBox = tkinter.Entry(window, state="normal")
    dirTextBox.insert(0, selectedDir)
    dirTextBox.config(state="readonly")
    dirTextBox.grid(row=1, column=2)

    dirFindButton = tkinter.Button(window, text="..Find", command=FindDirectory)
    dirFindButton.grid(row=1, column=3)

    if selectedDir == "":
        return
    
    keyNameLabel = tkinter.Label(window, text="Key file name:", padx=3, pady = 10)
    keyNameLabel.grid(row=2, column=1)

    global strVar
    strVar = tkinter.StringVar(window)
    keyFileNameEntry = tkinter.Entry(window, textvariable=strVar)
    keyFileNameEntry.grid(row=2, column=2)

    generateKeyButton = tkinter.Button(window, text="Generate key", command=GenerateKey, padx=10)
    generateKeyButton.grid(row=3, column=1)


def MainWindow():
    window = tkinter.Tk(className=" Encrypt File")
    window.geometry('320x200')
    window.wm_resizable(False, False)

    mainLabel = tkinter.Label(window, text="Encrypting Program")
    mainLabel.pack(padx= 10, pady=10)
    gkButton = tkinter.Button(window, text="Generate key", command=OnGenerateKeyButtonClicked)
    gkButton.pack(pady = 5)
    eButton = tkinter.Button(window, text="Encrypt file", command=lambda:TestFunction(window))
    eButton.pack(pady = 5)
    dButton = tkinter.Button(window, text="Decrypt file", command=lambda:TestFunction(window))
    dButton.pack(pady = 5)

    return window

def close(event):
    sys.exit()

def MainLoop() :
    window = MainWindow()
    window.title("Encrypting File")
    window.bind("<Escape>", close)
    window.mainloop()

MainLoop()
