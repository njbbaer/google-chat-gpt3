# Google Chat GPT-3

This repo will help you fine-tune GPT-3 with a Google Chat conversation history. The trained model will be able to converse as one or both sides of the conversation in the participants' style.

1. Download your Chat archive from [Google Takeout](https://takeout.google.com/settings/takeout).
2. Locate the `messages.json` file of the conversation you would like to use as a training set.
3. Use the script to prepare data for training:

```shell
python preparer.py --messages <MESSAGES_FILE>
```

4. Test your training data with OpenAI's tool:

```shell
openai tools fine_tunes.prepare_data -f <TRAINING_FILE>
```

You should see: `No remediations found.`

5. Fine-tine GPT-3 with your training data:
```shell
openai api fine_tunes.create -t <TRAINING_FILE>
```

You should see: `Job complete! Status: succeeded 🎉`. Don't forget to note the name of the model.

7. Try out your model in the [Playground](https://beta.openai.com/playground) or with the CLI:
```
openai api completions.create -m <MODEL_NAME>
```
