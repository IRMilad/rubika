# rubika (beta-22.6.28)
rubika client for python 3


# نصب 

```pip install https://github.com/IRMilad/rubika/archive/refs/heads/main.zip```

# مثال 

```python 
import asyncio
from rubika import Client, handlers


async def main():
    app = Client('rubika')

    @app.on(handlers.MessageUpdates(pattern='^echo (.*)$'))
    async def updates(event):
        text = event.pattern_match.group(1)
        await event.reply(f'`{text}`')

    await app.start(phone_number='98912*******')
    await app.run_until_disconnected()

asyncio.run(main())
```

# وقت زیادی روی این پروژه نزاشتم و احتمالا مشکلاتی داره هر مشکلی بود داخل [گروه تلگرامم](https://t.me/irtelepy) بگید تا برطرف کنم

سعی کردم تمام متد هارو بنویسم ولی توی بخش ```gadgets.methods.channels``` کمی ضعف هست چون اجازه ساخت کانال بهم نداد

تنها کمبود مهمی که فکر میکنم داشته باشه ویس چت هست که اگر استقبال بشه اضافه میکنم


وقت نوشتن مستندات کامل ندارم از این نظر از شما معدزت میخوام اگر با vs code کد بزنید راحت متوجه میشین چی به چی هست



دوست دار شما میلاد 💚
