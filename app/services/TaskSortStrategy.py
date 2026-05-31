from abc import ABC, abstractmethod
from datetime import datetime, timezone


class TaskSortStrategy(ABC):
    @abstractmethod
    def apply(self, tasks, reverse=False):
        pass


class IdSortStrategy(TaskSortStrategy):
    def apply(self, tasks, reverse=False):
        return sorted(tasks or [], key=lambda task: task.id, reverse=reverse)


class DueSortStrategy(TaskSortStrategy):
    def apply(self, tasks, reverse=False):
        def sort_key(task):
            if task.deadline is None:
                return (1, datetime.max.replace(tzinfo=timezone.utc))
            return (0, task.deadline)

        return sorted(tasks or [], key=sort_key, reverse=reverse)


class PrioritySortStrategy(TaskSortStrategy):
    ORDER = {'CRITICAL': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3}

    def apply(self, tasks, reverse=False):
        def rank(task):
            if task.priority is None:
                return len(self.ORDER)
            return self.ORDER.get(task.priority.name, len(self.ORDER))

        return sorted(tasks or [], key=rank, reverse=reverse)


class StatusSortStrategy(TaskSortStrategy):
    ORDER = {'TODO': 0, 'IN_PROGRESS': 1, 'IN_REVIEW': 2, 'DONE': 3}

    def apply(self, tasks, reverse=False):
        def rank(task):
            if task.status is None:
                return len(self.ORDER)
            return self.ORDER.get(task.status.name, len(self.ORDER))

        return sorted(tasks or [], key=rank, reverse=reverse)


SORT_STRATEGIES = {
    'id': IdSortStrategy(),
    'due': DueSortStrategy(),
    'priority': PrioritySortStrategy(),
    'status': StatusSortStrategy(),
}
