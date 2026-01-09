import asyncio

# an async function returns 
# define an asynchronous function
# the async def, as opposed to just a plain def, makes this an asynchronous function (or “coroutine function”). 
# calling it creates and returns a coroutine object.
async def fibonacci(x: int, tid: str):
    if x == 0: return 0
    if x == 1: return 1

    print(f"{tid} Calculating fibonacci({x})...")
    await asyncio.sleep(0.1)
    fx_minus_1 = await fibonacci(x-1, tid)
    fx_minus_2 = await fibonacci(x-2, tid)
    return fx_minus_1 + fx_minus_2


async def main():
    y = await asyncio.gather(
        fibonacci(x=15, tid="A"),
        fibonacci(x=14, tid="B"),
        fibonacci(x=13, tid="C"),
        )
    print(y)


#asyncio.run(fibonacci(x=10, tid="A"))
asyncio.run(main())


