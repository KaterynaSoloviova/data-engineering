
SELECT
    DATE::DATE AS transaction_date,
    DATETIME::TIMESTAMP_NTZ AS transaction_timestamp,
    CASH_TYPE AS cash_type,
    CARD AS card,
    MONEY::NUMBER(10, 2) AS revenue,
    COFFEE_NAME AS coffee_name

FROM {{ source('raw', 'coffee_sales') }}
