from random import random


class Captor():
    id = 2
    def Captor():
        self.id = 2
        

    def callback(self):
        try :
            f = open('randomWalk', 'r')
            prev = int(f.read())
            f.close()
        except:
            prev = 50

        new = prev + random()*100 - 50
        if new < 0 :
            new = 0
        elif new > 100:
            new = 100

        try:
            f = open('randomWalk', 'w')
            f.write(new)
            f.close()
        except:
            pass
        
        return new
    
    def getId(self):
        return self.id
