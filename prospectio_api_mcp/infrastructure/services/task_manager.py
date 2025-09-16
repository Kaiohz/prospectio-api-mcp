from typing import Dict
from domain.ports.task_manager import TaskManagerPort
from domain.entities.task import Task


class InMemoryTaskManager(TaskManagerPort):
    """
    In-memory implementation of TaskManagerPort using asyncio.
    """

    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        
    async def submit_task(self, task_id: str) -> Task:
        """
        Submit a coroutine as a background task.

        Args:
            task_id (str): Unique task identifier.
            coro: The coroutine to run.

        Returns:
            str: The task ID.
        """
        task = Task(task_id=task_id, message="Task submitted", status="pending")
        self.tasks[task_id] = task
        return task

    async def update_task(self, task_id: str, message: str, status: str) -> Task:
        """
        Update the status of a background task.

        Args:
            task_id (str): Unique task identifier.

        Returns:
            str: The updated task ID.
        """
        if task_id in self.tasks:
            self.tasks[task_id].message = message
            self.tasks[task_id].status = status
            return self.tasks[task_id]
        else:
            raise ValueError(f"Task with ID {task_id} not found.")

    async def get_task_status(self, task_id: str) -> Task:
        """
        Get the status of a task.

        Args:
            task_id (str): The task ID.

        Returns:
            Task: The task entity with status.
        """
        return self.tasks.get(task_id, Task(task_id=task_id, message="Task not found", status="unknown"))
    
    async def remove_task(self, task_id: str) -> bool:
        """
        Remove a completed or failed task from the manager.

        Args:
            task_id (str): The task ID to remove.

        Returns:
            None
        """
        if task_id in self.tasks:
            del self.tasks[task_id]
            return True
        return False


task_manager = InMemoryTaskManager()