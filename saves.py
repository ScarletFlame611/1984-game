import global_peremen


def save():
    with open('data\saves.txt', 'a', newline='') as save:
        if global_peremen.NAME != '':
            save.write(str(global_peremen.WIDTH) + '/')
            save.write(str(global_peremen.HIGH) + '/')
            save.write(str(global_peremen.NAME) + '\n')


def load(id):
    try:
        with open('data\saves.txt', 'r', newline='') as load:
            loads = load.readlines()
            if id <= len(loads):
                return loads[id - 1]
            return None
    except NameError:
        print('нет такого файла')


def all_saves():
    try:
        with open('data\saves.txt', 'r', newline='') as load:
            return load.readlines()
    except NameError:
        print('нет такого файла')


def clear():
    with open('data\saves.txt', 'w', newline=''):
        pass
