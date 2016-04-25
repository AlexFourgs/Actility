#!/usr/bin/python3.4
# -*-coding:utf8 -*

# Simple programme pour tester une fonciton lambda

f = lambda x:x * x
g = lambda x, y: x + y
a = f(5)
print("5 au carre = ", a)
print("2 + 3 = %d", g(2, 3))
