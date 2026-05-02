from pathlib import Path

import polars as pl
import xlsxwriter


def generate_excel_report(
    df_abc: pl.DataFrame,
    df_time: pl.DataFrame,
    df_best_sellers: pl.DataFrame,
    output_path: Path,
) -> None:
    """Generates a formatted Excel report with an analytical narrative and embedded charts."""

    workbook = xlsxwriter.Workbook(output_path)
    header_format = workbook.add_format(
        {"bold": True, "bg_color": "#D3D3D3", "border": 1}
    )
    title_format = workbook.add_format({"bold": True, "font_size": 14})

    # ==========================================
    # SHEET 1: Analytical Narrative
    # ==========================================
    ws_narrative = workbook.add_worksheet("Executive Summary")
    ws_narrative.set_column("A:A", 80)

    ws_narrative.write("A1", "Olist Business Performance Report", title_format)
    ws_narrative.write(
        "A3", "State of the Business:", workbook.add_format({"bold": True})
    )
    ws_narrative.write(
        "A4",
        "Olist relies heavily on a small fraction of products (Tier A) for the vast majority of revenue. While overall revenue shows historical growth, our seller reliance is also highly concentrated.",
    )

    ws_narrative.write(
        "A6", "Problems & Opportunities:", workbook.add_format({"bold": True})
    )
    ws_narrative.write(
        "A7",
        'Opportunity: A small handful of top-performing sellers drive massive volume, while we carry too many "Tier C" products from underperforming sellers.',
    )

    ws_narrative.write(
        "A9", "Recommendations for Investigation:", workbook.add_format({"bold": True})
    )
    ws_narrative.write(
        "A10",
        "1. Seller Support: Offer premium support or lower commission rates to our Top 10 Best Sellers to retain them on the platform.",
    )
    ws_narrative.write(
        "A11",
        "2. Inventory Cleanup: Investigate the storage costs of Tier C items to see if low-performers should be delisted.",
    )

    # ==========================================
    # SHEET 2: Change Over Time (Line Chart)
    # ==========================================
    ws_time = workbook.add_worksheet("Revenue Trends")
    # Make sure these match the columns of whatever query you use for time!
    months = df_time["order_month"].to_list()
    revenue = df_time["total_revenue"].to_list()

    ws_time.write("A1", "Month", header_format)
    ws_time.write("B1", "Revenue", header_format)
    ws_time.write_column("A2", months)
    ws_time.write_column("B2", revenue)

    line_chart = workbook.add_chart({"type": "line"})
    line_chart.add_series(
        {
            "name": "Monthly Revenue",
            "categories": ["Revenue Trends", 1, 0, len(months), 0],
            "values": ["Revenue Trends", 1, 1, len(revenue), 1],
        }
    )
    line_chart.set_title({"name": "Total Revenue Over Time"})
    line_chart.set_x_axis({"name": "Month"})
    line_chart.set_y_axis({"name": "Revenue ($)"})
    ws_time.insert_chart("D2", line_chart)

    # ==========================================
    # SHEET 3: Category Comparison (ABC Bar Chart)
    # ==========================================
    ws_abc = workbook.add_worksheet("ABC Breakdown")
    tiers = df_abc["abc_tier"].to_list()
    tier_rev = df_abc["total_revenue"].to_list()

    ws_abc.write("A1", "Tier", header_format)
    ws_abc.write("B1", "Revenue", header_format)
    ws_abc.write_column("A2", tiers)
    ws_abc.write_column("B2", tier_rev)

    bar_chart = workbook.add_chart({"type": "column"})
    bar_chart.add_series(
        {
            "categories": ["ABC Breakdown", 1, 0, len(tiers), 0],
            "values": ["ABC Breakdown", 1, 1, len(tier_rev), 1],
        }
    )
    bar_chart.set_title({"name": "Revenue by ABC Tier"})
    bar_chart.set_x_axis({"name": "ABC Classification Tier"})
    bar_chart.set_y_axis({"name": "Total Revenue ($)"})
    ws_abc.insert_chart("D2", bar_chart)

    # ==========================================
    # SHEET 4: Best Sellers (Horizontal Bar Chart)
    # ==========================================
    ws_sellers = workbook.add_worksheet("Top Sellers")
    ws_sellers.set_column("A:A", 20)

    # Adjust these to match the columns in your Best Sellers SQL!
    sellers = df_best_sellers["seller_id"].to_list()
    # If they are long ID strings, we can truncate them for the chart so it looks clean:
    sellers = [str(s)[:8] + "..." for s in sellers]

    seller_revenue = df_best_sellers["total_revenue"].to_list()

    ws_sellers.write("A1", "Seller ID", header_format)
    ws_sellers.write("B1", "Revenue", header_format)
    ws_sellers.write_column("A2", sellers)
    ws_sellers.write_column("B2", seller_revenue)

    seller_chart = workbook.add_chart({"type": "bar"})  # Horizontal bar chart
    seller_chart.add_series(
        {
            "categories": ["Top Sellers", 1, 0, len(sellers), 0],
            "values": ["Top Sellers", 1, 1, len(seller_revenue), 1],
        }
    )
    seller_chart.set_title({"name": "Top 10 Sellers by Revenue"})
    seller_chart.set_x_axis({"name": "Revenue ($)"})
    seller_chart.set_y_axis({"name": "Seller ID"})
    ws_sellers.insert_chart("D2", seller_chart)

    workbook.close()
