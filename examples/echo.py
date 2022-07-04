import asyncio
from rubika import Client, handlers

async def main():
    async with Client(session='rubika') as client:
        @client.on(handlers.MessageUpdates)
        async def echo(update):
            if update.raw_text:
                await update.reply(update.raw_text)
        await client.run_until_disconnected()

asyncio.run(main())
