def hello():
    print('--> Hello world')


def hello2():
    print('--> Hello world2')


def main(*args, **kwargs):
    print('This is main app! And I will say \"Hello world\":')
    hello()
    print("Bye!")
