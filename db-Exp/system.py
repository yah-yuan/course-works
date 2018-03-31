# !/usr/bin/python
# -*- coding: UTF-8 -*-

'''
数据库大作业:图书馆图书管理系统
创建时间:Wed Dec 27 20:26:52 CST 2017
作者:张
注释:
注释 ①
    一个标准的时间戳格式: 2017-12-28 00:45:01
注释 ②
    使用更新\新增方法: 实例化一个需要更新\新增的表项的类,作为参数调用该方法
'''

import sys
import MySQLdb
from prettytable import PrettyTable

class DBcontroler(object):
    '''db的连接对象,完成与db的通信'''
    connect = None
    cursor = None

    def __init__(self):
        try:
            connect = MySQLdb.connect(host='localhost',user='yahweh',passwd='veritas',port=3306, charset='utf8')
            cursor = connect.cursor()
        except Exception,e:
            print e
            sys.exit()
        self.connect = connect
        self.connect.select_db('bookManager')
        self.cursor = cursor
    pass

    def Search(self, sql, param):
        '''查询之类的需要返回内容的操作'''
        try:
            if not self.cursor.execute(sql,param):
                return False
        except Exception,e:
            print e
            sys.exit()
        finally:
            return self.cursor.fetchall()

    def Execute(self, sql, param):
        '''改变数据库状态但不需要返回内容的操作'''
        try:
            if not self.cursor.execute(sql, param):
                return False
            self.connect.commit()
            return True
        except Exception,e:
            print e
            sys.exit()

class Book(object):
    '''书籍信息'''
    bookID = ''
    bookName = ''
    author = ''
    publisher = ''
    total = 0
    onShelf = 0
    type = ''
    location = ''

    def __init__(self, book):
        self.bookID = book[0]
        self.bookName = book[1]
        self.author = book[2]
        self.publisher = book[3]
        self.total = book[4]
        self.onShelf = book[5]
        self.type = book[6]
        self.location = book[7]

    def List(self):
        return [self.bookID,self.bookName,self.author,\
            self.publisher,self.total,self.onShelf,self.type,self.location]

    @staticmethod
    def Segment():
        return ['bookID','bookName','author',\
         'publisher','total','onShelf','type','location']



class BorrowInfo(object):
    '''借阅信息'''
    infoID = 0
    readerID = ''
    bookID = ''
    borrowTime = ''
    deadline = ''
    returnTime = ''
    returned = False

    def __init__(self, borrowInfo):
        self.infoID = borrowInfo[0]
        self.readerID = borrowInfo[1]
        self.bookID = borrowInfo[2]
        self.borrowTime = borrowInfo[3]
        self.deadline = borrowInfo[4]
        self.returnTime = borrowInfo[5]
        self.returned = borrowInfo[6]
    
    @staticmethod #装饰器,静态方法
    def Segment():
        return ['infoID','rederID','bookID',
            'borrowTime','deadLine','returnTime','returned']
    
    def List(self):
        return [self.infoID,self.readerID,self.bookID,self.borrowTime,self.deadline,self.returnTime,self.returned]

class ManageInfo(object):
    '''管理员行为'''
    infoID = 0
    managerID = ''
    bookID = ''
    amount = 0
    operate = ''
    timestamp = ''
    def __init__(self, info):
        self.infoID = info[0]
        self.managerID = info[1]
        self.amount = info[2]
        self.operate = info[3]
        self.timestamp = info[4]

