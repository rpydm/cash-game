SELECT
    tmp.category
  , tmp.sum_2022_01
  , tmp.sum_2023_01
  , tmp.sum_2022_01 - tmp.sum_2023_01 AS 'YoY'
FROM (
  SELECT 
      category
    , amount
    , SUM(
        CASE WHEN strftime('%Y-%m', date) = '2022-01'
        THEN amount ELSE 0 END
      ) AS 'sum_2022_01'
    , SUM(
        CASE WHEN strftime('%Y-%m', date) = '2023-01'
        THEN amount ELSE 0 END
      ) AS 'sum_2023_01'
  FROM 
    moneytree 
  WHERE
    date BETWEEN '2022-01-01' AND '2022-01-31'
    OR date BETWEEN '2023-01-01' AND '2023-01-31'
  GROUP BY 
    category
  ORDER BY
    sum(amount)
) tmp
WHERE
  tmp.amount < 1
  AND tmp.category NOT IN ('カード返済', '振替')
ORDER by YoY desc
;

/*
SELECT 
	sum(amount) 
from moneytree
where 
	date >= '2023-01-01' 
	and date <= '2023-1-31'
	and category not in ('カード返済', '投資', '振替')
	and amount < 1
;
