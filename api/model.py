import aiomysql

class Model:
    def __init__(self, cfg, loop):
        self.CFG = cfg
        self.loop = loop
        self.conn = None

    async def create_connection(self):
        self.conn = await aiomysql.connect(**self.CFG.MYSQL, loop=self.loop)
        return 


    async def make_record(self, **kvargs):
        async with self.conn.cursor() as cur:
            await cur.execute(f"""
                INSERT INTO jobs SET 
                name = 'search_planet',
                created_at = FROM_UNIXTIME(UNIX_TIMESTAMP()),
                done_at = FROM_UNIXTIME(UNIX_TIMESTAMP() + 1)
            """)
            await cur.execute(f"""
                SELECT name FROM jobs LIMIT 1
            """)
            print(cur.description)            
            (r,) = await cur.fetchone()
            print(r)
        return
