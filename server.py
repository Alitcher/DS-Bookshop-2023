# server.py

import grpc
from concurrent import futures
import time
import BookStore_pb2
import BookStore_pb2_grpc
from DataStore import DataStoreProcess, Chain
from config import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class BookStoreService(BookStore_pb2_grpc.BookStoreServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.chain = Chain()
        self.local_data_store_processes = []

    def LocalStorePS(self, request, context):
        k = request.k
        for i in range(1, k + 1):
            process = DataStoreProcess(self.node_id, i)
            self.local_data_store_processes.append(process)
        process_ids = [process.id for process in self.local_data_store_processes]
        return BookStore_pb2.LocalStorePSResponse(process_ids=process_ids)

    def CreateChain(self, request, context):
        self.chain.create_chain(self.local_data_store_processes)
        process_ids = [process.id for process in self.chain.processes]
        return BookStore_pb2.CreateChainResponse(process_ids=process_ids)

    def ListChain(self, request, context):
        process_ids = [process.id for process in self.chain.processes]
        response = " -> ".join(process_ids)
        return BookStore_pb2.ListChainResponse(chain=response)

    def WriteOperation(self, request, context):
        book_name = request.book_name
        price = request.price
        response = self.chain.write_operation(book_name, price)
        return BookStore_pb2.WriteOperationResponse(message=response)

    def ListBooks(self, request, context):
        books = self.chain.list_books()
        response = "\n".join([f"{i+1}) {book}" for i, book in enumerate(books)])
        return BookStore_pb2.ListBooksResponse(books=response)

    def ReadOperation(self, request, context):
        book_name = request.book_name
        response = self.chain.read_operation(book_name)
        return BookStore_pb2.ReadOperationResponse(price=response)

    def TimeOut(self, request, context):
        timeout = request.timeout
        self.chain.set_timeout(timeout)
        return BookStore_pb2.TimeOutResponse(message=f"Timeout set to {timeout} seconds.")

    def DataStatus(self, request, context):
        status = self.chain.data_status()
        response = "\n".join([f"{i+1}) {book} - {stat}" for i, (book, stat) in enumerate(status.items())])
        return BookStore_pb2.DataStatusResponse(data=response)

    def RemoveHead(self, request, context):
        self.chain.remove_head()
        return BookStore_pb2.RemoveHeadResponse(message="Head removed.")

    def RestoreHead(self, request, context):
        head = self.chain.restore_head()
        return BookStore_pb2.RestoreHeadResponse(message=f"Head restored to {head.id}.")

def serve():
    node_id = get_node_id()
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    BookStore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreService(node_id), server)
    server.add_insecure_port(f'[::]:{node_id}')
    server.start()

    print(f'Starting server. Listening on port {node_id}.')
    server.wait_for_termination()


if __name__ == "__main__":
    serve()