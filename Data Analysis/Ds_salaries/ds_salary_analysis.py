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
    print("\n🚀 Initializing your EDA Engine Facade...")
    eda = EDA(df, output_dir=output_plots_dir)

    # 3. Print out a quick console overview using your custom methods
    print("\n🔍 Step 1: Structural Overview Summary:")
    print(eda.overview())

    print("\n🛡️ Step 2: Running full pipeline report & saving visual plots...")
    # This automatically invokes schema.detect(), quality.analyze(), profiler.profile(),
    # and visualizer.generate_all_plots() saving them to the output_dir
    report_data = eda.report(save_plots=True)

    # 4. Save the raw JSON statistics profile text to the folder for documentation reference
    # Cleaning up non-serializable objects (like sets or sub-dataframes) if present
    serializable_report = {}
    for key, val in report_data.items():
        if key in ["quality", "statistics"]:
            serializable_report[key] = val

    report_json_path = os.path.join(current_dir, "automated_report.json")
    with open(report_json_path, "w") as f:
        json.dump(serializable_report, f, indent=4, default=str)

    print(f"\n✅ Analysis complete!")
    print(f"🎨 Plots cleanly generated and saved to: {output_plots_dir}/")
    print(f"📄 Structured JSON data profile saved to: {report_json_path}")


if __name__ == "__main__":
    main()