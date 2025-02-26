from src.config import config_obj
import httpx
from fastapi import HTTPException
import os
import json

# rapid api configs
rapid_api_url = config_obj.RAPID_API_URL
rapid_api_key = config_obj.RAPID_API_KEY
rapid_api_host = config_obj.RAPID_API_HOST

# headers for the api
headers = {
    "x-rapidapi-key": rapid_api_key,
    "x-rapidapi-host": rapid_api_host
}

# Get the current file directory and construct the file path
json_file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data.json")


async def get_open_schemes_codes(scheme_code):
    # query parameters
    querystring = {"Scheme_Type": 'Open'}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(rapid_api_url, headers=headers, params=querystring)

            # Check for non-200 responses
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error fetching data: {response.text}"
                )

            try:
                data = response.json()  # Ensure JSON is valid
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from API")

            found_scheme = find_scheme_code(scheme_code, data)

            if found_scheme:
                return found_scheme
            else:
                return None
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API Error: {str(e)}")


async def get_fund_details_from_RapidAPI():
    # query parameters
    querystring = {"Scheme_Type": 'Open'}

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(rapid_api_url, headers=headers, params=querystring)

            # Check for non-200 responses
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error fetching data: {response.text}"
                )

            try:
                data = response.json()

                scheme_codes = [item["Scheme_Code"] for item in data]
                fund_details = {item["Scheme_Code"]: {k: v for k, v in item.items() if k != "Scheme_Code"} for item in
                                data}

                return {
                    "scheme_codes": scheme_codes,
                    "fund_details": fund_details
                }
            except ValueError:
                raise HTTPException(status_code=500, detail="Invalid JSON response from API")
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"External API Error: {str(e)}")

# Function to search for a Scheme_Code
def find_scheme_code(scheme_code, data):
    """Find a scheme by Scheme_Code in API response."""
    return next((scheme for scheme in data if scheme["Scheme_Code"] == scheme_code), None)


async def read_json_from_file():

    try:
        with open(json_file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        scheme_codes = [item["Scheme_Code"] for item in data]
        fund_details = {item["Scheme_Code"]: {k: v for k, v in item.items() if k != "Scheme_Code"} for item in data}

        return {
            "scheme_codes": scheme_codes,
            "fund_details": fund_details
        }
    except Exception as e:
        print(f"Error reading JSON from file: {str(e)}")
        return {
            "scheme_codes": [],
            "fund_details": {}
        }