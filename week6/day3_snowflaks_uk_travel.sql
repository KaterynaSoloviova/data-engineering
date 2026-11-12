CREATE DATABASE IF NOT EXISTS TRAVEL_DB;

CREATE SCHEMA IF NOT EXISTS TRAVEL_DB.BOOKINGS;

-- Step 1. Create the warehouse
CREATE WAREHOUSE IF NOT EXISTS travel_wh
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60
  AUTO_RESUME = TRUE;

--Step 2. Activate the warehouse and schema:
-- Tells Snowflake which warehouse to use and which schema should be the default location for your objects.
USE WAREHOUSE travel_wh;
USE SCHEMA travel_db.bookings;

--Step 3. Step 3. Create the file format
-- This is the instruction manual Snowflake uses to understand your CSV
CREATE OR REPLACE FILE FORMAT csv_ff
    TYPE = CSV
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    NULL_IF = ('');

-- Step 4. Create the table
CREATE OR REPLACE TABLE bookings (
    booking_id INT,
    booking_date DATE,
    customer_id STRING,
    customer_name STRING,
    home_city STRING,
    destination_city STRING,
    destination_country STRING,
    package_type STRING,
    travel_start_date DATE,
    nights INT,
    travellers INT,
    price_per_person_gbp NUMBER(10,2),
    discount_pct NUMBER(5,2),
    payment_mode STRING,
    status STRING,
    rating INT
);

-- Step 5. Create a stage
-- A stage is where Snowflake stores your uploaded CSV before loading it into the table

CREATE OR REPLACE STAGE bookings_stage
FILE_FORMAT = csv_ff;

-- Step 6. Import the data after uploading the CSV file to the stage
COPY INTO bookings
FROM @bookings_stage/uk_travel_bookings.csv;

-- Step 6. Check the result
SELECT COUNT(*) AS total_bookings
FROM bookings;



-- Level 1: Basics
-- Q1. Show first 10 bookings
SELECT *
FROM bookings
LIMIT 10;

-- Q2. How many bookings are there in total?
SELECT COUNT(*) AS total_bookings
FROM bookings;

-- Q3.  List all bookings to Spain.
SELECT booking_id, customer_name,
       destination_city, travel_start_date
FROM bookings
WHERE destination_country = 'Spain';

-- Q4. Find all Cancelled bookings.
SELECT booking_id, customer_name, destination_city, status
FROM bookings
WHERE status = 'Cancelled';

-- Q5. Which bookings have no discount recorded (NULL)?
SELECT booking_id, customer_name, discount_pct
FROM bookings
WHERE discount_pct IS NULL;

-- Level 2: Aggregations
-- Q6. Calculate the revenue for every booking.
SELECT booking_id,
       round(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100),2) AS revenue_gbp
FROM bookings;

-- Q7. Total revenue by package type for non-cancelled bookings, highest first.
-- <> means not equal to
-- COALESCE checks whether a value is missing (NULL).
   -- If discount is 10 → returns 10.
    -- If discount is NULL → returns 0.
SELECT package_type,
       ROUND(SUM(travellers * price_per_person_gbp * (1 - COALESCE(discount_pct,0)/100)), 2) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY package_type
ORDER BY revenue_gbp DESC;

-- Q8. Which destination country is booked most often?
SELECT destination_country, COUNT(*) AS bookings
FROM bookings
GROUP BY destination_country
ORDER BY bookings DESC
LIMIT 1;

