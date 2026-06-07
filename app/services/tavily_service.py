from tavily import TavilyClient
from app.config import TAVILY_API_KEY

client = TavilyClient(api_key=TAVILY_API_KEY)

def research_company(company_name: str):
    query = f"""
    {company_name}
    company overview
    recent news
    products
    funding
    """

    response = client.search(
        query=query,
        search_depth="advanced",
        max_results=5
    )

    return response