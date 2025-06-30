import httpx

server_url = "10.42.0.114"

with httpx.Client() as client:
    response = client.post(
        f"http://{server_url}:8000/rpc/add",
        json={
            "x": 10,
            "y": 1,
        }
    )

data = response.json()
print(data)