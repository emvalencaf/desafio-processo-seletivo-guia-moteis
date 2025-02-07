from typing import List
from prisma.models import message

def format_messages(messages: List[message]) -> List[str]:
    """
    Formats a list of messages by sorting them by creation date and transforming each message
    into a dictionary with relevant details.

    :param messages: A list of message objects to be formatted.
    :return: A list of strings, each containing the role and content of a message.
    """
    # Sort the list of messages by creation date
    sorted_messages = sorted(messages, key=lambda msg: msg.created_at, reverse=False)

    # Create the formatted list
    formatted_messages = [
        f"{'user' if msg.remote else 'bot'}:{msg.content}"

        for msg in sorted_messages
    ]
    
    return formatted_messages