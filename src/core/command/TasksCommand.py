import asyncio

from src.core.utility.Utility import Utility
from src.core.command.base.BaseCommand import BaseCommand

ansi = Utility.colors()


class TasksCommand(BaseCommand):

    helper: dict = {
        'name': 'tasks',
        'help': 'This command will print all the currently running tasks',
        'usage': 'tasks'
    }

    def __init__(self, command: str, print_queue: asyncio.Queue):
        super().__init__()
        self.command: str = command
        self.print_queue: asyncio.Queue = print_queue

    async def main(self) -> None:
        await self.execute()

    async def execute(self) -> None:
        tasks = asyncio.all_tasks()
        pending = [task for task in tasks if task != asyncio.current_task or not task.done()]
        await self.print_queue.put(f"\n{ansi['red']}Running Tasks\n{ansi['red']}{'=' * 13}{ansi['reset']}")
        field_names = [f'{"Coroutine":<20}', f'{"Name":<20}', f'{"Loop":<30}']
        field_values = []
        for pending_task in pending:
            coro = str(pending_task.get_coro()).split(' ')[2:]
            field_values.append([' '.join(coro).rstrip('>'), pending_task.get_name(), str(pending_task.get_loop())])
        output: str = Utility.create_table(field_names, field_values)
        await self.print_queue.put(f"{output}\n")
