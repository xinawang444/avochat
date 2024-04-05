# the os module helps us access environment variables
# i.e., our API keys
import os
import json
import requests
import discord
from dotenv import load_dotenv

load_dotenv() # load variables

DISCORD_TOKEN=os.environ["DISCORD_TOKEN"]

from transformers import AutoModelWithLMHead, AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
model = AutoModelForCausalLM.from_pretrained("TODO: path to model")

class MyClient(discord.Client):
    def __init__(self, model_name):
        # adding intents module to prevent intents error in __init__ method in newer versions of Discord.py
        intents = discord.Intents.default() # Select all the intents in your bot settings as it's easier
        intents.message_content = True
        super().__init__(intents=intents)

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        data = json.loads(data)
        data = data.get('inputs', None) # input text from user

        """
        TODO: write code so that output_string is assigned to the correct output
        We want to query the model using data to get an outputted message for the bot to reply with to the user
        hint hint this will be VERY similar to the last cell in your colab notebook from week 2!
        """

        output_string = # CODE HERE
        ret = [{"generated_text": output_string}]
        return ret

    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': 'Hello!'})

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        # form query payload with the content of the message
        payload = {'inputs': message.content}

        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
          response = self.query(payload)
        bot_response = response[0].get('generated_text', None)

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)

def main():
    

    client = MyClient('michael-chat-bot')
    client.run(DISCORD_TOKEN)

if __name__ == '__main__':
  main()


