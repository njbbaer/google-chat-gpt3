import json
import pprint


def is_valid(completion):
    return completion.get('prompt') is not None and \
        completion.get('completion') is not None


with open('messages.json') as file:
    messages = json.load(file)['messages']

completions = []
thread = ''
author = messages[0]['creator']['name']
completion = {}
for message in messages:
    if message['creator']['name'] != author:
        if author == 'Nate Baer':
            completion['prompt'] = thread + '\n\n###\n\n'
        if author == 'Joseph Baer':
            completion['completion'] = thread + ' END'
            if is_valid(completion):
                completions.append(completion)
            completion = {}
        thread = ''
        author = message['creator']['name']

    if 'text' in message:
        if thread:
            thread += '\n\n'
        thread += message['text']

with open("chat_joey.jsonl", 'w') as f:
    for completion in completions:
        f.write(json.dumps(completion) + "\n")
