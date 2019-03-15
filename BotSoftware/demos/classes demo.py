"""
Demos classes exchanging info with each other using a separate 'Info' class
"""


class Info:
    def __init__(self):
        self.info1 = 1
        self.info2 = 'something else'
        print('initialised')


class MainFrame:
    def __init__(self):
        a = Info()
        print('MainF: ', a.info1)
        b = Page1(a)
        c = Page2(a)
        print('MainF: ', a.info1)


class Page1:
    def __init__(self, information):
        self.info = information
        self.info.info1 = 3


class Page2:
    def __init__(self, information):
        self.info = information
        print('Page2: ', self.info.info1)


t = MainFrame()
