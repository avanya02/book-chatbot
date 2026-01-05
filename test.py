import requests

res = requests.post(
    "http://127.0.0.1:5000/chat",
    json={"query": "python"}
)

print(res.status_code)
print("Status:", res.status_code)
print("Text:", res.text)