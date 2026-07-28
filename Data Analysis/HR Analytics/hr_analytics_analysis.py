import os
import json
import pandas as pd
from eda_engine.core import EDA


def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = "aug_train.csv"
    output_plots_dir = os.path.join(current_dir, "plots")

    df = pd.read_csv(data_path)

    print("\nInitializing EDA Engine Facade...")
    eda = EDA(df, output_dir=output_plots_dir)

    print("\n Structural Overview Summary:")
    print(eda.overview())

    print("\n Running full pipeline report & saving visual plots...")
    report_data = eda.report(save_plots=True)

    report_json_path = os.path.join(current_dir, "automated_report.json")
    with open(report_json_path, "w") as f:
        json.dump(report_data, f, indent=4, default=str)

    print(f"\n Analysis complete!")
    print(f" Plots cleanly generated and saved to: {output_plots_dir}/")
    print(f" Structured JSON data profile saved to: {report_json_path}")


if __name__ == "__main__":
    main()