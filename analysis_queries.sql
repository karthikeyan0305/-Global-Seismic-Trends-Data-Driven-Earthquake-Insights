-- analysis_queries.sql
-- All queries labelled Q1 ... Q30
-- Table assumed: earthquakes

-- Q1: Top 10 strongest earthquakes (mag)
SELECT id, time, place, country, mag, depth_km
FROM earthquakes
ORDER BY mag DESC
LIMIT 10;

-- Q2: Top 10 deepest earthquakes (depth_km)
SELECT id, time, place, country, mag, depth_km
FROM earthquakes
ORDER BY depth_km DESC
LIMIT 10;

-- Q3: Shallow earthquakes < 50 km and mag > 7.5
SELECT id, time, place, country, mag, depth_km
FROM earthquakes
WHERE depth_km < 50
  AND mag > 7.5
ORDER BY mag DESC;

-- Q4: Average depth per continent (requires country_continent table)
SELECT cc.continent,
       AVG(e.depth_km) AS avg_depth_km,
       COUNT(*) AS events
FROM earthquakes e
LEFT JOIN country_continent cc ON e.country = cc.country
GROUP BY cc.continent
ORDER BY avg_depth_km DESC;

-- Q5: Average magnitude per magType
SELECT magType, COUNT(*) AS cnt, AVG(mag) AS avg_mag
FROM earthquakes
GROUP BY magType
ORDER BY avg_mag DESC;

-- Q6: Year with most earthquakes
SELECT YEAR(time) AS year, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY year
ORDER BY quake_count DESC
LIMIT 1;

-- Q7: Month with highest number of earthquakes (overall)
SELECT MONTH(time) AS month, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY month
ORDER BY quake_count DESC
LIMIT 1;

-- Q8: Day of week with most earthquakes
SELECT DAYNAME(time) AS day_of_week, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY day_of_week
ORDER BY quake_count DESC;

-- Q9: Count of earthquakes per hour of day
SELECT HOUR(time) AS hour, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY hour
ORDER BY hour;

-- Q10: Most active reporting network (net)
SELECT net, COUNT(*) AS quake_count
FROM earthquakes
GROUP BY net
ORDER BY quake_count DESC
LIMIT 1;

-- Q11: Top 5 places with highest casualties
SELECT place, country, SUM(casualties) AS total_casualties, COUNT(*) AS events
FROM earthquakes
WHERE casualties IS NOT NULL AND casualties > 0
GROUP BY place, country
ORDER BY total_casualties DESC
LIMIT 5;

-- Q12: Total estimated economic loss per continent (requires country_continent)
SELECT cc.continent,
       SUM(e.economic_loss) AS total_loss
FROM earthquakes e
LEFT JOIN country_continent cc ON e.country = cc.country
WHERE e.economic_loss IS NOT NULL
GROUP BY cc.continent
ORDER BY total_loss DESC;

-- Q13: Average economic loss by alert level
SELECT alert, AVG(economic_loss) AS avg_loss, COUNT(*) AS events
FROM earthquakes
WHERE alert IS NOT NULL AND economic_loss IS NOT NULL
GROUP BY alert
ORDER BY avg_loss DESC;

-- Q14: Count of reviewed vs automatic earthquakes (status)
SELECT status, COUNT(*) AS cnt
FROM earthquakes
GROUP BY status;

-- Q15: Count by earthquake type (type)
SELECT type, COUNT(*) AS cnt
FROM earthquakes
GROUP BY type
ORDER BY cnt DESC;

-- Q16: Number of earthquakes by data type (types)
SELECT
  SUM(CASE WHEN types LIKE '%shakemap%' THEN 1 ELSE 0 END) AS shakemap_events,
  SUM(CASE WHEN types LIKE '%dyfi%' THEN 1 ELSE 0 END) AS dyfi_events,
  SUM(CASE WHEN types LIKE '%origin%' THEN 1 ELSE 0 END) AS origin_events
FROM earthquakes;

-- Q17: Average RMS and gap per continent (requires country_continent)
SELECT cc.continent,
       AVG(e.rms) AS avg_rms,
       AVG(e.gap) AS avg_gap
FROM earthquakes e
LEFT JOIN country_continent cc ON e.country = cc.country
GROUP BY cc.continent
ORDER BY avg_rms DESC;

-- Q18: Events with high station coverage (nst > 100)
SELECT id, time, place, country, nst
FROM earthquakes
WHERE nst > 100
ORDER BY nst DESC;

-- Q19: Number of tsunamis triggered per year
SELECT YEAR(time) AS year,
       SUM(CASE WHEN tsunami = 1 THEN 1 ELSE 0 END) AS tsunami_events
FROM earthquakes
GROUP BY year
ORDER BY year;

-- Q20: Count earthquakes by alert levels
SELECT alert, COUNT(*) AS cnt
FROM earthquakes
WHERE alert IS NOT NULL
GROUP BY alert
ORDER BY cnt DESC;

-- Q21: Top 5 countries with highest average magnitude (past 10 years)
SELECT country, AVG(mag) AS avg_mag, COUNT(*) AS events
FROM earthquakes
WHERE YEAR(time) >= YEAR(CURDATE()) - 10
  AND country IS NOT NULL
