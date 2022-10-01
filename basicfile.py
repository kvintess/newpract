#fishing

# -*-coding: utf-8 -*-
import os
import random
from collections import defaultdict
from multiprocessing import Process, Pipe, Queue
from Queue import empty

Fish = [None, 'плотва', 'окунь', 'лещ']