import requests

username = "pranesh"
password = "pass1234"

headers = {
    "Content-Type": "application/json",
}

res = requests.post(
    "http://localhost:8000/v1/user-sessions/",
    json={"username": "pranesh", "password": "pass1234"},
    headers=headers,
)
print(res)


# res = requests.get("http://localhost:8000/v1/trips/locations/", headers=headers)

# print(res.json())

# res = requests.get("http://localhost:8000/v1/trips/weather-check/", headers=headers, params={
#                     "latitude": "19.0760",
#                     "longitude": "72.8777",
#                     "trip_date": "2023-11-10",
# })
# print(res.json())

# res = requests.post("http://localhost:8000/v1/trips/", headers=headers, json={"is_draft": False, "itinerary": {}})
# print(res.status_code, res.json())
