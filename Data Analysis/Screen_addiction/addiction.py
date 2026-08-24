from eda_engine.core import EDA
import pandas as pd
import os
import json


def main():
    data_path = "train.csv"
    current_dir = os.getcwd()

    plot_dir = os.path.join(current_dir, "plots")

    try:
        df = pd.read_csv(data_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(data_path, encoding="latin-1")

    eda = EDA(df, output_dir=plot_dir)
    print(eda.overview())

    report_data = eda.report(save_plots=True)

    report_json_path = os.path.join(current_dir, "automated_report.json")
    with open(report_json_path, "w") as f:
        json.dump(report_data, f,indent=4,default=str)

    print(f"\nAnalysis complete!")
    print(f"Plots cleanly generated and saved to: {plot_dir}/")
    print(f"Structured JSON data profile saved to: {report_json_path}")

if __name__ == "__main__":
     main()
