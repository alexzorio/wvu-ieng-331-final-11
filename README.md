# Final Project: Complete Data Product
Team 11: [Alexander Zorio], [Tanzim Raffi]

## Final Deliverables

We chose to investigate key aspects of the Olist business to provide insight into its success and potential future. Our report has been generated
in Excel for two reasons. The first is that Excel is widely used in the corporate space and is readily available for most, if not all, computers. This means the
report is easily accessible for the end user. The second reason is that we, the students, wanted to familiarize ourselves with writing reports in the Excel format because of the underlying reasoning behind the first. Excel is widely used, and we are guaranteed to use it in our future.
To look into the success of the business, we first wanted to analyze revenue over time. This is our line graph in Excel. When looking at the Excel report, we can see that there is considerable growth over time in revenue. After the peak revenue was hit, there was a substantial decrease, followed by a small increase, to leave revenue to plateau just before the peak until the end of the dataset. This suggests that the current business has likely found its optimal level of product volume to produce. With a proper level of production met, we should shift from increasing output to retaining the volume over the long term.
With the sustainability of the business now the focus, we wanted to look at which products and sellers drive revenue. First, to look at products, we expanded our previously created ABC analysis. Now we are looking at all products over the entire dataset instead of one period. From the generated bar chart in Excel, we can see that tier A products almost entirely drive the company's revenue. Disruptions in the production of tier A products would likely result in catastrophic drops in revenue. Tiers B and C products only account for a very small part of the company's revenue.
When looking into the sellers, there comes a very similar issue. When we plot our sellers on a horizontal bar chart against each other, we find an extremely unbalanced list of sellers. A small group of top sellers moves a massive portion of the company's product volume.
When looking at these two problems with the products and sellers, we have recommendations for improvement. First, we suggest that the company attempt to diversify with sellers and reward top sellers. A VIP program could be implemented to incentivise the better sellers whilst attracting other sellers to move more product. As for the distribution of products between the tiers, our recommendation is to prioritize tier A products. Since most volume is tier A, we should cut the operational costs of tiers B and C products. Strictly looking at revenue, they do not do well compared to tier A products and are likely not turning as much of a profit. Therefore, we should shrink the total product catalogue and focus on reducing costs by eliminating products with poor sales.

## How to Run
Instructions to run the pipeline from a fresh clone:
```bash
git clone [https://github.com/alexzorio/wvu-ieng-331-final-11.git](https://github.com/alexzorio/wvu-ieng-331-final-11.git)
cd wvu-ieng-331-final-11
uv sync
# place olist.duckdb in the data/ directory
uv run wvu-ieng-331-final-11
```
Also make sure that there is a "data" and "output" folder in your local cloned project. Data folder required olist.duckdb present for the pipeline to run.

# Milestone 2: Python Pipeline

## Parameters
| Parameter | Type | Default | Description |
|------------------------------------------|
|`--start-date` | date (str) | 2000-01-01 | The start date for filtering orders (Format: YYYY-MM-DD). |
|`--end-date` | date (str) | 2099-12-31 | The end date for filtering orders (Format: YYYY-MM-DD). |
|`--db-path` | string | data/olist.duckdb | Path to the DuckDB database file.|

## Outputs
Currently we are running outputs for one of 4 sql queries, ABC.sql. All 4 sql files can be run with few changes to the pipeline file.
There are three output files produced they are as follows:
detail.parquet: Lists individual products along with their total revenue, cumulative revenue percentage, and assigned ABC classification tier.
Contains a full scored and classified dataset.
summary.csv: Shows how many products fall into each tier and the total revenue for each tier.
chart.html: The Altair visualization, interactive bar chart, of total revenue broken into the ABC tier list.

## Validation Checks
Before running the main queries the following data checks are run. Note if a check fails a warning will be shown in the terminal with a note as to what failed
but the pipeline will run with disclaimers in the logs of problems with the data. The following checks are run:
Table Existence: Verification that all 9 expected tables are present in the dataset.
Null Checks: Verification that key columns are not completely null.
Date Range Validation: Checks orders.order_purchase_timestamp to make sure that there are no dates that exist in the future. (No time travel)
Row Count Minimums: Verifies that core tables have at least 1000 rows each.

## Analysis Summary
The ABC analysis shows a distribution of data much like a pareto chart. The majority of value for orders falls within the A category which is relatively small
number of products compared to their total value. This suggests that a small portion of the product catalogue drives the majority of sales. This leads to a
recommendation for the company to maybe remove some of the B category products and possibly most of C as they may not generate enough revenue to justify the
cost of production when the A category products sell so well in comparison.

## Limitation & Caveats
One current limitation is the current hardcoded tier threshold for the ABC tier lists. This could changed into a dynamic CLI argument on top of date filtering.
Another limitation is the current process of having to change code in the pipeline to adapt to the other prepared sql queries in the sql folder. All of these
files have been parameterized to be used in the pipeline but the pipeline itself is not currently able to run them without small changes.
Additionally the current pipeline is assuming that the Schema will not be changed. If there are updates to column or table names the sql queries and validation
checks will require manual updates.
