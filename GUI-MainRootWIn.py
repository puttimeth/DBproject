from tkinter import *
from myDBFunc2019 import *
from tkinter import font
from tkinter import messagebox

class RootWin():
    def __init__(self):
        root = Tk()
        root.title("Kerry - Aroi Jang Food DBMS")
        root.geometry('500x500')
        
        header_font = ('open sans', 15)
        body_font = ('open sans', 12)

        manageOrderFrame = Frame(root)
        manageOrderFrame.pack()
        
        manageOrderHeaderLabel = Label(manageOrderFrame, text="Order Management", font=header_font, pady=10)
        manageOrderHeaderLabel.pack(side=TOP)
        
        createOrderButton = Button(manageOrderFrame, text="Create Order", command=self.popAddWin, font=body_font, width=30)
        createOrderButton.pack(side=TOP)
        
        deleteButton = Button(manageOrderFrame, text="Delete Order", command=self.popDeleteWin, font=body_font,
                              width=30)
        deleteButton.pack(side=TOP)
        
        updateButton = Button(manageOrderFrame, text="Update Order", command=self.popUpdateWin, font=body_font,
                              width=30)
        updateButton.pack(side=TOP)
        
        searchByCustomerIDButton = Button(manageOrderFrame, text="Search Order by Customer ID",
                                          command=self.popSearchCustomerIDWin, font=body_font, width=30)
        searchByCustomerIDButton.pack(side=TOP)
        
        root.mainloop()

    def popAddWin(self):
        r1 = AddOrderWin("Add Order")

    def popDeleteWin(self):
        s1 = DeleteOrderWin("Delete Order")

    def popUpdateWin(self):
        s1 = UpdateOrderWin("Update Order")

    def popSearchCustomerIDWin(self):
        d1 = SearchCustomerIDWin("Search Order by Customer ID")

    def popSearchRestaurantIDWin(self):
        d1 = SearchRestaurantIDWin("Search Order by Restaurant ID")


