from typing import TypedDict

class ResearchState(TypedDict):
    company_name : str
    sender_company : str
    pitch_context : str
    
    research_data : dict
    summary : str
    email_body : str

    score : float
    feedback : str

    report_id : int

    retry_count: int