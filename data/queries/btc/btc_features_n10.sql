SELECT *

-- AROR Diffs
-- (AROR_2 - AROR_5)   as DIFF_AROR_2_AROR_5,
-- (AROR_4 - AROR_5)   as DIFF_AROR_4_AROR_5,
-- (AROR_2 - AROR_10)   as DIFF_AROR_2_AROR_10,
-- (AROR_4 - AROR_10)   as DIFF_AROR_4_AROR_10,
-- (AROR_5 - AROR_30)   as DIFF_AROR_5_AROR_30,
-- (AROR_5 - AROR_40)   as DIFF_AROR_5_AROR_40,
-- (AROR_5 - AROR_60)   as DIFF_AROR_5_AROR_60,
-- (AROR_5 - AROR_70)   as DIFF_AROR_5_AROR_70,
-- (AROR_5 - AROR_80)   as DIFF_AROR_5_AROR_80,
-- (AROR_5 - AROR_90)   as DIFF_AROR_5_AROR_90,

-- (AROR_10 - AROR_15)   as DIFF_AROR_10_AROR_15,
-- (AROR_10 - AROR_30)   as DIFF_AROR_10_AROR_30,
-- (AROR_10 - AROR_40)   as DIFF_AROR_10_AROR_40,
-- (AROR_10 - AROR_60)   as DIFF_AROR_10_AROR_60,
-- (AROR_10 - AROR_70)   as DIFF_AROR_10_AROR_70,
-- (AROR_10 - AROR_80)   as DIFF_AROR_10_AROR_80,
-- (AROR_10 - AROR_90)   as DIFF_AROR_10_AROR_90,

-- (AROR_20 - AROR_30)   as DIFF_AROR_20_AROR_30,
-- (AROR_20 - AROR_40)   as DIFF_AROR_20_AROR_40,
-- (AROR_20 - AROR_50)   as DIFF_AROR_20_AROR_50,
-- (AROR_20 - AROR_60)   as DIFF_AROR_20_AROR_60,
-- (AROR_20 - AROR_70)   as DIFF_AROR_20_AROR_70,
-- (AROR_20 - AROR_80)   as DIFF_AROR_20_AROR_80,
-- (AROR_20 - AROR_90)   as DIFF_AROR_20_AROR_90,
-- (AROR_20 - AROR_100)  as DIFF_AROR_20_AROR_100,


-- -- RSI Diffs
-- (RSI_10 - RSI_20)   as DIFF_RSI_10_RSI_20,
-- (RSI_10 - RSI_30)   as DIFF_RSI_10_RSI_30,
-- (RSI_10 - RSI_40)   as DIFF_RSI_10_RSI_40,
-- (RSI_10 - RSI_50)   as DIFF_RSI_10_RSI_50,
-- (RSI_10 - RSI_100)  as DIFF_RSI_10_RSI_100,

-- (RSI_20 - RSI_30)   as DIFF_RSI_20_RSI_30,
-- (RSI_20 - RSI_40)   as DIFF_RSI_20_RSI_40,
-- (RSI_20 - RSI_50)   as DIFF_RSI_20_RSI_50,
-- (RSI_20 - RSI_100)  as DIFF_RSI_20_RSI_100,

-- (RSI_30 - RSI_50)   as DIFF_RSI_30_RSI_50,
-- (RSI_30 - RSI_100)  as DIFF_RSI_30_RSI_100,
-- (RSI_50 - RSI_100)  as DIFF_RSI_50_RSI_100,

-- -- Average True Range Ratios
-- safe_divide(ATR_3, ATR_5)   as RATIO_ATR_3_ATR_5,
-- safe_divide(ATR_3, ATR_10)  as RATIO_ATR_3_ATR_10,
-- safe_divide(ATR_3, ATR_25)  as RATIO_ATR_3_ATR_25,
-- safe_divide(ATR_3, ATR_50)  as RATIO_ATR_3_ATR_50,
-- safe_divide(ATR_3, ATR_100) as RATIO_ATR_3_ATR_100,

-- safe_divide(ATR_5, ATR_10)  as RATIO_ATR_5_ATR_10,
-- safe_divide(ATR_5, ATR_25)  as RATIO_ATR_5_ATR_25,
-- safe_divide(ATR_5, ATR_50)  as RATIO_ATR_5_ATR_50,
-- safe_divide(ATR_5, ATR_100) as RATIO_ATR_5_ATR_100,

-- safe_divide(ATR_10, ATR_25)  as RATIO_ATR_10_ATR_25,
-- safe_divide(ATR_10, ATR_50)  as RATIO_ATR_10_ATR_50,
-- safe_divide(ATR_10, ATR_100) as RATIO_ATR_10_ATR_100,
-- safe_divide(ATR_10, ATR_150) as RATIO_ATR_10_ATR_150,

-- safe_divide(ATR_25, ATR_50)  as RATIO_ATR_25_ATR_50,
-- safe_divide(ATR_25, ATR_100) as RATIO_ATR_25_ATR_100,
-- safe_divide(ATR_25, ATR_150) as RATIO_ATR_25_ATR_150,
-- safe_divide(ATR_50, ATR_100) as RATIO_ATR_50_ATR_100,
-- safe_divide(ATR_50, ATR_150) as RATIO_ATR_50_ATR_150

FROM `algomosaic-nyc.yahoo_features.features_BTC_USD_{partition}`
