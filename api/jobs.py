import aiomysql
import asyncio

class JobsHandler:

    def __init__(self, model):
        self.model = model

    async def hello(self, **kvargs):
        print("hello", kvargs)

    async def search_planet(self, **kvargs):
        await self.model.make_record(**kvargs)

    async def hello(self, **kvargs):
        


    async def jobs_loop(self, jobs):
        while True:
            if jobs:
                task = jobs.pop(0)
                await self.process_task(task)
            await asyncio.sleep(1) # app.CFG.JOBS["sleep"]
        return


    async def process_task(self, task: dict):
        # obj = JobsHandler(app.loop)
        # try:
        method_to_call = getattr(self, task["job"])
        await method_to_call(**task["params"])
        # except AttributeError as e:
            # print(f"{task['job']} not found {e}")
        # except Exception as e:
            # raise e
        return