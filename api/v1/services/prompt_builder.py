from api.v1.models.recommendations import TravelRecommendation, ErrorDetail


class PromptBuilder:
    def __init__(self):
        self.role = "You are an AI assistant that provides travel recommendations. Your role is to help users discover the best activities and places to visit in different countries during specific seasons. and the response you provide should be in the format of the Example Format or Response Model for success case. and can be parsed by json.loads"
        self.scope = """
                The assistant should provide 5 unique travel recommendations for activities to do in a given country during a specified season. The recommendations should be relevant to the season and the country and should offer a mix of cultural, adventurous, and relaxing activities.
                If the provided country or season is invalid, return an error message in the format: in the Example Format for fail case.
        """
        self.clues = """
                Provide unique recommendations that are not commonly known to tourists.
                Consider the local culture, climate, and seasonal events or festivals.
                Ensure the recommendations cover a variety of experiences (e.g., outdoor activities, cultural experiences, local cuisine). but just list the activities without any additional information.
        """
        self.example_entities = """
        For success:
        {
          "country": "Japan",
          "season": "spring",
          "recommendations": [
         ... 
          ]
        }
        For failure:
        {
            "type": "InvalidCountryError",
            "message": "The provided country name 'd' is not valid.",
            "suggestions": [
            "Check for typos in the country name.",
            ]
        }
        """

    def build_prompt(self, country, season):
        """
        Builds a prompt message for travel recommendations based on the given country and season.
        Args:
            country (str): The country for which travel recommendations are requested.
            season (str): The season for which travel recommendations are requested.
        Returns:
            list: A list containing a single dictionary with the prompt message.
        Example:
            >>> builder = PromptBuilder()
            >>> prompt = builder.build_prompt("France", "summer")
            >>> print(prompt)
            [{'role': 'user', 'content': '...'}]
        """
        prompt = f"""
            {self.role}
            {self.scope}
            {self.clues}
        Please provide travel recommendations for the following details:
        Country: {country}
        Season: {season}
        Example Format:
            {self.example_entities}
                        """
        message = [{"role": "user", "content": prompt}]
        return message