class AddOrderWin():
    def __init__(self, title):
        self.cwin = Toplevel()
        self.cwin.title(title)
        self.cwin.geometry('290x125')

        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)
        
        # variable
        self.productList = set()
        self.promotionList = set()
        
        self.createOrderFrame = Frame(self.cwin)
        self.editOrderFrame = Frame(self.cwin)
        self.selectDeliverymanFrame = Frame(self.cwin)
        self.createOrderFrame.grid(row=0,column=0,sticky='news')
        self.editOrderFrame.grid(row=0,column=0, sticky='news')
        self.selectDeliverymanFrame.grid(row=0,column=0, sticky='news')
        
        self.createOrder_headerLabel = Label(self.createOrderFrame, text='Create Order',font=headerFont)
        self.createOrder_customerIDLabel = Label(self.createOrderFrame, text='Customer ID',font=bodyFont)
        self.createOrder_customerIDEntry = Entry(self.createOrderFrame)
        self.createOrder_nextButton = Button(self.createOrderFrame, text='next',font=bodyFont,command=self.createOrderNext)
        
        self.createOrder_headerLabel.grid(row=0,column=0,columnspan=2)
        self.createOrder_customerIDLabel.grid(row=1,column=0)
        self.createOrder_customerIDEntry.grid(row=1,column=1)
        self.createOrder_nextButton.grid(row=2,column=0,columnspan=2)
        
        self.editOrder_headerLabel = Label(self.editOrderFrame, text='Edit Order',font=headerFont)
        self.editOrder_productIDLabel = Label(self.editOrderFrame, text='Product ID',font=bodyFont)
        self.editOrder_productIDEntry = Entry(self.editOrderFrame)
        self.editOrder_quantityLabel = Label(self.editOrderFrame, text='Quantity',font=bodyFont)
        self.editOrder_quantityEntry = Entry(self.editOrderFrame)
        self.editOrder_addProductButton = Button(self.editOrderFrame, text='add product',font=bodyFont, command=self.addProduct)
        self.editOrder_promotionIDLabel = Label(self.editOrderFrame, text='Promotion ID',font=bodyFont)
        self.editOrder_promotionIDEntry = Entry(self.editOrderFrame)
        self.editOrder_addPromotionButton = Button(self.editOrderFrame, text='add promotion',font=bodyFont, command=self.addPromotion)
        self.editOrder_nextButton = Button(self.editOrderFrame, text='next',font=bodyFont,command=self.editOrderNext)
        
        self.editOrder_headerLabel.grid(row=0,column=0,columnspan=2)
        self.editOrder_productIDLabel.grid(row=1,column=0)
        self.editOrder_productIDEntry.grid(row=1,column=1)
        self.editOrder_quantityLabel.grid(row=2,column=0)
        self.editOrder_quantityEntry.grid(row=2,column=1)
        self.editOrder_addProductButton.grid(row=3,column=0,columnspan=2)
        self.editOrder_promotionIDLabel.grid(row=4,column=0)
        self.editOrder_promotionIDEntry.grid(row=4,column=1)
        self.editOrder_addPromotionButton.grid(row=5,column=0,columnspan=2)
        self.editOrder_nextButton.grid(row=6,column=0,columnspan=2)
        
        self.selectDeliveryman_headerLabel = Label(self.selectDeliverymanFrame, text='Select Deliveryman',font=headerFont)
        self.selectDeliveryman_deliverymanIDLabel = Label(self.selectDeliverymanFrame, text='Deliveryman ID',font=bodyFont)
        self.selectDeliveryman_deliverymanIDEntry = Entry(self.selectDeliverymanFrame)
        self.selectDeliveryman_submitOrderButton = Button(self.selectDeliverymanFrame, text='submit order',font=bodyFont, command=self.submitOrder)
        
        self.selectDeliveryman_headerLabel.grid(row=0,column=0,columnspan=2)
        self.selectDeliveryman_deliverymanIDLabel.grid(row=1,column=0)
        self.selectDeliveryman_deliverymanIDEntry.grid(row=1,column=1)
        self.selectDeliveryman_submitOrderButton.grid(row=2,column=0,columnspan=2)
        
        self.createOrderFrame.tkraise()

    def submitOrder(self):
        self.cwin.title("Added")
        dataentry = [self.createOrder_customerIDEntry.get(), list(self.productList), list(self.promotionList), self.selectDeliveryman_deliverymanIDEntry.get()]
        print(dataentry)
        aCustomer = Customer(dataentry)
        retmsg = aCustomer.add()
        messagebox.showinfo(parent=self.cwin,title='Result', message=retmsg[1])
        #self.cwin.destroy()
        
    def createOrderNext(self):
        self.cwin.geometry('300x260')
        self.editOrderFrame.tkraise()
        
    def editOrderNext(self):        
        self.cwin.geometry('320x125')
        self.selectDeliverymanFrame.tkraise()
        
    def addProduct(self):
        pid = self.editOrder_productIDEntry.get()
        quan = self.editOrder_quantityEntry.get()
        find = 0
        for i,j in self.productList:
            if i==pid:
                find = 1
        if find == 0:
            self.productList.add( (self.editOrder_productIDEntry.get(),self.editOrder_quantityEntry.get()) )
    
    def addPromotion(self):
        self.promotionList.add( self.editOrder_promotionIDEntry.get() )


class DeleteOrderWin():
    def __init__(self, title):
        self.cwin = Toplevel()
        self.cwin.title(title)
        self.cwin.geometry('260x120')

        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)

        self.headerLabel = Label(self.cwin, text='Delete Order', font=headerFont)

        self.label_order_id = Label(self.cwin, text="Order ID", font=bodyFont)
        self.entry_order_id = Entry(self.cwin)

        self.submit_button = Button(self.cwin, text='Delete', font=bodyFont, width=5, padx=20, command=self.deleteOrder)

        self.headerLabel.grid(row=0, column=0, columnspan=2)
        self.label_order_id.grid(row=1, column=0)
        self.entry_order_id.grid(row=1, column=1)
        self.submit_button.grid(row=2, column=0, columnspan=2)

    def deleteOrder(self):
        self.cwin.title("Deleted")
        dataentry = [self.entry_order_id.get()]
        aCustomer = Customer(dataentry)
        retmsg = aCustomer.delete()
        messagebox.showinfo(parent=self.cwin,title='Result', message=retmsg[1])


