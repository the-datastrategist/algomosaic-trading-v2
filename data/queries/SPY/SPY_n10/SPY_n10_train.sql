SELECT
Date,
Ticker,
Week,
Month,
Quarter,
Year,
Day_of_Week,
Day_of_Year,

# AROR Diffs
(AROR_2 - AROR_5)   as DIFF_AROR_2_AROR_5,
(AROR_3 - AROR_5)   as DIFF_AROR_3_AROR_5,
(AROR_4 - AROR_5)   as DIFF_AROR_4_AROR_5,

(AROR_2 - AROR_10)   as DIFF_AROR_2_AROR_10,
(AROR_3 - AROR_10)   as DIFF_AROR_3_AROR_10,
(AROR_4 - AROR_10)   as DIFF_AROR_4_AROR_10,
(AROR_5 - AROR_10)   as DIFF_AROR_5_AROR_10,

-- (AROR_5 - AROR_15)   as DIFF_AROR_5_AROR_15,
-- (AROR_5 - AROR_20)   as DIFF_AROR_5_AROR_20,
-- (AROR_5 - AROR_25)   as DIFF_AROR_5_AROR_25,
(AROR_5 - AROR_30)   as DIFF_AROR_5_AROR_30,
(AROR_5 - AROR_40)   as DIFF_AROR_5_AROR_40,
-- (AROR_5 - AROR_50)   as DIFF_AROR_5_AROR_50,
(AROR_5 - AROR_60)   as DIFF_AROR_5_AROR_60,
(AROR_5 - AROR_70)   as DIFF_AROR_5_AROR_70,
(AROR_5 - AROR_80)   as DIFF_AROR_5_AROR_80,
(AROR_5 - AROR_90)   as DIFF_AROR_5_AROR_90,
-- (AROR_5 - AROR_100)  as DIFF_AROR_5_AROR_100,

(AROR_10 - AROR_15)   as DIFF_AROR_10_AROR_15,
-- (AROR_10 - AROR_20)   as DIFF_AROR_10_AROR_20,
-- (AROR_10 - AROR_25)   as DIFF_AROR_10_AROR_25,
(AROR_10 - AROR_30)   as DIFF_AROR_10_AROR_30,
(AROR_10 - AROR_40)   as DIFF_AROR_10_AROR_40,
-- (AROR_10 - AROR_50)   as DIFF_AROR_10_AROR_50,
(AROR_10 - AROR_60)   as DIFF_AROR_10_AROR_60,
(AROR_10 - AROR_70)   as DIFF_AROR_10_AROR_70,
(AROR_10 - AROR_80)   as DIFF_AROR_10_AROR_80,
(AROR_10 - AROR_90)   as DIFF_AROR_10_AROR_90,
-- (AROR_10 - AROR_100)  as DIFF_AROR_10_AROR_100,

(AROR_20 - AROR_30)   as DIFF_AROR_20_AROR_30,
(AROR_20 - AROR_40)   as DIFF_AROR_20_AROR_40,
(AROR_20 - AROR_50)   as DIFF_AROR_20_AROR_50,
(AROR_20 - AROR_60)   as DIFF_AROR_20_AROR_60,
(AROR_20 - AROR_70)   as DIFF_AROR_20_AROR_70,
(AROR_20 - AROR_80)   as DIFF_AROR_20_AROR_80,
(AROR_20 - AROR_90)   as DIFF_AROR_20_AROR_90,
(AROR_20 - AROR_100)  as DIFF_AROR_20_AROR_100,


-- # RSI Diffs: removed

# Average True Range Ratios
safe_divide(ATR_3, ATR_5)   as RATIO_ATR_3_ATR_5,
safe_divide(ATR_3, ATR_10)  as RATIO_ATR_3_ATR_10,
safe_divide(ATR_3, ATR_25)  as RATIO_ATR_3_ATR_25,
safe_divide(ATR_3, ATR_50)  as RATIO_ATR_3_ATR_50,
safe_divide(ATR_3, ATR_100) as RATIO_ATR_3_ATR_100,

