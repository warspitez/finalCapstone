import os
from datetime import datetime, date

# Define the date format
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Function to register a new user
def reg_user(username_password):
    new_username = input("New Username: ")

    # Check if the username already exists
    if new_username in username_password:
        print("Username already exists. Please try a different username.")
        return

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    # Check if the passwords match
    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        # Add the new user to the user.txt file
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{new_username};{new_password}")
    else:
        print("Passwords do not match")

# Function to add a new task
def add_task(username_password, task_list):
    task_username = input("Name of person assigned to task: ")
    # Check if the assigned user exists
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        return

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    # Create a new task
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    # Add the new task to the task list and update the tasks.txt file
    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

# Function to view all tasks
def view_all(task_list):
    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

# Function to view tasks assigned to the current user
def view_mine(curr_user, task_list):
    print("Tasks assigned to you:")
    for i, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task {i+1}:\n"
            disp_str += f"Title: {t['title']}\n"
            disp_str += f"Date Assigned: {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Description: {t['description']}\n"
            disp_str += f"Completed: {'Yes' if t['completed'] else 'No'}\n"
            print(disp_str)

    task_index = input("Enter the number of the task you want to select, or enter '-1' to return to the main menu: ")
    if task_index == '-1':
        return

    try:
        task_index = int(task_index) - 1
        if task_index < 0 or task_index >= len(task_list):
            print("Invalid task number.")
            return
    except ValueError:
        print("Invalid input. Please enter a number.")
        return

    selected_task = task_list[task_index]

    print(f"\nSelected Task: {selected_task['title']}")
    print("1. Mark as Complete")
    print("2. Edit Task")
    print("3. Return to Main Menu")

    choice = input("Enter your choice: ")

    if choice == '1':
        if not selected_task['completed']:
            selected_task['completed'] = True
            print("Task marked as complete.")
        else:
            print("Task is already marked as complete.")
    elif choice == '2':
        if not selected_task['completed']:
            print("What do you want to edit?")
            print("1. Assignee")
            print("2. Due Date")
            edit_choice = input("Enter your choice: ")
            if edit_choice == '1':
                new_assignee = input("Enter the new assignee's username: ")
                selected_task['username'] = new_assignee
                print("Assignee updated.")
            elif edit_choice == '2':
                while True:
                    new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                    try:
                        due_date_time = datetime.strptime(new_due_date, DATETIME_STRING_FORMAT)
                        selected_task['due_date'] = due_date_time
                        print("Due date updated.")
                        break
                    except ValueError:
                        print("Invalid datetime format. Please use the format specified")
            else:
                print("Invalid choice.")
        else:
            print("Task cannot be edited as it is already completed.")
    elif choice == '3':
        return
    else:
        print("Invalid choice.")

    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))

