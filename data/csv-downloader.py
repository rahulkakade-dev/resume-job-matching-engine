import kagglehub
import os
import shutil

# ---- Job descriptions dataset ----
jobs_path = kagglehub.dataset_download("jayakishan225/job-descriptions-dataset")

# find the CSV file
for file in os.listdir(jobs_path):
    if file.endswith(".csv"):
        shutil.copy(
            os.path.join(jobs_path, file),
            "data/raw/jobs.csv"
        )
        break

print("Saved to data/raw/jobs.csv")


# ---- Resume dataset ----
resumes_path = kagglehub.dataset_download("jithinjagadeesh/resume-dataset")

for file in os.listdir(resumes_path):
    if file.endswith(".csv"):
        shutil.copy(
            os.path.join(resumes_path, file),
            "data/raw/resumes.csv"
        )
        break

print("Saved to data/raw/resumes.csv")