import grpc
import time
import BookStore_pb2
import BookStore_pb2_grpc
from tutorial import *

class BookStoreClient:
    def __init__(self):
        self.port = input("Enter the server port: ")
        self.init_client_data()

    def init_client_data(self):
        self.serverip = "localhost"
        self.set_stub()

    def set_stub(self):
        self.channel = grpc.insecure_channel(f'{self.serverip}:{self.port}')
        self.stub = BookStore_pb2_grpc.BookStoreStub(self.channel)

    def local_store_processes(self, k):
        request = BookStore_pb2.LocalStorePSRequest(k=k)
        response = self.stub.LocalStorePS(request)
        print(f"Created {k} local data store processes. Process IDs: {response.process_ids}")

    def create_chain(self):
        request = BookStore_pb2.CreateChainRequest()
        response = self.stub.CreateChain(request)
        print(f"Chain created with processes: {response.process_ids}")

    def list_chain(self):
        request = BookStore_pb2.ListChainRequest()
        response = self.stub.ListChain(request)
        print(f"Current chain: {response.process_ids}")

    def write_operation(self, book_name, price):
        request = BookStore_pb2.WriteOperationRequest(book_name=book_name, price=price)
        response = self.stub.WriteOperation(request)
        print(response.message)

    def list_books(self):
        request = BookStore_pb2.ListBooksRequest()
        response = self.stub.ListBooks(request)
        print("Available books:")
        for book in response.books:
            print(f"{book.name} = {book.price} EUR")

    def read_operation(self, book_name):
        request = BookStore_pb2.ReadOperationRequest(book_name=book_name)
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

    # Define other methods for other commands here

    def run(self):
        while True:
            command = input("Enter command: ")
            if command == "quit":
                break
            elif command.startswith("local-store-ps"):
                k = int(command.split(" ")[1])
                self.local_store_processes(k)
            elif command == "create-chain":
                self.create_chain()
            elif command == "list-chain":
                self.list_chain()
            elif command.startswith("write-operation"):
                book_name = command.split(" ")[1]
                price = float(command.split(" ")[2])
                self.write_operation(book_name, price)
            elif command == "list-books":
                self.list_books()
            elif command.startswith("read-operation"):
                book_name = command.split(" ")[1]
                self.read_operation(book_name)
            elif command.startswith("time-out"):
                timeout = int(command.split(" ")[1])
                self.set_timeout(timeout)
            elif command == "data-status":
                self.data_status()
            elif command == "remove-head":
                self.remove_head()
            elif command == "restore-head":
                self.restore_head()

if __name__ == "__main__":
    bookshop_welcome()
    client = BookStoreClient()
    client.run()
