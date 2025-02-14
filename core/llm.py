# core/llm.py
"""
LLM Integration Module using Groq API.

This module integrates with the Groq API to generate dynamic, human-like responses
based on the conversation context provided in the prompt.

It uses the Groq client to interact with the API and constructs the messages from the prompt.
"""

import re
import logging
from groq import Groq
from config import settings

logger = logging.getLogger(__name__)

def parse_prompt_to_messages(prompt: str) -> list:
    """
    Parse the prompt string into a list of messages suitable for the Groq API.

    Args:
        prompt (str): The full conversation prompt with context.

    Returns:
        list: A list of dictionaries with keys "role" and "content".
    """
    messages = []
    for line in prompt.split("\n"):
        line = line.strip()
        if not line:
            continue
        if line.startswith("User:"):
            messages.append({"role": "user", "content": line[len("User:"):].strip()})
        elif line.startswith("Bot:"):
            messages.append({"role": "assistant", "content": line[len("Bot:"):].strip()})
        else:
            messages.append({"role": "system", "content": line})
    return messages

def get_llm_response(prompt: str) -> str:
    """
    Send a prompt to the Groq API and return the generated response.

    Args:
        prompt (str): The conversation prompt including context.

    Returns:
        str: The cleaned response text from the Groq API.

    Raises:
        Exception: Propagates any exceptions encountered during the API call.
    """
    client = Groq(api_key=settings.GROQ_API_KEY)
    messages = parse_prompt_to_messages(prompt)
    model = getattr(settings, "DEFAULT_GROQ_MODEL", "deepseek-r1-distill-llama-70b")

    try:
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        response = chat_completion.choices[0].message.content
        logger.info("Prompt sent to LLM:\n%s", prompt)
        logger.info("LLM raw response:\n%s", response)

        cleaned_response = re.sub(r'<think>.*?</think>\s*', '', response, flags=re.DOTALL).strip()
        logger.info("Cleaned LLM response:\n%s", cleaned_response)
        return cleaned_response
    except Exception as e:
        logger.error("LLM API call failed", exc_info=True)
        raise e
