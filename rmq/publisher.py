import datetime

import aio_pika
import aio_pika.abc


async def publish(loop, message):
    connection = aio_pika.RobustConnection = await aio_pika.connect_robust(
        "ampq://guest:guest@localhost:5672/", loop=loop
    )

    routing_key = "migration"

    channel = aio_pika.abc.AbstractChannel = await connection.channel()

    await channel.default_exchange.publish(
        aio_pika.Message(
            body=message.__str__().encode(),
        ),
        routing_key=routing_key
    )

    await connection.close()
