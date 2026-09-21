"""RetailPulse — exploración, limpieza y creación de tablas analíticas.
"""

# %% 1. Librerías y rutas
from pathlib import Path
import json
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_FILE = PROJECT_ROOT / "data" / "raw" / "online_retail_II.xlsx"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
IMAGES_DIR = PROJECT_ROOT / "images"
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

# %% 2. Carga de las dos hojas
# Se leen juntas para analizar los dos años como un solo periodo.
sheets = pd.read_excel(RAW_FILE, sheet_name=None)
frames = []
for sheet_name, frame in sheets.items():
    frame["source_period"] = sheet_name
    frames.append(frame)

raw = pd.concat(frames, ignore_index=True)
print("Dimensiones originales:", raw.shape)
print(raw.head())

# %% 3. Normalización de nombres y tipos
df = raw.rename(
    columns={
        "Invoice": "invoice_no",
        "StockCode": "stock_code",
        "Description": "description",
        "Quantity": "quantity",
        "InvoiceDate": "invoice_date",
        "Price": "unit_price",
        "Customer ID": "customer_id",
        "Country": "country",
    }
).copy()

df["invoice_no"] = df["invoice_no"].astype("string").str.strip()
df["stock_code"] = df["stock_code"].astype("string").str.strip()
df["description"] = df["description"].astype("string").str.strip()
df["country"] = df["country"].astype("string").str.strip()
df["invoice_date"] = pd.to_datetime(df["invoice_date"], errors="coerce")
df["customer_id"] = pd.to_numeric(df["customer_id"], errors="coerce").astype("Int64")
df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
df["unit_price"] = pd.to_numeric(df["unit_price"], errors="coerce")

# %% 4. Diagnóstico de calidad
quality_before = {
    "rows": int(len(df)),
    "duplicate_rows": int(df.duplicated().sum()),
    "missing_customer_id": int(df["customer_id"].isna().sum()),
    "missing_description": int(df["description"].isna().sum()),
    "missing_invoice_date": int(df["invoice_date"].isna().sum()),
    "non_positive_quantity": int((df["quantity"] <= 0).sum()),
    "non_positive_price": int((df["unit_price"] <= 0).sum()),
}
print(pd.Series(quality_before, name="count"))

# %% 5. Reglas de negocio
# Cancelación: la factura comienza con C.
# Venta válida: no cancelada, cantidad positiva y precio positivo.
# Un registro sin Customer ID sí puede contar para ventas, pero no para RFM/cohortes.
df = df.drop_duplicates().copy()
df["is_cancelled"] = df["invoice_no"].str.upper().str.startswith("C", na=False)
df["is_return"] = df["quantity"] < 0
df["gross_line_value"] = df["quantity"] * df["unit_price"]
df["is_valid_sale"] = (
    ~df["is_cancelled"]
    & (df["quantity"] > 0)
    & (df["unit_price"] > 0)
    & df["invoice_date"].notna()
)

sales = df.loc[df["is_valid_sale"]].copy()
sales["line_revenue"] = sales["quantity"] * sales["unit_price"]
sales["invoice_month"] = sales["invoice_date"].dt.to_period("M").dt.to_timestamp()
sales["invoice_year"] = sales["invoice_date"].dt.year
sales["invoice_hour"] = sales["invoice_date"].dt.hour
sales["invoice_weekday"] = sales["invoice_date"].dt.day_name()
non_merchandise_codes = {
    "POST", "DOT", "M", "BANK CHARGES", "AMAZONFEE", "CRUK", "D", "S",
}
sales["is_non_merchandise"] = sales["stock_code"].str.upper().isin(non_merchandise_codes)

# %% 6. Tabla de pedidos
orders = (
    sales.groupby("invoice_no", as_index=False)
    .agg(
        invoice_date=("invoice_date", "min"),
        customer_id=("customer_id", "first"),
        country=("country", "first"),
        order_revenue=("line_revenue", "sum"),
        units=("quantity", "sum"),
        distinct_products=("stock_code", "nunique"),
    )
)
orders["invoice_month"] = orders["invoice_date"].dt.to_period("M").dt.to_timestamp()
order_p99 = orders["order_revenue"].quantile(0.99)
orders["is_high_value_outlier"] = orders["order_revenue"] > order_p99

# %% 7. KPIs principales
cancelled_invoices = df.loc[df["is_cancelled"], "invoice_no"].nunique()
all_invoices = df["invoice_no"].nunique()
kpis = {
    "valid_revenue_gbp": round(float(sales["line_revenue"].sum()), 2),
    "valid_orders": int(orders["invoice_no"].nunique()),
    "identified_customers": int(sales["customer_id"].nunique()),
    "average_order_value_gbp": round(float(orders["order_revenue"].mean()), 2),
    "cancelled_invoices": int(cancelled_invoices),
    "invoice_cancellation_rate": round(float(cancelled_invoices / all_invoices), 4),
    "valid_rows": int(len(sales)),
}
print(json.dumps(kpis, indent=2))

