import json
import datetime
import argparse
import dateutil.parser


def read_messages(filepath):
    with open(filepath) as file:
        return json.load(file)['messages']


def write_completions(filepath, completions):
    with open(filepath, 'w') as f:
        for completion in completions:
            f.write(json.dumps(completion) + '\n')


def prepare_messages(messages):
    completions = []
    completion = {'prompt': '', 'completion': ''}
    last_message_time = dateutil.parser.parse(messages[0]['created_date'])
    last_creator = ''

    for message in messages:
        same_creator = message['creator']['name'] == last_creator
        last_creator = message['creator']['name']

        # Calculate time elapsed since the last message
        date_text = message.get('created_date') or message['updated_date']
        message_time = dateutil.parser.parse(date_text)
        delta = message_time - last_message_time
        last_message_time = message_time

        # Start a new completion if more than a set time has passed
        if completion['completion']:
            if (same_creator and delta > datetime.timedelta(hours=3)) or \
               (not same_creator and delta > datetime.timedelta(hours=12)):
                if '\n' in completion['completion']:
                    completions.append(completion)
                completion = {'prompt': '', 'completion': ''}

        # Add message to the current completion
        if 'text' in message:
            completion['completion'] += '\n ' if completion['completion'] else ' '
            completion['completion'] += message['creator']['name'] + ': ' + message['text']

    # Add final completion
    completions.append(completion)

    # Remove duplicates
    completions = {frozenset(item.items()): item for item in completions}.values()
    return completions


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('--messages', type=str, default='messages.json')
    parser.add_argument('--output', type=str, default='training.jsonl')
    return parser.parse_args()


def estimate_tokens(completions):
    num_chars = 0
    for completion in completions:
        num_chars += len(completion['prompt']) + len(completion['completion'])
    return int(num_chars / 4)


def print_statistics(messages, completions):
    print(f'Finished writing {args.output}'.format(args.output))
    print(f'     tokens: {estimate_tokens(completions)}')
    print(f'   messages: {len(messages)}')
    print(f'completions: {len(completions)}')


if __name__ == "__main__":
    args = parse_arguments()
    messages = read_messages(args.messages)
    completions = prepare_messages(messages)
    write_completions(args.output, completions)
    print_statistics(messages, completions)
