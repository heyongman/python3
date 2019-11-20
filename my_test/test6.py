print("1")


def my_fun():
    print("22")


class MyClass:
    def __init__(self):
        print("init")
    my_fun()
    print("11")


print("2")
my_class = MyClass()
print("3")

