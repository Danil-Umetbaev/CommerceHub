import asyncio

from fastapi import FastAPI, Query
from app.consumer import consume_events
from contextlib import asynccontextmanager, suppress
from app.database import mongodb_client, events_collection
@asynccontextmanager
async def lifespan(_: FastAPI):
    task = asyncio.create_task(consume_events(events_collection))
    try:
        yield
    finally:
        task.cancel()
        with suppress(asyncio.CancelledError):
            await task
        await mongodb_client.close()

app = FastAPI(lifespan=lifespan)


@app.get('/events')
async def get_events(limit: int=10):
    stmt = (
        events_collection.find().sort('created_at', -1).limit(limit)
    )
    return stmt.to_list()