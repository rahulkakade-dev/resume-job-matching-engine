from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import traceback

from src.matcher import match_resume

app = FastAPI()


class ResumeRequest(BaseModel):
    resume_text: str


# Lazily try to load heavy dependencies. If they fail, the app still starts
# and the endpoint will return a 503 with a helpful message.
model = None
index = None
jobs_df = None
load_errors = []

try:
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    load_errors.append(f"SentenceTransformer load error: {e}")

try:
    # prefer faiss native index loader when available
    import faiss
    try:
        index = faiss.read_index("models/index.faiss")
    except Exception:
        # fallback: if index was pickled (older flows)
        import pickle
        with open("models/index.faiss", "rb") as f:
            index = pickle.load(f)
except Exception as e:
    load_errors.append(f"FAISS/index load error: {e}")

try:
    jobs_df = pd.read_csv("data/processed/jobs.csv")
except Exception as e:
    load_errors.append(f"jobs.csv load error: {e}")


@app.post("/match")
def match_resume_api(request: ResumeRequest):
    if model is None or index is None or jobs_df is None:
        detail = {
            "message": "Model, index, or jobs data not loaded.",
            "errors": load_errors,
        }
        raise HTTPException(status_code=503, detail=detail)

    try:
        emb = model.encode([request.resume_text])[0]
        results = match_resume(emb, index, jobs_df)

        # Normalize output to keys expected by the frontend
        records = results.copy()
        if 'score' not in records.columns:
            records['score'] = None

        out = []
        for _, row in records.iterrows():
            out.append({
                'job_title': row.get('Job Title', row.get('job_title', '')),
                'description': row.get('Description', row.get('description', '')),
                'score': float(row['score']) if pd.notnull(row['score']) else None,
                'company': row.get('Company', row.get('company', '')),
            })

        return out
    except Exception as e:
        tb = traceback.format_exc()
        raise HTTPException(status_code=500, detail={"error": str(e), "traceback": tb})
