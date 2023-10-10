#!/usr/bin/env python3

from brain_module import ChatGPT

if  __name__ == "__main__":
    bot = ChatGPT()
    response = bot.request_openai("Hello!")
    print(response)
