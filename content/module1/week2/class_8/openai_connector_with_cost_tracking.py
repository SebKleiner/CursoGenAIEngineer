import asyncio
import os
from typing import List, Dict
from openai import AsyncOpenAI
from supabase import create_client, Client

# Constants
MODEL_TEMPERATURE = 0
REPLY_MAX_TOKENS = 1000
OPENAI_PRICING = {
    'gpt-4o': {'input': 0.005 / 1000, 'output': 0.015 / 1000},
    'gpt-4-turbo': {'input': 0.01 / 1000, 'output': 0.03 / 1000},
    'gpt-3.5-turbo': {'input': 0.0005 / 1000, 'output': 0.0015 / 1000}
}

# Get environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


class OpenaiConnector:
    def __init__(self, api_key: str) -> None:
        """
        Initializes an instance of OpenaiConnector asynchronously.

        Args:
            api_key (str): API key for OpenAI.
        """
        os.environ["OPENAI_API_KEY"] = api_key
        self.client = AsyncOpenAI()  # Use async OpenAI client

    async def get_gpt_reply(self,
                            prompt: List[Dict[str, str]],
                            temperature: float = MODEL_TEMPERATURE,
                            max_tokens: int = REPLY_MAX_TOKENS,
                            response_format=None,
                            model: str = 'gpt-4o') -> str:
        """Asynchronously generates a GPT reply based on the given prompt, tracks token usage, and logs cost to Supabase.

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

        reply_content = response.choices[0].message.content
        usage = response.usage

        if usage:
            input_tokens = usage.prompt_tokens
            output_tokens = usage.completion_tokens
            total_tokens = usage.total_tokens
            cost = self.calculate_cost(model, input_tokens, output_tokens)

            # Save cost to Supabase
            await self.save_request_cost(model, input_tokens, output_tokens, total_tokens, cost)

        return reply_content

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """Calculates the cost of an OpenAI request based on the model and token usage."""
        if model in OPENAI_PRICING:
            input_cost = input_tokens * OPENAI_PRICING[model]["input"]
            output_cost = output_tokens * OPENAI_PRICING[model]["output"]
            return round(input_cost + output_cost, 6)  # Round to 6 decimal places
        return 0.0

    async def save_request_cost(self, model: str, input_tokens: int, output_tokens: int, total_tokens: int, cost: float):
        """Inserts request cost details into Supabase."""
        data = {
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost": cost
        }
        response = supabase.table("openai_requests").insert(data).execute()
        return response


# Initialize OpenAI Connector
OPEN_AI_CONNECTOR = OpenaiConnector(api_key=OPENAI_API_KEY)
