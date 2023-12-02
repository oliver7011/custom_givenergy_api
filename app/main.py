import datetime
import json

import requests
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

app = FastAPI()


async def get_energy_flows():
    api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTc3MDIxOS1jYWE2LTRmOTctOTE3Ni0zNDBlZGMzZDQxNTgiLCJqdGkiOiIzMWZkNmUzNDAwMTIyMzNmN2E2ZTJkMzE0M2EwYTMwZWUyYWJjMjQ4YTE1MDViNDAzMTg2NGNiMTZiNDdlMzFmYzhkOGU5NmQ4YzQzMjRiNiIsImlhdCI6MTcwMTU0MTY2Ny43Njc1NywibmJmIjoxNzAxNTQxNjY3Ljc2NzU3NCwiZXhwIjozMjUwMzY4MDAwMC4wMDgzMDUsInN1YiI6IjU3NjI5Iiwic2NvcGVzIjpbImFwaSJdfQ.GQYwSLY-3pZkEBQGqz3y2NUeAIeMrsv_rpWe0LA8TnvQ1q9ODqbeWkfxsGZY2pazIVYtd0o8BtHszmabMLpkmg"

    inverter_id = "FA2308G729"
    url = f"https://api.givenergy.cloud/v1/inverter/{inverter_id}/energy-flows"

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    payload = {
        "start_time": "2023-11-01",
        "end_time": today,
        "grouping": 1,
        "types": [0, 1, 2],
    }

    response = requests.post(
        url,
        data=json.dumps(payload),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        verify=True,
    )

    if response.status_code != 200:
        return "Error: " + str(response.status_code)

    return response.json()


@app.get("/energy-flows")
async def energy_flows():
    energy_flows = await get_energy_flows()

    return energy_flows
