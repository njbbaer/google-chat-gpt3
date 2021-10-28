import json
import datetime
from dateutil import parser


def is_valid(completion):
    return completion.get('prompt') and completion.get('completion')


with open('messages.json') as file:
    messages = json.load(file)['messages']

completions = []
completion = {}
thread = ''
author = messages[0]['creator']['name']
last_message_time = parser.parse(messages[0]['created_date'])

for message in messages:
    message_time = parser.parse(message['created_date'])
    delta = message_time - last_message_time
    last_message_time = message_time
    if delta > datetime.timedelta(hours=1):
        thread = ''
        completion = {}
        author = message['creator']['name']

    if message['creator']['name'] != author:
        if 'prompt' not in completion:
            if thread:
                completion['prompt'] = thread + '\n' + message['creator']['name'] + ':'
        else:
            completion['completion'] = ' ' + thread
            if is_valid(completion):
                completions.append(completion)
            completion = {'prompt': completion['prompt'] + completion['completion'] + '\n' + message['creator']['name'] + ':'}
        thread = ''
        author = message['creator']['name']

    if 'text' in message:
        if thread:
            thread += '\n'
        if thread or 'prompt' not in completion:
            thread += author + ': '
        thread += message['text']

with open("chat_nate_joey.jsonl", 'w') as f:
    for completion in completions:
        f.write(json.dumps(completion) + "\n")
