import asyncio
import datetime
import time

i = 0

async def other_work():
    global i
    i += 1
    print(f"I like work. Work work. {i}")

########### this is ddoing the same as asyncio.sleep(seconds: in) #############
class YieldToEventLoop:
    def __await__(self):
        yield

async def _sleep_watcher(future, time_to_wake):
    while True:
        if time.time() >= time_to_wake:
            # This marks the future as done.
            future.set_result(None)
            break
        else:
            await YieldToEventLoop()

async def async_sleep(seconds: float):
    print(
        "Beginning asynchronous sleep at time: "
        f"{datetime.datetime.now().strftime("%H:%M:%S")}."
    )
    global i
    i += 1
    future = asyncio.Future()
    time_to_wake = time.time() + seconds
    # Add the watcher-task to the event loop.
    watcher_task = asyncio.create_task(_sleep_watcher(future, time_to_wake))
    # Block until the future is marked as done.
    await future
###############################################################################


async def main():
    # Add a few other tasks to the event loop, so there's something
    # to do while asynchronously sleeping.
    work_tasks = [
        asyncio.create_task(other_work()),
        asyncio.create_task(other_work()),
        asyncio.create_task(other_work())
    ]
    await asyncio.create_task(async_sleep(3))
    print(
        "Done asynchronous sleep at time: "
        f"{datetime.datetime.now().strftime("%H:%M:%S")}."
    )
    work_tasks.append(asyncio.create_task(other_work()))
    
    # asyncio.gather effectively awaits each task in the collection.
    await asyncio.gather(*work_tasks)


if __name__ == "__main__":
    asyncio.run(main())