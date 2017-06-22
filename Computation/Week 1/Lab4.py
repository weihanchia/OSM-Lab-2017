#OOP Lab Classes

import math

class Backpack(object):

    def __init__(self,name,color,maxsize=5):
        self.name = name
        self.color= color
        self.maxsize = maxsize
        self.contents = []

    def put(self,item):
        if len(self.contents) < self.maxsize:
            self.contents.append(item)
        else:
            print("No Room!")

    def take(self,item):
        self.contents.remove(item)

    def dump(self):
        self.contents = []

class Jetpack(Backpack):

    def __init__(self,name,color,maxsize=2,fuel=10):
        Backpack.__init__(self,name,color,maxsize)
        self.fuel = fuel

    def fly(self,dist):
        if self.fuel - dist >= 0:
            self.fuel = self.fuel - dist
            print("You flew " +str(dist)+ "!")
        else:
            print("Not enough Fuel")

    def dump(self):
        self.contents = []
        self.fuel = 0

    def __eq__(self, other):
        return self.name == other.name and len(self.contents) == len(other.contents) and self.color == other.color

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "Owner:\t"+ self.name + "\nColor:\t" +self.color+  "\nSize: \t"+ str(len(self.contents)) + "\nMax Size:\t" + str(self.maxsize) + "\nContents:\t" + str(self.contents)

class Complex(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return Complex(self.real, -self.imag)

    def __abs__(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __lt__(self, other):
        return abs(self) < abs(other)

    def __gt__(self, other):
        return abs(self) > abs(other)

    def __eq__(self, other):
        return self.real ==other.real and self.imag == other.imag

    def __ne__(self, other):
        return not self == other

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return Complex(real, imag)

    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return Complex(real, imag)

    def __mul__(self, other):
        real = self.real * other.real - self.imag * other.imag
        imag = self.imag * other.real + other.imag * self.real
        return Complex(real, imag)

    def __truediv__(self, other):
        if other.real == 0 and other.imag == 0:
            raise ValueError("Cannot divide by zero!!")
        bottom = (other.conjugate()*other*1.).real
        top = self * other.conjugate()
        return Complex(top.real / bottom, top.imag / bottom)

    def __str__(self):
        return"{}{}{}i".format(self.real, '+' if self.imag >= 0 else '-',
                               abs(self.imag))
