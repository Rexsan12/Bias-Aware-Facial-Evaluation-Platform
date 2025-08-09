import os
import csv

# Update this path if your images are stored elsewhere
image_folder = 'datasets/UTKFace'
output_csv = 'datasets/utkface_labels.csv'

# Ensure dataset folder exists
if not os.path.isdir(image_folder):
    print(f"[ERROR] Image folder not found: {image_folder}")
    exit(1)

# CSV header
header = ['image_path', 'age', 'gender', 'race']
rows = []

for filename in os.listdir(image_folder):
    if filename.lower().endswith('.jpg'):
        parts = filename.split('_')
        if len(parts) < 4:
            print(f"[WARNING] Skipping unexpected filename: {filename}")
            continue
        try:
            age = int(parts[0])
            gender = int(parts[1])
            race = int(parts[2])
            rows.append([filename, age, gender, race])
        except ValueError:
            print(f"[WARNING] Could not parse labels from: {filename}")
            continue

if not rows:
    print("[ERROR] No valid filenames found in folder.")
    exit(1)

# Write to CSV
with open(output_csv, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(header)
    writer.writerows(rows)

print(f"[INFO] Output written to {output_csv} ({len(rows)} records)")
