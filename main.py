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
    """,

  

 
    "Average time of delivery":

    """SELECT ROUND(AVG(o.order_delivered_customer_date::DATE - o.order_estimated_delivery_date::DATE), 2) AS avg_delay_days
    FROM olist_orders_dataset o
    WHERE o.order_delivered_customer_date IS NOT NULL;""",
    "Average order check":
    """SELECT ROUND(AVG(total), 2) AS avg_order_value
    FROM (
        SELECT order_id, SUM(price) AS total
        FROM olist_order_items_dataset
        GROUP BY order_id
    ) ;""",
    "Top five cities by amount of customers ":
    """SELECT c.customer_city,
        COUNT(*) AS total_customers
    FROM olist_customers_dataset c
    GROUP BY c.customer_city
    ORDER BY total_customers DESC
    LIMIT 5;""",
    "How many reviews with every score":
    """SELECT review_score,
        COUNT(*) AS count_reviews
    FROM olist_order_reviews_dataset
    GROUP BY review_score
    ORDER BY review_score;""",
    "Tob 5 sellers by revenue":
    """
    SELECT oi.seller_id,
        ROUND(SUM(oi.price), 2) AS revenue
    FROM olist_order_items_dataset oi
    GROUP BY oi.seller_id
    ORDER BY revenue DESC
    LIMIT 5;""",
    "Number of orders by years":
    """
    SELECT DATE_PART('year', order_purchase_timestamp) AS year,
       COUNT(*) AS total_orders
    FROM olist_orders_dataset
    GROUP BY year
    ORDER BY year;"""

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
<<<<<<< HEAD

=======
>>>>>>> 5c531c0 (new commit)
