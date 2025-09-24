
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("OPENAI_API_KEY")

if not api_key:
    print("Error: OPENAI_API_KEY environment variable not set.")
else:
    try:
        client = OpenAI(api_key=api_key)
        models = client.models.list()
        print("Successfully connected to OpenAI API.")
        print(f"Found {len(models.data)} models.")
    except Exception as e:
        print(f"An error occurred: {e}")
