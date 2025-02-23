from src.config import config_obj
import httpx
from fastapi import HTTPException

# rapid api configs
rapid_api_url = config_obj.RAPID_API_URL
rapid_api_key = config_obj.RAPID_API_KEY
rapid_api_host = config_obj.RAPID_API_HOST

# headers for the api
headers = {
    "x-rapidapi-key": rapid_api_key,
    "x-rapidapi-host": rapid_api_host
}


class RapidAPIService:
    async def get_open_schemes(self, scheme_type):
        # query parameters
        querystring = {"Scheme_Type": scheme_type}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(rapid_api_url, headers=headers, params=querystring)

                # Check for non-200 responses
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error fetching data: {response.text}"
                    )

                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"External API Error: {str(e)}")

    async def get_open_schemes_fund_family(self, scheme_type, fund_family):
        # query parameters
        querystring = {"Mutual_Fund_Family": fund_family, "Scheme_Type": scheme_type}

        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(rapid_api_url, headers=headers, params=querystring)

                # Check for non-200 responses
                if response.status_code != 200:
                    raise HTTPException(
                        status_code=response.status_code,
                        detail=f"Error fetching data: {response.text}"
                    )

                return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=500, detail=f"External API Error: {str(e)}")