safe_divide(ATR_5, ATR_10)  as RATIO_ATR_5_ATR_10,
safe_divide(ATR_5, ATR_25)  as RATIO_ATR_5_ATR_25,
safe_divide(ATR_5, ATR_50)  as RATIO_ATR_5_ATR_50,
safe_divide(ATR_5, ATR_100) as RATIO_ATR_5_ATR_100,

safe_divide(ATR_10, ATR_25)  as RATIO_ATR_10_ATR_25,
safe_divide(ATR_10, ATR_50)  as RATIO_ATR_10_ATR_50,
safe_divide(ATR_10, ATR_100) as RATIO_ATR_10_ATR_100,
safe_divide(ATR_10, ATR_150) as RATIO_ATR_10_ATR_150,

safe_divide(ATR_25, ATR_50)  as RATIO_ATR_25_ATR_50,
safe_divide(ATR_25, ATR_100) as RATIO_ATR_25_ATR_100,
safe_divide(ATR_25, ATR_150) as RATIO_ATR_25_ATR_150,
safe_divide(ATR_50, ATR_100) as RATIO_ATR_50_ATR_100,
safe_divide(ATR_50, ATR_150) as RATIO_ATR_50_ATR_150

# Min/Max Price Ratios
-- safe_divide(Close, MIN_3)  as RATIO_Close_MIN_3,
-- safe_divide(Close, MIN_4)  as RATIO_Close_MIN_4,
-- safe_divide(Close, MIN_5)  as RATIO_Close_MIN_5,
-- safe_divide(Close, MIN_6)  as RATIO_Close_MIN_6,
-- safe_divide(Close, MIN_7)  as RATIO_Close_MIN_7,
-- safe_divide(Close, MIN_8)  as RATIO_Close_MIN_8,
-- safe_divide(Close, MIN_9)  as RATIO_Close_MIN_9,
-- safe_divide(Close, MIN_10)  as RATIO_Close_MIN_10,

-- safe_divide(Close, MAX_3)  as RATIO_Close_MAX_3,
-- safe_divide(Close, MAX_4)  as RATIO_Close_MAX_4,
-- safe_divide(Close, MAX_5)  as RATIO_Close_MAX_5,
-- safe_divide(Close, MAX_6)  as RATIO_Close_MAX_6,
-- safe_divide(Close, MAX_7)  as RATIO_Close_MAX_7,
-- safe_divide(Close, MAX_8)  as RATIO_Close_MAX_8,
-- safe_divide(Close, MAX_9)  as RATIO_Close_MAX_9,
-- safe_divide(Close, MAX_10) as RATIO_Close_MAX_10,

-- safe_divide(MIN_3, MAX_3)  as RATIO_MIN_3_MAX_3,
-- safe_divide(MIN_4, MAX_4)  as RATIO_MIN_4_MAX_4,
-- safe_divide(MIN_5, MAX_5)  as RATIO_MIN_5_MAX_5,
-- safe_divide(MIN_6, MAX_6)  as RATIO_MIN_6_MAX_6,
-- safe_divide(MIN_7, MAX_7)  as RATIO_MIN_7_MAX_7,
-- safe_divide(MIN_8, MAX_8)  as RATIO_MIN_8_MAX_8,
-- safe_divide(MIN_9, MAX_9)  as RATIO_MIN_9_MAX_9,
-- safe_divide(MIN_10, MAX_10) as RATIO_MIN_10_MAX_10


--  'MIN_3',
--  'MIN_4',
--  'MIN_5',
--  'MIN_6',
--  'MIN_7',
--  'MIN_8',
--  'MIN_9',
--  'MIN_10',
--  'MIN_20',
--  'MIN_30',
--  'MIN_40',
--  'MIN_50',
--  'MIN_100',
--  'MIN_200',

FROM `algomosaic-nyc.yahoo_features.features_SPY_{partition}`
