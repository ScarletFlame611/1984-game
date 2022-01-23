import global_peremen


class Saves_error(Exception):
    pass


try:
    def save():
        with open('data\saves.txt', 'a', newline='') as save:
            if global_peremen.NAME != '':
                for elem in global_peremen.levels:
                    save.write(str(elem) + ':' + str(global_peremen.levels[elem]) +',')
                save.write(str(global_peremen.NAME) + '\n')


    def load(id):
        try:
            with open('data\saves.txt', 'r', newline='') as load:
                loads = load.readlines()
                if id <= len(loads):
                    return loads[id - 1][:-1]
                return None
        except NameError:
            print('нет такого файла')


    def all_saves():
        try:
            with open('data\saves.txt', 'r', newline='') as load:
                return load.readlines()
        except NameError:
            print('нет такого файла')


    def delete(id):
        with open('data\saves.txt', 'r', newline='') as load:
            loads = load.readlines()
        with open('data\saves.txt', 'w', newline='') as load:
            for i in range(len(loads)):
                if i != id - 1:
                    load.write(loads[i])


    def clear():
        with open('data\saves.txt', 'w', newline=''):
            pass
except:
    raise Saves_error()