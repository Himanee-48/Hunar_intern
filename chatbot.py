import re
import random
from datetime import datetime
jokes = [
    ("Why did the computer go to the doctor?", "Because it had a virus!"),
    ("Why was the math book sad?", "Because it had too many problems."),
    ("Why did the scarecrow win an award?", "Because he was outstanding in his field!"),
    ("Why don't scientists trust atoms?", "Because they make up everything!"),
    ("Why did the student eat his homework?", "Because the teacher said it was a piece of cake!"),
]

def get_time():
    now = datetime.now()
    return "The current time is " + now.strftime("%I:%M %p")

def get_date():
    now = datetime.now()
    return "Today's date is " + now.strftime("%A, %d %B %Y")

def calculate_expression(expr):
    try:
        expr = re.sub(r'[^0-9+\-*/(). ]', '', expr)
        result = eval(expr)
        return f"The answer is {result}"
    except Exception:
        return "Sorry, I couldn’t calculate that. Try something like '10 + 5' or '25 * 3'."

def chatbot_response(text, joke_state):
    text = text.lower().strip()

    if joke_state.get("waiting"):
        if "why" in text or "because" in text:
            answer = joke_state["answer"]
            joke_state["waiting"] = False
            joke_state["answer"] = None
            return answer, joke_state
        else:
            return "You’re supposed to ask 'why?'", joke_state

    if re.search(r'\b(hi|hello|hey|hola|hii)\b', text):
        return random.choice([
            "Hello there! How can I help you today?",
            "Hi! I’m your friendly chatbot.",
            "Hey! Nice to meet you "
        ]), joke_state

    elif re.search(r'\b(date|today)\b', text):
        return get_date(), joke_state

    elif re.search(r'\b(time|clock|current time)\b', text):
        return get_time(), joke_state

    elif re.search(r'\b(joke|funny|laugh)\b', text):
        q, a = random.choice(jokes)
        joke_state["waiting"] = True
        joke_state["answer"] = a
        return q, joke_state

    elif re.search(r'[0-9]', text) and re.search(r'[+\-*/]', text):
        return calculate_expression(text), joke_state

    elif re.search(r'\b(thank you|thanks)\b', text):
        return random.choice([
            "You're welcome!",
            "No problem at all!",
            "Glad to help!"
        ]), joke_state

    elif re.search(r'\b(bye|exit|quit|goodbye)\b', text):
        return "Goodbye! Have a great day!", joke_state

    else:
        with open("unknown_queries.txt", "a", encoding="utf-8") as f:
            f.write(f"{datetime.now()} — {text}\n")
        return random.choice([
            "I didn’t quite get that. Try asking for time, date, or a joke.",
            "Hmm… I don’t understand that yet. Ask 'tell me a joke' or 'what’s the time'."
        ]), joke_state

def main():
    print("RuleBot v3 — Type 'bye' to exit.\n")
    joke_state = {"waiting": False, "answer": None}

    while True:
        user_input = input("You: ")
        response, joke_state = chatbot_response(user_input, joke_state)
        print("Bot:", response)
        if "goodbye" in response.lower() or "bye" in user_input.lower():
            break

if __name__ == "__main__":
    main()