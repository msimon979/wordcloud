import json

import requests

url = "http://0.0.0.0:8000/clouds/submit/"


urls = [
    "https://en.wikipedia.org/wiki/Team_sport",
    "https://en.wikipedia.org/wiki/Football_at_the_Summer_Olympics",
    "https://en.wikipedia.org/wiki/FIFA_World_Cup",
    "https://en.wikipedia.org/wiki/Qatar",
    "https://en.wikipedia.org/wiki/Saudi_Arabia",
]

for u in urls:
    payload = json.dumps({"url": u})
    headers = {"Content-Type": "application/json"}

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
