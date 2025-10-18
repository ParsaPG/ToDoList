# cli/main.py
from datetime import datetime

from Projects.services import ProjectService
from Projects.storage import InMemoryStorage as ProjectStorage
from Tasks.services import TaskService
from Tasks.storage import InMemoryStorage as TaskStorage


def main():
    project_store = ProjectStorage()
    task_store = TaskStorage()

    projects_service = ProjectService(project_store)
    tasks_service = TaskService(task_store, project_store)
    
    MENU = (
        "\n====== ToDoList ======\n"
        "1) Add Project\n"
        "2) List Projects\n"
        "3) Edit Project\n"
        "4) Delete Project\n"
        "5) Add Task\n"
        "6) List Tasks (by Project)\n"
        "7) Edit Task\n"
        "8) Delete Task\n"
        "9) Exit\n"
    )
    
    while True:
        
        print(MENU)
        choice = input("> ")
        if choice == "1":
            """
            Add a new project.
            """
            n = input("Project name: ")
            d = input("Description: ")
            
            print("Project added: ")
            print(projects_service.add(n, d))
        elif choice == "2":
            """
            List all projects.
            """
            for p in projects_service.list():
                print(p)
                
        elif choice == "3":
            new_name = input("New name (leave blank to keep current): ").strip()
            new_desc = input("New description (leave blank to keep current): ").strip()
            try:
                pid = int(input("Project ID to delete: "))
            except ValueError:
                print("Please enter a valid integer ID.")
                continue
            if not new_name or not new_desc:
                current = None
                for p in projects_service.list():
                    if p.id == pid:
                        current = p
                        break
                if current is None:
                    print("Project not found.")
                    continue
                if not new_name:
                    new_name = current.name
                if not new_desc:
                    new_desc = current.description
                    
            p = projects_service.edit(pid, new_name, new_desc)
            print(f"Updated Project [{p.id}] {p.name}")
        elif choice == "4":
            """
            Delete a project by its ID.
            """
            try:
                pid = int(input("Project ID to delete: "))
            except ValueError:
                print("Please enter a valid integer ID.")
                continue
            try:
                projects_service.delete(pid)
                print("Project deleted (tasks removed as well).")
            except Exception as e:
                print(f"{e}")
        elif choice == "5":
            """
            Add a new task to a project.
            """
            try:
                pid = int(input("Project ID: "))
            except ValueError:
                print("Please enter a valid integer ID.")
                continue
            
            t = input("Task title: ")
            desc = input("Description: ")
            while True:
                dl_in = input("New deadline YYYY-MM-DD (blank = keep): ").strip()
                if dl_in == "":
                    break
                try:
                    datetime.strptime(dl_in, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")
            print("Task added: ")
            try:
                print(tasks_service.add(pid, t, desc, dl_in if dl_in else None))
            except Exception as e:
                print(f"{e}")
        elif choice == "6":
            """
            List tasks for a specific project.
            """
            try:
                pid = int(input("Project ID to list tasks: "))
            except ValueError:
                print("Please enter a valid integer ID.")
                continue
            try:
                for t in tasks_service.list(pid):
                    print(t)
            except Exception as e:
                print(f"{e}")
        elif choice == "7":
            try:
                pid = int(input("Project ID: "))
            except ValueError:
                print("Please enter a valid integer ID.")
                continue
            try:
                tid = int(input("Task ID to edit: ").strip())
            except ValueError:
                print("Please enter a valid integer ID.")
                continue

            new_title = input("New title (blank = keep): ").strip()
            new_desc = input("New description (blank = keep): ").strip()
            
            while True:
                new_status = input("New status [todo|doing|done] (blank = keep): ").strip().lower()
                if new_status in {"", "todo", "doing", "done"}:
                    break
                print("Invalid status. Choose from todo, doing, done.")
            while True:
                dl_in = input("New deadline YYYY-MM-DD (blank = keep): ").strip()
                if dl_in == "":
                    break
                try:
                    datetime.strptime(dl_in, "%Y-%m-%d")
                    break
                except ValueError:
                    print("Invalid date format. Use YYYY-MM-DD.")

            changes = {}
            if new_title:
                changes["title"] = new_title
            if new_desc:
                changes["description"] = new_desc
            if new_status:
                changes["status"] = new_status
            if dl_in:
                changes["deadline"] = datetime.strptime(dl_in, "%Y-%m-%d").date()

            if not changes:
                print("Nothing to update.")
                continue

            t = tasks_service.edit(pid, tid, **changes)
            print(f"Updated Task [{t.id}] {t.title}")
        elif choice == "8":
            """
            Delete a task from a project.
            """
            try:
                pid = int(input("Project ID: "))
                tid = int(input("Task ID to delete: "))
            except ValueError:
                print("Please enter valid integer IDs.")
                continue
            try:
                tasks_service.delete(pid, tid)
                print("Task deleted.")
            except Exception as e:
                print(f"{e}")

        elif choice == "8":
            print("Exiting...")
            break
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
    main()
