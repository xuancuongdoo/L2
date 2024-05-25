from openai import OpenAI
from api.v1.models.recommendations import Error, ErrorDetail
from loguru import logger
from .prompt_builder import PromptBuilder
import json
import re
import ast


class OpenAIClient:
    def __init__(self, api_key: str) -> None:
        self.client = OpenAI(api_key=api_key)
        self.prompt_builder = PromptBuilder()

    def get_completion(self, country: str, season: str, model="gpt-4o"):
        """
        Retrieves a completion from the OpenAI chat model based on the given country and season.

        Args:
            country (str): The country for which the completion is requested.
            season (str): The season for which the completion is requested.
            model (str, optional): The name of the OpenAI model to use. Defaults to "gpt-4o".

        Returns:
            str: The completion response from the OpenAI chat model.
        """
        messages = self.prompt_builder.build_prompt(country, season)
        messages[0]["content"] = (
            messages[0]["content"].replace("\n", " ").strip()
        )  # reduce token cost
        openai_response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=0,
        )
        content = self.clean_content(openai_response.choices[0].message.content)
        try:
            parsed_content = ast.literal_eval(content)

            if "type" in parsed_content:
                return Error(error=ErrorDetail(**parsed_content))

            return self.clean_response(content)

        except json.JSONDecodeError as e:
            logger.error("JSON decoding error: {}", e)
            return {"status": "failed", "error": "Invalid JSON format"}

    def clean_content(self, text: str) -> dict:
        """
        Clean and parse the output to a JSON format.
        Args:
            text (str): The cleaned output from the OpenAI API.
        Returns:
            parsed_response (dict): The output in a JSON format.
        """
        return text.strip().strip("```json").strip("```")

    def clean_response(self, text: str) -> dict:
        """
        Clean and parse the output to a JSON format.
        Args:
            text (str): The cleaned output from the OpenAI API.
        Returns:
            parsed_response (dict): The output in a JSON format.
        """
        text = text.replace("\n", " ").replace("|", "")
        text = re.sub(r'[^\{\}\[\],:"]+$', "", text)

        try:
            parsed_response = json.loads(text)
        except json.JSONDecodeError as e:
            logger.error("JSON decoding error: {}", e)
            return {"error": "Invalid JSON format"}

        logger.info(type(parsed_response))
        return parsed_response
