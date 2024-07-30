import tkinter.filedialog
import EncryptCore
import os
import sys

import tkinter
from tkinter import filedialog

subWindow = None
selectedDir = "" # Dir to Decrypt
selectedFile = "" # File to Encrypt

publicKey = { "dir": "",
             "fileName": "",
             "key": None }
privateKey = { "dir": "",
             "fileName": "",
             "key": None }
strVar = None

def FindDirectory():
    global selectedDir
    selectedDir = filedialog.askdirectory()
    OnGenerateKeyButtonClicked()

def FindFile():
    global selectedFile
    selectedFile = filedialog.askopenfilename()
    OnEncryptFileButtonClicked()

def FindKeyFile(isPublic = bool, isEncrypt = bool):
    fullPath = filedialog.askopenfilename()
    splited = fullPath.split('/')
    fileName = splited[-1]
    filePath = "/".join(splited[0:-1])
    
    key = None
    dic = None
    os.chdir(filePath)
    if isPublic:
        dic = publicKey
        key = EncryptCore.RSAGetPublicKey(fileName)
    else :
        dic = privateKey
        key = EncryptCore.RSAGetPrivateKey(fileName)
    
    dic['dir'] = filePath
    dic['fileName'] = fileName
    dic['key'] = key
    
    if isEncrypt:
        OnEncryptFileButtonClicked()
    else:
        OnDecryptFileButtonClicked()

def GetSubWindow(title, geometry):
    global subWindow
    if subWindow == None:
        subWindow = tkinter.Tk()
    
    window = subWindow
    for w in window.winfo_children():
        w.destroy()
    window.title(title)
    window.geometry(geometry)
    window.wm_resizable(False, False)
    window.protocol("WM_DELETE_WINDOW", SubWindowClose)

    return subWindow

def SubWindowClose():
    global subWindow
    if subWindow is not None :
        subWindow.destroy()
        subWindow = None

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
    (pub, pvk) = EncryptCore.RSAInitialize(True, fileName)
    publicKey['key'] = pub
    publicKey["dir"] = selectedDir
    publicKey["fileName"] = fileName+".pub"
    
    privateKey['key'] = pvk
    privateKey["dir"] = selectedDir
    privateKey["fileName"] = fileName+".pvk"

def OnGenerateKeyButtonClicked():
    window = GetSubWindow('Generate Key', '320x240')

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

def OnEncryptFileButtonClicked():
    window = GetSubWindow('Encrypt', '320x240')
    
    keyLabel = tkinter.Label(window, text="Public Key:", padx=3, pady=10)
    keyLabel.grid(row=1, column=1)
    
    keyTextBox = tkinter.Entry(window, state="normal")
    s = ""
    if publicKey['dir'] != "" and publicKey['fileName'] != "":
        s = publicKey["dir"] + "/" + publicKey["fileName"]
    keyTextBox.insert(0, s)
    keyTextBox.config(state="readonly")
    keyTextBox.grid(row=1, column=2)
    
    keyFindButton = tkinter.Button(window, text="..Find", command=lambda:FindKeyFile(True, True))
    keyFindButton.grid(row=1, column=3)
    
    fileLabel = tkinter.Label(window, text="Selected File:", padx=3, pady=10)
    fileLabel.grid(row=2, column=1)

    global selectedFile
    fileTextBox = tkinter.Entry(window, state="normal")
    fileTextBox.insert(0, selectedFile)
    fileTextBox.config(state="readonly")
    fileTextBox.grid(row=2, column=2)

    fileFindButton = tkinter.Button(window, text="..Find", command=FindFile)
    fileFindButton.grid(row=2, column=3)

    if selectedFile == "":
        return

    encryptFileButton = tkinter.Button(window, text="Encrypt file", command=lambda:EncryptCore.EncryptSingleFile(publicKey['key'], publicKey['dir'], publicKey['fileName']), padx=10)
    encryptFileButton.grid(row=4, column=1)

def OnDecryptFileButtonClicked():
    window = GetSubWindow('Decrypt', '320x240')

def MainWindow():
    window = tkinter.Tk(className=" Encrypt File")
    window.geometry('320x200')
    window.wm_resizable(False, False)

    mainLabel = tkinter.Label(window, text="Encrypting Program")
    mainLabel.pack(padx= 10, pady=10)
    gkButton = tkinter.Button(window, text="Generate key", command=OnGenerateKeyButtonClicked)
    gkButton.pack(pady = 5)
    eButton = tkinter.Button(window, text="Encrypt file", command=OnEncryptFileButtonClicked)
    eButton.pack(pady = 5)
    dButton = tkinter.Button(window, text="Decrypt file", command=OnDecryptFileButtonClicked)
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
