import psycopg2
import pandas as pd

conn = psycopg2.connect(
    dbname='postgres',
    user='postgres',
    password='Your_password',
    host='localhost',
    port=5433
)
cur = conn.cursor()

queries = {
    "Number of clients": "SELECT COUNT(*) FROM olist_customers_dataset;",
    "Customers unique id with order id and status": """
        SELECT o.order_id, c.customer_unique_id, o.order_status
        FROM olist_orders_dataset o
        INNER JOIN olist_customers_dataset c
        ON o.customer_id = c.customer_id
        LIMIT 10;
    """,
    "Average product price": "SELECT AVG(price) FROM olist_order_items_dataset;",
    "Top 5 categories of products": """
        SELECT p.product_category_name, COUNT(*) AS total
        FROM olist_order_items_dataset oi
        JOIN olist_products_dataset p ON oi.product_id = p.product_id
        GROUP BY p.product_category_name
        ORDER BY total DESC
        LIMIT 5;
    """
}

results = {}

for desc, sql in queries.items():
    print(f"\n=== {desc} ===")
    cur.execute(sql)

    colnames = [desc[0] for desc in cur.description]

    rows = cur.fetchall()
    for row in rows:
        print(row)

    df = pd.DataFrame(rows, columns=colnames)
    results[desc] = df

with pd.ExcelWriter("query_results.xlsx") as writer:
    for desc, df in results.items():
        sheet_name = desc[:31]
        df.to_excel(writer, sheet_name=sheet_name, index=False)

for desc, df in results.items():
    safe_name = desc.replace(" ", "_").lower()
    df.to_csv(f"{safe_name}.csv", index=False)

cur.close()
conn.close()

