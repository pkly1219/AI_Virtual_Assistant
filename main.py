import openai   #for using openai API
import pyttsx3  #for text to speech conversion
import random  #for generate random chat phrases
import time

# set OpenAI keyJ
openai.api_key = "API_Key_here "
model_id = "gpt-3.5-turbo"              #define the AI model for chat GPT

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# change speech rate
engine.setProperty('rate', 180)

# get the available voice
voices = engine.getProperty('voices')

# choose a voice based on the voice id
engine.setProperty('voices', voices[1].id)

# counter just for interacting purposes
interaction_counter = 0

# function to generate responses from the chatGPT API
def ChatGPT_conversation(conversation):
    try:
        response = openai.ChatCompletion.create(
            model = model_id,
            messages = conversation
        )
        api_usage = response['usage']
        print('Total token consumed: {0}'.format(api_usage['total_tokens']))
        conversation.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})
    except openai.error.RateLimitError as e:
        print(f"Rate limit exceeded. Current usage: {e.usage}")
        # You might want to handle rate limit errors gracefully, for example, wait until the quota resets.
        #time.sleep(60)  # Wait for 60 seconds
    except Exception as e:
        print(f"An error occurred: {e}")
    return conversation

# function to speak text
def speak_text(text):
    engine.say(text)
    engine.runAndWait()

# starting conversation
conversation = []
user_input = input("Enter your initial message: ")
conversation.append({'role': 'user', 'content': user_input})
conversation = ChatGPT_conversation(conversation)
print(f'{conversation[-1]["role"].strip()}: {conversation[-1]["content"].strip()}\n')
speak_text(conversation[-1]['content'].strip())

# while loop to continue the conversation
while True:
    user_input = input("You: ")
    conversation.append({'role': 'user', 'content': user_input})
    if user_input.lower() == "end":
        print("Ending the program. Thank you for using.")
        break

    # generate response using ChatGPT
    conversation = ChatGPT_conversation(conversation)

    print(f'{conversation[-1]["role"].strip()}: {conversation[-1]["content"].strip()}\n')
    speak_text(conversation[-1]['content'].strip())
