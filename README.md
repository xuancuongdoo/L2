# Travel Recommendations API

## Overview

The Travel Recommendations API provides travel suggestions based on the given country and season. This API leverages OpenAI's language model to generate unique travel recommendations that are relevant to the specified parameters.

## Features

- Get travel recommendations based on country and season.
- Handles errors and provides suggestions for invalid input.

## Project Structure

- **OpenAIClient**: Manages interaction with the OpenAI API.
- **PromptBuilder**: Constructs prompts for the OpenAI API.
- **Models**: Defines the data structures for travel recommendations and errors.
- **API Routes**: Defines the endpoints for fetching travel recommendations.
- **Application Setup**: Initializes and configures the FastAPI application.
- **Configuration**: Handles environment settings and configurations.

## Setup
1. Install dependencies:
    ```bash
    poetry install
    ```

2. Create a `.env` file with your OpenAI API key:
    ```env
    OPENAI_API_KEY=your_openai_api_key
    ```

3. Run the application staight from the command line using `uvicorn`:
    ```bash
    poetry run uvicorn main:app --reload --host 0.0.0.0 --port 3000
    ```
  or using `docker`
  ```bash
      make build; make up
  ```

4. Access the API documentation at `http://0.0.0.0:3000/docs`.

## Endpoints

- `GET /api/v1/recommendations?country={country}&season={season}`: Fetch travel recommendations for a specific country and season.



## Usage

### Endpoint

- **GET /api/v1/recommendations**

  Retrieves travel recommendations based on the specified country and season.

#### Parameters

- `country` (string, required): The name of the country.
- `season` (string, required): The season for which recommendations are requested. Must be one of 'spring', 'summer', 'fall', or 'winter'.

#### Response

- **Success (200)**: Returns a JSON object with travel recommendations.
- **Error (400)**: Returns a JSON object with error details.

### Example Request

```bash
curl -X 'GET' \
  'http://localhost:3000/api/v1/recommendations?country=Japan&season=spring' \
  -H 'accept: application/json'
```

### Example Response

```json
{
  "status": "Success",
  "data": {
    "country": "Japan",
    "season": "spring",
    "recommendations": [
      "Visit cherry blossom festivals",
      "Explore traditional tea houses",
      "Hike in the countryside",
      "Experience local spring festivals",
      "Enjoy spring-themed cuisine"
    ]
  }
}
```

```json
{
  "status": "Failed",
  "data": {
    "error": {
      "type": "InvalidCountryError",
      "message": "The provided country name '123' is not valid.",
      "suggestions": [
        "Check for typos in the country name."
      ]
    }
  }
}
```