from utils import dataset_loader
import os
import shutil
import random
import matplotlib.pyplot as plt

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image as RLImage
from reportlab.lib.styles import getSampleStyleSheet

# Global variables
current_dataset = None
current_dataset_name = None
current_images_dir = None
uploaded_image_path = None
selected_metric = None
last_evaluation = None


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def show_main_menu():
    clear()
    print("=" * 60)
    print("   Bias-Aware Facial Recognition Evaluation Tool (CLI)   ")
    print("=" * 60)
    print("[1] Load Dataset")
    print("[2] Upload Image")
    print("[3] Select Fairness Metric")
    print("[4] Run Bias Evaluation")
    print("[5] Visualise Results")
    print("[6] Export Report")
    print("[7] About / Help")
    print("[0] Exit")
    print("-" * 60)
    print("Enter your choice (0–7): ", end="")


def load_dataset_menu():
    global current_dataset, current_dataset_name, current_images_dir

    clear()
    print("=" * 60)
    print("               Load Available Datasets")
    print("=" * 60)
    print("[1] UTKFace Dataset")
    print("[2] FairFace Dataset")
    print("[3] Cancel")
    print("-" * 60)
    choice = input("Select dataset to load: ").strip()

    if choice == '1':
        df, msg = dataset_loader.load_utkface_dataset()
        print(msg)
        if df is not None:
            current_dataset = df
            current_dataset_name = "UTKFace"
            current_images_dir = "datasets/UTKFace"
    elif choice == '2':
        df, msg = dataset_loader.load_fairface_dataset()
        print(msg)
        if df is not None:
            current_dataset = df
            current_dataset_name = "FairFace"
            current_images_dir = "datasets/FairFace"
    else:
        print("\n[INFO] Dataset loading cancelled.")

    input("\nPress Enter to return to the main menu...")


def upload_image():
    global uploaded_image_path

    clear()
    print("=" * 60)
    print("               Upload Image for Testing")
    print("=" * 60)

    file_path = input("Enter the full path to the image file: ").strip()

    if not os.path.isfile(file_path):
        print(f"[ERROR] File not found: {file_path}")
    else:
        uploads_dir = "uploads"
        os.makedirs(uploads_dir, exist_ok=True)

        dest_path = os.path.join(uploads_dir, os.path.basename(file_path))
        shutil.copy(file_path, dest_path)
        uploaded_image_path = dest_path
        print(f"[INFO] Image uploaded and saved to: {dest_path}")

    input("\nPress Enter to return to the main menu...")


def select_fairness_metric():
    global selected_metric

    clear()
    print("=" * 60)
    print("              Select Fairness Metric")
    print("=" * 60)
    print("[1] Accuracy by Demographic Group")
    print("[2] Demographic Parity")
    print("[3] Equal Opportunity")
    print("[4] False Positive/Negative Rate by Group")
    print("[0] Cancel")
    print("-" * 60)

    choice = input("Choose a metric (0–4): ").strip()

    metrics = {
        '1': "Accuracy by Demographic Group",
        '2': "Demographic Parity",
        '3': "Equal Opportunity",
        '4': "False Positive/Negative Rate by Group"
    }

    if choice in metrics:
        selected_metric = metrics[choice]
        print(f"[INFO] You selected: {selected_metric}")
    else:
        print("[INFO] Metric selection cancelled.")

    input("\nPress Enter to return to the main menu...")


def run_bias_evaluation():
    global current_dataset, current_dataset_name, selected_metric, last_evaluation

    clear()
    print("=" * 60)
    print("              Run Bias Evaluation")
    print("=" * 60)

    if current_dataset is None:
        print("[ERROR] No dataset loaded. Please load a dataset first.")
        input("\nPress Enter to return to the main menu...")
        return

    if selected_metric is None:
        print("[ERROR] No fairness metric selected. Please choose a metric first.")
        input("\nPress Enter to return to the main menu...")
        return

    print(f"[INFO] Running bias evaluation on: {current_dataset_name}")
    print(f"[INFO] Using metric: {selected_metric}\n")

    last_evaluation = {}

    if "gender" in current_dataset.columns:
        groups = current_dataset["gender"].unique()

        # Map UTKFace numeric genders to Male/Female
        gender_map = {0: "Male", 1: "Female"}

        for group in groups:
            group_size = len(current_dataset[current_dataset["gender"] == group])
            simulated_acc = round(random.uniform(70, 99), 2)
            group_label = gender_map.get(group, str(group))
            last_evaluation[group_label] = simulated_acc
            print(f"Group: {group_label:10s} | Samples: {group_size:5d} | Simulated Accuracy: {simulated_acc}%")
    else:
        print("[WARNING] Dataset does not contain a 'gender' column.")
        print(current_dataset.head())

    input("\nPress Enter to return to the main menu...")


