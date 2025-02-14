# core/llm.py
"""
LLM Integration Module using Groq API.

This module integrates with the Groq API to generate dynamic, human-like responses
based on the conversation context provided in the prompt.

Implementation Details:
- Uses the Groq package (from groq import Groq) to interact with the Groq API.
- The prompt (a multi-line string) is parsed into a list of messages with roles:
  - Lines without a prefix are treated as system messages.
  - Lines starting with "User:" become user messages.
  - Lines starting with "Bot:" become assistant messages.
- Calls the Groq API's chat completions endpoint with these messages and a specified model.
- Cleans the API response by removing any extraneous tags (like <think>...</think>) before returning it.

For more details, refer to the official Groq API documentation:
https://console.groq.com/docs/api-reference#chat-create
"""

import os
import re
from groq import Groq  # Import Groq's client library
from config import settings  # Import settings (which contains GROQ_API_KEY and potentially a default model)


def parse_prompt_to_messages(prompt: str) -> list:
    """
    Parse the prompt string into a list of messages suitable for the Groq API.

    The prompt is expected to be a multi-line string where:
      - Lines starting with "User:" indicate user messages.
      - Lines starting with "Bot:" indicate assistant responses.
      - Other lines are treated as system messages (e.g., personality cues).

    Args:
        prompt (str): The full conversation prompt with personality and history.

    Returns:
        list: A list of dictionaries with keys "role" and "content" as required by the Groq API.
    """
    messages = []
    # Split the prompt into lines and iterate over each line.
    for line in prompt.split("\n"):
        line = line.strip()
        if not line:
            continue  # Skip empty lines
        if line.startswith("User:"):
            # Strip the prefix and create a user message.
            messages.append({"role": "user", "content": line[len("User:"):].strip()})
        elif line.startswith("Bot:"):
            # Strip the prefix and create an assistant message.
            messages.append({"role": "assistant", "content": line[len("Bot:"):].strip()})
        else:
            # Treat any other line as a system message.
            messages.append({"role": "system", "content": line})
    return messages


def get_llm_response(prompt: str) -> str:
    """
    Send a prompt to the Groq API and return the generated response.

    This function:
      1. Creates a Groq client using the API key from settings.
      2. Parses the prompt into a list of messages.
      3. Retrieves the model to use (defaulting to "deepseek-r1-distill-llama-70b" if not specified).
      4. Calls the Groq chat completions API.
      5. Extracts and cleans the response before returning it.

    Args:
        prompt (str): The conversation prompt including personality cues and history.

    Returns:
        str: The cleaned response text from the Groq API.

    Raises:
        Exception: Propagates any exceptions encountered during the API call.
    """
    # Initialize the Groq client using the API key.
    client = Groq(api_key=settings.GROQ_API_KEY)

    # Convert the prompt into a list of message dictionaries.
    messages = parse_prompt_to_messages(prompt)

    # Retrieve the model from settings or use a default value.
    model = getattr(settings, "DEFAULT_GROQ_MODEL", "deepseek-r1-distill-llama-70b")

    try:
        # Call the Groq API to create a chat completion.
        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        # Extract the response from the first choice.
        response = chat_completion.choices[0].message.content
        print(f"That's the prompt sent to the LLM: \n"
              f"{prompt}")
        print(f"That's the response from the LLM including reasoning/thinking: \n"
              f"{response}")

        # Clean up the response by removing any text within <think>...</think> tags.
        cleaned_response = re.sub(r'<think>.*?</think>\s*', '', response, flags=re.DOTALL).strip()
        print(f"That's the clean response from the LLM without reasoning/thinking: \n"
              f"{cleaned_response}")
        return cleaned_response

    except Exception as e:
        # Propagate any exceptions to be handled by the caller.
        raise e
