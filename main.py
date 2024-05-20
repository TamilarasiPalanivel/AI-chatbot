import json
import re
import random

# Load JSON data
def load_json(file):
    with open(file) as bot_responses:
        print(f"Loaded '{file}' successfully!")
        return json.load(bot_responses)

# Store JSON data
response_data = load_json("bot.json")

# Function to get a random response from a list of predefined responses
def random_string():
    responses = ["I'm not sure I understand. Can you elaborate?", "Interesting, tell me more.", "Hmm, that's something to think about."]
    return random.choice(responses)

# Function to get the appropriate response based on user input
def get_response(input_string):
    split_message = re.split(r'\s+|[,;?!.-]\s*', input_string.lower())
    score_list = []

    # Check all the responses
    for response in response_data:
        response_score = 0
        required_score = 0
        required_words = response.get("required_words", [])

        # Check if there are any required words
        if required_words:
            for word in split_message:
                if word in required_words:
                    required_score += 1

        # Amount of required words should match the required score
        if required_score == len(required_words):
            # Check each word the user has typed
            for word in split_message:
                # If the word is in the response, add to the score
                if word in response.get("user_input", []):
                    response_score += 1

        # Add score to list
        score_list.append(response_score)

    # Find the best response and return it if they're not all 0
    best_response = max(score_list, default=0)
    if best_response != 0:
        response_index = score_list.index(best_response)
        return response_data[response_index].get("bot_response", random_string())

    return random_string()

# Main loop for chatting
while True:
    user_input = input("You: ")
    print("Bot:", get_response(user_input))