class UpdateOrderWin():
    def __init__(self, title):
        self.cwin = Toplevel()
        self.cwin.title(title)
        self.cwin.geometry('260x140')

        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)

        status_options = ['in process', 'deliver', 'complete', 'cancel']
        self.variable = StringVar(self.cwin)
        self.variable.set(status_options[0])

        self.headerLabel = Label(self.cwin, text='Update Order', font=headerFont)

        self.label_order_id = Label(self.cwin, text="Order ID", font=bodyFont)
        self.entry_order_id = Entry(self.cwin)

        self.label_status = Label(self.cwin, text="Status", font=bodyFont)
        self.option_status = OptionMenu(self.cwin, self.variable, *(status_options))

        self.submit_button = Button(self.cwin, text='Update', font=bodyFont, width=5, padx=20,
                                    command=self.UpdateOrderStatus)

        self.headerLabel.grid(row=0, column=0, columnspan=2)
        self.label_order_id.grid(row=1, column=0)
        self.entry_order_id.grid(row=1, column=1)
        self.label_status.grid(row=2, column=0)
        self.option_status.grid(row=2, column=1)
        self.submit_button.grid(row=3, column=0, columnspan=2)

    def UpdateOrderStatus(self):
        self.cwin.title("Updated")
        dataentry = [self.entry_order_id.get(), self.variable.get()]
        aCustomer = Customer(dataentry)

        retmsg = aCustomer.updateOrderStatus()

        messagebox.showinfo(parent=self.cwin,title='Result', message=retmsg[1])


