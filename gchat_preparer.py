import json
import datetime
from dateutil import parser

with open('messages.json') as file:
    messages = json.load(file)['messages']

completions = []
completion = {'prompt': '', 'completion': ''}
last_message_time = parser.parse(messages[0]['created_date'])

for message in messages:
    message_time = parser.parse(message['created_date'])
    delta = message_time - last_message_time
    last_message_time = message_time
    if delta > datetime.timedelta(hours=12) and completion['completion']:
        completions.append(completion)
        completion = {'prompt': '', 'completion': ''}

    if 'text' in message:
        if completion['completion']:
            completion['completion'] += '\n'
        completion['completion'] += message['creator']['name'] + ': ' + message['text']

# Remove duplicates
completions = {frozenset(item.items()): item for item in completions}.values()

with open("chat_nate_joey_v2.jsonl", 'w') as f:
    for completion in completions:
        f.write(json.dumps(completion) + "\n")
