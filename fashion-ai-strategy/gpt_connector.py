import os
import json
import requests


def call_gpt(prompt: str) -> str:
    """Call Azure OpenAI API and return the response text."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not endpoint or not api_key or not deployment:
        print("Azure OpenAI environment variables not set. Returning placeholder insight.")
        return "[Azure OpenAI credentials missing. Insight unavailable.]"

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version=2023-07-01-preview"
    headers = {"Content-Type": "application/json", "api-key": api_key}
    data = {"messages": [{"role": "user", "content": prompt}], "max_tokens": 300}
    print("Calling Azure OpenAI API")
    resp = requests.post(url, headers=headers, data=json.dumps(data), timeout=30)
    if resp.status_code == 200:
        content = resp.json()["choices"][0]["message"]["content"]
        return content.strip()
    print(f"Azure OpenAI API error: {resp.text}")
    return "[Error fetching insight from Azure OpenAI]"
