import logging
import openai
from chat_utils import ask
from secrets import OPENAI_API_KEY

if __name__ == "__main__":
    while True:
        user_query = input("Enter your question(want to exit, just \"exit\"): ")
        if user_query == "exit":
            print("Thank you!")
            break
        openai.api_key = OPENAI_API_KEY
        logging.basicConfig(level=logging.WARNING,
                            format="%(asctime)s %(levelname)s %(message)s")
        print('\n')
        print(ask(user_query))
        print('\n')