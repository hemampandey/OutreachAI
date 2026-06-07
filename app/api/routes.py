from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import SessionLocal
from app.database import crud

from app.schemas.company import CompanyCreate, CompanyResponse, GraphRunRequest

from app.services.tavily_service import research_company
from app.services.llm_service import summarize_research
from app.database.models import ResearchReport
from app.graph.workflow import graph

from pydantic import BaseModel
from datetime import datetime
from app.services.email_sender import send_gmail_email

class SendEmailRequest(BaseModel):
    report_id: int
    recipient_email: str
    subject: str
    body: str
    sender_email: str | None = None
    app_password: str | None = None

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/company",response_model=CompanyResponse)
def create_company(
    company: CompanyCreate,
    db: Session = Depends(get_db)
):
    return crud.create_company(db, company.name, company.website)

@router.get("/company/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: int,
    db: Session = Depends(get_db)
):
    company = crud.get_company(db,company_id)

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found"
        )
    return company

@router.get("/research/{company_name}")
def research(company_name: str):
    return research_company(company_name)

@router.get("/research-summary/{company_name}")
def research_summary(company_name: str):
    research = research_company(company_name)

    summary = summarize_research(research)

    return {
        "company" : company_name,
        "summary" : summary
    }

@router.post("/graph")
def run_graph(request: GraphRunRequest):
    result = graph.invoke({
        "company_name": request.company_name,
        "sender_company": request.sender_company,
        "pitch_context": request.pitch_context,
        "retry_count": 0,
        "feedback": ""
    })
    return result

@router.get("/history")
def get_history(db: Session = Depends(get_db)):
    reports = (
        db.query(ResearchReport).order_by(ResearchReport.created_at.desc()).all()
    )
    return reports

@router.get("/report/{report_id}")
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = (db.query(ResearchReport).filter(ResearchReport.id == report_id).first())

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return report

@router.post("/send-email")
def send_email(request: SendEmailRequest, db: Session = Depends(get_db)):
    try:
        send_gmail_email(
            to_email=request.recipient_email,
            subject=request.subject,
            body=request.body,
            from_email=request.sender_email,
            app_password=request.app_password
        )
    except ValueError as val_err:
        raise HTTPException(status_code=400, detail=str(val_err))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"SMTP/Gmail error: {str(e)}"
        )

    crud.update_report_sent_status(
        db=db,
        report_id=request.report_id,
        recipient_email=request.recipient_email,
        sent_at=datetime.now()
    )

    return {"status": "success", "message": f"Email successfully sent to {request.recipient_email}"}
