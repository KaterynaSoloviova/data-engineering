
import argparse
import time

from confluent_kafka import Consumer


def main():
    parser = argparse.ArgumentParser(
        description='Write Kafka messages to separate files'
    )
    parser.add_argument('--topic', default='file-topic')
    parser.add_argument('--bootstrap', default='localhost:9092')
    parser.add_argument(
        '--idle',
        type=int,
        default=10,
        help='stop after this many seconds without messages'
    )
    parser.add_argument(
        '--group',
        default=f'file-consumer-{int(time.time())}'
    )

    args = parser.parse_args()

    # Connect to Kafka
    consumer = Consumer({
        'bootstrap.servers': args.bootstrap,
        'group.id': args.group,
        'auto.offset.reset': 'earliest',
    })

    consumer.subscribe([args.topic])

    # Map Kafka message keys to output filenames
    outputs = {
        'sample.txt': 'sample_received.txt',
        'numbered.txt': 'numbered_received.txt'
    }

    # Store opened files
    file_handles = {}

    # Count messages for each source file
    counts = {
        key: 0 for key in outputs
    }

    last_message = time.time()

    try:
        # Open all output files
        for key, filename in outputs.items():
            file_handles[key] = open(
                filename,
                'w',
                encoding='utf-8',
                newline='\n'
            )

        # Read messages from Kafka
        while True:
            msg = consumer.poll(1.0)

            if msg is None:
                if time.time() - last_message > args.idle:
                    break
                continue

            if msg.error():
                print(f'Consumer error: {msg.error()}')
                continue

            # Read message key and value
            key_bytes = msg.key()

            if key_bytes is None:
                print('Skipping message without a key')
                continue

            key = key_bytes.decode('utf-8')
            value = msg.value().decode('utf-8')

            if value == '__EOF__':
                print(f'End of file received for {key}')
                break

            # Check whether the message key is recognized
            if key not in file_handles:
                print(f'Unknown message key: {key}')
                continue

            # Display and save the message
            print(f'[{key}] {value}')

            file_handles[key].write(value + '\n')

            # Update counters
            counts[key] += 1
            last_message = time.time()

    except KeyboardInterrupt:
        print('Consumer stopped by user')

    finally:
        # Close all output files
        for file in file_handles.values():
            file.close()

        # Close Kafka consumer
        consumer.close()

    # Display final results
    print('\nTransfer completed:')

    for key, filename in outputs.items():
        print(f'Wrote {counts[key]} lines to {filename}')


if __name__ == '__main__':
    main()
