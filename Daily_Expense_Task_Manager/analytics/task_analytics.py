from datetime import date
from models.task_model import TaskModel

def summary():
    counts = TaskModel.counts()
    total = sum(counts.values())
    completed = counts["Completed"]
    return {
        **counts,
        "total": total,
        "completion_rate": (completed / total * 100) if total else 0
    }
