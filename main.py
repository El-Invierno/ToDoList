from task_class import Task
from tabulate import tabulate
import mysql.connector


def sort_list():
    for i in range(len(Task.task_list)):
        Task.task_list[i][0] = i


def task_input(t_idx):
    desc = input('Enter the description of the task: ')
    priority = input('Enter the priority of the task (H/M/L): ').upper()
    new_task = Task(t_idx, desc, priority, 'Pending')
    new_task.add_task(priority)
    if priority == 'H':
        sort_list()
    save_data()


def print_table():
    headers = ["Task_Id", "Task_Description", "Task_Priority", "Task_Status"]
    table = tabulate(Task.task_list, headers, tablefmt="fancy_grid")
    print(table)


def remove():
    if len(Task.task_list) == 0:
        print("The list is empty, you can't delete anything from it.")
        return
    t_id = int(input("Enter the task_id of the task to be removed: "))
    Task.task_list.pop(t_id)
    sort_list()
    query = 'truncate task'
    cursor.execute(query)
    db_connection.commit()
    save_data()


def remove_all():
    if len(Task.task_list) > 0:
        Task.task_list.clear()
    query = 'truncate task'
    cursor.execute(query)
    db_connection.commit()
    save_data()


def edit_task():
    if len(Task.task_list) == 0:
        print("The list is empty, you can't edit anything in it.")
        return
    t_id = int(input("Enter the t_id of the task to edit: "))
    new_task = input("Enter the edited version of the task: ")
    Task.task_list[t_id][1] = new_task
    save_data()


def mark_done():
    if len(Task.task_list) == 0:
        print("The list is empty, you can't mark anything done in it.")
        return
    try:
        t_id = int(input("Enter the t_id to mark as completed."))
        Task.task_list[t_id][3] = "Completed"
        save_data()
    except ValueError:
        print('Try to enter a numerical value of the t_id!')


def conv_to_str():
    final = []
    for row in Task.task_list:
        units = []  # Initialize units list inside the loop for each row
        for item in row:
            units.append(str(item))
        final.append(units)
    return final


def write_toList():  # This function writes data to the notepad file.
    final = conv_to_str()
    with open('C:/Users/yasht/OneDrive/Desktop/ToDoList.txt', 'w') as file:
        file.write('')  # We have refreshed the file before saving something new.
        for item in final:
            file.write(' | '.join(item))
            file.write('\n')


def save_data():
    query = "insert into task values (%s,%s,%s,%s)"
    for task in Task.task_list:
        data = tuple(task)
        try:
            cursor.execute(query, data)
            db_connection.commit()
        except mysql.connector.errors.IntegrityError:
            update_query = 'update Task set t_name = %s, t_status = %s, t_priority = %s where t_id = %s'
            cursor.execute(update_query, (task[1], task[3], task[2], task[0]))
            db_connection.commit()
    write_toList()


def main(size):
    check_start = True
    task_no = size
    while check_start:
        # Options:
        print('================ToDo-list Options=================')
        print(f'1) Add a task to the list. Priority: (H!!/M!/L). Status: (Pending/Complete).')
        print(f'2) Remove a task from the list.')
        print(f'3) Remove all tasks from the list.')
        print(f'4) Edit Tasks.')
        print(f'5) Exit Terminal.')
        print(f'6) Print the table.')
        print(f'7) Mark the task as done.')
        print(f'8) Save the data to the database. (No need to do it manually, Auto-save enabled.)')

        num = 0
        try:
            num = int(input('Enter the option id: '))
        except ValueError as error:
            print('****I/p type Error: You entered a string value inside a field intended to accept only integral '
                  'values from 1-8.', end='\n')
            num = 0

        match num:
            case 1:
                task_input(task_no)
                task_no += 1
            case 2:
                task_no -= 1
                remove()
            case 3:
                task_no = 0
                remove_all()
            case 4:
                edit_task()
            case 5:
                # Program ends.
                check_start = False
            case 6:
                print_table()
            case 7:
                mark_done()
            case 8:
                save_data()
            case _:
                print(f'****The num {num} is not an option, pls select another option from 1 - 7')


# Driver Code. The code begins from here.
if __name__ == "__main__":
    db_connection = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="yash",
        database="todo_list"
    )
    cursor = db_connection.cursor()
    query = 'SELECT * FROM todo_list.task'
    cursor.execute(query)
    res = cursor.fetchall()  # It returns a list of tuple.
    for r in res:
        Task.task_list.append(list(r))

    size_preload = len(Task.task_list)
    print_table()
    main(size_preload)  # Call to the main function.

    cursor.close()
    db_connection.close()
