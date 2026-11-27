# Backtest of 031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-03.b1.b1.e1_volatility-scaled-monthly-trend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | -0.04967 | 9.82 |
| w2 | 16 | 0.068355 | 48.212 |
| w3 | 51 | -0.088738 | 74.02 |
| w4 | 34 | -0.142877 | -36.984 |
| w5 | 21 | 0.075372 | 138.398 |
| w6 | 31 | -0.001188 | 88.574 |
| w7 | 15 | -0.124866 | -16.225 |
| w8 | 17 | -0.02326 | -10.247 |
| w9 | 15 | -0.097963 | -56.066 |
| w10 | 23 | 0.020227 | 39.02 |
| w11 | 32 | -0.060972 | 50.25 |
| w12 | 8 | -0.057724 | -7.732 |
| w13 | 28 | 0.034012 | 23.708 |
| w14 | 30 | 0.003659 | 28.967 |
| w15 | 22 | 0.096056 | 131.619 |
| w16 | 36 | -0.097945 | 6.272 |
| w17 | 11 | 0.100226 | 14.544 |
| w18 | 20 | 0.039826 | -5.584 |
| w19 | 17 | -0.081226 | -10.586 |
| w20 | 13 | 0.046004 | -2.954 |
| w21 | 11 | -0.134547 | -15.964 |
| w22 | 27 | -0.00572 | 52.563 |
| w23 | 10 | 0.042589 | 3.554 |
| w24 | 29 | 0.026263 | 60.594 |
| w25 | 18 | 0.102974 | 56.83 |
| w26 | 22 | -0.140288 | -26.812 |
| w27 | 33 | 0.01021 | 83.624 |
| w28 | 12 | -0.080242 | -2.862 |
| w29 | 36 | -0.005815 | 13.328 |
| w30 | 11 | -0.010696 | -14.945 |
| w31 | 22 | -0.075673 | -13.795 |
| w32 | 20 | 0.07904 | 21.161 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.030598 | 17.022 |
| w2 | 19 | 0.018492 | 10.815 |
| w3 | 30 | -0.235504 | -23.917 |
| w4 | 22 | 0.128688 | 236.602 |
| w5 | 32 | -0.029289 | 40.178 |
| w6 | 23 | 0.035181 | 93.593 |
| w7 | 11 | -0.061937 | -13.146 |
| w8 | 9 | -0.033017 | -12.762 |
| w9 | 9 | -0.131133 | -11.723 |
| w10 | 38 | -0.111509 | 25.557 |
| w11 | 27 | 0.060459 | 17.208 |
| w12 | 10 | -0.068265 | -9.496 |
| w13 | 26 | 0.034335 | 18.939 |
| w14 | 29 | 0.00963 | 15.343 |
| w15 | 28 | 0.03623 | 53.572 |
| w16 | 39 | -0.179418 | 6.021 |
| w17 | 14 | 0.060715 | 13.328 |
| w18 | 23 | 0.004499 | -8.771 |
| w19 | 15 | -0.092355 | -20.006 |
| w20 | 12 | 0.015112 | -4.089 |
| w21 | 23 | -0.029651 | 6.985 |
| w22 | 29 | -0.036757 | -0.623 |
| w23 | 21 | -0.152179 | -22.658 |
| w24 | 20 | -0.171364 | -14.447 |
| w25 | 23 | 0.099082 | 40.27 |
| w26 | 5 | -0.124587 | -4.737 |
| w27 | 31 | -0.01748 | 69.751 |
| w28 | 13 | -0.083042 | -14.478 |
| w29 | 29 | 0.040827 | 32.084 |
| w30 | 9 | -0.381462 | -30.773 |
| w31 | 14 | -0.067201 | -5.057 |
| w32 | 19 | -0.086926 | -15.182 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 28 | 0.123108 | 130.823 |
| w7 | 11 | -0.068104 | -7.358 |
| w8 | 5 | -0.068076 | -12.093 |
| w9 | 16 | -0.084229 | -11.753 |
| w10 | 19 | -0.207302 | -22.355 |
| w11 | 9 | -0.02967 | -4.875 |
| w12 | 13 | 0.041856 | -12.311 |
| w13 | 27 | 0.007036 | 5.466 |
| w14 | 20 | 0.10663 | 42.73 |
| w15 | 13 | 0.182299 | 171.281 |
| w16 | 33 | 0.005485 | 91.843 |
| w17 | 9 | 0.091955 | 32.236 |
| w18 | 7 | -0.044595 | -13.491 |
| w19 | 16 | -0.132404 | -9.698 |
| w20 | 10 | 0.036353 | -6.745 |
| w21 | 14 | 0.046871 | 21.866 |
| w22 | 18 | -0.097828 | -0.169 |
| w23 | 16 | -0.115257 | -18.484 |
| w24 | 14 | 0.000871 | 19.651 |
| w25 | 15 | 0.018436 | 11.7 |
| w26 | 15 | -0.027873 | 3.535 |
| w27 | 24 | 0.305336 | 293.928 |
| w28 | 5 | -0.13754 | -4.566 |
| w29 | 30 | 0.086054 | 41.32 |
| w30 | 7 | -0.079437 | -20.651 |
| w31 | 15 | -0.155079 | -26.418 |
| w32 | 12 | -0.00403 | -2.095 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 11 | 0.023912 | -13.162 |
| w9 | 5 | -0.10711 | -43.304 |
| w10 | 22 | 0.073154 | 69.101 |
| w11 | 23 | -0.123969 | -3.137 |
| w12 | 12 | -0.025239 | -10.737 |
| w13 | 17 | 0.083149 | 45.65 |
| w14 | 28 | -0.039896 | -5.259 |
| w15 | 30 | -0.136366 | -5.581 |
| w16 | 27 | -0.022049 | 59.485 |
| w17 | 17 | 0.078959 | 27.665 |
| w18 | 16 | -0.07621 | -24.871 |
| w19 | 12 | -0.092746 | -16.025 |
| w20 | 8 | -0.011006 | -7.858 |
| w21 | 15 | -0.131007 | -22.757 |
| w22 | 16 | 0.034456 | 10.073 |
| w23 | 7 | 0.141035 | 89.584 |
| w24 | 33 | -0.196143 | -5.833 |
| w25 | 26 | 0.094964 | 73.305 |
| w26 | 11 | -0.215962 | -19.94 |
| w27 | 25 | -0.015956 | 34.414 |
| w28 | 11 | -0.108906 | -7.868 |
| w29 | 49 | -0.130411 | 20.231 |
| w30 | 26 | -0.097067 | -18.654 |
| w31 | 10 | -0.041412 | -8.309 |
| w32 | 12 | -0.10655 | -42.236 |

