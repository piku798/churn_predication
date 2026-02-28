from pathlib import Path
from ydata_profiling import ProfileReport

from src.data.data_loader import load_raw_data
from src.data.data_preprocessing import preprocess_data


def run_eda():

    # Project root
    BASE_DIR = Path(__file__).resolve().parents[2]

    data_path = BASE_DIR / "data" / "raw" / "WA_Fn-UseC_-Telco-Customer-Churn.csv"
    report_path = BASE_DIR / "reports"
    report_path.mkdir(exist_ok=True)

    # Load + preprocess
    df = load_raw_data(data_path)
    df = preprocess_data(df)

    # Generate report
    profile = ProfileReport(
        df,
        title="Customer Churn EDA Report",
        explorative=True
    )

    output_file = report_path / "eda_report.html"
    profile.to_file(output_file)

    print(f"✅ EDA report saved at {output_file}")


if __name__ == "__main__":
    run_eda()