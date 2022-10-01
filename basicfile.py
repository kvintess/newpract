#fishing

# -*-coding: utf-8 -*-
import os
import random
from collections import defaultdict
from multiprocessing import Process, Pipe, Queue
from Queue import empty

FISH = [None, 'плотва', 'окунь', 'лещ']

def fishing(name, worms):
    print(f'{name} parent process:', os.getppid())
    print(f'{name} process id:', os.getpid())
    catch = defaultdict(int)

    for worm in worms:
        print(f'{name} Червяк номер {worm} - забросил, ждём...', flush=true)
        _ = 3 ** (10000 * random.randint(70, 100))
        fish = random.choice(FISH)