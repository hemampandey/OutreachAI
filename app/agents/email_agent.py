from app.services.llm_service import generate_email

def email_node(state):
    email = generate_email(
        company_name=state["company_name"],
        summary=state["summary"],
        sender_company=state.get("sender_company", "Our Company"),
        pitch_context=state.get("pitch_context", ""),
        feedback=state.get("feedback", "")
    )
    return {
        "email_subject" : email["subject"],
        "email_body": email["body"],
        "retry_count": state["retry_count"] + 1
    }

