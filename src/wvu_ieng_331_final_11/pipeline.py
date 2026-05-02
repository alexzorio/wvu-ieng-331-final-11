# Imports

import argparse
from pathlib import Path

import altair as alt
import duckdb
import polars as pl
from loguru import logger

from wvu_ieng_331_final_11.queries import (
    get_abc_analysis,
    get_best_sellers,
    get_monthly_revenue,
)
from wvu_ieng_331_final_11.report import generate_excel_report
from wvu_ieng_331_final_11.validation import validate_database


def parse_args():
    """Parses command-line arguments for the pipeline."""
    parser = argparse.ArgumentParser(description="Olist Data Pipeline")
    parser.add_argument(
        "--db-path",
        type=str,
        default="data/olist.duckdb",
        help="Path to DuckDB database",
    )
    parser.add_argument(
        "--start-date", type=str, default="2016-01-01", help="Start date (YYYY-MM-DD)"
    )
    parser.add_argument(
        "--end-date", type=str, default="2018-12-31", help="End date (YYYY-MM-DD)"
    )
    return parser.parse_args()


def main():
    args = parse_args()
    db_path = Path(args.db_path)

    # 1. Error Handling: Check if database file exists
    if not db_path.exists():
        logger.error(f"Database file not found: {db_path}")
        raise FileNotFoundError(f"Database file not found: {db_path}")

    try:
        # 2. Validation
        logger.info("Running database validation...")
        if not validate_database(db_path):
            logger.warning(
                "Validation failed, but continuing pipeline via graceful degradation..."
            )

        # 3. Data Extraction (Queries)
        logger.info("Executing database queries...")
        df_abc_detail = get_abc_analysis(db_path, args.start_date, args.end_date)
        df_best_sellers = get_best_sellers(db_path, args.start_date, args.end_date)
        df_time = get_monthly_revenue(db_path, args.start_date, args.end_date)

        print("\n--- DEBUGGING ---")
        print("Monthly Revenue Data:\n", df_time.head())
        print("Best Sellers Data:\n", df_best_sellers.head())

        # 4. Data Processing (Summarize ABC for the M2 requirements)
        logger.info("Processing data for outputs...")
        df_summary = (
            df_abc_detail.group_by("abc_tier")
            .agg(
                pl.sum("total_revenue").alias("total_revenue"),
                pl.count().alias("item_count"),
            )
            .sort("abc_tier")
        )

        # Setup Output Directory
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        # 5. Save M2 Outputs
        logger.info("Saving M2 Outputs (CSV, Parquet, HTML)...")

        # Detail Parquet
        df_abc_detail.write_parquet(output_dir / "detail.parquet")

        # Summary CSV
        df_summary.write_csv(output_dir / "summary.csv")

        # Exploratory Altair Chart
        pd_summary = df_summary.to_pandas()
        chart = (
            alt.Chart(pd_summary)
            .mark_bar()
            .encode(
                x=alt.X("abc_tier", title="ABC Tier"),
                y=alt.Y("total_revenue", title="Total Revenue"),
            )
            .properties(title="Revenue by ABC Tier")
        )
        chart.save(output_dir / "chart.html")

        # 6. Save Final Deliverable (Excel Report)
        logger.info("Generating Final Excel Deliverable...")
        report_path = output_dir / "report.xlsx"

        generate_excel_report(
            df_abc=df_summary,
            df_time=df_time,
            df_best_sellers=df_best_sellers,
            output_path=report_path,
        )

        logger.info(f"Successfully saved final deliverable to {report_path}")
        logger.info("Pipeline completed successfully!")

    except duckdb.Error as e:
        logger.error(f"A DuckDB database error occurred: {e}")
        raise


if __name__ == "__main__":
    main()
