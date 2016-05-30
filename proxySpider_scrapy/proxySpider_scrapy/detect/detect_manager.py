#coding:utf-8
from threading import Thread
import time

from proxySpider_scrapy.db.db_helper import DB_Helper
from proxySpider_scrapy.detect.detect_proxy import Detect_Proxy

'''
定义一个管理线程,来管理产生的线程
'''
class Detect_Manager(Thread):

    def __init__(self,threadSum):
        Thread.__init__(self)
        sqldb = DB_Helper()#将序号重新恢复
        sqldb.updateID()
        self.pool =[]
        for i in range(threadSum):
            self.pool.append(Detect_Proxy(DB_Helper(),i+1,threadSum))


    def run(self):
        self.startManager()
        self.checkState()


    def startManager(self):
        for thread in self.pool:
            thread.start()

    def checkState(self):
        '''
        这个函数是用来检测线程的状态
        :return:
        '''
        now = 0
        while now < len(self.pool):
            for thread in self.pool:
                if thread.isAlive():
                    now = 0
                    break
                else:
                    now+=1
            time.sleep(0.1)
        goodNum=0
        badNum =0
        for i in self.pool:

            goodNum += i.goodNum
            badNum += i.badNum
        sqldb = DB_Helper()#将序号重新恢复
        sqldb.updateID()
        print 'proxy good Num ---',goodNum
        print 'proxy bad Num ---',badNum







