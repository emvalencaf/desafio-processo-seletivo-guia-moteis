from langchain_core.messages import BaseMessage
from pydantic import BaseModel
from typing import Any, Dict, Type, Union
import re
import json

from ia.schema import MetadataSchema

def parser_to_json(content: str) -> Union[dict, list, None]:
    """
    Parses a JSON-formatted string, removing Markdown-style code blocks if present.

    This function cleans the input string by removing triple backticks and optional "json" markers,
    then attempts to parse it into a Python dictionary or list.

    :param content: A string containing JSON data, possibly wrapped in Markdown code blocks.
    :return: A dictionary or list if parsing is successful, otherwise None.
    """
    try:
        # Remove Markdown-style JSON code block markers (```json ... ```)
        cleaned_json_str = re.sub(r'^```json\n?|```$', '', content, flags=re.MULTILINE).strip()
        return json.loads(cleaned_json_str)
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None
    
    
def parser_metadata(raw_metadata: Dict[str, Any]) -> MetadataSchema:
    """
    Parses raw metadata into a structured MetadataSchema object.

    :param raw_metadata: A dictionary containing metadata, including token usage and model name.
    :return: A MetadataSchema instance with structured metadata.
    """
    token_usage: Dict[str, Any] = raw_metadata.get("token_usage", {})

    metadata = {
        "output_tokens": token_usage.get("completion_tokens"),
        "input_tokens": token_usage.get("prompt_tokens"),
        "llm_model": raw_metadata.get("model_name")
    }

    return MetadataSchema(**metadata)

def parser_output(response: BaseMessage, schema: Type[BaseModel]) -> BaseModel:
    """
    Parses the response content and metadata into a structured schema.

    :param response: The message response containing content and metadata.
    :param schema: A Pydantic model class used to validate and structure the parsed output.
    :return: An instance of the provided schema containing the parsed response data.
    """
    json_response = parser_to_json(content=response.content)
    parsed_metadata = parser_metadata(raw_metadata=response.response_metadata)

    parsed = {
        **json_response,
        "metadata": parsed_metadata
    }

    return schema(**parsed)
    