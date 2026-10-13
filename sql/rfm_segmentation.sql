-- RFM (Recency, Frequency, Monetary) Customer Segmentation
WITH customer_orders AS (
    SELECT
        customer_id,
        MAX(order_date) AS last_order_date,
        COUNT(order_id) AS total_orders,
        SUM(amount) AS total_spend
    FROM orders
    GROUP BY customer_id
),
rfm_scores AS (
    SELECT
        customer_id,
        last_order_date,
        total_orders,
        total_spend,
        NTILE(5) OVER (ORDER BY last_order_date ASC) AS r_score,
        NTILE(5) OVER (ORDER BY total_orders ASC) AS f_score,
        NTILE(5) OVER (ORDER BY total_spend ASC) AS m_score
    FROM customer_orders
)
SELECT
    customer_id,
    total_orders,
    total_spend,
    (r_score + f_score + m_score) AS rfm_total,
    CASE
        WHEN r_score >= 4 AND f_score >= 4 THEN 'Champions'
        WHEN f_score >= 3 THEN 'Loyal Customers'
        WHEN r_score <= 2 AND f_score >= 3 THEN 'At-Risk'
        ELSE 'Needs Attention'
    END AS customer_segment
FROM rfm_scores
ORDER BY total_spend DESC;
