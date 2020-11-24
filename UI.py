from tkinter import *

class ProductQuantityEntryScrollFrame(Frame):
    def __init__(self,parent,width,height):
        Frame.__init__(parent)
        frame = Frame(parent,width=width,height=height)
        frame.pack()
        self.upperFrame = Frame(frame)
        self.upperFrame.pack()
        lowerFrame = Frame(frame)
        lowerFrame.pack()
        self.currentPosition = 0
        self.productEntryList = []
        self.quantityEntryList = []
        initProductLabel = Label(self.upperFrame, text='Product ID')
        initProductEntry = Entry(self.upperFrame)
        self.productEntryList.append(initProductEntry)
        initQuantityLabel = Label(self.upperFrame, text='Quantity')
        initQuantityEntry = Entry(self.upperFrame)
        self.quantityEntryList.append(initQuantityEntry)
        initProductLabel.grid(row=self.currentPosition, column=0)
        initProductEntry.grid(row=self.currentPosition, column=1)
        initQuantityLabel.grid(row=self.currentPosition, column=2)
        initQuantityEntry.grid(row=self.currentPosition, column=3)
        self.currentPosition += 1
        addButton = Button(lowerFrame, text='+', command=self.addNewBlock)
        addButton.pack()
        
    def addNewBlock(self):
        genProductLabel = Label(self.upperFrame, text='Product ID')        
        genProductEntry = Entry(self.upperFrame)
        self.productEntryList.append(genProductEntry)
        genQuantityLabel = Label(self.upperFrame, text='Quantity')
        genQuantityEntry = Entry(self.upperFrame)
        self.quantityEntryList.append(genQuantityEntry)        
        genProductLabel.grid(row=self.currentPosition, column=0)
        genProductEntry.grid(row=self.currentPosition, column=1)
        genQuantityLabel.grid(row=self.currentPosition, column=2)
        genQuantityEntry.grid(row=self.currentPosition, column=3)
        self.currentPosition += 1
        
    
    def getInfo(self):
        ret = []
        for i in range(len(self.productEntryList)):
            a = self.productEntryList[i].get()
            b = self.quantityEntryList[i].get()
            ret.append( (a,b) )
        return ret
        