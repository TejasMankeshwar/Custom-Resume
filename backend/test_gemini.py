import sys
from google import genai
from google.genai.errors import APIError

def test_validation(api_key: str):
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents='Respond with the word "OK" only.'
        )
        print(f"Success! Response: {response.text}")
    except Exception as e:
        print(f"Error type: {type(e)}")
        print(f"Error message: {e}")

if __name__ == "__main__":
    test_validation("dummy_key")
