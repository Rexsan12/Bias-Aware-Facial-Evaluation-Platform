from utils import dataset_loader
import os

# Global variables to hold dataset info
current_dataset = None
current_dataset_name = None
current_images_dir = None

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

def placeholder_action(action_name):
    clear()
    print("=" * 60)
    print(f"            {action_name}            ")
    print("=" * 60)
    print(f"\n[INFO] '{action_name}' functionality will be implemented.")
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
            placeholder_action("Upload Image")
        elif choice == '3':
            placeholder_action("Select Fairness Metric")
        elif choice == '4':
            placeholder_action("Run Bias Evaluation")
        elif choice == '5':
            placeholder_action("Visualise Results")
        elif choice == '6':
            placeholder_action("Export Report")
        elif choice == '7':
            about_section()
        elif choice == '0':
            print("\n[INFO] Exiting. Goodbye!")
            break
        else:
            input("\n[ERROR] Invalid choice. Press Enter to try again...")

if __name__ == "__main__":
    main()
from utils import dataset_loader
import os

# Global variables to hold dataset info
current_dataset = None
current_dataset_name = None
current_images_dir = None

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

def placeholder_action(action_name):
    clear()
    print("=" * 60)
    print(f"            {action_name}            ")
    print("=" * 60)
    print(f"\n[INFO] '{action_name}' functionality will be implemented.")
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
            placeholder_action("Upload Image")
        elif choice == '3':
            placeholder_action("Select Fairness Metric")
        elif choice == '4':
            placeholder_action("Run Bias Evaluation")
        elif choice == '5':
            placeholder_action("Visualise Results")
        elif choice == '6':
            placeholder_action("Export Report")
        elif choice == '7':
            about_section()
        elif choice == '0':
            print("\n[INFO] Exiting. Goodbye!")
            break
        else:
            input("\n[ERROR] Invalid choice. Press Enter to try again...")

if __name__ == "__main__":
    main()
