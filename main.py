import asyncio
import aiomysql

from api.server import app
from api.views import *
from api.jobs import jobs_loop
from api.model import Model


from config import CFG

async def main(loop):
    model = Model(CFG, loop=loop)
    app.CFG = CFG
    app.loop = loop
    app.model = model
    app.conn = await model.create_connection()
    #Runs in this event loop
    asyncio.ensure_future(jobs_loop(model, app.jobs))


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    app.run(host='127.0.0.1', port=5000, debug=True) #  
    # pool.close()
    # await pool.wait_closed()  