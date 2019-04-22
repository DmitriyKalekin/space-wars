import aiomysql
import json
from api.commands.command import CommandInvoker

class Model:
    def __init__(self, cfg, loop):
        self.CFG = cfg
        self.loop = loop
        self.conn = None
        self.players_cache = {}
        self.command_invoker = CommandInvoker()

    async def create_connection(self):
        self.conn = await aiomysql.connect(**self.CFG.MYSQL, loop=self.loop)
        return 

    async def drop_cache(self):
        self.players_cache = {}
        return

    async def create_job(self, player_id:int, payload:dict):
        cmd = self.command_invoker.get_command(payload["name"])

        async with self.conn.cursor() as cur:
            if not cmd.get_arg("async"):
                print("NOT ASYNC")
                await cur.execute(f"""
                    SELECT t1.name FROM jobs t1
                    WHERE name = '{payload["name"]}'
                    AND player_id = {int(player_id)}
                    AND t1.done_at >= FROM_UNIXTIME(UNIX_TIMESTAMP())
                    LIMIT 1;
                """)
                already_run_commands = list(await cur.fetchall())
                if len(already_run_commands) > 0:
                    print("VIOLATION: command already started!")
                    return

            q = f"""
                INSERT INTO jobs SET 
                player_id = {int(player_id)},
                name = '{payload["name"]}',
                payload = '{json.dumps(payload)}',
                created_at = FROM_UNIXTIME(UNIX_TIMESTAMP()),
                done_at = FROM_UNIXTIME(UNIX_TIMESTAMP() + {cmd.get_arg("duration")})
            """
            # print(q)
            await cur.execute(q)

            # print(cur.description)            
            # (r,) = await cur.fetchone()
            # print(r)
        return

    async def process_updates(self):
        updates = await self.get_updates()
        updates_ids = []
        if updates:
            for u in updates:
                id_, player_id, name, _, payload, _, _ = u
                updates_ids.append(int(id_))
                player = await self.get_player(int(player_id))
                success, msg, result = self.command_invoker.run(name, payload, player)
                print(success, msg, result)
            await self.clean_updates(updates_ids)

    async def clean_updates(self, ids:list):
        if len(ids)==0:
            return

        async with self.conn.cursor() as cur:
            q = f"""
                DELETE FROM jobs 
                WHERE done_at <= FROM_UNIXTIME(UNIX_TIMESTAMP())
                AND job_id IN ({",".join([str(_) for _ in ids])});
            """
            

            # q = f"""
            #     UPDATE jobs t1
            #     SET t1.done = 1
            #     WHERE t1.done = 0
            #     AND t1.done_at >= FROM_UNIXTIME(UNIX_TIMESTAMP())
            #     AND job_id IN ({",".join([str(_) for _ in ids])});
            # """
            # print(q)
            await cur.execute(q)
        return

    async def get_updates(self):
        records = []
        async with self.conn.cursor() as cur:
            q = f"""
                SELECT 
                    t1.job_id, 
                    t1.player_id, 
                    t1.name, 
                    t1.done, 
                    t1.payload, 
                    t1.created_at, 
                    t1.done_at
                FROM jobs t1
                WHERE t1.done = 0
                AND t1.done_at <= FROM_UNIXTIME(UNIX_TIMESTAMP())
                ORDER BY created_at ASC;
            """
            await cur.execute(q)
            records = await cur.fetchall()
        
        return records     

    async def get_player(self, player_id:int):
        """
        """
        if player_id in self.players_cache:
            return self.players_cache[player_id]

        ret = None
        async with self.conn.cursor() as cur:
            q = f"""
                SELECT 
                    t1.player_id, 
                    t1.name, 
                    t1.payload 
                FROM players t1
                WHERE t1.player_id = {int(player_id)}
                LIMIT 1;
            """
            await cur.execute(q)
            (_, name, payload) = await cur.fetchone()
            ret = json.loads(payload)
            self.players_cache[player_id] = ret
        return ret          
