"""
    Project model.
"""

class Project:
    def __init__(self, id: int, name: str, description: str):
        if len(name) > 30:
            raise ValueError("Project name too long.")
        elif len(description) > 150:
            raise ValueError("Project description too long.")
        self.id = id
        self.name = name
        self.description = description

    def __repr__(self):
        return f"<Project {self.id}: {self.name}>"
    
    def __str__(self):
        return f"Project {self.id}: {self.name}"