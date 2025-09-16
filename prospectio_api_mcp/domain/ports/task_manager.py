from abc import ABC, abstractmethod
from typing import Any
from domain.entities.task import Task


class TaskManagerPort(ABC):
    """
    Port for managing background tasks.
    """

    @abstractmethod
    async def submit_task(self, task_id: str) -> Task:
        """
        Submit a coroutine as a background task.

        Args:
            task_id (str): Unique task identifier.
            coro: The coroutine to run.

        Returns:
            str: The task ID.
        """
        pass

    @abstractmethod
    async def update_task(self, task_id: str, message: str, status: str) -> Task:
        """
        Update the status of a background task.

        Args:
            task_id (str): Unique task identifier.

        Returns:
            str: The updated task ID.
        """
        pass


    @abstractmethod
    async def get_task_status(self, task_id: str) -> Task:
        """
        Get the status of a task.

        Args:
            task_id (str): The task ID.

        Returns:
            Task: The task entity with status.
        """
        pass

    @abstractmethod
    async def remove_task(self, task_id: str) -> None:
        """
        Remove a completed or failed task from the manager.

        Args:
            task_id (str): The task ID to remove.

        Returns:
            None
        """
        pass