"""Controller of the Tasks module. Module-private."""
from gui.services.auth_manager import AuthManager
from gui.services.request_context import RequestContext
from service.processing.MyWorkFlow import MyWorkFlow
from modules.tasks.service import TaskService
from modules.tasks.domain import Task


class TaskController:
    def __init__(self, workflow: MyWorkFlow, auth_manager: AuthManager):
        self.db = workflow.db
        self.workflow = workflow
        self.auth_manager = auth_manager
        self.log_manager = self.workflow.log_manager

    def get_all_tasks(self, ctx: RequestContext, search_filter=None):
        service = TaskService(self.db, ctx)
        return service.get_all_tasks(search_filter)

    def update_task_status(self, ctx: RequestContext, task_id: int, new_status: str):
        service = TaskService(self.db, ctx)
        return service.change_status(task_id, new_status)

    def save_task(self, ctx: RequestContext, task: Task):
        self.log_manager.debug('UI:' + ctx.user_name + ': Зберігаємо задачу: ' + str(task.task_subject))
        service = TaskService(self.db, ctx)
        return service.save_task(task)

    def delete_task(self, ctx: RequestContext, task_id: int):
        self.log_manager.debug('UI:' + ctx.user_name + ': Видаляємо задачу: ' + str(task_id))
        service = TaskService(self.db, ctx)
        service.delete_task(task_id)

    def get_task_by_id(self, ctx: RequestContext, task_id: int) -> Task:
        service = TaskService(self.db, ctx)
        return service.get_task_by_id(task_id)

    def get_my_task_counts(self, ctx: RequestContext) -> tuple[int, int]:
        service = TaskService(self.db, ctx)
        return service.get_task_counts_for_user(ctx.user_id)

    def get_available_users(self):
        return self.auth_manager.get_all_users()

    def get_my_alarms(self, ctx: RequestContext):
        service = TaskService(self.db, ctx)
        return service.get_triggered_alarms(ctx.user_id)

    def create_task(self, ctx: RequestContext, task: Task):
        service = TaskService(self.db, ctx)
        return service.save_task(task)
