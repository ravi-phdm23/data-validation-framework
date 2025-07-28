-- COMPREHENSIVE VALIDATION EDGE CASE TESTS
-- Test various failure scenarios to ensure validation properly detects issues

-- =============================================================================
-- TEST 1: Basic String Mismatch (Should FAIL - 40% match)
-- =============================================================================
WITH test1_source AS (
  SELECT 1 as id, 'John' as first_name, 'Smith' as last_name
  UNION ALL SELECT 2, 'Jane', 'Doe'
  UNION ALL SELECT 3, 'Bob', 'Johnson'
  UNION ALL SELECT 4, 'Alice', 'Wilson'
  UNION ALL SELECT 5, 'Charlie', 'Brown'
),
test1_target AS (
  SELECT 1 as id, 'John Smith' as full_name      -- MATCH
  UNION ALL SELECT 2, 'Jane X. Doe'              -- MISMATCH 
  UNION ALL SELECT 3, 'Robert Johnson'           -- MISMATCH
  UNION ALL SELECT 4, 'Alice Wilson'             -- MATCH
  UNION ALL SELECT 5, 'Chuck Brown'              -- MISMATCH
),
test1_comparison AS (
  SELECT 
    'TEST1_STRING_MISMATCH' as test_name,
    s.id,
    CONCAT(s.first_name, ' ', s.last_name) as calculated,
    t.full_name as actual,
    CASE WHEN CONCAT(s.first_name, ' ', s.last_name) = t.full_name THEN 'MATCH' ELSE 'MISMATCH' END as result
  FROM test1_source s
  FULL OUTER JOIN test1_target t ON s.id = t.id
),
test1_summary AS (
  SELECT 
    test_name,
    COUNT(*) as total_rows,
    COUNTIF(result = 'MATCH') as matches,
    ROUND(COUNTIF(result = 'MATCH') * 100.0 / COUNT(*), 2) as match_percentage,
    CASE 
      WHEN COUNTIF(result = 'MATCH') = COUNT(*) THEN 'PASS'
      WHEN COUNTIF(result = 'MATCH') >= COUNT(*) * 0.95 THEN 'WARN'
      ELSE 'FAIL'
    END as status
  FROM test1_comparison
  GROUP BY test_name
),

-- =============================================================================
-- TEST 2: Numeric Aggregation Mismatch (Should FAIL - 33% match)
-- =============================================================================
test2_transactions AS (
  SELECT 101 as account_id, 100.00 as amount
  UNION ALL SELECT 101, 250.00
  UNION ALL SELECT 102, 75.50
  UNION ALL SELECT 102, 124.50
  UNION ALL SELECT 103, 500.00
),
test2_summary AS (
  SELECT 101 as account_id, 350.00 as total_amount    -- MATCH (100+250=350)
  UNION ALL SELECT 102, 150.00                        -- MISMATCH (75.50+124.50=200, not 150)
  UNION ALL SELECT 103, 499.99                        -- MISMATCH (500≠499.99)
),
test2_comparison AS (
  SELECT 
    'TEST2_NUMERIC_MISMATCH' as test_name,
    s.account_id,
    s.calculated_total,
    t.total_amount as actual_total,
    CASE 
      WHEN ABS(s.calculated_total - t.total_amount) < 0.01 THEN 'MATCH' 
      ELSE 'MISMATCH' 
    END as result
  FROM (SELECT account_id, SUM(amount) as calculated_total FROM test2_transactions GROUP BY account_id) s
  FULL OUTER JOIN test2_summary t ON s.account_id = t.account_id
),
test2_summary_stats AS (
  SELECT 
    test_name,
    COUNT(*) as total_rows,
    COUNTIF(result = 'MATCH') as matches,
    ROUND(COUNTIF(result = 'MATCH') * 100.0 / COUNT(*), 2) as match_percentage,
    CASE 
      WHEN COUNTIF(result = 'MATCH') = COUNT(*) THEN 'PASS'
      WHEN COUNTIF(result = 'MATCH') >= COUNT(*) * 0.95 THEN 'WARN'
      ELSE 'FAIL'
    END as status
  FROM test2_comparison
  GROUP BY test_name
),

