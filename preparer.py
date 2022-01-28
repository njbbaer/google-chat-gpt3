import json
import datetime
import argparse
import dateutil.parser

MAX_TIME_DELTA = datetime.timedelta(hours=12)


def read_messages(filepath):
    with open(filepath) as file:
        return json.load(file)['messages']


def write_completions(filepath, completions):
    with open(filepath, 'w') as f:
        for completion in completions:
            f.write(json.dumps(completion) + "\n")


def prepare_messages(messages):
    completions = []
    completion = {'prompt': '', 'completion': ''}
    last_message_time = dateutil.parser.parse(messages[0]['created_date'])

    for message in messages:
        message_time = dateutil.parser.parse(message['created_date'])
        delta = message_time - last_message_time
        last_message_time = message_time

        if delta > MAX_TIME_DELTA and completion['completion']:
            completions.append(completion)
            completion = {'prompt': '', 'completion': ''}

        if 'text' in message:
            completion['completion'] += '\n ' if completion['completion'] else ' '
            completion['completion'] += message['creator']['name'] + ': ' + message['text']

    completions.append(completion)
    # Remove duplicates
    completions = {frozenset(item.items()): item for item in completions}.values()
    return completions


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--messages', type=str, default='messages.json')
    parser.add_argument('--output', type=str, default='output.jsonl')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()
    messages = read_messages(args.messages)
    completions = prepare_messages(messages)
    write_completions(args.output, completions)
    print(f'Wrote {len(messages)} messages into {len(completions)} completions')
