import requests
import json

url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "f53fd7c70d86a6a89be38a4fd967c305",
    "redirect_uri" : "https://localhost.com",
    "code" : "VUuUydNrFUSohQFVKFjAqyFlDEnc-iHrK4J4yAm1EYx_STg1xFMjgIcw65H2vYYGhH6oQwopb9UAAAF9mKlkKQ"
}
response = requests.post(url, data = data)
tokens = response.json()
print(tokens)

with open("kakao_token.json", "w") as fp:
   json.dump(tokens, fp)
    