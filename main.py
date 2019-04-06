import asyncio
import aiomysql

from api.server import app
from api.endpoints import *
from api.jobs import JobsHandler
from api.model import Model


from config import CFG

async def main(loop):
    model = Model(CFG, loop=loop)
    # pool = aiomysql.create_pool(**CFG.MYSQL, loop=loop)
    # conn = aiomysql.connect(**CFG.MYSQL, loop=loop)
    jobs_handler = JobsHandler(model)
    app.CFG = CFG
    app.loop = loop
    app.model = model
    app.jobs_handler = jobs_handler
    await model.create_connection()
    # app.conn = conn
    # loop.run_until_complete(model.create_connection())

    # Runs in this event loop
    asyncio.ensure_future(jobs_handler.jobs_loop(app.jobs))
    
    if False:
        # Runs on another thread
        loop.run_in_executor(None, cpu_background_task)



if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    
    
    app.run(host='127.0.0.1', port=5000, debug=True)
    # pool.close()
    # await pool.wait_closed()  