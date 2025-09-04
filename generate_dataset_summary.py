import pandas as pd
from utils import dataset_loader
import os

def summarize_dataset(df, dataset_name, output_dir="reports"):
    """
    Generate demographic summary statistics for a dataset and save as CSV.
    """
    os.makedirs(output_dir, exist_ok=True)

    summary = {}

    # ---- Age Distribution ----
    if "age" in df.columns:
        if pd.api.types.is_numeric_dtype(df["age"]):
            # UTKFace: numeric ages → bin them
            bins = [0, 10, 20, 30, 40, 50, 60, 200]  # 8 edges = 7 intervals
            labels = ["0–9", "10–19", "20–29", "30–39", "40–49", "50–59", "60+"]
            df["age_bin"] = pd.cut(df["age"], bins=bins, labels=labels, right=False)
            age_counts = df["age_bin"].value_counts().sort_index()
        else:
            # FairFace: age already in string ranges (e.g. "0-2", "3-9", "60+")
            age_counts = df["age"].value_counts().sort_index()

        summary["Age Distribution"] = age_counts

    # ---- Gender Distribution ----
    if "gender" in df.columns:
        gender_map = {0: "Male", 1: "Female"}  # UTKFace numeric genders
        if pd.api.types.is_numeric_dtype(df["gender"]):
            df["gender_label"] = df["gender"].map(gender_map).fillna(df["gender"].astype(str))
        else:
            df["gender_label"] = df["gender"]
        gender_counts = df["gender_label"].value_counts()
        summary["Gender Distribution"] = gender_counts

    # ---- Race Distribution ----
    if "race" in df.columns:
        race_map = {
            0: "White",
            1: "Black",
            2: "Asian",
            3: "Indian",
            4: "Others"
        }
        if pd.api.types.is_numeric_dtype(df["race"]):
            df["race_label"] = df["race"].map(race_map).fillna(df["race"].astype(str))
        else:
            df["race_label"] = df["race"]
        race_counts = df["race_label"].value_counts()
        summary["Race Distribution"] = race_counts

    # ---- Save summary to CSV ----
    output_path = os.path.join(output_dir, f"{dataset_name}_summary.csv")
    with open(output_path, "w") as f:
        for section, counts in summary.items():
            f.write(f"{section}\n")
            counts.to_csv(f, header=True)
            f.write("\n")

    print(f"[INFO] {dataset_name} summary saved to {output_path}")


if __name__ == "__main__":
    # UTKFace
    df_utk, msg1 = dataset_loader.load_utkface_dataset()
    print(msg1)
    if df_utk is not None:
        summarize_dataset(df_utk, "UTKFace")

    # FairFace
    df_fair, msg2 = dataset_loader.load_fairface_dataset()
    print(msg2)
    if df_fair is not None:
        summarize_dataset(df_fair, "FairFace")
