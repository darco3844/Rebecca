class TaskState:
    def __init__(self):
        self.project = None
        self.current_task = None
        self.goal = None
        self.status = "idle"
        self.pending = []

    def set_project(self, project):
        self.project = project

    def set_task(self, task):
        self.current_task = task
        self.status = "in_progress"

    def set_goal(self, goal):
        self.goal = goal

    def add_pending(self, item):
        if item not in self.pending:
            self.pending.append(item)

    def remove_pending(self, item):
        if item in self.pending:
            self.pending.remove(item)

    def complete_task(self):
        self.status = "completed"

    def clear_task(self):
        self.current_task = None
        self.status = "idle"

    def get_context(self):
        return {
            "project": self.project,
            "current_task": self.current_task,
            "goal": self.goal,
            "status": self.status,
            "pending": list(self.pending),
        }

    def describe(self):
        lines = []

        if self.project:
            lines.append(
                f"Proyecto: {self.project}"
            )

        if self.current_task:
            lines.append(
                f"Tarea actual: {self.current_task}"
            )

        if self.goal:
            lines.append(
                f"Objetivo: {self.goal}"
            )

        lines.append(
            f"Estado: {self.status}"
        )

        if self.pending:
            lines.append("Pendientes:")

            for item in self.pending:
                lines.append(
                    f"- {item}"
                )

        return "\n".join(lines)