# %% 8. Tablas para el dashboard
monthly = (
    sales.groupby("invoice_month", as_index=False)
    .agg(
        revenue=("line_revenue", "sum"),
        units=("quantity", "sum"),
        orders=("invoice_no", "nunique"),
        customers=("customer_id", "nunique"),
    )
)
monthly["average_order_value"] = monthly["revenue"] / monthly["orders"]

countries = (
    sales.groupby("country", as_index=False)
    .agg(revenue=("line_revenue", "sum"), orders=("invoice_no", "nunique"), customers=("customer_id", "nunique"))
    .sort_values("revenue", ascending=False)
)

products = (
    sales.loc[~sales["is_non_merchandise"]]
    .groupby(["stock_code", "description"], as_index=False)
    .agg(revenue=("line_revenue", "sum"), units=("quantity", "sum"), orders=("invoice_no", "nunique"))
    .sort_values("revenue", ascending=False)
)

# %% 9. Segmentación RFM
customer_sales = sales.dropna(subset=["customer_id"]).copy()
analysis_date = customer_sales["invoice_date"].max() + pd.Timedelta(days=1)
rfm = (
    customer_sales.groupby("customer_id", as_index=False)
    .agg(
        last_purchase=("invoice_date", "max"),
        frequency=("invoice_no", "nunique"),
        monetary=("line_revenue", "sum"),
    )
)
rfm["recency_days"] = (analysis_date - rfm["last_purchase"]).dt.days
rfm["r_score"] = pd.qcut(rfm["recency_days"].rank(method="first"), 4, labels=[4, 3, 2, 1]).astype(int)
rfm["f_score"] = pd.qcut(rfm["frequency"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["m_score"] = pd.qcut(rfm["monetary"].rank(method="first"), 4, labels=[1, 2, 3, 4]).astype(int)
rfm["rfm_score"] = rfm[["r_score", "f_score", "m_score"]].sum(axis=1)
rfm["segment"] = pd.cut(
    rfm["rfm_score"],
    bins=[2, 5, 8, 10, 12],
    labels=["At risk", "Needs attention", "Loyal", "Champions"],
)

# %% 10. Cohortes mensuales
customer_sales["order_month"] = customer_sales["invoice_date"].dt.to_period("M")
customer_sales["cohort_month"] = customer_sales.groupby("customer_id")["order_month"].transform("min")
customer_sales["cohort_index"] = (
    (customer_sales["order_month"].dt.year - customer_sales["cohort_month"].dt.year) * 12
    + customer_sales["order_month"].dt.month
    - customer_sales["cohort_month"].dt.month
)
cohort_counts = (
    customer_sales.groupby(["cohort_month", "cohort_index"])["customer_id"]
    .nunique()
    .unstack(fill_value=0)
)
cohort_retention = cohort_counts.divide(cohort_counts[0], axis=0)

# %% 11. Exportación a CSV y SQLite
sales.to_csv(PROCESSED_DIR / "sales_clean.csv", index=False)
orders.to_csv(PROCESSED_DIR / "orders.csv", index=False)
monthly.to_csv(PROCESSED_DIR / "monthly_kpis.csv", index=False)
countries.to_csv(PROCESSED_DIR / "country_performance.csv", index=False)
products.to_csv(PROCESSED_DIR / "product_performance.csv", index=False)
rfm.to_csv(PROCESSED_DIR / "customer_rfm.csv", index=False)
cohort_retention.to_csv(PROCESSED_DIR / "cohort_retention.csv")

with sqlite3.connect(PROCESSED_DIR / "retailpulse.db") as connection:
    sales.to_sql("sales", connection, if_exists="replace", index=False)
    orders.to_sql("orders", connection, if_exists="replace", index=False)
    rfm.to_sql("customer_rfm", connection, if_exists="replace", index=False)

summary = {
    "quality_before": quality_before,
    "rows_after_duplicates": int(len(df)),
    "kpis": kpis,
    "analysis_date": str(analysis_date.date()),
    "order_revenue_p99_gbp": round(float(order_p99), 2),
    "high_value_orders": int(orders["is_high_value_outlier"].sum()),
}
with open(PROCESSED_DIR / "analysis_summary.json", "w", encoding="utf-8") as file:
    json.dump(summary, file, ensure_ascii=False, indent=2)

# %% 12. Visualizaciones rápidas
sns.set_theme(style="whitegrid")
fig, ax = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x="invoice_month", y="revenue", marker="o", ax=ax)
ax.set(title="Ingresos mensuales válidos (diciembre de 2011 es parcial)", xlabel="Mes", ylabel="Ingresos (£)")
fig.tight_layout()
fig.savefig(IMAGES_DIR / "monthly_revenue.png", dpi=160)
plt.close(fig)

top_countries = countries.loc[countries["country"] != "United Kingdom"].head(10)
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=top_countries, y="country", x="revenue", ax=ax)
ax.set(title="Top 10 mercados internacionales", xlabel="Ingresos (£)", ylabel="País")
fig.tight_layout()
fig.savefig(IMAGES_DIR / "top_countries.png", dpi=160)
plt.close(fig)

print("Proceso finalizado. Archivos guardados en:", PROCESSED_DIR)
