import time
import random
from typing import Type, TypeVar, Any
from google import genai
from pydantic import BaseModel

T = TypeVar('T', bound=BaseModel)

class GeminiError(Exception):
    def __init__(self, message: str, retryable: bool = False):
        # Ensure API keys are never accidentally included in the exception message
        self.message = message
        self.retryable = retryable
        super().__init__(self.message)

class GeminiService:
    @staticmethod
    def _get_client(api_key: str) -> genai.Client:
        if not api_key or not api_key.strip():
            raise GeminiError("API Key is missing or empty.", retryable=False)
        # Request-scoped client, API key is not persisted on the server
        return genai.Client(api_key=api_key.strip())

    @staticmethod
    def validate_key(api_key: str) -> bool:
        """Performs a minimal request to validate the API key."""
        try:
            client = GeminiService._get_client(api_key)
            # Use a fast, cheap model for validation
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents='Respond with the word "OK" only.'
            )
            return "OK" in response.text
        except Exception as e:
            # Catching generic exception to prevent any leak of the raw error which might contain keys/paths
            raise GeminiError("Failed to validate Gemini API Key. Ensure it is correct and has quota.", retryable=False)

    @staticmethod
    def generate_structured(api_key: str, prompt: str, content: str, schema: Type[T], max_retries: int = 2) -> T:
        """
        Calls Gemini to generate structured output matching the provided Pydantic schema.
        Implements bounded retries with exponential backoff and jitter for transient failures.
        """
        client = GeminiService._get_client(api_key)
        
        attempt = 0
        while attempt <= max_retries:
            try:
                # Use gemini-2.5-flash for structured data tasks
                response = client.models.generate_content(
                    model='gemini-2.5-flash',
                    contents=[prompt, content],
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=0.1 # Low temperature for analytical tasks
                    ),
                )
                
                # The SDK automatically validates against the schema when parsing, 
                # but we can explicitly parse it using the Pydantic schema class.
                if response.parsed:
                    return response.parsed
                
                # Fallback if parsed is empty but text exists
                return schema.model_validate_json(response.text)

            except Exception as e:
                attempt += 1
                
                # Check if it's a known non-retryable error (e.g., Auth, Invalid Argument)
                err_str = str(e).lower()
                if "api key" in err_str or "unauthenticated" in err_str or "permission" in err_str or "invalid" in err_str:
                     raise GeminiError("Authentication or Invalid Argument error occurred.", retryable=False)

                if attempt > max_retries:
                    raise GeminiError("Max retries exceeded while calling Gemini.", retryable=False)
                
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
        
        raise GeminiError("Failed to generate structured content.", retryable=False)