# Function to generate reports
def generate_reports(task_list, username_password):
    # Task Overview
    total_tasks = len(task_list)
    completed_tasks = sum(1 for task in task_list if task['completed'])
    incomplete_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['due_date'].date() < date.today())
    incomplete_percentage = (incomplete_tasks / total_tasks) * 100 if total_tasks != 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks != 0 else 0

    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write("Task Overview\n")
        task_overview_file.write(f"Total tasks: {total_tasks}\n")
        task_overview_file.write(f"Completed tasks: {completed_tasks}\n")
        task_overview_file.write(f"Uncompleted tasks: {incomplete_tasks}\n")
        task_overview_file.write(f"Overdue tasks: {overdue_tasks}\n")
        task_overview_file.write(f"Percentage of incomplete tasks: {incomplete_percentage}%\n")
        task_overview_file.write(f"Percentage of overdue tasks: {overdue_percentage}%\n")

    # User Overview
    total_users = len(username_password)
    tasks_assigned_to_users = {username: 0 for username in username_password}
    completed_tasks_by_users = {username: 0 for username in username_password}
    for task in task_list:
        tasks_assigned_to_users[task['username']] += 1
        if task['completed']:
            completed_tasks_by_users[task['username']] += 1

    with open("user_overview.txt", "w") as user_overview_file:
        user_overview_file.write("User Overview\n")
        user_overview_file.write(f"Total users: {total_users}\n")
        user_overview_file.write(f"Total tasks: {total_tasks}\n")
        for username in username_password:
            total_tasks_assigned = tasks_assigned_to_users[username]
            completed_tasks = completed_tasks_by_users[username]
            incomplete_tasks = total_tasks_assigned - completed_tasks
            overdue_tasks = sum(1 for task in task_list if not task['completed'] and task['username'] == username and task['due_date'].date() < date.today())
            percentage_total = (total_tasks_assigned / total_tasks) * 100 if total_tasks != 0 else 0
            percentage_completed = (completed_tasks / total_tasks_assigned) * 100 if total_tasks_assigned != 0 else 0
            percentage_incomplete = (incomplete_tasks / total_tasks_assigned) * 100 if total_tasks_assigned != 0 else 0
            percentage_overdue = (overdue_tasks / total_tasks_assigned) * 100 if total_tasks_assigned != 0 else 0

            user_overview_file.write(f"\nUser: {username}\n")
            user_overview_file.write(f"Total tasks assigned: {total_tasks_assigned}\n")
            user_overview_file.write(f"Percentage of total tasks: {percentage_total}%\n")
            user_overview_file.write(f"Percentage of completed tasks: {percentage_completed}%\n")
            user_overview_file.write(f"Percentage of incomplete tasks: {percentage_incomplete}%\n")
            user_overview_file.write(f"Percentage of overdue tasks: {percentage_overdue}%\n")
            
# Function to display statistics
def display_statistics(task_list, username_password):
    # If reports haven't been generated yet, generate them
    if not os.path.exists("task_overview.txt") or not os.path.exists("user_overview.txt"):
        generate_reports(task_list, username_password)

    # Display Task Overview
    with open("task_overview.txt", "r") as task_overview_file:
        print("Task Overview:")
        print(task_overview_file.read())

    # Display User Overview
    with open("user_overview.txt", "r") as user_overview_file:
        print("User Overview:")
        print(user_overview_file.read())

if __name__ == "__main__":
    # Create tasks.txt file if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w"):
            pass

    # Load tasks from tasks.txt
    with open("tasks.txt", 'r') as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    # Parse task data
    task_list = []
    for t_str in task_data:
        curr_t = {}
        task_components = t_str.split(";")
        curr_t['username'] = task_components[0]
        curr_t['title'] = task_components[1]
        curr_t['description'] = task_components[2]
        curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
        curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
        curr_t['completed'] = True if task_components[5] == "Yes" else False
        task_list.append(curr_t)

    # Create user.txt file if it doesn't exist
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    # Load user data
    with open("user.txt", 'r') as user_file:
        user_data = user_file.read().split("\n")

    # Parse user data
    username_password = {}
    for user in user_data:
        username, password = user.split(';')
        username_password[username] = password

    # Login
    logged_in = False
    while not logged_in:
        print("LOGIN")
        curr_user = input("Username: ")
        curr_pass = input("Password: ")
        if curr_user not in username_password.keys():
            print("User does not exist")
            continue
        elif username_password[curr_user] != curr_pass:
            print("Wrong password")
            continue
        else:
            print("Login Successful!")
            logged_in = True

    # Main menu loop
    while True:
        print()
        # Presenting the menu options to the user
        menu = input('''Please select one of the following options:
r - register user
a - add task
va - view all tasks
vm - view my tasks
gr - generate reports
ds - display statistics
e - exit
: ''').lower()

        # Execute the selected option
        if menu == 'r':
            reg_user(username_password)
        elif menu == 'a':
            add_task(username_password, task_list)
        elif menu == 'va':
            view_all(task_list)
        elif menu == 'vm':
            view_mine(curr_user, task_list)
        elif menu == 'gr':
            generate_reports(task_list, username_password)
            print("Reports generated successfully.")
        elif menu == 'ds':
            display_statistics(task_list, username_password)
        elif menu == 'e':
            print('Goodbye!!!')
            exit()
        else:
            print("You have made a wrong choice, Please Try again")
            