- w7 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.187285 | 218.604 |
| w2 | 20 | 0.000714 | 8.036 |
| w3 | 14 | 0.029046 | -8.281 |
| w4 | 36 | 0.056245 | 225.606 |
| w5 | 22 | 0.147056 | 110.545 |
| w6 | 15 | 0.059641 | 62.264 |
| w7 | 14 | 0.102368 | 19.828 |
| w8 | 11 | 0.069715 | -7.241 |
| w9 | 3 | -0.176888 | -19.572 |
| w10 | 36 | -0.20376 | -14.393 |
| w11 | 20 | 0.057034 | 29.961 |
| w12 | 13 | -0.129241 | -22.79 |
| w13 | 24 | 0.038419 | 39.733 |
| w14 | 36 | -0.019903 | 62.561 |
| w15 | 23 | 0.089203 | 51.027 |
| w16 | 36 | -0.028089 | 73.981 |
| w17 | 17 | 0.055433 | 42.742 |
| w18 | 22 | -0.027266 | -12.624 |
| w19 | 20 | -0.013692 | -8.895 |
| w20 | 15 | 0.066262 | 3.955 |
| w21 | 12 | -0.064872 | -8.622 |
| w22 | 27 | -0.037308 | 24.516 |
| w23 | 13 | -0.050705 | -3.147 |
| w24 | 26 | 0.027845 | 25.273 |
| w25 | 20 | 0.054219 | 28.901 |
| w26 | 9 | -0.014899 | -2.094 |
| w27 | 20 | 0.06049 | 43.816 |
| w28 | 0 | -0.047881 | 0.0 |
| w29 | 24 | 0.042659 | 82.907 |
| w30 | 12 | -0.042935 | -7.612 |
| w31 | 23 | -0.114423 | -22.532 |
| w32 | 22 | 0.05097 | 9.684 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 26 | 0.04987 | 59.728 |
| w11 | 9 | -0.042413 | -5.863 |
| w12 | 12 | -0.059245 | -20.102 |
| w13 | 15 | 0.06981 | 44.21 |
| w14 | 38 | -0.112073 | 28.781 |
| w15 | 25 | 0.020842 | 11.849 |
| w16 | 35 | 0.003187 | 71.734 |
| w17 | 15 | 0.049436 | 69.766 |
| w18 | 5 | -0.076386 | -10.856 |
| w19 | 18 | -0.054131 | -23.458 |
| w20 | 12 | 0.000691 | -5.127 |
| w21 | 2 | -0.014016 | -1.073 |
| w22 | 27 | -0.046973 | 12.686 |
| w23 | 8 | -0.057437 | -5.274 |
| w24 | 20 | 0.084782 | 143.283 |
| w25 | 19 | 0.051863 | 2.878 |
| w26 | 14 | -0.111832 | -21.504 |
| w27 | 22 | 0.172035 | 148.824 |
| w28 | 4 | -0.276636 | -6.985 |
| w29 | 23 | -0.000417 | 8.798 |
| w30 | 11 | 0.050228 | -8.961 |
| w31 | 10 | -0.220934 | -10.49 |
| w32 | 23 | -0.093585 | -19.0 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 19 | -0.033022 | -17.929 |
| w14 | 38 | -0.146791 | 15.46 |
| w15 | 19 | -0.227799 | -21.918 |
| w16 | 29 | 0.030518 | 61.507 |
| w17 | 14 | 0.028167 | 27.826 |
| w18 | 14 | 0.00575 | 18.887 |
| w19 | 14 | -0.008334 | -15.015 |
| w20 | 20 | 0.028578 | 6.96 |
| w21 | 17 | -0.123991 | -13.022 |
| w22 | 15 | 0.090057 | 23.659 |
| w23 | 4 | -0.024791 | -0.703 |
| w24 | 18 | -0.051293 | 8.809 |
| w25 | 16 | 0.086767 | 15.319 |
| w26 | 5 | -0.029361 | 0.008 |
| w27 | 21 | 0.12141 | 61.033 |
| w28 | 5 | -0.102938 | -9.17 |
| w29 | 29 | -0.108535 | -11.463 |
| w30 | 6 | -0.058035 | -5.417 |
| w31 | 19 | -0.148526 | -18.224 |
| w32 | 19 | -0.053294 | -16.181 |

