#server.py

import grpc
from grpc import StatusCode
from concurrent import futures
import time
import BookStore_pb2
import BookStore_pb2_grpc
from DataStore import DataStoreProcess, Chain, Book
from config import *

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

nodes_in_server = [None] * 3
nodes_active = [False] * 3
bode_count = 0
port1 = 0

class BookStoreService(BookStore_pb2_grpc.BookStoreServicer):
    def __init__(self, node_id):
        self.node_id = node_id
        self.chain = Chain()
        self.local_data_store_processes = []

    def access_to_server(self, request, context):
        print(f"client-{request.name} has joined the server!")
        return BookStore_pb2.AccessResponse(id = f"{request.name}{self.node_id}")
    
    def logout(self, request, context):
        left = f"{request.name} has left the server"
        print(left)
        response = BookStore_pb2.AccessResponse(id = left)
        return response
    
    def LocalStorePS(self, request, context):
        self.local_data_store_processes.clear()
        k = request.k
        for i in range(1, k + 1):
            process = DataStoreProcess(self.node_id, i)
            self.local_data_store_processes.append(process)
        process_ids = [process.id for process in self.local_data_store_processes]
        print(f"client-{self.node_id} request {k} process(es).")
        print(f"Created {k} local data store processes. Process IDs: {process_ids}")
        return BookStore_pb2.LocalStorePSResponse(process_ids=process_ids)

    def GetLocalDataStoreProcesses(self, request, context):
        process_list = BookStore_pb2.ProcessList()
        for process in self.local_data_store_processes:
            books_str = ",".join(process.books)
            grpc_process = BookStore_pb2.Process(id=process.id, k = process.process_id, books=books_str)
            process_list.processes.extend([grpc_process])
        return process_list

    def setchainallnodes(self):
        self.data_store_processes_copy = self.local_data_store_processes.copy()
        # other nodes for their local_data_store_processes and append to data_store_processes_copy
        global port1
        self.other_servers = [port for port in [50051, 50052, 50053] if port != port1]
        for server_port in self.other_servers:
            global port1
            if server_port == port1:
                continue
            try:
                with grpc.insecure_channel(f"{ip(port1)}:{server_port}") as channel:
                    stub = BookStore_pb2_grpc.BookStoreStub(channel)
                    response = stub.GetLocalDataStoreProcesses(BookStore_pb2.Empty())
                    for process in response.processes:
                        self.data_store_processes_copy.append(DataStoreProcess(node_id=server_port, process_id=process.k, books=process.books))

            except grpc.RpcError as e:
                if e.code() == StatusCode.UNAVAILABLE:
                    print(f"Server {server_port} is inactive.")
                    continue
                else:
                    print(f"An error occurred while connecting to server {server_port}: {e}")
                    continue

        for process in self.data_store_processes_copy:
            print(f"{port1} Process ID: {process.process_id}, Books: {process.books}")

    def SetChainAllNodes(self, request, context):
        self.setchainallnodes()

    def CreateChain(self, request, context):
        if self.chain.processes:
            recreate_chain = input("A chain already exists. Do you want to recreate the chain? (y/n): ")
            if recreate_chain.lower() != "y":
                # If the user decides to recreate the chain, clear the existing chain data
                self.chain.processes.clear()
            else:
                process_ids = [process.id for process in self.chain.processes]
                return BookStore_pb2.CreateChainResponse(process_ids=process_ids)
        self.setchainallnodes()
        self.chain.create_chain(self.data_store_processes_copy)
        process_ids = [process.id for process in self.chain.processes]

        #Update other nodes with the new chain
        # for server_port in self.other_servers:
        #     if server_port == port1:
        #         continue
        #     try:
        #         with grpc.insecure_channel(f"{ip(port1)}:{server_port}") as channel:
        #             stub = BookStore_pb2_grpc.BookStoreStub(channel)
        #             processes = [BookStore_pb2.Process(id=str(server_port), k=2, books="") for process in self.chain.processes]
        #             response = stub.UpdateChain(BookStore_pb2.UpdateChainRequest(processes=processes))
        #             print(f"Updated chain on server {server_port}")

        #     except grpc.RpcError as e:
        #         if e.code() == StatusCode.UNAVAILABLE:
        #             print(f"Server {server_port} is inactive.")
        #             continue
        #         else:
        #             print(f"An error occurred while connecting to server {server_port}: {e}")
        #             continue

        return BookStore_pb2.CreateChainResponse(process_ids=process_ids)


    def UpdateChain(self, request, context):
        processes = [
            DataStoreProcess(
                id=2222,
                process_id=process.k,
                books=process.books
            )
            for process in request.processes
        ]
        self.chain.processes = processes
        print("Updated chain")
        return BookStore_pb2.UpdateChainResponse(message="Chain updated successfully")

    def ListChain(self, request, context):
        # Build the response message
        process_ids = []
        for process in self.chain.processes:
            process_id = process.id
            if process.head:
                process_id += " (Head)"
            if process.tail:
                process_id += " (Tail)"
            process_ids.append(process_id)

        chain = " -> ".join(process_ids)
        response = BookStore_pb2.ListChainResponse(chain=chain)
        
        return response

    def WriteOperation(self, request, context):
        book_name = request.book
        price = request.price
        print(f"client-{self.node_id} request {book_name} {price} EUR.")
        
        response = self.chain.write_operation(book_name, price)
        return BookStore_pb2.WriteOperationResponse(message=response)

    def ListBooks(self, request, context):
        for book, price in self.chain.processes[len(self.chain.processes)-1].books.items():
            print(f"{book} = {price} EUR")
        response_books = [{"name": book, "price": price} for book, price in self.chain.processes[len(self.chain.processes)-1].books.items()]
        response = BookStore_pb2.ListBooksResponse(books=response_books)
        return response

    def ReadOperation(self, request, context):
        book_name = request.book
        message = self.chain.read_operation(book_name)
        exist = False if message == "Not yet in the stock" else True
        response = message if exist else -1
        return BookStore_pb2.ReadOperationResponse(price=response, exists = exist)

    def Timeout(self, request, context):
        timeout = request.timeout
        self.chain.set_timeout(timeout)
        return BookStore_pb2.TimeoutResponse(message=f"Timeout set to {timeout} seconds.")

    def DataStatus(self, request, context):
        status = self.chain.data_status()
        response = "\n".join([f"{i+1}) {book} - {stat}" for i, (book, stat) in enumerate(status.items())])
        return BookStore_pb2.DataStatusResponse(statuses=response)

    def RemoveHead(self, request, context):
        self.chain.remove_head()
        return BookStore_pb2.RemoveHeadResponse(new_head="Head removed.")

    def RestoreHead(self, request, context):
        head = self.chain.restore_head()
        return BookStore_pb2.RestoreHeadResponse(new_head=f"{ self.chain.processes[0].id}")

def serve():
    global port1
    port1 = int(input("Please put your port id:"))
    port2 = int(port1) + 1 if int(port1) < first_port + total_processes - 1 else first_port
    next_node_address = int(port2)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    BookStore_pb2_grpc.add_BookStoreServicer_to_server(BookStoreService(port1), server)
    server.add_insecure_port(f'[::]:{port1}')
    server.start()

    print(f'Starting server. Listening on port {port1}.')
    server.wait_for_termination()


if __name__ == "__main__":
    serve()