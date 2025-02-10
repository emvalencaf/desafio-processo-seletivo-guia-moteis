import requests
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
from decimal import Decimal

class WhereScrappingAPITokensPriceSchema(BaseModel):
    """
    Schema for filtering API token price data based on provider and model ID.
    """
    provider: Optional[str]
    model_id: Optional[str]

class TokenPriceScrappingSchema(BaseModel):
    """
    Schema representing the token pricing details for a specific model and provider.
    """
    provider: str = Field(description="The name of the AI service provider (e.g., OpenAI, Anthropic).")
    model_id: str = Field(description="The model identifier (e.g., 'gpt-4', 'claude-2').")
    input_tokens: Decimal = Field(description="The price per 1 million input tokens (in USD).")
    output_tokens: Decimal = Field(description="The price per 1 million output tokens (in USD).")
  

def fetch_html(url: str) -> str:
    """
    Makes an HTTP request to the provided URL and returns the page's HTML content.

    :param url: URL of the page to be requested.
    :return: HTML content of the page.
    """
    response = requests.get(url)
    response.raise_for_status()
    
    return response.text


def parse_html(html: str) -> BeautifulSoup:
    """
    Parses the HTML and returns a BeautifulSoup object.

    :param html: HTML content of the page.
    :return: BeautifulSoup object for HTML analysis.
    """
    return BeautifulSoup(html, 'html.parser')

def extract_table_data(soup: BeautifulSoup,
                       where: Optional[WhereScrappingAPITokensPriceSchema] = None) -> List[TokenPriceScrappingSchema]:
    """
    Extracts data from the HTML table and returns a list of structured data.

    :param soup: BeautifulSoup object containing the parsed HTML.
    :param where: Optional filtering conditions based on provider and model_id.
    :return: List of TokenPriceScrappingSchema objects with extracted table data.
    """
    table = soup.find('table')
    if not table:
        return []

    rows = table.find("tbody").find_all("tr")
    data = []

    for row in rows:
        cells = row.find_all("td")
        print(cells)
        if not cells:
            continue

        provider = cells[0].text.strip()
        if where and where.provider and provider != where.provider:
          continue

        model_id = cells[1].find("div").text.strip() if cells[1].find("div") else None
        if not model_id:
          model_id = cells[1].find("a")["href"].split('/')[2].strip() if cells[1].find("a") else cells[1].text
        if where and where.model_id and model_id != where.model_id:
          continue
        
        input_price = cells[3].text.strip().replace("$", "")
        output_price = cells[4].text.strip().replace("$", "")
        print(model_id)
        price = TokenPriceScrappingSchema(provider=provider,
                                          model_id=model_id,
                                          input_tokens=Decimal(input_price),
                                          output_tokens=Decimal(output_price))
        
        data.append(price)

    return data

def extract_model_price_details(model_id: Optional[str] = None,
                                provider: Optional[str] = None) -> List[TokenPriceScrappingSchema]:
    """
    Extracts model pricing details from the DocsBot AI pricing page.

    :param model_id: Optional model identifier to filter results.
    :param provider: Optional provider name to filter results.
    :return: List of TokenPriceScrappingSchema objects containing model pricing details.
    """
    html = fetch_html(url="https://docsbot.ai/tools/gpt-openai-api-pricing-calculator/")
    soup = parse_html(html=html)
    
    where_filter = WhereScrappingAPITokensPriceSchema(model_id=model_id,
                                                      provider=provider) if model_id or provider else None
    
    price_table = extract_table_data(soup=soup,
                                     where=where_filter)
    
    return price_table