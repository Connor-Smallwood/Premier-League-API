import http.client

conn = http.client.HTTPSConnection("v3.football.api-sports.io")

headers = {
    'x-rapidapi-host': "v3.football.api-sports.io",
    'x-rapidapi-key': "6e0dfc805474353f8cd2a4e30cda460b"
    }

conn.request("GET", "/teams/statistics?season=2020&team=33&league=47", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))