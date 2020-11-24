import mysql.connector
from mysql.connector import Error


class Customer():
    def __init__(self, data):
        self.custDataObj = CustomerDB(data)

    def add(self):
        return self.custDataObj.addDB("aroijang", "ordert")

    def delete(self):
        return self.custDataObj.deleteDB("aroijang", "ordert")

    def updateOrderStatus(self):
        return self.custDataObj.updateOrderStatusDB("aroijang")

    def getInfo(self):
        return self.custDataObj.data
    def searchOrderByCustomerID(self):
        return self.custDataObj.searchOrderByCustomerID("aroijang")

class CustomerDB():

    def __init__(self, data):
        self.data = data
        self.user = 'puttimeth'
        self.password = '123456'

    def addDB(self, databasename, table):
        # have to check
        # there is cid, did, pdid+quantity at least 1
        # 1. cid have reference key
        # 2. pdid have reference key and quality is positive
        # 3. pid have reference key
        # 4. did have reference key
        wdata = self.data

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database=databasename,
                                                 user=self.user,
                                                 password=self.password)
            
            cursor = connection.cursor()
            # check
            if wdata[0] == '':
                retmsg = ["1","customer id cannot be blank"]
                return
            if wdata[1] == []:                
                retmsg = ["1","product must have at least 1"]
                return
            if wdata[2] == '':                
                retmsg = ["1","deliveryman id cannot be blank"]
                return
            # check 1
            checkQuery = "select * from customer where cid=%s"            
            cursor.execute(checkQuery,(wdata[0],))
            myresult = cursor.fetchall()
            if myresult == []:
                retmsg = ["1","customer id is not found"]
                return
            # check 2
            for i,j in wdata[1]:
                checkQuery = "select * from product where pdid=%s"
                cursor.execute(checkQuery,(i,))
                myresult = cursor.fetchall()
                if myresult == []:
                    retmsg = ["1","product id is not found"]
                    return
            # check 3
            for i in wdata[2]:
                checkQuery = "select * from promotion where pid=%s"
                cursor.execute(checkQuery,(i,))
                myresult = cursor.fetchall()
                if myresult == []:
                    retmsg = ["1","promotion id is not found"]
                    return
            # check 4
            checkQuery = "select * from deliveryman where did=%s"            
            cursor.execute(checkQuery,(wdata[3],))
            myresult = cursor.fetchall()
            if myresult == []:
                retmsg = ["1","deliveryman id is not found"]
                return
                        
            query = "insert into ordert (cid,did) values (%s,%s)"
            cursor.execute(query,(wdata[0],wdata[3]))
            query = "select last_insert_id()"
            cursor.execute(query)            
            myresult = cursor.fetchall()            
            odid = myresult[0][0]
            print("insert ordert complete")
            
            restaurant_set = set()
            for i,j in wdata[1]:
                print(odid,i,j)
                query = "insert into order_have_product (odid,pdid,ohpdquantity) values (%s,%s,%s)"
                cursor.execute(query,(odid,i,j))
                query = "select rid from product where pdid=%s"
                cursor.execute(query,(i,))
                myresult = cursor.fetchall()
                rid = myresult[0][0]
                print("insert order_have_product complete")
                
                if rid not in restaurant_set:
                    print(rid,odid)
                    query = "insert into receive_order(rid,odid) values (%s,%s)"
                    cursor.execute(query,(rid,odid))
                    restaurant_set.add(rid)
                    print("insert receive_order complete")
                
            for i in wdata[2]:
                print(odid,i)
                query = "insert into order_use_promotion (odid,pid) values (%s,%s)"
                cursor.execute(query, (odid,i))
                print("insert order_use_promotion complete")
                
            query = 'select calculateTotalPrice(%s)'
            cursor.execute(query, (odid,))
            myresult = cursor.fetchall()
            total_price = myresult[0][0]
            
            query = "insert into transaction (tbalance,odid) values (%s,%s)"
            cursor.execute(query, (total_price, odid))
            print("insert transaction complete")
            
            connection.commit()

        except Error as e:            
            retmsg = ["1", "add error"]
        else:
            retmsg = ["0", "add done"]
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
            return retmsg

    ##########################################################################

    def deleteDB(self, databasename, table):
        # check
        # 1. order id is found
        
        wdata = self.data[0]

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database=databasename,
                                                 user=self.user,
                                                 password=self.password)
            
            objdata = (wdata,)
            cursor = connection.cursor()
            # check 1
            checkQuery = "select * from ordert where odid=%s"            
            cursor.execute(checkQuery, objdata)            
            myresult = cursor.fetchall()
            if myresult == []:
                retmsg = ["1","order id is not found"]
                return
            
            sqlQuery = "delete from " + table + " where odid = %s"
            cursor.execute(sqlQuery, objdata)
            connection.commit()

        except:
            retmsg = ["1", "Delete Error"]
        else:
            retmsg = ["0", "Delete Complete"]
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
            return retmsg

    ##########################################################################

    def updateOrderStatusDB(self, databasename):
        # check
        # 1. order id is found
        
        wdata = self.data

        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database=databasename,
                                                 user=self.user,
                                                 password=self.password)
            
            cursor = connection.cursor()
            # check 1
            checkQuery = "select * from ordert where odid=%s"            
            cursor.execute(checkQuery, (wdata[0],))            
            myresult = cursor.fetchall()
            if myresult == []:
                retmsg = ["1","order id is not found"]
                return
            
            objdata = (wdata[0],wdata[1])
            print(objdata)
            sqlQuery = "call UpdateOrderStatus(%s,%s)"
            cursor.execute(sqlQuery, objdata)
            connection.commit()

        except:
            retmsg = ["1", "Update Error"]
        else:
            retmsg = ["0", "Update Complete"]
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
            return retmsg

    def searchOrderByCustomerID(self,databasename):
        wdata = self.data[0]
        try:
            connection = mysql.connector.connect(host='localhost',
                                                 database=databasename,
                                                 user=self.user,
                                                 password=self.password)
            
            objdata = (wdata,)         
            cursor = connection.cursor()
            cursor.callproc("searchCustomerID",objdata)
            myresult = []
            for result in cursor.stored_results():
                a=result.fetchall()
                myresult.append(a)
            if myresult == []:
                retmsg = ["1","customer id is not found"]
                return  
            connection.commit()     
        except Error as e:
            retmsg = ["1", None]
        else:
            retmsg = ["0", myresult]
        finally:
            if (connection.is_connected()):
                connection.close()
                cursor.close()
            return retmsg