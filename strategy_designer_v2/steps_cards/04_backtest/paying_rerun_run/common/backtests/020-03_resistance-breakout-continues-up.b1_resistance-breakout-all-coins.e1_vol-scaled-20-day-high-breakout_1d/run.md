# Backtest of 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.e1_vol-scaled-20-day-high-breakout_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | -0.030376 | 8.446 |
| w2 | 6 | 0.15552 | 45.911 |
| w3 | 17 | 0.062017 | 61.437 |
| w4 | 19 | -0.060484 | -38.149 |
| w5 | 17 | -0.004243 | 56.908 |
| w6 | 17 | 0.169642 | 78.731 |
| w7 | 3 | -0.110063 | 0.387 |
| w8 | 6 | 0.044281 | 0.32 |
| w9 | 3 | -0.046654 | -10.812 |
| w10 | 12 | 0.017098 | 13.632 |
| w11 | 16 | 0.048175 | 30.586 |
| w12 | 2 | 0.070852 | 0.128 |
| w13 | 14 | -0.059186 | 2.212 |
| w14 | 13 | -0.061836 | 8.694 |
| w15 | 11 | 0.073216 | 121.165 |
| w16 | 11 | 0.079031 | 5.686 |
| w17 | 3 | 0.040617 | 7.621 |
| w18 | 8 | -0.056071 | 2.457 |
| w19 | 4 | 0.053688 | -1.643 |
| w20 | 4 | 0.068716 | -0.783 |
| w21 | 6 | -0.115396 | -8.906 |
| w22 | 14 | 0.119857 | 42.609 |
| w23 | 4 | 0.023736 | 1.054 |
| w24 | 13 | 0.129505 | 31.998 |
| w25 | 11 | -0.004351 | 22.776 |
| w26 | 7 | -0.064222 | -1.444 |
| w27 | 16 | 0.09123 | 32.827 |
| w28 | 4 | 0.046506 | 1.053 |
| w29 | 15 | -0.054715 | -0.677 |
| w30 | 3 | 0.046235 | -2.047 |
| w31 | 10 | -0.043796 | -1.182 |
| w32 | 6 | 0.254703 | 18.173 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.070342 | 9.356 |
| w2 | 5 | 0.021042 | -17.495 |
| w3 | 7 | -0.136932 | -7.895 |
| w4 | 8 | -0.102737 | 9.433 |
| w5 | 9 | -0.01872 | 8.465 |
| w6 | 14 | 0.181507 | 73.415 |
| w7 | 5 | -0.035085 | -0.172 |
| w8 | 1 | -0.035056 | -2.056 |
| w9 | 2 | -0.092744 | -9.193 |
| w10 | 15 | 0.062104 | 9.475 |
| w11 | 8 | -0.037764 | 6.597 |
| w12 | 5 | 0.04346 | -8.677 |
| w13 | 11 | -0.082588 | 5.301 |
| w14 | 9 | -0.094089 | 4.247 |
| w15 | 14 | 0.053223 | 22.49 |
| w16 | 10 | 0.002491 | -1.128 |
| w17 | 7 | -0.065115 | -8.983 |
| w18 | 7 | -0.019515 | -12.803 |
| w19 | 2 | -0.077033 | -0.869 |
| w20 | 3 | -0.056129 | 0.563 |
| w21 | 7 | 0.057301 | -5.775 |
| w22 | 13 | -0.151473 | -1.091 |
| w23 | 4 | -0.072159 | -9.047 |
| w24 | 7 | -0.100583 | -12.919 |
| w25 | 8 | 0.045661 | 4.5 |
| w26 | 1 | -0.009587 | -1.772 |
| w27 | 12 | -0.059459 | 8.873 |
| w28 | 3 | -0.038983 | -2.808 |
| w29 | 11 | 0.037623 | 3.586 |
| w30 | 2 | -0.421984 | -10.932 |
| w31 | 3 | -0.010171 | -1.153 |
| w32 | 9 | 0.003889 | -17.93 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 11 | 0.118611 | 51.645 |
| w7 | 4 | 0.012283 | -2.517 |
| w8 | 1 | -0.05774 | -1.059 |
| w9 | 5 | 0.158835 | 1.622 |
| w10 | 5 | -0.126413 | -11.064 |
| w11 | 3 | 0.146761 | -6.604 |
| w12 | 5 | 0.034135 | -13.388 |
| w13 | 9 | 0.050201 | -0.441 |
| w14 | 9 | 0.102406 | 12.261 |
| w15 | 4 | 0.223446 | 139.471 |
| w16 | 9 | 0.092225 | 47.32 |
| w17 | 6 | 0.046756 | 14.281 |
| w18 | 5 | -0.2615 | -11.279 |
| w19 | 3 | 0.06309 | -1.793 |
| w20 | 3 | -0.012795 | -0.855 |
| w21 | 5 | -0.064426 | -0.052 |
| w22 | 7 | -0.218503 | 9.958 |
| w23 | 6 | -0.12189 | -1.092 |
| w24 | 11 | 0.097482 | 0.533 |
| w25 | 5 | -0.071566 | 3.406 |
| w26 | 2 | -0.004729 | 6.657 |
| w27 | 11 | 0.32841 | 124.372 |
| w28 | 4 | 0.054234 | 0.907 |
| w29 | 10 | 0.123364 | 15.186 |
| w30 | 2 | 0.002592 | -1.337 |
| w31 | 6 | 0.079565 | -6.556 |
| w32 | 4 | 0.353129 | 0.496 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 3 | 0.132201 | 9.352 |
| w8 | 4 | 0.015164 | -3.639 |
| w9 | 5 | 0.051009 | -12.405 |
| w10 | 7 | 0.139013 | 23.294 |
| w11 | 8 | -0.043929 | -0.6 |
| w12 | 7 | -0.00281 | -10.707 |
| w13 | 8 | -0.106147 | 1.276 |
| w14 | 7 | -0.061187 | 8.956 |
| w15 | 8 | -0.181622 | -1.606 |
| w16 | 12 | 0.064699 | 11.465 |
| w17 | 8 | 0.011503 | 0.77 |
| w18 | 4 | -0.158013 | -15.597 |
| w19 | 2 | -0.015486 | -0.017 |
| w20 | 3 | -0.025085 | 3.369 |
| w21 | 1 | -0.023343 | -7.04 |
| w22 | 12 | 0.108819 | 8.942 |
| w23 | 3 | 0.129764 | 47.623 |
| w24 | 6 | -0.129623 | -10.527 |
| w25 | 9 | 0.118946 | 15.954 |
| w26 | 3 | 0.050737 | -6.428 |
| w27 | 10 | -0.006631 | -1.644 |
| w28 | 3 | -0.043804 | -2.788 |
| w29 | 15 | -0.28937 | 2.585 |
| w30 | 5 | -0.183315 | -4.614 |
| w31 | 1 | -0.076392 | -2.366 |
| w32 | 4 | 0.155724 | 0.411 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | 0.071672 | 91.691 |
| w2 | 9 | -0.034313 | -11.358 |
| w3 | 5 | -0.00834 | -2.171 |
| w4 | 14 | 0.245693 | 261.162 |
| w5 | 17 | 0.038538 | 88.76 |
| w6 | 10 | 0.188072 | 19.962 |
| w7 | 8 | 0.079394 | 6.637 |
| w8 | 2 | -0.013611 | -0.722 |
| w9 | 4 | 0.028326 | -5.091 |
| w10 | 10 | -0.112148 | 2.136 |
| w11 | 7 | 0.100888 | 25.471 |
| w12 | 4 | 0.087701 | -4.985 |
| w13 | 14 | -0.04202 | 21.632 |
| w14 | 11 | -0.006524 | 48.645 |
| w15 | 13 | -0.047884 | 2.756 |
| w16 | 17 | 0.116269 | 29.728 |
| w17 | 10 | -0.085304 | 0.803 |
| w18 | 10 | -0.049545 | -9.779 |
| w19 | 3 | 0.041463 | -1.41 |
| w20 | 4 | -0.021223 | 3.122 |
| w21 | 5 | 0.055117 | -3.35 |
| w22 | 12 | 0.071858 | 7.63 |
| w23 | 4 | -0.113947 | -5.472 |
| w24 | 11 | -0.114959 | -5.035 |
| w25 | 8 | 0.015985 | 16.206 |
| w26 | 3 | 0.0762 | 1.247 |
| w27 | 7 | -0.069157 | 7.291 |
| w28 | 0 | -0.0252 | 0.0 |
| w29 | 13 | 0.138304 | 28.238 |
| w30 | 3 | -0.100202 | -4.477 |
| w31 | 4 | -0.070686 | -2.225 |
| w32 | 4 | 0.073419 | 11.593 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 9 | 0.00131 | 17.818 |
| w11 | 2 | 0.048332 | -1.091 |
| w12 | 4 | 0.065068 | -10.267 |
| w13 | 14 | -0.04984 | 17.904 |
| w14 | 13 | -0.0253 | 51.225 |
| w15 | 7 | 0.15679 | 14.53 |
| w16 | 19 | 0.158088 | 64.403 |
| w17 | 10 | 0.044479 | 43.365 |
| w18 | 1 | -0.176777 | -2.939 |
| w19 | 4 | -0.008059 | -4.208 |
| w20 | 4 | -0.060755 | -3.262 |
| w21 | 0 | -0.041015 | 0.0 |
| w22 | 10 | 0.033977 | 4.501 |
| w23 | 2 | -0.204907 | -9.006 |
| w24 | 12 | 0.140499 | 72.237 |
| w25 | 9 | 0.066249 | 9.27 |
| w26 | 5 | -0.025496 | -3.979 |
| w27 | 10 | 0.28114 | 73.255 |
| w28 | 3 | -0.219026 | -6.334 |
| w29 | 10 | 0.071299 | 5.571 |
| w30 | 0 | -0.079389 | 0.0 |
| w31 | 2 | 0.017488 | -0.684 |
| w32 | 6 | -0.019876 | -13.929 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 12 | -0.054215 | -3.335 |
| w13 | 7 | -0.053453 | -6.188 |
| w14 | 15 | 0.085226 | 17.318 |
| w15 | 5 | -0.106089 | -5.423 |
| w16 | 12 | 0.028225 | 12.623 |
| w17 | 10 | 0.030455 | 8.009 |
| w18 | 6 | -0.208314 | 8.528 |
| w19 | 4 | -0.080794 | -5.182 |
| w20 | 6 | -0.057025 | -4.973 |
| w21 | 5 | 0.093558 | -2.347 |
| w22 | 10 | 0.038095 | 7.951 |
| w23 | 1 | -0.051761 | -0.157 |
| w24 | 10 | -0.136421 | 13.551 |
| w25 | 3 | -0.03253 | -1.611 |
| w26 | 1 | -0.070085 | -2.041 |
| w27 | 8 | -0.011742 | 19.105 |
| w28 | 0 | -0.109856 | 0.0 |
| w29 | 7 | 0.151837 | -0.613 |
| w30 | 0 | -0.072235 | 0.0 |
| w31 | 5 | 0.029593 | 0.92 |
| w32 | 6 | -0.088486 | -12.756 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | -0.058358 | 0.598 |
| w16 | 14 | 0.081917 | 26.115 |
| w17 | 3 | -0.011391 | 2.237 |
| w18 | 7 | 0.020326 | 17.274 |
| w19 | 2 | -0.038674 | -2.281 |
| w20 | 2 | -0.007738 | -1.242 |
| w21 | 8 | 0.11873 | -18.997 |
| w22 | 4 | -8.3e-05 | 2.283 |
| w23 | 1 | -0.035146 | -2.291 |
| w24 | 10 | -0.023128 | 27.787 |
| w25 | 7 | 0.116903 | 8.379 |
| w26 | 4 | 0.045168 | -4.963 |
| w27 | 9 | 0.141295 | 53.766 |
| w28 | 4 | 0.086543 | -0.264 |
| w29 | 6 | 0.028128 | 6.294 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | 0.04592 | -1.772 |
| w32 | 5 | -0.068862 | -17.775 |

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 18 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 4 | -0.201062 | -7.652 |
| w16 | 14 | -0.033914 | 47.941 |
| w17 | 5 | 0.050126 | 8.032 |
| w18 | 7 | -0.150696 | -5.525 |
| w19 | 4 | 0.047292 | -5.198 |
| w20 | 3 | -0.230348 | -8.944 |
| w21 | 3 | -0.130756 | -2.745 |
| w22 | 13 | -0.144246 | 9.913 |
| w23 | 14 | 0.067602 | -12.806 |
| w24 | 20 | 0.033792 | 12.531 |
| w25 | 7 | 0.019852 | 6.217 |
| w26 | 13 | 0.108311 | 23.364 |
| w27 | 14 | 0.035024 | 36.939 |
| w28 | 3 | 0.024039 | -1.114 |
| w29 | 20 | -0.137275 | 12.633 |
| w30 | 0 | -0.071845 | 0.0 |
| w31 | 13 | -0.135398 | 1.633 |
| w32 | 13 | 0.049946 | -10.48 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 12 | -0.020026 | 30.638 |
| w17 | 7 | -0.039851 | -8.556 |
| w18 | 9 | -0.049311 | 0.7 |
| w19 | 4 | 0.001316 | -2.789 |
| w20 | 6 | -0.067926 | 0.429 |
| w21 | 2 | -0.027874 | -6.12 |
| w22 | 12 | -0.023211 | 3.874 |
| w23 | 2 | 0.030998 | -0.533 |
| w24 | 9 | -0.093126 | 15.166 |
| w25 | 9 | 0.087713 | 6.97 |
| w26 | 2 | -0.0229 | -1.023 |
| w27 | 9 | 0.170486 | 10.368 |
| w28 | 1 | 0.021291 | -0.67 |
| w29 | 5 | 0.132772 | 0.144 |
| w30 | 3 | -0.03603 | -2.687 |
| w31 | 4 | -0.074684 | -2.653 |
| w32 | 3 | -0.080575 | -7.542 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | 0.037684 | -0.972 |
| w21 | 3 | -0.056991 | -3.735 |
| w22 | 10 | -0.005117 | 3.94 |
| w23 | 2 | 0.085445 | -0.644 |
| w24 | 10 | 0.079631 | 69.586 |
| w25 | 7 | 0.028236 | 7.444 |
| w26 | 5 | 0.042999 | -8.742 |
| w27 | 10 | -0.097493 | 14.663 |
| w28 | 3 | -0.002927 | -2.291 |
| w29 | 8 | 0.003435 | 0.164 |
| w30 | 3 | 0.021017 | -0.32 |
| w31 | 1 | 0.038497 | -2.253 |
| w32 | 7 | 0.108429 | -3.844 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | -0.087189 | 2.586 |
| w23 | 0 | -0.086512 | 0.0 |
| w24 | 9 | 0.075045 | 47.135 |
| w25 | 6 | -0.132208 | 28.827 |
| w26 | 6 | -0.006779 | -3.618 |
| w27 | 6 | -0.151243 | 4.124 |
| w28 | 0 | 0.021951 | 0.0 |
| w29 | 5 | 0.066485 | -1.161 |
| w30 | 4 | 0.029407 | -9.442 |
| w31 | 5 | -0.108172 | -0.017 |
| w32 | 9 | 0.051899 | 16.302 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 7 | -0.131104 | 1.847 |
| w25 | 10 | 0.017046 | -4.785 |
| w26 | 1 | -0.118624 | -1.042 |
| w27 | 15 | 0.061838 | 39.387 |
| w28 | 6 | 0.148131 | 0.025 |
| w29 | 5 | -0.031064 | -0.604 |
| w30 | 1 | -0.113431 | -2.176 |
| w31 | 5 | 0.042056 | -2.903 |
| w32 | 9 | 0.227109 | -5.737 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 17 | 0.348793 | 52.494 |
| w6 | 11 | -0.05265 | 0.836 |
| w7 | 3 | -0.068457 | -4.766 |
| w8 | 4 | 0.024837 | -3.99 |
| w9 | 3 | -0.041945 | -6.086 |
| w10 | 10 | 0.047084 | 6.461 |
| w11 | 7 | 0.040629 | -2.094 |
| w12 | 5 | 0.004226 | -8.243 |
| w13 | 12 | 0.022438 | 17.889 |
| w14 | 9 | -0.111182 | 5.521 |
| w15 | 5 | -0.058905 | -1.473 |
| w16 | 10 | 0.004772 | 11.496 |
| w17 | 6 | -0.008426 | 5.476 |
| w18 | 7 | -0.058483 | -10.984 |
| w19 | 2 | -0.015667 | 1.278 |
| w20 | 3 | 0.059476 | -0.734 |
| w21 | 2 | 0.020739 | 0.017 |
| w22 | 6 | 0.003514 | -7.065 |
| w23 | 2 | 0.007182 | -4.139 |
| w24 | 10 | -0.174701 | -14.28 |
| w25 | 5 | -0.032885 | 8.015 |
| w26 | 11 | 0.079481 | 10.03 |
| w27 | 10 | -0.022258 | 1.566 |
| w28 | 3 | -0.214706 | -5.296 |
| w29 | 9 | -0.021126 | -1.11 |
| w30 | 16 | 0.060903 | 174.682 |
| w31 | 3 | 0.019257 | -4.247 |
| w32 | 12 | 0.129125 | 30.212 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 12 | -0.007508 | 55.045 |
| w6 | 6 | -0.174472 | 44.334 |
| w7 | 4 | 0.001722 | -2.433 |
| w8 | 1 | -0.090851 | -0.03 |
| w9 | 4 | -0.001881 | -12.86 |
| w10 | 11 | 0.071969 | 17.223 |
| w11 | 9 | -0.09706 | -1.947 |
| w12 | 1 | -0.115773 | -5.697 |
| w13 | 12 | -0.077641 | 2.823 |
| w14 | 10 | -0.230945 | 22.235 |
| w15 | 10 | -0.141895 | 6.17 |
| w16 | 14 | -0.107639 | 25.304 |
| w17 | 10 | 0.072952 | -6.179 |
| w18 | 1 | -0.058288 | -1.477 |
| w19 | 9 | -0.145341 | -11.708 |
| w20 | 3 | -0.004244 | 2.691 |
| w21 | 8 | -0.086015 | -21.745 |
| w22 | 10 | 0.004605 | 6.487 |
| w23 | 4 | 0.067237 | 3.236 |
| w24 | 10 | -0.065147 | -8.325 |
| w25 | 6 | -0.038147 | -16.818 |
| w26 | 11 | 0.06262 | 11.304 |
| w27 | 7 | -0.125509 | 8.533 |
| w28 | 8 | 0.147381 | 11.614 |
| w29 | 12 | 0.092434 | -12.233 |
| w30 | 14 | -0.25378 | -16.323 |
| w31 | 6 | 0.195066 | -8.955 |
| w32 | 11 | 0.027871 | 22.371 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | -0.041119 | 4.453 |
| w18 | 12 | 0.039065 | -1.45 |
| w19 | 3 | -0.028411 | -3.359 |
| w20 | 5 | -0.100072 | 4.106 |
| w21 | 2 | -0.054038 | -11.197 |
| w22 | 9 | 0.038362 | 18.388 |
| w23 | 3 | -0.016934 | -1.005 |
| w24 | 8 | -0.140674 | -0.291 |
| w25 | 5 | -0.082763 | 13.543 |
| w26 | 4 | -0.031518 | 0.234 |
| w27 | 5 | 0.042104 | 42.921 |
| w28 | 4 | -0.079879 | -0.883 |
| w29 | 9 | 0.163179 | 8.316 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | 0.011758 | -0.188 |
| w32 | 12 | 0.076383 | -3.889 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | -0.227728 | -10.218 |
| w18 | 3 | -0.03968 | 0.107 |
| w19 | 6 | -0.016617 | -3.153 |
| w20 | 5 | -0.101665 | -2.821 |
| w21 | 5 | -0.058178 | -13.013 |
| w22 | 8 | 0.120764 | 6.232 |
| w23 | 3 | -0.124102 | -5.065 |
| w24 | 15 | -0.064078 | -4.199 |
| w25 | 3 | 0.04745 | 11.277 |
| w26 | 7 | 0.004657 | -9.309 |
| w27 | 12 | 0.061284 | 5.018 |
| w28 | 2 | -0.07471 | -2.137 |
| w29 | 14 | 0.007034 | -2.721 |
| w30 | 0 | -0.043876 | 0.0 |
| w31 | 1 | 0.007596 | -4.239 |
| w32 | 8 | 0.162894 | 7.03 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | -0.086554 | -6.857 |
| w20 | 4 | 0.092188 | -0.726 |
| w21 | 6 | -0.033516 | -8.387 |
| w22 | 16 | -0.0308 | 70.299 |
| w23 | 5 | -0.018178 | -7.101 |
| w24 | 17 | 0.118702 | 132.927 |
| w25 | 4 | -0.124271 | -10.782 |
| w26 | 7 | -0.032026 | -7.664 |
| w27 | 6 | -0.029899 | 0.364 |
| w28 | 2 | 0.005989 | 0.348 |
| w29 | 9 | -0.001656 | 0.011 |
| w30 | 1 | -0.091628 | -1.962 |
| w31 | 6 | 0.034281 | 2.181 |
| w32 | 9 | 0.016237 | 5.97 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | -0.169323 | 8.769 |
| w23 | 5 | -0.088416 | -1.105 |
| w24 | 12 | -0.126884 | 3.779 |
| w25 | 8 | -0.164382 | -2.203 |
| w26 | 2 | -0.031449 | -0.225 |
| w27 | 8 | -0.072549 | 1.027 |
| w28 | 1 | -0.15148 | -5.475 |
| w29 | 10 | 0.143531 | 3.407 |
| w30 | 1 | -0.090884 | -1.588 |
| w31 | 6 | 0.058373 | 0.398 |
| w32 | 5 | -0.033097 | 4.812 |

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ONDOUSD: 6 of 6 windows run. w1 to w26 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w27 | 11 | 0.076988 | 10.27 |
| w28 | 3 | -0.011073 | -2.931 |
| w29 | 6 | -0.10466 | -5.257 |
| w30 | 2 | 0.077077 | -2.246 |
| w31 | 1 | -0.023668 | -0.97 |
| w32 | 7 | 0.138008 | 19.319 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | 0.026511 | 5.19 |
| w18 | 2 | 0.170093 | -7.01 |
| w19 | 3 | 0.126225 | -2.863 |
| w20 | 2 | 0.188305 | 0.97 |
| w21 | 3 | -0.109076 | -8.821 |
| w22 | 10 | 0.009277 | 9.992 |
| w23 | 3 | -0.126555 | -7.362 |
| w24 | 16 | -0.181249 | 3.038 |
| w25 | 7 | 0.068336 | 6.992 |
| w26 | 2 | 0.043115 | -2.214 |
| w27 | 8 | -0.033091 | 8.515 |
| w28 | 0 | -0.033007 | 0.0 |
| w29 | 5 | 0.0614 | -3.715 |
| w30 | 3 | 0.130629 | -1.572 |
| w31 | 3 | -0.023606 | -2.355 |
| w32 | 3 | -0.15011 | -16.825 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | 0.049606 | 5.352 |
| w18 | 4 | -0.021685 | 1.826 |
| w19 | 4 | 0.011949 | -3.417 |
| w20 | 5 | -0.005905 | -0.611 |
| w21 | 4 | -0.187155 | -17.816 |
| w22 | 11 | -0.036403 | 43.025 |
| w23 | 5 | -0.002859 | -5.006 |
| w24 | 9 | -0.160634 | 15.41 |
| w25 | 8 | 0.06657 | 29.634 |
| w26 | 3 | 0.020018 | -2.893 |
| w27 | 6 | -0.055148 | 11.377 |
| w28 | 2 | 0.091057 | 0.979 |
| w29 | 4 | 0.060209 | 0.203 |
| w30 | 1 | -0.04527 | -0.664 |
| w31 | 3 | 0.000183 | -0.33 |
| w32 | 4 | -0.129938 | -5.51 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 2 | 0.046368 | 2.316 |
| w29 | 6 | 0.054401 | -1.688 |
| w30 | 4 | 0.166691 | -2.429 |
| w31 | 7 | 0.164435 | 5.06 |
| w32 | 6 | -0.041167 | 0.973 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 7 | 0.366461 | 4.823 |
| w15 | 11 | -0.056754 | 16.186 |
| w16 | 10 | 0.128244 | 145.535 |
| w17 | 4 | -0.025822 | 2.599 |
| w18 | 2 | -0.090111 | -0.914 |
| w19 | 3 | -0.289206 | -2.398 |
| w20 | 3 | -0.119832 | -14.745 |
| w21 | 6 | 0.201056 | 23.038 |
| w22 | 8 | -0.031303 | -2.05 |
| w23 | 2 | -0.15061 | -5.18 |
| w24 | 11 | -0.230076 | -0.361 |
| w25 | 8 | 0.079307 | 62.5 |
| w26 | 5 | 0.02603 | -2.627 |
| w27 | 14 | 0.362238 | 70.214 |
| w28 | 3 | -0.061572 | -3.167 |
| w29 | 9 | 0.05991 | 6.162 |
| w30 | 4 | 0.138055 | -1.187 |
| w31 | 6 | 0.047148 | 1.084 |
| w32 | 6 | 0.266224 | 5.725 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | 0.350295 | 93.543 |
| w26 | 6 | 0.086562 | 15.931 |
| w27 | 12 | 0.199305 | 16.599 |
| w28 | 3 | 0.016626 | -1.001 |
| w29 | 10 | 0.138426 | 6.224 |
| w30 | 2 | -0.022713 | -1.618 |
| w31 | 6 | 0.126756 | 5.038 |
| w32 | 6 | 0.220925 | -2.767 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

