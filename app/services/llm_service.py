from pydantic import BaseModel
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate

llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0.2
)

summary_prompt = ChatPromptTemplate.from_template(
    """
    You are a company research analyst.

    Research Data:
    {research}

    Provide:

    1. Company Overview
    2. Main Products
    3. Recent News
    4. Potential Outreach Angles

    Keep it concise.
    """
)

def summarize_research(research_data):
    chain = summary_prompt | llm
    result = chain.invoke(
        {"research": str(research_data)}
    )
    return result.content


email_prompt = ChatPromptTemplate.from_template("""
You are an expert sales outreach writer.

Sender's Company: {sender_company}
Pitch Context / Value Proposition: {pitch_context}

Recipient Company Name: {company_name}
Recipient Company Research Summary: {summary}

Previous Feedback:
{feedback}
                                                
If feedback exists, improve the email based on it.
                                                
Generate:

1. Subject Line
2. Professional personalized cold email

Rules:
- Make sure to write the email from the perspective of {sender_company} offering the value proposition described in {pitch_context}.
- Mention recipient company-specific information
- Mention recent news if available
- Under 100 words
- Professional tone

Return JSON:

{{
    "subject" : ...
    "body" : ...
}}                                        
""")

def generate_email(company_name, summary, sender_company, pitch_context, feedback):

    class email(BaseModel):
        subject : str
        body : str

    structured_llm = llm.with_structured_output(email)
    chain = email_prompt | structured_llm

    result = chain.invoke({
        "company_name": company_name,
        "summary": summary,
        "sender_company": sender_company,
        "pitch_context": pitch_context,
        "feedback" : feedback
    })
    return {
        "subject" : result.subject,
        "body" : result.body
    }

evaluation_prompt = ChatPromptTemplate.from_template("""
Evaluate this outreach email.

Email:
{email}

Score from 1-10 for:

1. Personalization
2. Clarity
3. Professionalism
4. Relevance

Return JSON:

{{
    "score": 8.5,
    "feedback": "..."
}}
""")

def evaluate_email(email):
    class EvaluationResult(BaseModel):
        score: float
        feedback: str

    structured_llm = llm.with_structured_output(EvaluationResult)
    chain = evaluation_prompt | structured_llm
    result = chain.invoke({"email":email})

    return {
        "score" : result.score,
        "feedback" : result.feedback
    }