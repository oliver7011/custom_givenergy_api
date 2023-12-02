import datetime
import json

import requests
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder

app = FastAPI()

api_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI5NTc3MDIxOS1jYWE2LTRmOTctOTE3Ni0zNDBlZGMzZDQxNTgiLCJqdGkiOiIzMWZkNmUzNDAwMTIyMzNmN2E2ZTJkMzE0M2EwYTMwZWUyYWJjMjQ4YTE1MDViNDAzMTg2NGNiMTZiNDdlMzFmYzhkOGU5NmQ4YzQzMjRiNiIsImlhdCI6MTcwMTU0MTY2Ny43Njc1NywibmJmIjoxNzAxNTQxNjY3Ljc2NzU3NCwiZXhwIjozMjUwMzY4MDAwMC4wMDgzMDUsInN1YiI6IjU3NjI5Iiwic2NvcGVzIjpbImFwaSJdfQ.GQYwSLY-3pZkEBQGqz3y2NUeAIeMrsv_rpWe0LA8TnvQ1q9ODqbeWkfxsGZY2pazIVYtd0o8BtHszmabMLpkmg"
inverter_id = "FA2308G729"


async def get_energy_flows():
    url = f"https://api.givenergy.cloud/v1/inverter/{inverter_id}/energy-flows"

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    payload = {
        "start_time": "2023-12-01",
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


async def get_house_usage(source: str = "all"):
    url = f"https://api.givenergy.cloud/v1/inverter/{inverter_id}/energy-flows"

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    types = [0, 3, 5]
    if source.lower() == "pv":
        types = [0]
    elif source.lower() == "grid":
        types = [3]
    elif source.lower() == "battery":
        types = [5]

    payload = {
        "start_time": "2023-12-01",
        "end_time": today,
        "grouping": 0,
        "types": types,
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

    data = response.json()["data"]

    for entry in data.values():
        if source.lower() == "all":
            entry["total"] = (
                entry["data"].get("0", 0)
                + entry["data"].get("3", 0)
                + entry["data"].get("5", 0)
            )
        elif source.lower() == "pv":
            entry["total"] = entry["data"].get("0", 0)
        elif source.lower() == "grid":
            entry["total"] = entry["data"].get("3", 0)
        elif source.lower() == "battery":
            entry["total"] = entry["data"].get("5", 0)

        # Round to 2 decimal places
        entry["total"] = round(entry["total"], 5)

        del entry["data"]

    return data


@app.get("/energy-flows")
async def energy_flows():
    energy_flows = await get_energy_flows()

    return energy_flows


@app.get("/house-usage")
async def house_usage(source: str = "all"):
    house_usage = await get_house_usage(source=source)

    return house_usage
