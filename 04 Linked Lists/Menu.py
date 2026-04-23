from DSALL import  DSALinkedList, DSAListNode
# imports DSA linked list for use in menu
def menu():
    LL = DSALinkedList()
    choice = ""
    while choice != "6":
# menu
        print("---------DSA LINKED LIST MENU---------")
        print("1. Insert First")
        print("2. Insert Last")
        print("3. Remove First")
        print("4. Remove Last")
        print("5. Display")
        print("6. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            value = input("Enter value to insert at the beginning: ")
            LL.insert_first(value)
        elif choice == "2":
            value = input("Enter value to insert at the end: ")
            LL.insert_last(value)
        elif choice == "3":
            if not LL.isempty():
                removed_value = LL.remove_first()
                print("Removed value from the beginning:", removed_value)
            else:
                print("List is empty. Cannot remove.")
        elif choice == "4":
            if not LL.isempty():
                removed_value = LL.remove_last()
                print("Removed value from the end: ", removed_value)
            else:
                print("List is empty. Cannot remove.")
        elif choice == "5":
            print("Current List:")
            LL.display()
        elif choice == "6":
            print("Exiting...")
        else:
            print("Invalid choice. Please try again.")
menu()