- w12 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 14 | -0.112793 | -13.697 |
| w16 | 40 | 0.01519 | 63.104 |
| w17 | 16 | -0.003367 | 2.943 |
| w18 | 19 | 0.103493 | 35.686 |
| w19 | 11 | -0.179983 | -28.197 |
| w20 | 13 | 0.030335 | -8.928 |
| w21 | 19 | -0.08262 | -37.137 |
| w22 | 19 | 0.004236 | -6.589 |
| w23 | 4 | -0.059957 | -2.469 |
| w24 | 37 | -0.033316 | 51.32 |
| w25 | 16 | 0.098186 | 14.735 |
| w26 | 8 | -0.11126 | -9.419 |
| w27 | 21 | 0.177812 | 163.876 |
| w28 | 3 | -0.034814 | -2.981 |
| w29 | 29 | 0.059842 | 13.866 |
| w30 | 1 | -0.189986 | -2.601 |
| w31 | 28 | -0.082832 | -16.661 |
| w32 | 16 | -0.170603 | -27.998 |

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
| w15 | 25 | -0.084936 | -8.405 |
| w16 | 27 | -0.029517 | 80.107 |
| w17 | 10 | 0.056343 | 19.319 |
| w18 | 19 | -0.120026 | -14.839 |
| w19 | 17 | -0.104498 | -17.511 |
| w20 | 24 | -0.198296 | -24.513 |
| w21 | 20 | -0.059248 | -16.309 |
| w22 | 31 | -0.055936 | 8.282 |
| w23 | 28 | -0.032088 | 4.316 |
| w24 | 44 | -0.086772 | 32.786 |
| w25 | 19 | 0.10403 | 33.084 |
| w26 | 30 | -0.09984 | 5.687 |
| w27 | 32 | 0.101607 | 197.153 |
| w28 | 21 | -0.042765 | -12.996 |
| w29 | 39 | -0.008346 | 62.084 |
| w30 | 9 | -0.118025 | -13.376 |
| w31 | 41 | -0.037489 | 13.583 |
| w32 | 29 | -0.067279 | -0.092 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 7 | 0.043114 | 11.528 |
| w18 | 26 | -0.036463 | -3.382 |
| w19 | 14 | -0.024453 | -14.379 |
| w20 | 12 | -0.005415 | -6.227 |
| w21 | 6 | -0.178074 | -13.455 |
| w22 | 23 | -0.02461 | 2.606 |
| w23 | 9 | 0.038274 | -1.865 |
| w24 | 19 | -0.014242 | 39.322 |
| w25 | 20 | 0.074448 | 8.98 |
| w26 | 16 | -0.076853 | -12.385 |
| w27 | 22 | 0.151146 | 82.0 |
| w28 | 2 | -0.060365 | -3.259 |
| w29 | 23 | -0.007697 | -3.706 |
| w30 | 11 | -0.018945 | -33.119 |
| w31 | 9 | -0.152754 | -16.572 |
| w32 | 9 | -0.179013 | -21.153 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 15 | 0.062415 | 0.625 |
| w21 | 7 | -0.134698 | -17.063 |
| w22 | 20 | -0.039375 | 4.16 |
| w23 | 8 | 0.030992 | -3.708 |
| w24 | 28 | 0.233859 | 216.643 |
| w25 | 25 | 0.014018 | 11.218 |
| w26 | 8 | -0.137187 | -22.179 |
| w27 | 30 | 0.009521 | 47.95 |
| w28 | 4 | -0.025005 | 1.614 |
| w29 | 29 | -0.011074 | 3.136 |
| w30 | 16 | -0.008386 | -10.741 |
| w31 | 18 | -0.187415 | -18.319 |
| w32 | 12 | -0.028385 | -4.85 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 18 | -0.015639 | 3.611 |
| w23 | 9 | 0.070795 | 1.673 |
| w24 | 20 | 0.056698 | 124.402 |
| w25 | 17 | 0.123704 | 51.398 |
| w26 | 19 | -0.016706 | -18.981 |
| w27 | 25 | -0.117209 | -1.954 |
| w28 | 0 | -0.142641 | 0.0 |
| w29 | 28 | 0.001518 | -0.777 |
| w30 | 8 | -0.100495 | -20.188 |
| w31 | 22 | -0.168062 | -27.661 |
| w32 | 15 | 0.033476 | 64.558 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 24 | 0.003485 | 22.153 |
| w25 | 27 | 0.020264 | 7.75 |
| w26 | 8 | -0.107223 | -8.548 |
| w27 | 32 | -0.011318 | 102.541 |
| w28 | 10 | 0.086075 | 7.171 |
| w29 | 16 | 0.016866 | 1.887 |
| w30 | 9 | -0.034251 | -23.296 |
| w31 | 16 | -0.147408 | -25.216 |
| w32 | 21 | -0.042667 | -19.302 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 22 | 0.196559 | 132.032 |
| w6 | 27 | -0.039652 | 6.709 |
| w7 | 12 | -0.006545 | -6.57 |
| w8 | 17 | -0.036552 | -26.687 |
| w9 | 9 | -0.114891 | -25.864 |
| w10 | 12 | 0.012974 | 28.233 |
| w11 | 26 | 0.043303 | 3.104 |
| w12 | 5 | -0.043711 | -3.238 |
| w13 | 20 | 0.13636 | 79.899 |
| w14 | 40 | -0.107729 | 14.945 |
| w15 | 16 | -0.083992 | -6.869 |
| w16 | 42 | -0.187064 | 35.467 |
| w17 | 11 | 0.029416 | 8.672 |
| w18 | 18 | -0.040491 | -14.953 |
| w19 | 18 | 0.017924 | 23.665 |
| w20 | 14 | -0.028153 | -10.965 |
| w21 | 7 | -0.059107 | -8.146 |
| w22 | 21 | -0.120625 | -14.117 |
| w23 | 8 | 0.005825 | -1.829 |
| w24 | 27 | -0.174415 | -25.019 |
| w25 | 15 | 0.020784 | 3.223 |
| w26 | 26 | 0.028909 | 17.003 |
| w27 | 28 | -0.036772 | 33.93 |
| w28 | 11 | -0.126296 | -11.824 |
| w29 | 17 | 0.006264 | -0.327 |
| w30 | 24 | 0.176989 | 307.726 |
| w31 | 12 | 0.071593 | 8.804 |
| w32 | 27 | 0.070123 | 51.416 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 32 | 0.140238 | 180.52 |
| w6 | 15 | 0.067601 | 109.8 |
| w7 | 15 | -0.153094 | -18.967 |
| w8 | 13 | -0.06365 | -17.417 |
| w9 | 12 | -0.041101 | -22.606 |
| w10 | 24 | -0.045157 | 20.903 |
| w11 | 25 | -0.075934 | -9.243 |
| w12 | 10 | -0.021154 | -7.813 |
| w13 | 22 | 0.02872 | 23.06 |
| w14 | 26 | -0.030027 | 40.398 |
| w15 | 28 | -0.064611 | 9.709 |
| w16 | 36 | -0.058612 | 42.834 |
| w17 | 13 | 0.02783 | 11.436 |
| w18 | 12 | -0.109142 | -23.384 |
| w19 | 29 | -0.017247 | -7.09 |
| w20 | 22 | -0.031041 | -9.229 |
| w21 | 15 | -0.112396 | -21.54 |
| w22 | 21 | 0.013515 | 6.582 |
| w23 | 9 | 0.029286 | -1.036 |
| w24 | 35 | -0.057058 | 9.335 |
| w25 | 10 | -0.198858 | -27.27 |
| w26 | 28 | -0.017772 | 15.985 |
| w27 | 28 | -0.016762 | 3.008 |
| w28 | 27 | -0.015804 | 16.136 |
| w29 | 15 | 0.123365 | 25.401 |
| w30 | 47 | -0.21076 | 2.644 |
| w31 | 18 | -0.019886 | 4.953 |
| w32 | 30 | 0.077712 | 49.041 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 16 | -0.031374 | -2.749 |
| w18 | 35 | -0.104994 | 7.226 |
| w19 | 17 | -0.123763 | -37.944 |
| w20 | 15 | 0.053993 | 5.645 |
| w21 | 8 | -0.235637 | -21.904 |
| w22 | 19 | 0.01891 | 8.721 |
| w23 | 11 | -0.025577 | -14.855 |
| w24 | 29 | -0.12307 | -13.458 |
| w25 | 9 | 0.135945 | 24.02 |
| w26 | 12 | -0.139945 | -14.701 |
| w27 | 19 | 0.160515 | 182.315 |
| w28 | 11 | 0.083687 | 10.964 |
| w29 | 24 | 0.090761 | 21.244 |
| w30 | 1 | -0.160594 | -2.174 |
| w31 | 9 | -0.08504 | -14.958 |
| w32 | 21 | 0.101021 | 57.433 |

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
| w17 | 25 | -0.056255 | -8.464 |
| w18 | 17 | -0.095383 | -17.806 |
| w19 | 19 | -0.034234 | -10.369 |
| w20 | 19 | 0.037158 | -4.833 |
| w21 | 9 | -0.125161 | -29.832 |
| w22 | 20 | 0.029469 | 8.331 |
| w23 | 12 | -0.01837 | -5.447 |
| w24 | 34 | -0.201089 | 9.408 |
| w25 | 19 | 0.078955 | 6.542 |
| w26 | 29 | -0.216361 | -12.895 |
| w27 | 31 | 0.001007 | 46.025 |
| w28 | 4 | -0.000939 | -2.171 |
| w29 | 32 | -0.061324 | 7.411 |
| w30 | 7 | -0.043255 | -8.48 |
| w31 | 5 | -0.15205 | -12.183 |
| w32 | 18 | -0.035291 | -1.1 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 12 | -0.080145 | -7.266 |
| w20 | 16 | -0.005771 | -2.763 |
| w21 | 17 | -0.002679 | -1.831 |
| w22 | 30 | 0.026379 | 138.459 |
| w23 | 12 | -0.026612 | -6.51 |
| w24 | 26 | -0.011163 | 162.647 |
| w25 | 11 | -0.0215 | -13.663 |
| w26 | 10 | -0.110343 | -28.799 |
| w27 | 31 | -0.036339 | 1.264 |
| w28 | 3 | -0.09961 | -2.057 |
| w29 | 29 | -0.00865 | 13.754 |
| w30 | 2 | -0.07254 | -6.052 |
| w31 | 11 | -0.061358 | -4.856 |
| w32 | 15 | 0.050158 | 24.911 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 22 | 0.067396 | 24.965 |
| w23 | 13 | -0.120395 | -20.477 |
| w24 | 23 | -0.030878 | 18.369 |
| w25 | 24 | -0.072376 | -15.225 |
| w26 | 9 | 0.026152 | -10.104 |
| w27 | 18 | -0.07756 | 5.112 |
| w28 | 9 | -0.116025 | -10.589 |
| w29 | 29 | -0.024157 | 9.707 |
| w30 | 5 | -0.032885 | -3.715 |
| w31 | 14 | -0.064697 | -8.53 |
| w32 | 18 | -0.029107 | -4.904 |

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
| w27 | 21 | 0.030979 | 57.41 |
| w28 | 9 | -0.084477 | -5.105 |
| w29 | 21 | 0.031515 | 5.729 |
| w30 | 7 | -0.091867 | -19.898 |
| w31 | 11 | -0.058506 | -0.48 |
| w32 | 21 | 0.012937 | 29.511 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.050188 | 7.843 |
| w18 | 9 | 0.077338 | -1.769 |
| w19 | 9 | -0.07659 | -17.666 |
| w20 | 14 | 0.049982 | 3.183 |
| w21 | 7 | -0.165954 | -30.212 |
| w22 | 18 | -0.036383 | 5.534 |
| w23 | 9 | 0.011152 | -2.558 |
| w24 | 25 | -0.038964 | 37.214 |
| w25 | 15 | 0.054427 | 0.941 |
| w26 | 5 | -0.164436 | -11.545 |
| w27 | 26 | 0.005775 | 33.508 |
| w28 | 0 | -0.171266 | 0.0 |
| w29 | 22 | -0.024557 | -9.356 |
| w30 | 11 | -0.229291 | -31.997 |
| w31 | 17 | -0.087985 | -27.726 |
| w32 | 13 | 0.021284 | -11.176 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 17 | -0.01095 | -7.208 |
| w19 | 9 | -0.077155 | -10.68 |
| w20 | 10 | 0.010896 | -3.665 |
| w21 | 2 | 0.07855 | -2.442 |
| w22 | 28 | 0.102295 | 115.66 |
| w23 | 12 | -0.002557 | -6.678 |
| w24 | 25 | 0.053457 | 50.79 |
| w25 | 17 | 0.175346 | 62.298 |
| w26 | 7 | -0.021755 | -3.869 |
| w27 | 25 | -0.058372 | 24.563 |
| w28 | 1 | -0.046854 | -0.574 |
| w29 | 28 | 0.008127 | -0.381 |
| w30 | 7 | -0.126083 | -13.017 |
| w31 | 9 | -0.172096 | -16.026 |
| w32 | 14 | -0.046694 | -25.879 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 9 | 0.021519 | -0.664 |
| w29 | 26 | 0.022499 | -2.496 |
| w30 | 12 | -0.085329 | -4.082 |
| w31 | 25 | 0.060792 | 4.273 |
| w32 | 10 | 0.000284 | 1.775 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 27 | -0.039838 | 1.303 |
| w15 | 22 | 0.076614 | 69.824 |
| w16 | 26 | 0.004722 | 336.596 |
| w17 | 13 | 0.064979 | 7.391 |
| w18 | 13 | -0.031456 | -13.813 |
| w19 | 19 | -0.084109 | -12.487 |
| w20 | 14 | 0.030203 | -7.92 |
| w21 | 19 | 0.075406 | 50.718 |
| w22 | 20 | -0.119228 | -17.371 |
| w23 | 19 | 0.033009 | -5.747 |
| w24 | 25 | 0.043841 | 34.184 |
| w25 | 23 | 0.227856 | 106.416 |
| w26 | 10 | -0.119205 | -19.954 |
| w27 | 22 | 0.165674 | 205.392 |
| w28 | 4 | -0.172488 | -6.682 |
| w29 | 28 | 0.023256 | 12.075 |
| w30 | 11 | -0.055221 | -23.2 |
| w31 | 14 | -0.002897 | 1.459 |
| w32 | 14 | -0.006207 | -10.697 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 15 | 0.283629 | 248.781 |
| w26 | 13 | 0.038085 | 8.56 |
| w27 | 27 | 0.02795 | 56.164 |
| w28 | 9 | 0.027469 | -0.203 |
| w29 | 25 | 0.056291 | 15.883 |
| w30 | 6 | -0.134829 | -17.298 |
| w31 | 18 | -0.129952 | -14.93 |
| w32 | 20 | -0.029339 | -2.091 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

