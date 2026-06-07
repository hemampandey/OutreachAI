from langgraph.graph import StateGraph
from langgraph.graph import START, END

from app.graph.state import ResearchState

from app.agents.research_agent import research_node
from app.agents.email_agent import email_node
from app.agents.summary_agent import summary_node
from app.agents.evaluator_agent import evaluator_node, route_after_evaluation
from app.agents.database_agent import database_node

builder = StateGraph(ResearchState)

builder.add_node("research",research_node)
builder.add_node("summary",summary_node)
builder.add_node("email",email_node)
builder.add_node("evaluator",evaluator_node)
builder.add_node("database",database_node)

builder.add_edge(START,"research")
builder.add_edge("research","summary")
builder.add_edge("summary","email")
builder.add_edge("email","evaluator")
builder.add_conditional_edges(
    "evaluator",
    route_after_evaluation,
    {
        "email": "email",
        "database": "database"
    }
)
builder.add_edge("database",END)

graph = builder.compile()