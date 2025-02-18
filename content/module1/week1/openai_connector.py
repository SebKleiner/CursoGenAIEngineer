import asyncio
from typing import List, Dict
import os
from openai import AsyncOpenAI

MODEL_TEMPERATURE = 0
REPLY_MAX_TOKENS = 1000


class OpenaiConnector:
    def __init__(self, api_key: str) -> None:
        """
        Initializes an instance of OpenaiConnector asynchronously.

        Args:
            api_key (str): API key for OpenAI.
        """
        os.environ["OPENAI_API_KEY"] = api_key
        self.total_tokens_consumed = 0
        self.client = AsyncOpenAI()  # Use async OpenAI client

    async def get_gpt_reply(self,
                            prompt: List[Dict[str, str]],
                            temperature: float = MODEL_TEMPERATURE,
                            max_tokens: int = REPLY_MAX_TOKENS,
                            response_format=None,
                            model: str = 'gpt-4o') -> str:
        """Asynchronously generates a GPT reply based on the given prompt.

        Args:
            prompt (List[Dict[str, str]]): A list of messages in the conversation prompt.
            model (str): The model to use for generating the reply. Defaults to 'gpt-4o'.
            temperature (float): Controls the randomness of the reply. Defaults to MODEL_TEMPERATURE.
            max_tokens (int): The maximum number of tokens in the generated reply. Defaults to REPLY_MAX_TOKENS.

        Returns:
            str: The generated GPT reply.
        """
        response = await self.client.chat.completions.create(
            model=model,
            messages=prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )

        return response.choices[0].message.content

OPEN_AI_KEY = os.getenv('OPENAI_API_KEY')
OPEN_AI_CONNECTOR = OpenaiConnector(api_key=OPEN_AI_KEY)
