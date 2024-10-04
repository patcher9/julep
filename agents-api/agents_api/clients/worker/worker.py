import httpx

from ...env import temporal_worker_url
from .types import (
    MemoryManagementTask,
    MemoryManagementTaskArgs,
)


async def add_summarization_task(data: MemoryManagementTaskArgs):
    async with httpx.AsyncClient(timeout=30) as client:
        task = MemoryManagementTask(  # Renamed variable from 'data' to 'task'
            name="memory_management.v1",
            args=data,
        )

        await client.post(
            f"{temporal_worker_url}/task",
            json=task.model_dump(),  # Changed from 'data=' to 'json='
        )
