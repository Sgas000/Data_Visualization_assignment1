SELECT COUNT(*) FROM olist_customers_dataset;

SELECT o.order_id, c.customer_unique_id, o.order_status
FROM olist_orders_dataset o
INNER JOIN olist_customers_dataset c
ON o.customer_id = c.customer_id
LIMIT 10;

SELECT COUNT(*) FROM olist_customers_dataset;

SELECT AVG(price) FROM olist_order_items_dataset;

SELECT p.product_category_name, COUNT(*) AS total
FROM olist_order_items_dataset oi
JOIN olist_products_dataset p ON oi.product_id = p.product_id
GROUP BY p.product_category_name
ORDER BY total DESC
LIMIT 5;

SELECT ROUND(AVG(o.order_delivered_customer_date::DATE - o.order_estimated_delivery_date::DATE), 2) AS avg_delay_days
FROM olist_orders_dataset o
WHERE o.order_delivered_customer_date IS NOT NULL;

SELECT ROUND(AVG(total), 2) AS avg_order_value
FROM (
    SELECT order_id, SUM(price) AS total
    FROM olist_order_items_dataset
    GROUP BY order_id
) ;

SELECT c.customer_city,
       COUNT(*) AS total_customers
FROM olist_customers_dataset c
GROUP BY c.customer_city
ORDER BY total_customers DESC
LIMIT 5;

SELECT review_score,
       COUNT(*) AS count_reviews
FROM olist_order_reviews_dataset
GROUP BY review_score
ORDER BY review_score;

SELECT oi.seller_id,
       ROUND(SUM(oi.price), 2) AS revenue
FROM olist_order_items_dataset oi
GROUP BY oi.seller_id
ORDER BY revenue DESC
LIMIT 5;
