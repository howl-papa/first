
def build_prompt(sku: str, ad_spend: float, weather: str, weekday: str) -> str:
    """Create GPT prompt with business scenario."""
    print("Building GPT prompt")
    prompt = (
        f"You are analyzing fashion demand data for SKU {sku}. "
        f"Recent advertising spend was {ad_spend}. "
        f"Weather conditions are {weather}. "
        f"Today is {weekday}. "
        "Provide insights for inventory, marketing, and merchandising in either Korean or English."
    )
    return prompt
