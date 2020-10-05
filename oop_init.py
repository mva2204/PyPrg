
class Person:
    def __init__(self, name):
        self.name = name

    def say_hi(self):
        print('Привет! Меня зовут {0}!'.format(self.name))



p = Person('Вадим')
p.say_hi()
