# solutions.py
import math
import numpy as np
import itertools

# Problem 1 Write unit tests for addition().
# Be sure to install pytest-cov in order to see your code coverage change.


def addition(a, b):
    return a + b


def smallest_factor(n):
    """Finds the smallest prime factor of a number.
    Assume n is a positive integer.
    """
    if n == 1:
        return 1
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return i
    return n


# Problem 2 Write unit tests for operator().
def operator(a, b, oper):
    if type(oper) != str:
        raise ValueError("Oper should be a string")
    if len(oper) != 1:
        raise ValueError("Oper should be one character")
    if oper == "+":
        return a + b
    if oper == "/":
        if b == 0:
            raise ValueError("You can't divide by zero!")
        return a/float(b)
    if oper == "-":
        return a-b
    if oper == "*":
        return a*b
    else:
        raise ValueError("Oper can only be: '+', '/', '-', or '*'")

# Problem 3 Write unit test for this class.
class ComplexNumber(object):
    def __init__(self, real=0, imag=0):
        self.real = real
        self.imag = imag

    def conjugate(self):
        return ComplexNumber(self.real, -self.imag)

    def norm(self):
        return math.sqrt(self.real**2 + self.imag**2)

    def __add__(self, other):
        real = self.real + other.real
        imag = self.imag + other.imag
        return ComplexNumber(real, imag)

    def __sub__(self, other):
        real = self.real - other.real
        imag = self.imag - other.imag
        return ComplexNumber(real, imag)

    def __mul__(self, other):
        real = self.real*other.real - self.imag*other.imag
        imag = self.imag*other.real + other.imag*self.real
        return ComplexNumber(real, imag)

    def __truediv__(self, other):
        if other.real == 0 and other.imag == 0:
            raise ValueError("Cannot divide by zero")
        bottom = (other.conjugate()*other*1.).real
        top = self*other.conjugate()
        return ComplexNumber(top.real / bottom, top.imag / bottom)

    def __eq__(self, other):
        return self.imag == other.imag and self.real == other.real

    def __str__(self):
        return "{}{}{}i".format(self.real, '+' if self.imag >= 0 else '-',
                                                                abs(self.imag))

# Problem 5: Write code for the Set game here

def load(hand):
    if type(hand) != str:
        raise TypeError("Wrong File Type")
    if hand.endswith('.txt'):
        with open(hand) as f:
            return f.read().rstrip("/n")
    else:
        raise TypeError("Wrong File Type")

def parse(hand):
    hand = load(hand)
    hand = str.split(hand)
    if len(hand) < 12:
        raise ValueError("Too Few Cards")
    elif len(hand) > 12:
        raise ValueError("Too Many Cards")
    for card in hand:
        test = list(card)
        test = [int(i) for i in test]
        if max(test) > 2 or min(test) < 0:
            raise ValueError("Wrong Cards")
    if len(hand) != len(set(hand)):
        raise ValueError("Duplicate Cards")
    return hand

def solver(hand):
    hand = parse(hand)
    combi = itertools.combinations(hand,3)
    combi = list(combi)
    result = 0
    for cards in combi:
        a = np.asarray([int(i) for i in list(cards[0])])
        b = np.asarray([int(i) for i in list(cards[1])])
        c = np.asarray([int(i) for i in list(cards[2])])
        res = a + b + c
        if res[0]%3 == 0 and res[1]%3 == 0 and res[2]%3 == 0 and res[3]%3 == 0:
            result += 1
    return(result)
