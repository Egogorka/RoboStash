-- Вставка уникальных НЕ-NULL значений
INSERT INTO dim_referer (url)
SELECT DISTINCT referer_url
FROM staging_logs
WHERE referer_url IS NOT NULL
  AND referer_url NOT IN (SELECT url FROM dim_referer);