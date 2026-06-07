from app.services.tavily_service import research_company

def research_node(state):
    research = research_company(state["company_name"])

    return {"research_data" : research}