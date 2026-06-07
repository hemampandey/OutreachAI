from app.services.llm_service import evaluate_email

def evaluator_node(state):
    result = evaluate_email(state["email_body"])
    return {
        "score": result["score"],
        "feedback": result["feedback"]
    }

def route_after_evaluation(state):
    if state["score"] >= 8:
        return "database"

    if state["retry_count"] >= 3:
        return "database"

    return "email"