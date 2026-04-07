import requests
from PIL import Image
import io
import urllib.parse

# --- Option 1: Pollinations.ai (Free, No Token) ---
description = "A cute cat playing with a ball of yarn"
encoded_prompt = urllib.parse.quote(description)
api_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&enhance=true"

print("Sending request to Pollinations.ai...")
try:
    response = requests.get(api_url)
    if response.status_code == 200:
        image = Image.open(io.BytesIO(response.content))
        image.save("test_pollinations_output.png")
        print("Pollinations image saved successfully to test_pollinations_output.png")
    else:
        print(f"Pollinations Error: {response.status_code} - {response.text}")
except Exception as e:
    print("Pollinations Request Error:", e)

# --- Option 2: Hugging Face (Needs Token) ---
# hf_token = os.environ.get("HF_TOKEN", "") # Use environment variable instead
# Uncomment if you want to test HF specifically
# ...

