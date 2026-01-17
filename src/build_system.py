import pickle
from preprocessing import load_and_clean
from embedding import create_embeddings
from faiss_index import build_index

jobs = load_and_clean("data/raw/jobs.csv", "Description")
embeddings = create_embeddings(jobs['clean_text'].tolist())

index = build_index(embeddings)

with open("models/index.faiss", "wb") as f:
    pickle.dump(index, f)

jobs.to_csv("data/processed/jobs.csv", index=False)
