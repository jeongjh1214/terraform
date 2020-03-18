#!/bin/python3

import sys
import boto3
from twisted.internet import threads, defer, reactor


def proc1(a):
    while True:
        print ("Proc----------1")

def proc2(a):
    while True:
        print ("Proc----------2")

def proc3(a):
    while True:
        print ("Proc----------3")

#d1 = threads.deferToThread(proc1)
#d2 = threads.deferToThread(proc2)
#d3 = threads.deferToThread(proc3)
#
#reactor.run()

d1 = defer.Deferred()
d2 = defer.Deferred()
d3 = defer.Deferred()

d1.addCallback(proc1)
d2.addCallback(proc2)
d3.addCallback(proc3)

d1.callback('a')
d2.callback('a')
d3.callback('a')

reactor.run()
