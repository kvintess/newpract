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


if __name__ == '__main__':

    fisher_1 = Fisher('Vasya', 10)
    fisher_2 = Fisher('Kolya', 10)
    fisher_1.start()
    fisher_2.start()
    fisher_1.join()
    fisher_2.join()