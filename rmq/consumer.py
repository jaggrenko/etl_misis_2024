import asyncio
import aio_pika
import aio_pika.abc


async def main(loop):
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@localhost:5672/", loop=loop
    )

    async with connection:
        queue_name = "migration"
        channel: aio_pika.abc.AbstractChannel = await connection.channel()
        queue: aio_pika.abc.AbstractQueue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)

                    if queue.name in message.body.decode():
                        break

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main(loop))
    loop.run_forever()
