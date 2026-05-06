# Final Deliverable Grade

**Team 11 (Alex Zorio, Tanzim Raffi)**

| Criterion | Score | Max |
|-----------|------:|----:|
| Deliverable Quality | 6 | 6 |
| Visualizations | 6 | 6 |
| Pipeline Integration | 6 | 6 |
| Analytical Narrative | 6 | 6 |
| **Total (rubric portion)** | **24** | **24** |

Video walkthrough graded separately.

## Deliverable Quality (6/6)

`output/report.xlsx` is a four-sheet Excel workbook (Executive Summary, Revenue Trends, ABC Breakdown, Top Sellers). Native Excel charts embedded on each data sheet. Executive Summary has labelled sections (State of the Business, Problems & Opportunities, Recommendations for Investigation). Workbook opens without setup. Output structure matches the spec (summary.csv, detail.parquet, chart.html, report.xlsx) which is unusually clean compared to several other teams that renamed or omitted M2 outputs.

## Visualizations (6/6)

Three native Excel charts covering the required types:

- **Total Revenue Over Time** (line, temporal) - growth trajectory.
- **Revenue by ABC Tier** (column, categorical) - Pareto concentration.
- **Top 10 Sellers by Revenue** (horizontal bar, categorical/exploratory) - seller concentration.

All have chart titles. Chart types match the data well.

## Pipeline Integration (6/6)

`uv run wvu-ieng-331-final-11` after `uv sync` runs the full pipeline end-to-end with defaults: validation, queries, M2 outputs (summary.csv, detail.parquet, chart.html), then `report.build_report()` produces report.xlsx. Tested with the extended database; pipeline ran cleanly. Output filenames match the spec exactly.

## Analytical Narrative (6/6)

Executive Summary identifies the central tension: strong growth alongside dangerous concentration in Tier A products and top sellers. Two concrete Recommendations: premium support / lower commissions for top 10 sellers (retention play), and an investigation into Tier C storage costs to consider delisting low performers. README has a longer prose narrative covering revenue trajectory, ABC findings, seller concentration, and recommendations for VIP programs and tier rationalisation. Both narratives connect insights to the data and propose actionable next steps.
