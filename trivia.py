import requests
import random


def get_trivia_question():

    try:
        response = requests.get(
            'https://the-trivia-api.com/v2/questions'
        )

        data = response.json()

        q = data[0]

        question = q["question"]["text"]

        correct = q["correctAnswer"]

        options = q["incorrectAnswers"] + [correct]

        random.shuffle(options)

        return {
            "question": question,
            "correct": correct,
            "options": options
        }

    except Exception as e:

        print("Trivia API Error:", e)

        return None