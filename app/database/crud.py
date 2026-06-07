from sqlalchemy.orm import Session
from .models import Company, ResearchReport

def create_company(db: Session, name: str, website: str | None = None):
    company = Company(name=name, website=website)

    db.add(company)
    db.commit()
    db.refresh(company)

    return company

def get_company(db: Session, company_id: int):
    return (db.query(Company).filter(Company.id == company_id).first())

def save_report(db, company_name, summary, email, score, sender_company=None, pitch_context=None, email_subject=None):
    report = ResearchReport(
        company_name=company_name,
        sender_company=sender_company,
        pitch_context=pitch_context,
        summary=summary,
        email=email,
        email_subject=email_subject,
        score=score
    )

    db.add(report)
    db.commit()
    db.refresh(report)

    return report

def update_report_sent_status(db: Session, report_id: int, recipient_email: str, sent_at):
    report = db.query(ResearchReport).filter(ResearchReport.id == report_id).first()
    if report:
        report.recipient_email = recipient_email
        report.sent_at = sent_at
        db.commit()
        db.refresh(report)
    return report