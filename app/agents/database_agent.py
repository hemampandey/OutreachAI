from app.database.session import SessionLocal
from app.database.crud import save_report

def database_node(state):
    db = SessionLocal()
    try:
        report = save_report(
            db=db,
            company_name=state["company_name"],
            summary=state["summary"],
            email=state["email_body"],
            score=state["score"],
            sender_company=state.get("sender_company"),
            pitch_context=state.get("pitch_context"),
            email_subject=state.get("email_subject")
        )

        return {"report_id": report.id}

    finally:
        db.close()