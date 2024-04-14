import asyncio

from celery import current_app


async def foo(data: dict) -> None:
    ...


@current_app.task(name='some_name')
def foo(report_data: dict) -> None:
    asyncio.run(foo(report_data))
