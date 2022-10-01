#fishing

# -*-coding: utf-8 -*-
import os
import random
from collections import defaultdict
from multiprocessing import Process, Pipe, Queue
from queue import Empty

FISH = [None, 'плотва', 'окунь', 'лещ']

def fishing(name, worms):
    print(f'{name} parent process:', os.getppid())
    print(f'{name} process id:', os.getpid())
    catch = defaultdict(int)

    for worm in range(worms):
        print(f'{name} Червяк номер {worm} - забросил, ждём...', flush=True)
        fish = random.choice(FISH)
        if fish is None:
            _ = 3 ** (10000 * random.randint(70, 100))
            print(f'Тьфу!У {name} Сожрали червяка', flush=True)
        else:
            print(f'Ура!! У меня {fish}', flush=True)
            catch[fish] += 1
        print(f'Итого, рыбак {name} поймал')
        for name_fish, count in catch.items():
            print(f'{name_fish} - {count}')

class Fisher(Process):
    def __init__(self, name, worms, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.worms = worms

    def run(self):
        catch = defaultdict(int)

        for worm in range(self.worms):
            print(f'{self.name} Червяк номер {worm} - забросил, ждём...', flush=True)
            _ = 3 ** (10000 * random.randint(70, 100))
            fish = random.choice(FISH)
            if fish is None:
                print(f'Тьфу!У {self.name} Сожрали червяка', flush=True)
            else:
                print(f'Ура!! У меня {fish}', flush=True)
                catch[fish] += 1
        print(f'Итого, рыбак {self.name} поймал')
        for name_fish, count in catch.items():
            print(f'{name_fish} - {count}')

#
# if __name__ == '__main__':

    # fisher_1 = Fisher('Vasya', 10)
    # fisher_2 = Fisher('Kolya', 10)
    # fisher_1.start()
    # fisher_2.start()
    # fisher_1.join()
    # fisher_2.join()

#добавим функционал, добавим лодку, будем управлять процессами родительскими
# и дочками
class Fisher(Process):
    def __init__(self, name, worms, fish_receiver, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.worms = worms
        self.fish_receiver = fish_receiver
    def run(self):
        for worm in range(self.worms):
            print(f'{self.name} Червяк номер {worm} - забросил, ждём...', flush=True)
            _ = 3 ** (10000 * random.randint(70, 100))
            fish = random.choice(FISH)
            if fish is None:
                print(f'У меня съели червя {self.name}', flush=True)
            else:
                print(f'{self.name} поймал {fish} и хочет положить в садок')
                if self.fish_receiver.full():
                    print(f'{self.name} садок полон')
                self.fish_receiver.put(fish)
                print(f'{self.name} наконец-то положил')


class Boat(Process):

    def __init__(self, worms_per_fisher, humans, *args, **kwargs):
        super().__init__(*args,**kwargs)
        self.fishers = []
        self.worms_per_fisher = worms_per_fisher
        self.fish_receiver = Queue(maxsize=2)
        self.fish_tank = defaultdict(int)
        self.humans = humans

    def run(self):
        print('Лодка вышла в море', flush=True)
        for name in self.humans:
            fisher = Fisher(name=name, worms=self.worms_per_fisher, fish_receiver=self.fish_receiver)
            self.fishers.append(fisher)
        for fisher in self.fishers:
            fisher.start()
        while True:
            try:
                fish = self.fish_receiver.get(timeout=1)
                print(f'садок принял {fish}',flush=True)
                self.fish_tank[fish] += 1
            except Empty:
                print(f'В садке пусто в течении 1 секунды', flush=True)
                if not any(fisher.is_alive() for fisher in self.fishers):
                    break
        for fisher in self.fishers:
            fisher.join()
            print(f'Лодка возвращается домой с {self.fish_tank}', flush=True)

if __name__ == '__main__':

    boat = Boat(worms_per_fisher=10, humans=['Васек', 'Колян', 'Петрович', 'Хмурый', 'Клава', ])
    boat.start()
    boat.join