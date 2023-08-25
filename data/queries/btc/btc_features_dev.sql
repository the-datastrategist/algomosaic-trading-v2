SELECT *
FROM `algomosaic-nyc.crypto_features.features_{ticker}_{interval}_{partition}`
ORDER BY ticker_time DESC
LIMIT 50