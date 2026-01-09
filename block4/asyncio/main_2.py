class Rock:
    def __await__(self):
        value_sent_in = yield 7 # yield, as usual, pauses execution and returns control to the caller
        print(f"Rock.__await__ resuming with value: {value_sent_in}.")
        return value_sent_in

async def main():
    print("Beginning coroutine main().")
    rock = Rock()
    
    # await calls the __await__() method of the given object.
    # await also does one more very special thing: it propagates (or “passes along”) any yields it receives up the call chain.
    print("Awaiting rock...")
    value_from_rock = await rock
    
    print(f"Coroutine received value: {value_from_rock} from rock.")
    
    return 23

coroutine = main()
intermediate_result = coroutine.send(None)
print(f"Coroutine paused and returned intermediate value: {intermediate_result}.")

print(f"Resuming coroutine and sending in value: 42.")
try:
    coroutine.send(42)
    # The coroutine is resumed via the coroutine.send(42) call on line 26. 
    # The coroutine picks back up from where it yielded (or paused) on line 3 
    # and executes the remaining statements in its body. 

# When a coroutine finishes, it raises a StopIteration exception 
# with the return value attached in the value attribute.
except StopIteration as e:
    returned_value = e.value
print(f"Coroutine main() finished and provided value: {returned_value}.")