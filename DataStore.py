# DataStore.py

import random

class DataStoreProcess:
    def __init__(self, node_id, process_id):
        self.id = f'Node{node_id}-PS{process_id}'
        self.predecessor = None
        self.successor = None
        self.head = False
        self.tail = False
        self.books = {}

class Chain:
    def __init__(self):
        self.head = None
        self.tail = None
        self.processes = []

    def create_chain(self, data_store_processes):
        random.shuffle(data_store_processes)
        for i, process in enumerate(data_store_processes):
            if i == 0:
                process.head = True
                self.head = process
            else:
                process.predecessor = data_store_processes[i - 1]

            if i == len(data_store_processes) - 1:
                process.tail = True
                self.tail = process
            else:
                process.successor = data_store_processes[i + 1]

            self.processes.append(process)

