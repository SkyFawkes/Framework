"""
Demos asyncio creating multiple coroutines from an instance of a class
"""
import asyncio


class TestClass:
    def __init__(self, a=0, b=0):
        print('Loop from __init__: ', asyncio.get_event_loop())
        print(a, b)
        self.a = a
        self.c = None

    async def say(self, what, when):
        await asyncio.sleep(when)
        print(what, when, self.a)  # self.b won't work
        self.c = when

    async def stop_after(self, loop, when):
        print('Loop from stop_after: ', loop)
        await asyncio.sleep(when)
        print('c: ', self.c)
        loop.stop()


loop = asyncio.get_event_loop()
print('Loop from outside: ', loop)
testInstance = TestClass(a=1, b=2)

# create_task is non-breaking, nothing happens until loop is run.

loop.create_task(testInstance.say('first hello', 2))
loop.create_task(testInstance.say('second hello', 1))
loop.create_task(testInstance.say('third hello', 4))

# To end:
loop.create_task(testInstance.stop_after(loop, 5))  # If this is 3, program ends early with a warning
loop.run_forever()  # Run until loop.stop called from inside a task

# Alternative ending:
#loop.run_until_complete(testInstance.stop_after(loop, 5))  # Run until a specific task is complete

print('Loop finished')
loop.close()
print('Loop closed')
