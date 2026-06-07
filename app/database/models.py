from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from datetime import datetime
from .session import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    website = Column(String, nullable=True)

class ResearchReport(Base):
    __tablename__ = "research_reports"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(Text)
    sender_company = Column(Text, nullable=True)
    pitch_context = Column(Text, nullable=True)
    summary = Column(Text)
    email = Column(Text)
    email_subject = Column(Text, nullable=True)
    recipient_email = Column(Text, nullable=True)
    sent_at = Column(DateTime, nullable=True)
    score = Column(Float)

    created_at = Column(DateTime, default=datetime.now)