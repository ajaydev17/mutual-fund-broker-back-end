from src.config import config_obj
import httpx
from fastapi import HTTPException
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

# Function to search for a Scheme_Code
def find_scheme_code(scheme_code, data):
    """Find a scheme by Scheme_Code in API response."""
    return next((scheme for scheme in data if scheme["Scheme_Code"] == scheme_code), None)