class Public(object):
    '''读者和管理员的公用对象\公用方法'''
    '''操作表的方法统一写在这里,读者功能和管理员功能调用这些方法'''
    '''方法大部分用不到'''
    dbControler = None

    def __init__(self,dbControler):
        self.dbControler = dbControler

    def SearchBook(self, searchMessage):
        '''查找图书'''
        searchMessage = '%'+searchMessage+'%'
        sql = '''select * from book
                where bookName like %s or author like %s or publisher like %s or type like %s;'''
        param = (searchMessage,searchMessage,searchMessage,searchMessage,)
        books = self.dbControler.Search(sql,param)
        if not books:
            return False
        book_list = []
        for book in books:
            book_list.append(Book(book))
        return book_list


    def BorrowRank(self,timeLimit = ''):
        '''热门书籍榜'''
        if not timeLimit:
            sql = '''select * from bookRankingList'''
            param = ()
            result = self.dbControler.Search(sql,param)
            if not result:
                return False
            return result
        else:
            if self.dbControler.cursor.callproc('bookRankingList',(timeLimit,)):
                return self.dbControler.cursor.fetchall()
        pass

    def UserRank(self,timeLimit = ''):
        '''借阅排行榜'''
        if not timeLimit:
            sql = '''select * from readerRankingList'''
            param = ()
            result = self.dbControler.Search(sql,param)
            if not result:
                return False
            return result
        else:
            if self.dbControler.cursor.callproc('readerRankingList',(timeLimit,)):
                return self.dbControler.cursor.fetchall()
    
    def newBook(self):
        '''新书上架'''
        sql = '''select * from newBook'''
        param = ()
        result = self.dbControler.Search(sql,param)
        if not result:
            return False
        return result
        pass
        
class ManageSystem(object):
    '''管理系统实例,实例化后提供两种登录\一种注册方法'''
    currentReader = None
    currentManager = None
    public = None
    dbControler = None

    def __init__(self):
        self.dbControler = DBcontroler()
        self.public = Public(self.dbControler)
        pass
    
    def readerLogin(self,readerID,passwd):
        '''读者登录'''
        sql = '''select * from reader
                where readerID = %s and password = %s'''
        param = (readerID,passwd)
        result = self.dbControler.Search(sql,param)
        if not result:
            '''返回值是一个False,说明没有查到,登录失败'''
            return False
        result = result[0]
        self.currentReader = Reader(result,self.dbControler)
        return True

    def ManagerLogin(self, managerID, passwd):
        '''管理员登录'''
        sql = '''select * from manager
                where managerID = %s and password = %s'''
        param = (managerID, passwd)
        result = self.dbControler.Search(sql,param)
        if not result:
            '''返回值是一个False,说明没有查到,登录失败'''
            return False
        result = result[0]
        self.currentManager = Manager(result,self.dbControler)
        return True
    
    def ReaderRegist(self,passwd, readerName, telephone):
        '''读者注册'''
        # 生成一个userid,构造Reader实例
        # 现在将由触发器自动递增readerID
        sql = '''insert into reader (password,readerName,telephone) 
                value (%s,%s,%s); '''
        param = (passwd, readerName, telephone)
        if not self.dbControler.Execute(sql, param):
            return False
        # 注册成功后自动登录
        sql = '''select @@IDENTITY''' #返回刚刚注册的那个id
        param = ()
        readerID = self.dbControler.Search(sql,param)
        readerID = readerID[0][0]
        return readerID

class Reader(Public):
    '''读者对象'''
    '''读者模块,实例化需要一个登录成功的用户和已实例化的DBcontroller,成功实例化后提供读者可使用的功能'''
    readerID = 0
    passwd = ''
    readerName = ''
    telephone = ''
    banned = False

    def __init__(self, reader, dbControler):
        self.readerID = reader[0]
        self.passwd = reader[1]
        self.readerName = reader[2]
        self.telephone = reader[3]
        self.banned = bool(reader[4])
        self.dbControler = dbControler

    @staticmethod
    def Segment():
        return ('readerID', 'password', 'readerName', 'telephone', 'banned')

    def List(self):
        return (self.readerID,self.passwd,self.readerName,self.telephone,self.banned )

    def ChangeAccount(self, passwd, readerName, telephone):
        '''更改账户信息'''
        sql = '''update reader
                set password = %s,readerName = %s, telephone = %s
                where readerID = %s;'''
        param = (passwd,readerName,telephone,self.readerID)
        if not self.dbControler.Execute(sql,param):
            return False
        '''成功后更改账户当前信息'''
        self.passwd = passwd
        self.readerName = readerName
        self.telephone = telephone
        return True
    
    def BorrowRecords(self):
        '''查看的读者的借阅信息'''
        borrowInfo_list = []
        sql = '''select * from borrowInfo
                where readerID = %s;'''
        param = (str(self.readerID),)
        result = self.dbControler.Search(sql,param)
        if not result:
            return False
        for item in result:
            borrowInfo_list.append(BorrowInfo(item))
        # 查询成功后返回一个borrowInfo的list
        return borrowInfo_list

    def Borrow(self, bookID):
        '''借书'''
        sql = '''insert into borrowInfo (readerID,bookID)
                values (%s,%s)'''
        param = (str(self.readerID),str(bookID))
        if not self.dbControler.Execute(sql,param):
            return False
        sql = '''select @@IDENTITY''' #返回刚刚注册的那个id
        param = ()
        borrowInfoID = self.dbControler.Search(sql,param)
        borrowInfoID = borrowInfoID[0][0]
        sql = '''select * from borrowInfo
                where borrowInfoID = %s'''
        param = (borrowInfoID,)
        result = self.dbControler.Search(sql,param)
        if not result:
            return False
        result =result[0]
        borrowInfo = BorrowInfo(result)
        return borrowInfo

    def Return(self, bookID):
        '''还书'''
        # 同一本书能不能借两次?否则不知道还哪本?一次只能还一本?逻辑
        sql = '''select borrowInfoID from borrowInfo
                where bookID = %s and returned = 0'''
        borrowInfoID = self.dbControler.Search(sql,param)
        print borrowInfoID
        borrowInfoID = borrowInfoID[0][0]
        sql = '''update borrowInfo
                set returned = 1
                where borrowInfoID = %s;'''
        param = (str(borrowInfoID),)
        success = self.dbControler.Execute(sql,param)
        return success

