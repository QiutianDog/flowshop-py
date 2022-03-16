from modele.factory import *

if __name__ == '__main__':
    factory = Factory()
    factory.load_data('./a.txt')
    # factory.generate_data(3, 4)
    # factory.complete([0, 1, 2])
    # factory.save_data('./a.txt')

    print(factory.machines)
