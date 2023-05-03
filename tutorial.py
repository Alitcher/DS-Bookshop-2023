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
    print("1. Each node(computer) will act as a server and a client using the same port and id.")
    print(f"2. Start by {commands[0]} to create data store processes on your local node.")
    print(f"3. Run the '{commands[1]}' command to create a replication chain for strong data consistency once the data store processes are created.")
    print(f"4. Use the '{commands[2]}' command to add or update the price of a book.")
    print(f"5. Use the '{commands[3]}' command to view the available books in the store.")
    print(f"6. Use the '{commands[4]}' command to retrieve the price of a particular book.")
    print(f"7. Use the '{commands[5]}' command to list the current status of the replication chain.")
    print(f"8. Use the '{commands[6]}' command to set the timeout for propagating write updates between processes.")
    print(f"9. Use the '{commands[7]}' command to list the status of each data item, whether clean or dirty.")
    print(f"10. Use the '{commands[8]}' command to remove the current head from the chain.")
    print(f"11. Use the '{commands[9]}' command to restore the most recent removed head back to the chain.")
    print("Note: Each command should be run on the node where you want to perform the operation.")
    print("Thank you for using our online book shop system!")
