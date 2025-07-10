todo_list = []

def show_menu():
    print("\n--- To-Do List Menu ---")
    print("1. View tasks")
    print("2. Add task")
    print("3. Remove task")
    print("4. Exit")

def view_tasks():
    if not todo_list:
        print("No tasks yet.")
    else:
        for idx, task in enumerate(todo_list, 1):
            print(f"{idx}. {task}")

def add_task():
    task = input("Enter task: ")
    todo_list.append(task)
    print("Task added!")

def remove_task():
    view_tasks()
    try:
        index = int(input("Enter task number to remove: ")) - 1
        removed = todo_list.pop(index)
        print(f"Removed task: {removed}")
    except (IndexError, ValueError):
        print("Invalid task number!")

while True:
    show_menu()
    choice = input("Choose an option (1-4): ")

    if choice == "1":
        view_tasks()
    elif choice == "2":
        add_task()
    elif choice == "3":
        remove_task()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid choice. Try again.")