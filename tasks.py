def task():
    tasks=[]
    print("Welcome to Task App📜🖊️")

    total_task=int(input("Enter how many task you want to add❓"))

    for i in range (1,total_task+1):
        task_name=input(f"enter task{i}= ")
        tasks.append(task_name)
        
    print(f"Today's Tasks are\n {tasks}")

    while True:
            operation =int(input("Enter 1-Add\n 2-Update\n 3-Delete\n 4-View\n 5-Exit"))
            if operation ==1:
                add=input("Enter task to add")
                tasks.append(add)
                print(f"Task{add} has been added..")

            elif operation ==2:
                update_val= input("Enter task you want to update")
                if update_val in tasks:
                    up=input("Enter new task to replace")
                    ind=tasks.index(update_val)
                    tasks[ind]=up
                    print(f"Updated task{up}")
            elif operation==3:
                del_val=input("Which task you want to delete")
                if del_val in tasks:
                     ind=tasks.index(del_val)
                     del tasks[ind]
                     print(f"Deleted task has been remove")

            elif operation ==4:
                print(f"Total tasks={tasks}")

            elif operation == 5:
                print(f"Closing .Thank you")
                break
            else:
                print("Invalid choice")

task()
