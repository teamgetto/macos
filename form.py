#import TextSummarizerBase
from tkinter import *
from TextSummarizerBase import *


def Start():
    print("başladı.")
    fullTextPath = fullTextEntry.get()
    abstractPath = abstractEntry.get()
    print(fullTextPath + "\n")
    print(abstractPath + "\n")
    StartTextSummarizer()

root = Tk()
root.title = ("Doküman Doğrulama")
root.geometry('1000x500')

global fullTextLabel
fullTextLabel = Label(root,text ='Full Text Path')
fullTextLabel.pack(pady=10)

global fullTextEntry
fullTextEntry = Entry(root,width =100)
fullTextEntry.pack()

global abstractLabel
abstractLabel = Label(root,text ='Abstract Path')
abstractLabel.pack(pady=10)

global abstractEntry
abstractEntry = Entry(root,width =100)
abstractEntry.pack(pady=10)

global messageLabel
messageLabel = Label(root,text ='İşlemler')
messageLabel.pack(pady=10)

global messageEntry
messageEntry = Listbox(root,width =300)
messageEntry.pack(pady=30)

global exeButton
exeButton = Button(root,text='Doküman Doğrulama',command = Start, width =50, height =2)
exeButton.pack()

root.mainloop()