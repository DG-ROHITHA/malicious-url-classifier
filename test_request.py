import requests

url_to_check = "http://bit.ly/update-login"

response = requests.post(
    "http://127.0.0.1:5000/api/check_url",
    json={"url": url_to_check}
)

print("Response from server:")
print(response.json())
