import re
from fastapi import APIRouter, HTTPException, Query
from loguru import logger
from api.v1.services.prompt_trigger import OpenAIClient
from config import settings
from api.v1.models.recommendations import TravelRecommendation, Response, Error
import traceback
from typing import Any

router = APIRouter()


@router.get("/recommendations")
def get_travel_recommendations(
    country: str = Query(..., min_length=1),
    season: str = Query(..., regex="^(spring|summer|fall|winter)$"),
) -> Any:
    """
    Get travel recommendations based on the specified country and season.

    Args:
        country (str): The name of the country for which travel recommendations are requested.
        season (str): The season for which travel recommendations are requested. Must be one of 'spring', 'summer', 'fall', or 'winter'.

    Returns:
        Response: The HTTP response containing the travel recommendations.

    Raises:
        HTTPException: If there is an error fetching the recommendations.
    """
    try:
        openai_client = OpenAIClient(api_key=settings.OPENAI_API_KEY)
        response = openai_client.get_completion(country, season)
        logger.info(response)
        if isinstance(response, Error):
            return Response(status="Failed", data=response)
        else:
            travel_recommendation = TravelRecommendation(**response)
            return Response(data=travel_recommendation)
    except Exception as e:
        logger.error("Error fetching recommendations: {}", traceback.format_exc())
        raise HTTPException(
            status_code=500, detail="Could not fetch recommendations"
        ) from e
