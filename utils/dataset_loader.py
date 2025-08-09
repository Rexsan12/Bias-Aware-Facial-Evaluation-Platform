import pandas as pd
import os

def _verify_images_exist(df, images_dir):
    """
    Check if all images listed in the dataframe exist in the given directory.
    Returns a list of missing image names.
    """
    missing_images = [
        img for img in df['image_path']
        if not os.path.exists(os.path.join(images_dir, img))
    ]
    return missing_images


def load_fairface_dataset():
    csv_path = 'datasets/fairface_labels.csv'
    images_dir = 'datasets/FairFace'

    if not os.path.exists(csv_path):
        return None, "[ERROR] FairFace labels file not found."
    if not os.path.exists(images_dir):
        return None, "[ERROR] FairFace images folder not found."

    try:
        df = pd.read_csv(csv_path)

        required_cols = {'file', 'gender', 'race'}
        if not required_cols.issubset(df.columns):
            return None, f"[ERROR] Missing columns in CSV: {required_cols - set(df.columns)}"

        df = df.rename(columns={'file': 'image_path'})

        missing_images = _verify_images_exist(df, images_dir)
        msg = f"[INFO] FairFace loaded successfully with {len(df)} records."
        if missing_images:
            msg += f" WARNING: {len(missing_images)} images missing."

        return df, msg

    except Exception as e:
        return None, f"[ERROR] Failed to load FairFace dataset: {e}"


def load_utkface_dataset():
    csv_path = 'datasets/utkface_labels.csv'
    images_dir = 'datasets/UTKFace'

    if not os.path.exists(csv_path):
        return None, "[ERROR] UTKFace labels file not found."
    if not os.path.exists(images_dir):
        return None, "[ERROR] UTKFace images folder not found."

    try:
        df = pd.read_csv(csv_path)

        required_cols = {'image_path', 'gender', 'race'}
        if not required_cols.issubset(df.columns):
            return None, f"[ERROR] Missing columns in CSV: {required_cols - set(df.columns)}"

        missing_images = _verify_images_exist(df, images_dir)
        msg = f"[INFO] UTKFace loaded successfully with {len(df)} records."
        if missing_images:
            msg += f" WARNING: {len(missing_images)} images missing."

        return df, msg

    except Exception as e:
        return None, f"[ERROR] Failed to load UTKFace dataset: {e}"
