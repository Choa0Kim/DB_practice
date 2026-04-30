-- Active: 1777334538899@@127.0.0.1@3306
-- 01. Querying data
SELECT 
  LastName
FROM
  employees;



-- 02. Sorting data







-- NULL 정렬 예시
SELECT 
  ReportsTo
FROM
  employees
ORDER BY
  ReportsTo;


-- 03. Filtering data
SELECT
  Country
FROM
  customers
ORDER BY
  Country;



-- 04. Grouping data
-- SELECT 
--   c1, c2,..., cn, aggregate_function(ci)
-- FROM
--   table_name
-- GROUP BY 
--   c1, c2, ..., cn;

SELECT
  Country
FROM
  customers
GROUP BY
  Country;


-- 에러
SELECT
  Composer,
  AVG(Milliseconds / 60000) AS avgOfMinute
FROM
  tracks
WHERE 
  avgOfMinute < 10
GROUP BY
  Composer;

-- 에러 해결