class SearchCustomerIDWin():
    def __init__(self, title):
        self.msg = []
        self.cwin = Toplevel()
        self.cwin.title(title)
        self.cwin.geometry('290x140')

        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)

        self.headerLabel = Label(self.cwin, text='Search Order', font=headerFont)
        self.headerLabel.pack()
        self.label_order_id = Label(self.cwin, text="Customer ID", font=bodyFont)
        self.entry_order_id = Entry(self.cwin)


        self.submit_button = Button(self.cwin, text='Search', font=bodyFont, width=5, padx=20,
                                    command=self.searchOrderbyID)

        self.headerLabel.grid(row=0, column=0, columnspan=2)
        self.label_order_id.grid(row=1, column=0)
        self.entry_order_id.grid(row=1, column=1)

        self.submit_button.grid(row=3, column=0, columnspan=2)

    def searchOrderbyID(self):
        self.cwin.title("Search order")
        dataentry = [self.entry_order_id.get()]
        aCustomer = Customer(dataentry)
        self.id = self.entry_order_id.get();

        retmsg = aCustomer.searchOrderByCustomerID()
        self.msg = retmsg

        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)
        
        if(retmsg[0] == '0'):
            if(len(retmsg[1]) > 0):
                
                order_list = []
                for i in range(len(retmsg[1])):
                    order_list.append(retmsg[1][i][0][1])
                
                self.cwin = Toplevel()
                self.cwin.geometry('160x150')
                
                self.headerLabel = Label(self.cwin, text="Search order", font=headerFont)
                self.label_order_id1 = Label(self.cwin, text="Order ID ", font=bodyFont)
                
                self.variable = StringVar(self.cwin)
                self.variable.set(order_list[0])
                self.option_status = OptionMenu(self.cwin, self.variable, *(order_list))
                
                self.submit_button = Button(self.cwin, text='Search', font=bodyFont, width=5, padx=20,
                                            command=self.viewOrderID)

                self.headerLabel.grid(row=0, column=0, columnspan=2)
                self.label_order_id1.grid(row=1, column=0)
                self.option_status.grid(row=1, column=1)

                self.submit_button.grid(row=3, column=0, columnspan=2)
            else:
                messagebox.showinfo(parent=self.cwin,title='No Result', message='There is no order for this Customer ID')
        else:
            messagebox.showinfo(parent=self.cwin,title='Result', message=retmsg[1])
    
    def viewOrderID(self):
        self.cwin = Toplevel()
        self.cwin.geometry('440x300')
        headerFont = ('open sans', 15)
        bodyFont = ('open sans', 12)
        self.cwin.title("View order")
        dataentry = self.variable.get()
        retmsg = self.msg
        ind = 0;
        pd = ""
        for i in range(len(retmsg[1])):
            if str(retmsg[1][i][0][1]) == str(dataentry):
                ind = i;
                for x in retmsg[1][i]:
                    pd = pd + "["+str(x[2])+"]"+str(x[4])+" x"+str(x[5])+"\n"
                break
        result = retmsg[1][ind][0]
        pd_list = pd.split("\n")
        
        self.headerLabel = Label(self.cwin, text='Order', font=headerFont)
        self.label_order_id1 = Label(self.cwin, text="Order ID", font=bodyFont)
        self.label_order_id1_val = Label(self.cwin, text=result[1])

        self.label_order_id2 = Label(self.cwin, text="Customer ID", font=bodyFont)
        self.label_order_id2_val = Label(self.cwin, text=result[0])

        self.label_order_id3 = Label(self.cwin, text="Deliveryman ID", font=bodyFont)
        self.label_order_id3_val = Label(self.cwin, text=result[3])

        self.label_order_id4 = Label(self.cwin, text="order status", font=bodyFont)
        self.label_order_id4_val = Label(self.cwin, text=result[7])
        
        self.label_order_id5 = Label(self.cwin, text="Total price", font=bodyFont)
        self.label_order_id5_val = Label(self.cwin, text=result[6])
        
        self.label_order_id6 = Label(self.cwin, text="Product", font=bodyFont)

        self.label_order_id1.grid(row=1, column=0)
        self.label_order_id1_val.grid(row=1, column=1)

        self.label_order_id2.grid(row=2, column=0)
        self.label_order_id2_val.grid(row=2, column=1)

        self.label_order_id3.grid(row=3, column=0)
        self.label_order_id3_val.grid(row=3, column=1)

        self.label_order_id4.grid(row=4, column=0)
        self.label_order_id4_val.grid(row=4, column=1)
        
        self.label_order_id5.grid(row=5, column=0)
        self.label_order_id5_val.grid(row=5, column=1)
        
        self.label_order_id6.grid(row=6, column=0)
        for i in range(len(pd_list)):
            self.label_order_id6_val = Label(self.cwin, text=pd_list[i])
            self.label_order_id6_val.grid(row=6+i, column=1)
            self.cwin.rowconfigure(6+i,weight=1)
                
        self.submit_button = Button(self.cwin, text='Close', font=bodyFont, width=5, padx=20,command=self.cwin.withdraw)
        self.headerLabel.grid(row=0, column=0, columnspan=2)

        self.submit_button.grid(row=7+i, column=0, columnspan=2)
        self.cwin.rowconfigure(7+i,weight=1)
        self.cwin.columnconfigure(0,weight=1)
        self.cwin.columnconfigure(1, weight=1)
        self.cwin.rowconfigure(0,weight=1)
        self.cwin.rowconfigure(1,weight=1)
        self.cwin.rowconfigure(2,weight=1)
        self.cwin.rowconfigure(3,weight=1)
        self.cwin.rowconfigure(4,weight=1)
        self.cwin.rowconfigure(5,weight=1)
            
class SearchRestaurantIDWin():
    def __init__(self, title):
        super().__init__(title)
        self.button_submit.config(text="Delete", command=self.deleteCus)
        self.button_submit = Button(self.cwin)

    def deleteCus(self):
        self.cwin.title("Deleted")
        dataentry = [self.entry_id.get(), self.entry_name.get()]
        aCustomer = Customer(dataentry)

        retmsg = aCustomer.delete()

        if retmsg[0] == "0":
            self.entry_id.delete(0, END)
            self.entry_id.insert(0, aCustomer.getInfo()[0])
            self.entry_name.delete(0, END)
            self.entry_name.insert(0, aCustomer.getInfo()[1])

        else:
            self.entry_id.delete(0, END)
            self.entry_id.insert(0, "?????")
        self.label_status.config(text=retmsg[1])
    
Mainmenu = RootWin()