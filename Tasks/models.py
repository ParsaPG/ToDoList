from datetime import date

STATUSES = {"todo", "doing", "done"}

class Task:
    def __init__(self, id: int, title: str, description: str, project_id: int, status: str = "todo", deadline: date = None):
        if len(title) > 30 or len(description) > 150:
            raise ValueError("Title or description exceeds length limits.")
        if status not in STATUSES:
            raise ValueError("Invalid status value.")
        self.id = id
        self.title = title
        self.description = description
        self.project_id = project_id
        self.status = status
        self.deadline = deadline

    def __repr__(self):
        return f"<Task {self.id}: {self.title} ({self.status} - Deadline: {self.deadline} - desc: {self.description})>"
    
    def __str__(self):
        return f"Task {self.id}: {self.title} ({self.status} - Deadline: {self.deadline} - desc: {self.description})"