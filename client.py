#client.py

import grpc
import time
import BookStore_pb2
import BookStore_pb2_grpc
from tutorial import *
from config import *
import random

class BookStoreClient:
    def __init__(self):
        self.port = int(input("Enter the server port: "))
        self.init_client_data()
        self.access_to_server()
        self.process_ids_list = []

    def init_client_data(self):
        self.serverip = ip(self.port)
        self.reg_name = random.choice(nicknames)
        self.set_stub()

    def access_to_server(self):
        request = BookStore_pb2.AccessRequest()
        request.name = self.reg_name
        response = self.stub.access_to_server(request)
        self.id = response.id
        print(f"your id: {response.id} ")  
        return response
    
    def logout(self):
        req = BookStore_pb2.AccessRequest(name=self.reg_name)
        response = self.stub.logout(req)
        print(response.id)
        return response
    
    def set_stub(self):
        self.channel = grpc.insecure_channel(f'{self.serverip}:{self.port}')
        self.stub = BookStore_pb2_grpc.BookStoreStub(self.channel)

    def local_store_processes(self, k):
        self.process_ids_list.clear()
        request = BookStore_pb2.LocalStorePSRequest(k=k)
        response = self.stub.LocalStorePS(request)
        print(f"Created {k} local data store processes. Process IDs: {response.process_ids}")
        self.process_ids_list = list(response.process_ids)

    def create_chain(self):
        request = BookStore_pb2.CreateChainRequest(process_ids=self.process_ids_list)
        response = self.stub.CreateChain(request)
        print(f"Chain created with processes: {response.process_ids}")

    def list_chain(self):
        request = BookStore_pb2.ListChainRequest()
        response = self.stub.ListChain(request)
        print(f"Current chain: {response.chain}")

    def write_operation(self, book_name, price):
        request = BookStore_pb2.WriteOperationRequest(book=book_name, price=price)
        response = self.stub.WriteOperation(request)

    def list_books(self):
        request = BookStore_pb2.ListBooksRequest()
        response = self.stub.ListBooks(request)
        print("Available books:")
        for book in response.books:
            print(f"{book.name} = {book.price} EUR")

    def read_operation(self, book_name):
        request = BookStore_pb2.ReadOperationRequest(book=book_name)
        response = self.stub.ReadOperation(request)
        print(response.message)

    def set_timeout(self, timeout):
        request = BookStore_pb2.SetTimeoutRequest(timeout=timeout)
        response = self.stub.SetTimeout(request)
        print(response.message)
        

    def data_status(self):
        request = BookStore_pb2.DataStatusRequest()
        response = self.stub.DataStatus(request)
        print("Data item status:")
        for item in response.items:
            print(f"{item.name} - {item.status}")

    def remove_head(self):
        request = BookStore_pb2.RemoveHeadRequest()
        response = self.stub.RemoveHead(request)
        print(f"New chain: {response.process_ids}")

    def restore_head(self):
        request = BookStore_pb2.RestoreHeadRequest()
        response = self.stub.RestoreHead(request)
        print(response.message)


    def set_chain_all_nodes(self):
        response = self.stub.SetChainAllNodes()
        print(response.message) 
        
    def run(self):
        while True:
            command = input("Enter command: ")
            if command == "quit":
                self.logout()
                time.sleep(1)
                break
            elif command.startswith("local-store-ps") or command.startswith("01"):
                if " " not in command:
                    print("The command is missing an argument. How many process?")
                else:
                    k = int(command.split(" ")[1])
                    self.local_store_processes(k)
            elif command == "create-chain" or command == "02" :
                self.create_chain()
            elif command == "020" :
                self.create_chain()
            elif command == "list-chain" or command == "03" :
                self.list_chain()
            elif command.startswith("write-operation") or command.startswith("04"):
                if " " not in command:
                    print("The command is missing an argument. How many process?")
                else:
                    book_name = command.split(" ")[1]
                    price = float(command.split(" ")[2])
                    self.write_operation(book_name, price)
            elif command == "list-books" or command == "05" :
                self.list_books()
            elif command.startswith("read-operation") or command.startswith("06"):
                if " " not in command:
                    print("The command is missing an argument. How many process?")
                else:
                    book_name = command.split(" ")[1]
                    self.read_operation(book_name)
            elif command.startswith("time-out") or command.startswith("07"):
                if " " not in command:
                    print("The command is missing an argument. what is your time?")
                else:
                    timeout = int(command.split(" ")[1])
                    self.set_timeout(timeout)
            elif command == "data-status" or command == "08" :
                self.data_status()
            elif command == "remove-head" or command == "09" :
                self.remove_head()
            elif command == "restore-head" or command == "10" :
                self.restore_head()
            else:
                print("invalid command try again")
            
        client.logout()

if __name__ == "__main__":
    bookstore_welcome()
    client = BookStoreClient()
    try:
        client.run()
    except KeyboardInterrupt:
        client.logout()
