import requests
import random

response = requests.get('https://the-trivia-api.com/v2/questions')

print(response.status_code)
print(response.text)

if response.headers.get("Content-Type", "").startswith("application/json"):
    data = response.json()
    print(data)

    score = 0

    for q in data:
        question = q["question"]["text"]
        correct = q["correctAnswer"]
        options = q["incorrectAnswers"] + [correct]

        random.shuffle(options)

        print("\n" + question)

        for i, option in enumerate(options):
            print(f"{i + 1}. {option}")

        user_input = input("Enter the number of your answer: ")

        try:
            user_choice = options[int(user_input) - 1]

            if user_choice == correct:
                print(" Correct!")
                score += 1
            else:
                print(f" Wrong! The correct answer was: {correct}")
        except:
            print("Invalid input.")

    print(f"\nFinal score: {score}/{len(data)}")

else:
    print("Not JSON:", response.text)
