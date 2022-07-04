import asyncio
from rubika import Client, methods, models, handlers, exceptions

configuration = {
    #client kwargs
    'client': {
        'session': 'tabchi'
    },
    # admins guid
    'admins': ['u0B6POl021f56630fa6350c02e37c0cc']
}


async def main():
    async with Client(**configuration['client']) as client:
        @client.on(handlers.MessageUpdates(
                models.RegexModel(pattern=r'forward (\d+)')
                &
                models.author_guid(func=lambda author: author in configuration['admins'])
                &
                models.reply_message_id
            )
        )
        async def forward(update):
            sleep = int(update.pattern_match.group(1))
            dialogs = await client(methods.chats.GetChats(start_id=None))
            if dialogs.chats:
                total = len(dialogs.chats)
                successful = 0
                unsuccessful = 0
                message = await update.reply(f'تعداد {total} چت پیدا شد شروع فرایند ارسال ...')
                for index, dialog in enumerate(dialogs.chats, start=1):
                    if methods.groups.SendMessages in dialog.access:
                        try:
                            await update.forwards(dialog.object_guid, message_ids=update.reply_message_id)
                            successful += 1

                        except Exception:
                            unsuccessful += 1

                        progress = '|'
                        filled = int(index * 15 / total)
                        progress += '█' * filled
                        progress += '-' * (15 - filled)
                        progress += '| ▅▃▁' 
                        progress += f' [{int(index * 100 / total):,}%]'
    
                        await message.edit(
                            f'تعداد {index:,} چت از {total:,} چت بررسی شده است'
                            f'\nموفق : {successful:,}\nناموفق: {unsuccessful:,}\n\n{progress}'
                        )
                        await asyncio.sleep(sleep)
            else:
                await update.reply('در جستجوی چت ها با شکست مواجعه شد')
            

        await client.run_until_disconnected()

asyncio.run(main())
