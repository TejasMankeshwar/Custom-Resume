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
        # Add a timeout so that the client fails fast instead of hanging on rate limit backoffs
        return genai.Client(
            api_key=api_key.strip(),
            http_options={'timeout': 30.0}
        )

    @staticmethod
    def validate_key(api_key: str, model_name: str = "gemini-3.5-flash") -> bool:
        """Performs a minimal request to validate the API key."""
        try:
            client = GeminiService._get_client(api_key)
            # Use the selected model for validation
            response = client.models.generate_content(
                model=model_name,
                contents='Respond with the word "OK" only.'
            )
            return "ok" in response.text.lower()
        except Exception as e:
            # Print the actual error to the backend console for debugging without returning it to the user
            print(f"Gemini API Validation Error: {e}")
            err_str = str(e).lower()
            if "quota" in err_str or "exhausted" in err_str or "429" in err_str:
                raise GeminiError("Gemini API quota exceeded or rate limited. Please try again in a minute.", retryable=True)
            if "time" in err_str and "out" in err_str:
                raise GeminiError("The Gemini API timed out. The service might be overloaded or your free-tier key is being rate-limited. Please wait a moment and try again.", retryable=True)
            raise GeminiError(f"Failed to validate Gemini API Key. Reason: {str(e)}", retryable=False)

    @staticmethod
    def generate_structured(api_key: str, prompt: str, content: str, schema: Type[T], model_name: str = "gemini-3.5-flash", max_retries: int = 2) -> T:
        """
        Calls Gemini to generate structured output matching the provided Pydantic schema.
        Implements bounded retries with exponential backoff and jitter for transient failures.
        """
        client = GeminiService._get_client(api_key)
        
        attempt = 0
        while attempt <= max_retries:
            try:
                # Use selected model for structured data tasks
                print(f"    >>> [Gemini Service] Sending structured request to model: {model_name} (Attempt {attempt+1}/{max_retries+1})...")
                response = client.models.generate_content(
                    model=model_name,
                    contents=[prompt, content],
                    config=genai.types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema=schema,
                        temperature=0.1 # Low temperature for analytical tasks
                    ),
                )
                print(f"    <<< [Gemini Service] Received response successfully from model: {model_name}.")
                
                # The SDK automatically validates against the schema when parsing, 
                # but we can explicitly parse it using the Pydantic schema class.
                if response.parsed:
                    return response.parsed
                
                # Fallback if parsed is empty but text exists
                return schema.model_validate_json(response.text)

            except Exception as e:
                attempt += 1
                err_str = str(e).lower()
                
                # Print clean error details safely to the console
                print(f"Gemini Service error during attempt {attempt}: {e}")
                
                # Check if it's a known non-retryable error (e.g., Auth, Invalid Argument, Model Not Found)
                if "api key" in err_str or "unauthenticated" in err_str or "permission" in err_str or "invalid" in err_str:
                     raise GeminiError("Authentication or Invalid Argument error occurred. Please check your API key.", retryable=False)
                
                if "not found" in err_str or "404" in err_str:
                     raise GeminiError(f"Model or resource not found: {str(e)}", retryable=False)

                if attempt > max_retries:
                     if "quota" in err_str or "exhausted" in err_str or "429" in err_str:
                          raise GeminiError("Gemini API quota exceeded or rate limited. Please try again in a minute.", retryable=True)
                     if "unavailable" in err_str or "503" in err_str or "overloaded" in err_str:
                          raise GeminiError("Gemini service is currently overloaded or experiencing high demand. Please try again later.", retryable=True)
                     raise GeminiError(f"Gemini request failed: {str(e)}", retryable=True)
                
                # Exponential backoff with jitter
                sleep_time = (2 ** attempt) + random.uniform(0, 1)
                time.sleep(sleep_time)
        
        raise GeminiError("Failed to generate structured content due to persistent errors.", retryable=True)
