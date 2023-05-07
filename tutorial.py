#tutorial.py

commands = [
'local-store-ps <k>',
'create-chain',
'write-operation <book-name> <price>',
'list-books',
'read-operation <book-name>',
'list-chain',
'time-out <seconds>',
'data-status',
'remove-head',
'restore-head'
]

def bookstore_welcome():
    print("------------------WELCOME TO THE ONLINE BOOK SHOP!-----------------------------")
    print("Here's how to use the system:")
    print("Each node(computer) will act as a server and a client using the same port and id.")
    print(f"01. Start by {commands[0]} to create data store processes on your local node.")
    print(f"02. Run the '{commands[1]}' command to create a replication chain for strong data consistency once the data store processes are created.")
    print(f"03. Use the '{commands[2]}' command to add or update the price of a book.")
    print(f"04. Use the '{commands[3]}' command to view the available books in the store.")
    print(f"05. Use the '{commands[4]}' command to retrieve the price of a particular book.")
    print(f"06. Use the '{commands[5]}' command to list the current status of the replication chain.")
    print(f"07. Use the '{commands[6]}' command to set the timeout for propagating write updates between processes.")
    print(f"08. Use the '{commands[7]}' command to list the status of each data item, whether clean or dirty.")
    print(f"09. Use the '{commands[8]}' command to remove the current head from the chain.")
    print(f"10. Use the '{commands[9]}' command to restore the most recent removed head back to the chain.")
    print("Note: Each command should be run on the node where you want to perform the operation.")
    print("Thank you for using our online book shop system!")

def bookstore_welcome2():
    print("------------------WELCOME TO THE ONLINE BOOK SHOP!-----------------------------")
    print("Here's how to use the system:")
    print("Each node(computer) will act as a server and a client using the same port and id.")
    print("1. Start by 'local-store-ps <k>' to create data store processes on your local node.")
    print("2. Run the 'create-chain' to create a replication chain for strong data consistency once the data store processes are created.")
    print("3. Use the 'write-operation' command to add or update the price of a book.")
    print("4. Use the 'list-books' command to view the available books in the store.")
    print("5. Use the 'read-operation' command to retrieve the price of a particular book.")
    print("6. Use the 'list-chain' command to list the current status of the replication chain.")
    print("7. Use the 'time-out' command to set the timeout for propagating write updates between processes.")
    print("8. Use the 'data-status' command to list the status of each data item, whether clean or dirty.")
    print("9. Use the 'remove-head' command to remove the current head from the chain.")
    print("10. Use the 'restore-head' command to restore the most recent removed head back to the chain.")
    print("Note: Each command should be run on the node where you want to perform the operation.")