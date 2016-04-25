#!/usr/bin/python3.4
# -*-coding:Utf-8 -*

class Point:

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, obj):
        x = self.x + obj.x
        y = self.y + obj.y
        return Point(x, y)

    def printF(self):
        print("%s, %s" % (self.x, self.y))

a = Point(2, 4)
b = Point(3, 6)
c = Point()

a.printF()
b.printF()
c.printF()

c = a+b

c.printF()
