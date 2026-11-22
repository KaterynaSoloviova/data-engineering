-- Fail the test if the mart table has no records for today

SELECT
    CURRENT_DATE() AS missing_transaction_date
WHERE NOT EXISTS (
    SELECT 1
    FROM {{ ref('daily_revenue') }}
    WHERE transaction_date = CURRENT_DATE()
)