import requests

username = "test@test.com"
password = "pass1234"

headers = {
    "Content-Type": "application/json",
}

res = requests.post(
    "http://localhost:8000/v1/authn/user-sessions/",
    json={"username": username, "password": password},
    headers=headers,
)
print(res)
token = res.json()["token"]


headers["Authorization"] = f"Bearer {token}"
res = requests.get("http://localhost:8000/v1/trips/locations/", headers=headers)
print(res)


res = requests.get(
    "http://localhost:8000/v1/trips/weather-check/",
    headers=headers,
    params={
        "latitude": "19.0760",
        "longitude": "72.8777",
        "trip_date": "2023-11-10",
    },
)
print(res.json())

res = requests.post(
    "http://localhost:8000/v1/trips/",
    headers=headers,
    json={"is_draft": False, "itinerary": {}},
)

print(res.status_code, res.json())