def visualise_results():
    global last_evaluation

    clear()
    print("=" * 60)
    print("              Visualise Results")
    print("=" * 60)

    if not last_evaluation:
        print("[ERROR] No evaluation results found. Please run bias evaluation first.")
        input("\nPress Enter to return to the main menu...")
        return

    groups = list(last_evaluation.keys())
    accuracies = list(last_evaluation.values())

    plt.figure(figsize=(7, 5))
    plt.bar(groups, accuracies, color='skyblue')
    plt.xlabel("Group")
    plt.ylabel("Simulated Accuracy (%)")
    plt.title("Bias Evaluation Results")
    plt.ylim(0, 100)

    for i, v in enumerate(accuracies):
        plt.text(i, v + 1, f"{v}%", ha='center')

    plt.show()


def export_report():
    global last_evaluation, current_dataset_name, selected_metric

    clear()
    print("=" * 60)
    print("              Export Report")
    print("=" * 60)

    if not last_evaluation:
        print("[ERROR] No evaluation results found. Please run bias evaluation first.")
        input("\nPress Enter to return to the main menu...")
        return

    os.makedirs("reports", exist_ok=True)

    # Export CSV
    csv_path = f"reports/{current_dataset_name}_report.csv"
    with open(csv_path, "w") as f:
        f.write("Group,Accuracy\n")
        for group, acc in last_evaluation.items():
            f.write(f"{group},{acc}\n")

    # Save Graph as PNG
    png_path = f"reports/{current_dataset_name}_report.png"
    groups = list(last_evaluation.keys())
    accuracies = list(last_evaluation.values())

    plt.figure(figsize=(7, 5))
    plt.bar(groups, accuracies, color='skyblue')
    plt.xlabel("Group")
    plt.ylabel("Simulated Accuracy (%)")
    plt.title(f"Bias Evaluation Results - {selected_metric}")
    plt.ylim(0, 100)
    for i, v in enumerate(accuracies):
        plt.text(i, v + 1, f"{v}%", ha='center')

    plt.savefig(png_path)
    plt.close()

    # Generate PDF
    pdf_path = f"reports/{current_dataset_name}_report.pdf"
    doc = SimpleDocTemplate(pdf_path, pagesize=A4)
    elements = []

    styles = getSampleStyleSheet()
    title = Paragraph("Bias-Aware Facial Recognition Evaluation Report", styles['Title'])
    subtitle = Paragraph(f"Dataset: {current_dataset_name} <br/> Metric: {selected_metric}", styles['Heading2'])
    elements.extend([title, Spacer(1, 12), subtitle, Spacer(1, 24)])

    # Build results table
    table_data = [["Group", "Accuracy (%)"]]
    for group, acc in last_evaluation.items():
        table_data.append([group, acc])

    table = Table(table_data, hAlign="LEFT")
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    elements.append(Spacer(1, 24))

    # Add chart image
    elements.append(RLImage(png_path, width=400, height=300))

    doc.build(elements)

    print(f"[INFO] Report exported successfully!")
    print(f"       CSV: {csv_path}")
    print(f"       PNG: {png_path}")
    print(f"       PDF: {pdf_path}")

    input("\nPress Enter to return to the main menu...")


def about_section():
    clear()
    print("=" * 60)
    print("                   About / Help")
    print("=" * 60)
    print("""
This tool helps evaluate fairness in facial recognition systems.
It allows users to load datasets, upload test images, select
fairness metrics, and generate visual reports via a CLI interface.

Developed by Rexsan Shanthakumar for MSc Software Engineering
Project at University of Hertfordshire.
    """)
    input("\nPress Enter to return to the main menu...")


def main():
    while True:
        show_main_menu()
        choice = input().strip()
        if choice == '1':
            load_dataset_menu()
        elif choice == '2':
            upload_image()
        elif choice == '3':
            select_fairness_metric()
        elif choice == '4':
            run_bias_evaluation()
        elif choice == '5':
            visualise_results()
        elif choice == '6':
            export_report()
        elif choice == '7':
            about_section()
        elif choice == '0':
            print("\n[INFO] Exiting. Goodbye!")
            break
        else:
            input("\n[ERROR] Invalid choice. Press Enter to try again...")


if __name__ == "__main__":
    main()
