# -*- coding: UTF-8 -*-
'''
Created on 2017年5月15日

@author: Administrator
'''

 
import thread
import time
 
# 为线程定义一个函数
def print_time( threadName, delay):
    count = 0
    while count < 5:
        time.sleep(delay)
        count += 1
        print "%s: %s" % ( threadName, time.ctime(time.time()) )
 
# 创建两个线程
try:
    thread.start_new_thread( print_time, ("Thread-1", 2, ) )
    thread.start_new_thread( print_time, ("Thread-2", 4, ) )
    thread.start_new_thread( print_time, ("Thread-3", 6, ) )
    thread.start_new_thread( print_time, ("Thread-4", 8, ) )
    thread.start_new_thread( print_time, ("Thread-4", 8, ) )
    
except:
    print "Error: unable to start thread"
    
while 1:
    pass