class Manager(Public):
    '''管理员身份信息'''
    managerID = 0
    passwd = ''
    managerName = ''

    def __init__(self, manager, dbControler):
        if not isinstance(dbControler,DBcontroler):
            return False
        self.dbControler = dbControler
        self.managerID = manager[0]
        self.passwd = manager[1]
        self.managerName = manager[2]

    def BorrowRecords(self ,readerID):
        '''查看的读者的借阅信息'''
        borrowInfo_list = []
        sql = '''select * from borrowInfo
                where readerID = %s;'''
        param = (str(readerID),)
        result = self.dbControler.Search(sql,param)
        if not result:
            return False
        for item in result:
            borrowInfo_list.append(BorrowInfo(item))
        # 查询成功后返回一个borrowInfo的list
        return borrowInfo_list

    def AddNewBook(self, bookName,author,publisher, total, onShelf, type, location):
        '''新书籍入库'''
        if total != onShelf:
            return False
        sql = '''insert into book (bookName,author,publisher,type,location)
                values (%s,%s,%s,%s,%s);'''
        param = (bookName,author,publisher,type,location,)
        if not self.dbControler.Execute(sql,param):
            return False
        sql = '''select @@IDENTITY'''
        param = ()
        book = self.dbControler.Search(sql,param)
        bookID = book[0][0]
        sql = '''insert into manageInfo (managerID,bookID,amount,operation)
                values (%s,%s,%s,%s)'''
        param = (str(self.managerID),str(bookID),str(total),'入库',)
        self.dbControler.Execute(sql,param)
        return bookID

    def AddOldBook(self, bookID, increment):
        '''新增一本旧书'''
        sql = '''insert into manageInfo (managerID,bookID,amount,operation)
                values (%s,%s,%s,%s);'''
        param = (self.managerID,bookID,increment,'入库',)
        if not self.dbControler.Execute(sql,param):
            return False
        return True

    def DeleteBook(self, bookID, decrement):
        '''销毁一本书'''
        # 销毁被借书?销毁在架书?
        sql = '''insert into manageInfo (managerID,bookID,amount,operation)
                values (%s,%s,%s,%s);'''
        param = (self.managerID,bookID,decrement,'出库',)
        if not self.dbControler.Execute(sql,param):
            return False
        return True

    def BanReader(self, readerID, banned = False):
        '''禁用/解禁一个用户'''
        banned = int(banned)
        sql = '''update reader
                set banned = %s
                where readerID = %s'''
        param = (banned, readerID,)
        if not self.dbControler.Execute(sql,param):
            return False
        return True

    def InvalidAcount(self):
        '''列表所有违约账户'''
        readers_list = []
        sql = '''select * from overdue;'''
        param = ()
        result = self.dbControler.Search(sql,param)
        if not result:
            return False
        readers_list = result
        return readers_list

