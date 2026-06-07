from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path

from app.database.session import Base, engine
from app.api.routes import router
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

def run_migrations():
    with engine.connect() as conn:
        for query in [
            "ALTER TABLE research_reports ADD COLUMN IF NOT EXISTS email_subject TEXT;",
            "ALTER TABLE research_reports ADD COLUMN IF NOT EXISTS recipient_email TEXT;",
            "ALTER TABLE research_reports ADD COLUMN IF NOT EXISTS sent_at TIMESTAMP WITHOUT TIME ZONE;"
        ]:
            try:
                conn.execute(text(query))
                conn.execute(text("COMMIT;"))
            except Exception as e:
                print(f"Skipping migration query '{query}' due to: {e}")

run_migrations()

app = FastAPI(title="Email Research Agent")

# CORS (for development convenience)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api")

STATIC_DIR = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/")
def root():
    return FileResponse(str(STATIC_DIR / "index.html"))