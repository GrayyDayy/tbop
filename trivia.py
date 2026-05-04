import requests

response = requests.get('https://the-trivia-api.com/v2/questions')

print(response.status_code)
print(response.text)

if response.headers.get("Content-Type", "").startswith("application/json"):
    data = response.json()
    print(data)
else:
    print("Not JSON:", response.text)