def main():
    '''测试内容'''
    system = ManageSystem()
    if not system:
        print 'dbCon Failed'
    print '<--<--<--图书管理系统-->-->-->'
    public = system.public

    '''读者登录'''
    print '\n读者登录测试'
    if system.readerLogin('34','123456'):
        pass
    else:
        print '密码错误'
    print system.currentReader.readerName,'登录成功'
    reader = system.currentReader

    '''管理员登录'''
    print '\n管理员登录测试'
    if system.ManagerLogin('10000','123456'):
        pass
    else:
        print '密码错误'
        return False
    print system.currentManager.managerName,'登录成功'
    manager = system.currentManager

    '''读者注册测试'''
    # print '\n读者注册测试'
    # id = system.ReaderRegist('123456','Tony','18022011584')
    # if id:
    #     print '注册成功,用户id为:',id

    '''公开功能测试'''
    print '''\n<--<--<--公用功能测试-->-->-->'''

    '''借书榜查询'''
    # print '\n借书榜单查询'
    # result = public.UserRank('2017-10-01 00:00:01')
    # if result:
    #     table = PrettyTable(['readerID', 'readerName', 'sum'])
    #     for item in result:
    #         table.add_row(item)
    #     print table

    '''查找图书'''
    # searchMessage = ''
    # print '\n查找图书: ',searchMessage
    # book_list = public.SearchBook(searchMessage)
    # table = PrettyTable(Book.Segment())
    # if book_list:
    #     for item in book_list:
    #         table.add_row(item.List())
    #     print table
    # else:
    #     print '未找到该书'

    '''热门书籍榜查询'''
    # print '\n热门书籍查询'
    # result = public.BorrowRank('2017-10-01 00:00:01')
    # if result:
    #     table = PrettyTable(['bookID', 'bookName', 'sum'])
    #     for item in result:
    #         table.add_row(item)
    #     print table

    '''新书上架'''
    # print '\n新书上架'
    # result = public.newBook()
    # if result:
    #     table = PrettyTable(['bookID', 'bookName', 'type', 'sum'])
    #     for item in result:
    #         table.add_row(item)
    # print table

    '''读者功能测试'''
    print '\n<--<--<--读者功能测试-->-->-->'

    '''更改账户测试'''
    # print '\n更改账户测试'
    # reader.ChangeAccount('345678','大明','4323421')
    # print reader.readerName

    '''借阅'''
    # print '\n借阅'
    # borrowInfo = reader.Borrow('831')
    # if borrowInfo:
    #     table = PrettyTable(BorrowInfo.Segment())
    #     table.add_row(borrowInfo.List())
    #     print table

    '''还书'''
    # print '\n还书'
    # flag = reader.Return(831)
    # print flag

    '''借阅信息查询'''
    # print '\n我的借阅信息查询'
    # borrowInfo_list = reader.BorrowRecords()
    # if not borrowInfo_list:
    #     return False
    # table = PrettyTable(BorrowInfo.Segment())
    # for borrowInfo in borrowInfo_list:
    #     table.add_row(borrowInfo.List())
    # print table

    '''管理员功能测试'''
    print '<--<--<--管理员功能测试-->-->-->'

    '''新增图书'''
    # print '\n新增图书'
    # bookID = manager.AddNewBook('C语言程序设计基础','谭成予','武汉大学出版社',10,10,'计算机科学','B1')
    # print '新增书籍编号为:',bookID
    
    '''旧书新增'''
    # print '\n旧书新增'
    # if not manager.AddOldBook(833,1):
    #     return False
    # print True

    '''销毁书'''
    # print '\n销毁一本书'
    # if not manager.DeleteBook(825,2):
    #     return False
    # print True

    '''用户禁用'''
    # print '\n用户禁用'
    # print manager.BanReader(34,True)

    '''查看逾期账户'''
    # print '\n查看逾期账户'
    # result = manager.InvalidAcount()
    # table = PrettyTable(('borrowInfoID', 'readerID', 'readerName', 'telephone', 'bookName', 'overdueTime', 'banned'))
    # for item in result:
    #     table.add_row(item)
    # print table

    '''借阅信息查询'''
    # print '\n借阅信息查询'
    # borrowInfo_list = manager.BorrowRecords(34)
    # if not borrowInfo_list:
    #     return False
    # table = PrettyTable(BorrowInfo.Segment())
    # for borrowInfo in borrowInfo_list:
    #     table.add_row(borrowInfo.List())
    # print table

if __name__ == '__main__':
    main()