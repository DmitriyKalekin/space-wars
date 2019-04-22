import aiomysql
import asyncio
import json
from api.model import Model



async def jobs_loop(model:Model, jobs:list):
    """
    """
    counter = 0
    while True:
        print("Background task")
        await model.process_updates()
        await asyncio.sleep(1)

        counter += 1
        if counter >= 10:
            await model.drop_cache()
            counter = 0
    return


    






