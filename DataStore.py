# DataStore.py

import random

class DataStoreProcess:
    def __init__(self, node_id, process_id, books=None):
        self.node_id = node_id
        self.process_id = process_id
        self.id = f'Node{node_id}-PS{process_id}'
        self.predecessor = None
        self.successor = None
        self.head = False
        self.tail = False
        self.books = books if books else {}

class Book:
    def __init__(self, name, price):
        self.name = name
        self.price = price
    

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

    def list_books(self):
        for book_name, price in self.processes[0].books.items():
                self.books.append(Book(name=book_name, price=price))
        return self.books

    def read_operation(self, book_name):
        for process in self.processes:
            if book_name in process.books:
                return process.books[book_name]
        return "Not yet in the stock"

    def set_timeout(self, timeout):
        for process in self.processes:
            process.timeout = timeout

    def data_status(self):
        status = []
        for process in self.processes:
            for book, state in process.book_status.items():
                status.append(f"{book} - {state}")
        return status

    def remove_head(self):
        if not self.head:
            return "Chain is empty"
        self.processes.remove(self.head)
        self.head = self.head.successor
        self.head.head = True
        self.processes[0].head = True
        return f"{self.processes[0].id} (Head) -> {' -> '.join([process.id for process in self.processes[1:]])} (Tail)"

    def restore_head(self):
        if not self.head:
            return "Chain is empty"
        if not self.head.successor:
            return "Chain has only one process"
        restored_head = self.head
        deviation = 0
        while restored_head.successor != self.tail:
            restored_head = restored_head.successor
            deviation += 1
        if deviation > 5:
            self.processes.remove(self.head)
            self.head = self.head.successor
            self.head.head = True
            self.processes[0].head = True
            return "Restored head permanently deleted"
        else:
            restored_head.successor = self.head
            self.head.predecessor = restored_head
            self.head = restored_head
            self.head.head = True
            self.processes[0].head = False
            return self.processes[0].id

    def write_operation(self, book_name, price):
        if self.tail is None:
            self.tail = self.processes[-1]
        for process in self.processes:
            if book_name in process.books:
                process.books[book_name] = price
                return f"{book_name} updated to {price} EUR"
        self.tail.books[book_name] = price
        return f"{book_name} added to the book store with price {price} EUR"

   