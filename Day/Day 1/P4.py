#Concept : Class and Instance 

class Cat:
    def __init__(self,name):
        self.name = name
    def mew(self):
        print("Meowww")

my_cat = Cat("MaoMao")
my_cat.mew()