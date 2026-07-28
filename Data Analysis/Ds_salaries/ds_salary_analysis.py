import os
import json
import pandas as pd
from datetime import datetime

# Import your unified EDA class from the local package
from eda_engine.core import EDA


def main():
    # 1. Setup absolute directory and file paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = "ds_salaries.csv"
    output_plots_dir = os.path.join(current_dir, "plots")

    df = pd.read_csv(data_path)

    # 2. Instantiate your EDA engine facade
    print("\nInitializing your EDA Engine Facade...")
    eda = EDA(df, output_dir=output_plots_dir)

    # 3. Print out a quick console overview using your custom methods
    print("\nStep 1: Structural Overview Summary:")
    print(eda.overview())

    print("\nStep 2: Running full pipeline report & saving visual plots...")
    report_data = eda.report(save_plots=True)

    report_json_path = os.path.join(current_dir, "automated_report.json")
    with open(report_json_path, "w") as f:
        json.dump(report_data, f, indent=4, default=str)

    print(f"\nAnalysis complete!")
    print(f"Plots cleanly generated and saved to: {output_plots_dir}/")
    print(f"Structured JSON data profile saved to: {report_json_path}")


if __name__ == "__main__":
    main()