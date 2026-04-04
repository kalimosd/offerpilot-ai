import os

from openai import OpenAI

from offerpilot.config import load_project_env


PROVIDER_CONFIG = {
    "openai": {
        "api_key_env": "OPENAI_API_KEY",
        "base_url": None,
        "default_model": "gpt-5.2",
    },
    "deepseek": {
        "api_key_env": "DEEPSEEK_API_KEY",
        "base_url": "https://api.deepseek.com",
        "default_model": "deepseek-chat",
    },
}


def _get_provider_settings(provider: str) -> dict:
    normalized_provider = provider.lower().strip()
    if normalized_provider not in PROVIDER_CONFIG:
        supported = ", ".join(sorted(PROVIDER_CONFIG))
        raise ValueError(f"Unsupported provider: {provider}. Use one of: {supported}.")

    return PROVIDER_CONFIG[normalized_provider]


def call_llm(prompt: str, provider: str = "deepseek", model: str | None = None) -> str:
    """Call the configured LLM provider with a simple text prompt."""
    load_project_env()

    cleaned_prompt = prompt.strip()
    if not cleaned_prompt:
        raise ValueError("Prompt must not be empty.")

    settings = _get_provider_settings(provider)
    api_key = os.getenv(settings["api_key_env"])
    if not api_key:
        raise ValueError(f"{settings['api_key_env']} is not set.")

    client_kwargs = {"api_key": api_key}
    if settings["base_url"]:
        client_kwargs["base_url"] = settings["base_url"]

    client = OpenAI(**client_kwargs)

    response = client.chat.completions.create(
        model=model or settings["default_model"],
        messages=[
            {
                "role": "user",
                "content": cleaned_prompt,
            }
        ],
    )

    message = response.choices[0].message.content
    if message:
        return _normalize_text_output(message)

    raise ValueError("Model returned no text output.")


def _normalize_text_output(text: str) -> str:
    cleaned = text.strip()

    if cleaned.startswith("```") and cleaned.endswith("```"):
        lines = cleaned.splitlines()
        if len(lines) >= 3:
            cleaned = "\n".join(lines[1:-1]).strip()

    return cleaned
