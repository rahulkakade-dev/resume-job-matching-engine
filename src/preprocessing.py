import pandas as pd
import re

def clean_text(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z ]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def load_and_clean(path, text_col):
    df = pd.read_csv(path)
    df['clean_text'] = df[text_col].astype(str).apply(clean_text)
    return df
