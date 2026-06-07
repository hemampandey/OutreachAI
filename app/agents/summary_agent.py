from app.services.llm_service import summarize_research

def summary_node(state):
    summary = summarize_research(state["research_data"])

    return {"summary": summary}