-- Q9. Share of bookings by payment mode.
SELECT payment_mode,
       COUNT(*) AS bookings,
       ROUND(100 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct_share
FROM bookings
GROUP BY payment_mode
ORDER BY bookings DESC;

-- Q10. Customers with more than 2 bookings.
-- HAVING COUNT(*) > 2 — show only customers with 3 or more bookings.
-- HAVING filters groups, while WHERE filters individual rows.
SELECT customer_name, COUNT(*) AS bookings
FROM bookings
GROUP BY customer_name
-- HAVING COUNT(*) > 2;
ORDER BY bookings DESC;

-- Q11. Average rating per destination country (ignore NULL ratings), with at least 2 rated trips.
SELECT destination_country,
       ROUND(AVG(rating), 2) AS avg_rating,
       COUNT(rating) AS rated_trips
FROM bookings
GROUP BY destination_country
HAVING COUNT(rating) >= 2
ORDER BY avg_rating DESC;


-- Level 3: Intermediate / Dates and Window Functions

-- Q12. Work out each trip's return date and how far in advance it was booked
    -- We need to calculate the return date and the number of days between booking and travel.
    -- DATEADD means: add a certain amount of time to a date: (we add day, how many: nights, Starting date)
    -- DATEDIFF calculates the difference between two dates: (differ in days, starting date, ending date)
SELECT
    booking_id,
    customer_name,
    DATEADD('day', nights, travel_start_date) AS return_date,
    DATEDIFF('day', booking_date, travel_start_date) AS lead_time_days
FROM bookings;    

-- Q13. Monthly bookings count and revenue by travel month
-- How many bookings and how much revenue did we have in each month of travel
    -- DATE_TRUNC groups a date into a larger time period (in month)
SELECT
    DATE_TRUNC('month', travel_start_date) AS travel_month,
    COUNT(*) AS bookings,
    ROUND(
        SUM(travellers * price_per_person_gbp
        * (1 - COALESCE(discount_pct, 0) / 100)), 2
    ) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY travel_month
ORDER BY travel_month;

-- Q14. Rank customers by total spend within each home city
-- Which customers spend the most money in each home city?
    -- RANK() gives each customer a position.
        -- PARTITION BY home_city — create a separate ranking for each city.
        -- ORDER BY total_spend DESC — highest spend comes first.
        -- RANK() — assign rank numbers.
        -- OVER() tells SQL that we need to perform a calculation across a set of rows, without combining those rows into one result.

SELECT
    home_city,
    customer_name,
    total_spend,
    RANK() OVER (
        PARTITION BY home_city
        ORDER BY total_spend DESC
    ) AS city_rank
FROM (
    SELECT
        home_city,
        customer_name,
        SUM(travellers * price_per_person_gbp
        * (1 - COALESCE(discount_pct, 0) / 100)) AS total_spend
    FROM bookings
    WHERE status <> 'Cancelled'
    GROUP BY home_city, customer_name
);

-- Q15. For repeat customers, show the gap in days between consecutive bookings
-- If a customer books more than once, how many days pass between their bookings?
    -- LAG() looks at the previous row
    --HAVING filters grouped results.
    --QUALIFY filters results after window functions are calculated.

SELECT
    customer_name,
    booking_date,
    DATEDIFF(
        'day',
        LAG(booking_date) OVER (
            PARTITION BY customer_id
            ORDER BY booking_date
        ),
        booking_date
    ) AS days_since_last_booking
FROM bookings
QUALIFY COUNT(*) OVER (
    PARTITION BY customer_id
) > 1
ORDER BY customer_name, booking_date;

-- Q16. Top 2 destinations by revenue within each package type
-- For every package type, which two destination cities generate the most revenue?

SELECT
    package_type,
    destination_city,
    SUM(travellers * price_per_person_gbp) AS revenue_gbp
FROM bookings
WHERE status <> 'Cancelled'
GROUP BY package_type, destination_city
QUALIFY ROW_NUMBER() OVER (
    PARTITION BY package_type
    ORDER BY SUM(travellers * price_per_person_gbp) DESC
) <= 2;

-- Q17. Cancellation rate by package type
-- Which package types have the highest cancellation rate?
    -- IFF(): If true, return one value; otherwise another

SELECT
    package_type,
    COUNT(*) AS bookings,
    SUM(IFF(status = 'Cancelled', 1, 0)) AS cancelled,
    ROUND(
        100 * SUM(IFF(status = 'Cancelled', 1, 0))
        / COUNT(*), 1
    ) AS cancel_rate_pct
FROM bookings
GROUP BY package_type;

-- Q18. Segment bookings into Budget, Mid-range and Premium using CASE
-- Categorise each booking according to its price per person.
    -- CASE allows us to create categories based on conditions
    -- WHEN price_per_person_gbp < 400 THEN 'Budget': if the price is less than £400, label it Budget.

SELECT
    booking_id,
    destination_city,
    price_per_person_gbp,
    CASE
        WHEN price_per_person_gbp < 400 THEN 'Budget'
        WHEN price_per_person_gbp < 900 THEN 'Mid-range'
        ELSE 'Premium'
    END AS price_band
FROM bookings;

-- ==========================================
-- LEVEL 3: SQL FUNCTIONS CHEAT SHEET
-- ==========================================

-- DATEADD()
-- ADD: Adds days, months or years to a date.

-- DATEDIFF()
-- DIFFERENCE: Calculates the difference between two dates.

-- DATE_TRUNC()
-- TRUNCATE: Groups dates by month, year, etc.

-- RANK()
-- RANKING: Ranks rows. Ties receive the same rank.

-- ROW_NUMBER()
-- NUMBER: Gives every row a unique position.

-- LAG()
-- LAST: Looks at the previous row.

-- PARTITION BY
-- GROUP: Separates rows into groups for window calculations.

-- QUALIFY
-- FILTER: Filters results of window functions.

-- IFF()
-- IF: If true, returns one value; otherwise another.

-- CASE
-- CATEGORIES: Creates categories using conditions.

-- OVER()
-- WINDOW: Defines which rows a window function calculates over.

-- ==========================================
-- END OF LEVEL 3 CHEAT SHEET
-- ==========================================
