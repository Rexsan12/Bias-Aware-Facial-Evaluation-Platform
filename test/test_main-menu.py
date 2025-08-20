import pytest
import builtins
import os
from io import StringIO
import sys
import main


def run_main_with_inputs(inputs, monkeypatch):
    """
    Helper to simulate multiple user inputs and capture printed output.
    """
    input_iter = iter(inputs)
    monkeypatch.setattr(builtins, "input", lambda *args: next(input_iter))

    captured_output = StringIO()
    sys_stdout = sys.stdout
    sys.stdout = captured_output

    try:
        main.main()
    except StopIteration:
        # StopIteration is raised when inputs run out
        pass
    finally:
        sys.stdout = sys_stdout

    return captured_output.getvalue()


# -------------------------------
# MAIN MENU BEHAVIOUR
# -------------------------------

def test_exit_program(monkeypatch):
    output = run_main_with_inputs(["0"], monkeypatch)
    assert "Exiting. Goodbye!" in output



def test_about_section(monkeypatch):
    output = run_main_with_inputs(["7", "", "0"], monkeypatch)
    assert "About / Help" in output
    assert "Bias-Aware Facial Recognition" in output


# -------------------------------
# DATASET LOADING
# -------------------------------

def test_load_utkface_dataset(monkeypatch):
    fake_df = "FAKE_DF"
    monkeypatch.setattr(
        "utils.dataset_loader.load_utkface_dataset",
        lambda: (fake_df, "[INFO] UTKFace loaded successfully with 100 records."),
    )

    output = run_main_with_inputs(["1", "1", "", "0"], monkeypatch)
    assert "UTKFace loaded successfully" in output


def test_load_fairface_dataset(monkeypatch):
    fake_df = "FAKE_DF"
    monkeypatch.setattr(
        "utils.dataset_loader.load_fairface_dataset",
        lambda: (fake_df, "[INFO] FairFace loaded successfully with 200 records."),
    )

    output = run_main_with_inputs(["1", "2", "", "0"], monkeypatch)
    assert "FairFace loaded successfully" in output


# --------------
# IMAGE UPLOAD
# --------------

def test_upload_image(monkeypatch, tmp_path):
    # Create a fake image file
    fake_img = tmp_path / "test.jpg"
    fake_img.write_text("fake image content")

    inputs = ["2", str(fake_img), "", "0"]
    output = run_main_with_inputs(inputs, monkeypatch)

    assert "Image uploaded and saved to" in output
    assert os.path.exists("uploads/test.jpg")


# -------------------------------
# FAIRNESS METRIC SELECTION
# -------------------------------

def test_select_fairness_metric(monkeypatch):
    output = run_main_with_inputs(["3", "1", "", "0"], monkeypatch)
    assert "You selected: Accuracy by Demographic Group" in output


# -------------------------------
# BIAS EVALUATION + VISUALISATION
# -------------------------------

def test_bias_evaluation_and_visualisation(monkeypatch):
    import pandas as pd
    df = pd.DataFrame({"gender": [0, 1, 0, 1]})
    main.current_dataset = df
    main.current_dataset_name = "UTKFace"
    main.selected_metric = "Accuracy by Demographic Group"

    # Bias evaluation
    inputs = ["4", "", "0"]
    output = run_main_with_inputs(inputs, monkeypatch)
    assert "Running bias evaluation on: UTKFace" in output
    assert "Group:" in output

    # Simulate results for visualization
    main.last_evaluation = {"Male": 90, "Female": 85}
    inputs = ["5", "", "0"]
    output = run_main_with_inputs(inputs, monkeypatch)
    assert "Visualise Results" in output


# -------------------------------
# EXPORT REPORT
# -------------------------------

def test_export_report(monkeypatch):
    main.last_evaluation = {"Male": 90, "Female": 85}
    main.current_dataset_name = "UTKFace"
    main.selected_metric = "Accuracy by Demographic Group"

    inputs = ["6", "", "0"]
    output = run_main_with_inputs(inputs, monkeypatch)

    assert "Report exported successfully!" in output
    assert os.path.exists("reports/UTKFace_report.csv")
    assert os.path.exists("reports/UTKFace_report.png")
    assert os.path.exists("reports/UTKFace_report.pdf")

