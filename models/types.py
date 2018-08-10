from typing import List


class Task:
    def __init__(self, title: str, score: int):
        self.title: str = title
        self.score: int = score

    def __str__(self):
        return self.title


class User:
    def __init__(self):
        self.score = 0
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> int:
        self.tasks.append(task)
        self.tasks = list(sorted(self.tasks, key=lambda task: -1 * task.score))
        return self.tasks.index(task)

    def end_task(self, task: Task) -> None:
        self.tasks.remove(task)
        self.score += task.score
