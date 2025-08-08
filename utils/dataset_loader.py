import pandas as pd

def load_utkface_dataset():
    try:
        df = pd.read_csv('datasets/utkface_labels.csv')
        return df, "UTKFace dataset loaded successfully."
    except Exception as e:
        return None, f"Error loading UTKFace: {e}"

def load_fairface_dataset():
    try:
        df = pd.read_csv('datasets/fairface_labels.csv')
        return df, "FairFace dataset loaded successfully."
    except Exception as e:
        return None, f"Error loading FairFace: {e}"