GROUP BY country
HAVING COUNT(*) >= 10
ORDER BY avg_mag DESC
LIMIT 5;

-- Q22: Countries with both shallow and deep quakes within same month
SELECT country, YEAR(time) AS year, MONTH(time) AS month
FROM earthquakes
WHERE country IS NOT NULL
GROUP BY country, YEAR(time), MONTH(time)
HAVING SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END) > 0
   AND SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) > 0;

-- Q23: Year-over-year growth rate in total number of earthquakes
WITH yearly AS (
  SELECT YEAR(time) AS yr, COUNT(*) AS cnt
  FROM earthquakes
  GROUP BY yr
)
SELECT
  yr,
  cnt,
  LAG(cnt) OVER (ORDER BY yr) AS prev_cnt,
  ROUND((cnt - LAG(cnt) OVER (ORDER BY yr)) / NULLIF(LAG(cnt) OVER (ORDER BY yr),0) * 100, 2) AS growth_percent
FROM yearly
ORDER BY yr;

-- Q24: 3 most seismically active regions by frequency*avg_mag score (grouping by place)
SELECT place,
       COUNT(*) AS freq,
       AVG(mag) AS avg_mag,
       (COUNT(*) * AVG(mag)) AS score
FROM earthquakes
GROUP BY place
HAVING COUNT(*) >= 5
ORDER BY score DESC
LIMIT 3;

-- Q25: Avg depth for countries within ±5° latitude of equator
SELECT country, AVG(depth_km) AS avg_depth_km, COUNT(*) AS events
FROM earthquakes
WHERE latitude BETWEEN -5 AND 5
  AND country IS NOT NULL
GROUP BY country
ORDER BY avg_depth_km DESC;



-- doubt these questions

-- Q26: Countries with highest ratio of shallow to deep earthquakes
SELECT country,
       SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END) AS shallow_cnt,
       SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) AS deep_cnt,
       CASE WHEN SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END) = 0 THEN NULL
            ELSE ROUND(
                SUM(CASE WHEN depth_km < 50 THEN 1 ELSE 0 END)
                / SUM(CASE WHEN depth_km > 300 THEN 1 ELSE 0 END), 2)
       END AS shallow_deep_ratio
FROM earthquakes
WHERE country IS NOT NULL
GROUP BY country
HAVING shallow_cnt + deep_cnt >= 5
ORDER BY shallow_deep_ratio DESC
LIMIT 20;

-- Q27: Avg magnitude difference between tsunami vs no-tsunami
SELECT
  ROUND(AVG(CASE WHEN tsunami = 1 THEN mag END),3) AS avg_mag_tsunami,
  ROUND(AVG(CASE WHEN tsunami = 0 THEN mag END),3) AS avg_mag_no_tsunami,
  ROUND( (AVG(CASE WHEN tsunami = 1 THEN mag END) - AVG(CASE WHEN tsunami = 0 THEN mag END)),3) AS avg_diff
FROM earthquakes;

-- Q28: Events with lowest data reliability (high rms + gap)
SELECT id, time, place, country, rms, gap, (COALESCE(rms,0) + COALESCE(gap,0)) AS error_score
FROM earthquakes
ORDER BY error_score DESC
LIMIT 100;

-- Q29: Pairs of consecutive earthquakes within 50 km and 1 hour (uses window functions & Haversine)
WITH ordered AS (
  SELECT
    id, time, latitude, longitude, place,
    LAG(id) OVER (ORDER BY time) AS prev_id,
    LAG(time) OVER (ORDER BY time) AS prev_time,
    LAG(latitude) OVER (ORDER BY time) AS prev_lat,
    LAG(longitude) OVER (ORDER BY time) AS prev_lon
  FROM earthquakes
)
SELECT
  id, prev_id,
  TIMESTAMPDIFF(MINUTE, prev_time, time) AS minutes_diff,
  (6371 * 2 * ASIN(
      SQRT(
        POWER(SIN(RADIANS((latitude - prev_lat)/2)),2)
        + COS(RADIANS(prev_lat)) * COS(RADIANS(latitude))
          * POWER(SIN(RADIANS((longitude - prev_lon)/2)),2)
      )
  )) AS distance_km,
  place, prev_time, time
FROM ordered
WHERE prev_id IS NOT NULL
  AND TIMESTAMPDIFF(MINUTE, prev_time, time) BETWEEN 0 AND 60
  AND (6371 * 2 * ASIN(
      SQRT(
        POWER(SIN(RADIANS((latitude - prev_lat)/2)),2)
        + COS(RADIANS(prev_lat)) * COS(RADIANS(latitude))
          * POWER(SIN(RADIANS((longitude - prev_lon)/2)),2)
      )
  )) <= 50
ORDER BY time DESC;

-- Q30: Regions with highest frequency of deep-focus earthquakes (depth > 300 km)
SELECT country, COUNT(*) AS deep_count
FROM earthquakes
WHERE depth_km > 300
GROUP BY country
ORDER BY deep_count DESC
LIMIT 20;
