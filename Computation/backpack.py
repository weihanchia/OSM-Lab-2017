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
