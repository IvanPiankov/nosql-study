import asyncio
from uuid import uuid4

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer


async def send_one(producer: AIOKafkaProducer, msg: str) -> None:
    await producer.send("kafka_study_topic", key=str("python_key").encode(), value=msg.encode())


async def main():
    # Create kafka consumer
    consumer = AIOKafkaConsumer(
        'kafka_study_topic',
        bootstrap_servers='localhost:9092',
        group_id="python_consumer")

    # Create kafka producer
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    try:
        # Start producer
        await producer.start()
        await consumer.start()

        # Send some messages
        await send_one(producer, "First msg")
        await send_one(producer, "Second msg")
        await send_one(producer, "Third msg")

        # Consume this messages
        print("consumed: ", "topic", "partition", "offset", "key", "value", "timestamp")
        for _ in range(3):
            msg = await consumer.getone()
            print("consumed: ", msg.topic, msg.partition, msg.offset, msg.key, msg.value, msg.timestamp)

    finally:
        # Stop consumer and producer
        await producer.stop()
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(main())
