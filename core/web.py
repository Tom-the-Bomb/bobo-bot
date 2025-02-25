from datetime import datetime

from quart import Quart
from quart_cors import cors

app = Quart(__name__)

app.config['JSON_SORT_KEYS'] = False

app = cors(app)


@app.get('/')
async def index():
    return {'message': 'Hello World!'}


@app.get('/stats')
async def stats():
    async with app.bot.db.acquire() as conn:
        total_command_uses = await conn.fetchval('SELECT SUM(uses) FROM commands_usage')
        most_used_command = await conn.fetchval(
            'SELECT command FROM commands_usage ORDER BY uses DESC LIMIT 1'
        )

    latency = await app.bot.self_test()

    events = await app.bot.get_cog('Misc').get_event_counts()

    time_difference = (
        float(datetime.now().timestamp())
        - float(await app.bot.redis.get('events_start_time'))
    ) / 60

    return {
        'Servers': len(app.bot.guilds),
        'Users': len(app.bot.users),
        'Channels': len(list(app.bot.get_all_channels())),
        'Commands': len(list(app.bot.walk_commands())),
        'Total Command Uses': int(total_command_uses),
        'Most Used Command': most_used_command,
        'Postgres Latency': f'{latency.postgres} ms',
        'Redis Latency': f'{latency.redis} ms',
        'Discord REST Latency': f'{latency.discord_rest} ms',
        'Discord WebSocket Latency': f'{latency.discord_ws} ms',
        'Total Gateway Events': events,
        'Average Events per minute': f'{events // time_difference}',
    }