-- =============================================================================
-- TEST 3: NULL Handling (Should WARN - 75% match with nulls)
-- =============================================================================
test3_source AS (
  SELECT 1 as id, 'John Smith' as name
  UNION ALL SELECT 2, 'Jane Doe'
  UNION ALL SELECT 3, NULL         -- Source NULL
  UNION ALL SELECT 4, 'Bob Wilson'
),
test3_target AS (
  SELECT 1 as id, 'John Smith' as name     -- MATCH
  UNION ALL SELECT 2, NULL                 -- Target NULL  
  UNION ALL SELECT 3, 'Alice Brown'        -- Source was NULL
  UNION ALL SELECT 4, 'Bob Wilson'         -- MATCH
),
test3_comparison AS (
  SELECT 
    'TEST3_NULL_HANDLING' as test_name,
    COALESCE(s.id, t.id) as id,
    s.name as source_name,
    t.name as target_name,
    CASE 
      WHEN s.name IS NULL AND t.name IS NULL THEN 'BOTH_NULL'
      WHEN s.name IS NULL THEN 'SOURCE_NULL'
      WHEN t.name IS NULL THEN 'TARGET_NULL'
      WHEN s.name = t.name THEN 'MATCH'
      ELSE 'MISMATCH'
    END as result
  FROM test3_source s
  FULL OUTER JOIN test3_target t ON s.id = t.id
),
test3_summary_stats AS (
  SELECT 
    test_name,
    COUNT(*) as total_rows,
    COUNTIF(result = 'MATCH') as matches,
    COUNTIF(result = 'MISMATCH') as mismatches,
    COUNTIF(result LIKE '%NULL%') as nulls,
    ROUND(COUNTIF(result = 'MATCH') * 100.0 / COUNT(*), 2) as match_percentage,
    CASE 
      WHEN COUNTIF(result = 'MATCH') = COUNT(*) THEN 'PASS'
      WHEN COUNTIF(result = 'MATCH') >= COUNT(*) * 0.95 THEN 'WARN'
      ELSE 'FAIL'
    END as status
  FROM test3_comparison
  GROUP BY test_name
),

-- =============================================================================
-- TEST 4: Perfect Match (Should PASS - 100% match)
-- =============================================================================
test4_source AS (
  SELECT 1 as id, 100 as value
  UNION ALL SELECT 2, 200
  UNION ALL SELECT 3, 300
),
test4_target AS (
  SELECT 1 as id, 100 as value     -- MATCH
  UNION ALL SELECT 2, 200          -- MATCH
  UNION ALL SELECT 3, 300          -- MATCH
),
test4_comparison AS (
  SELECT 
    'TEST4_PERFECT_MATCH' as test_name,
    s.id,
    s.value as source_value,
    t.value as target_value,
    CASE WHEN s.value = t.value THEN 'MATCH' ELSE 'MISMATCH' END as result
  FROM test4_source s
  FULL OUTER JOIN test4_target t ON s.id = t.id
),
test4_summary_stats AS (
  SELECT 
    test_name,
    COUNT(*) as total_rows,
    COUNTIF(result = 'MATCH') as matches,
    ROUND(COUNTIF(result = 'MATCH') * 100.0 / COUNT(*), 2) as match_percentage,
    CASE 
      WHEN COUNTIF(result = 'MATCH') = COUNT(*) THEN 'PASS'
      WHEN COUNTIF(result = 'MATCH') >= COUNT(*) * 0.95 THEN 'WARN'
      ELSE 'FAIL'
    END as status
  FROM test4_comparison
  GROUP BY test_name
),

-- =============================================================================
-- FINAL RESULTS: Combine all test results
-- =============================================================================
all_results AS (
  SELECT * FROM test1_summary
  UNION ALL SELECT * FROM test2_summary_stats  
  UNION ALL SELECT * FROM test3_summary_stats
  UNION ALL SELECT * FROM test4_summary_stats
)

-- Show summary of all tests
SELECT 
  test_name,
  total_rows,
  matches,
  match_percentage,
  status,
  CASE 
    WHEN status = 'PASS' THEN '✅'
    WHEN status = 'WARN' THEN '⚠️' 
    ELSE '❌'
  END as result_icon
FROM all_results
ORDER BY test_name

UNION ALL

-- Show overall test suite status
SELECT 
  'OVERALL_TEST_SUITE' as test_name,
  COUNT(*) as total_rows,
  COUNTIF(status IN ('PASS', 'WARN')) as matches,
  ROUND(COUNTIF(status IN ('PASS', 'WARN')) * 100.0 / COUNT(*), 2) as match_percentage,
  CASE 
    WHEN COUNTIF(status = 'FAIL') = 0 THEN 'ALL_TESTS_BEHAVING_CORRECTLY'
    ELSE 'SOME_TESTS_UNEXPECTED'
  END as status,
  '🎯' as result_icon
FROM all_results;
