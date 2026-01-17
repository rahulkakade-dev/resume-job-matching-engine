import numpy as np

def match_resume(resume_embedding, index, jobs_df, top_k=5):
    D, I = index.search(np.array([resume_embedding]), top_k)
    results = jobs_df.iloc[I[0]].copy()
    results['score'] = D[0]
    return results
