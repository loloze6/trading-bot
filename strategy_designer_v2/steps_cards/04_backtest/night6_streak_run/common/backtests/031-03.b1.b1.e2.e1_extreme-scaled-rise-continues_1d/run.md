# Backtest of 031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-03.b1.b1.e2.e1_extreme-scaled-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.005673 | 8.691 |
| w2 | 6 | 0.096392 | 48.627 |
| w3 | 15 | -0.007993 | 65.214 |
| w4 | 15 | -0.039305 | -29.637 |
| w5 | 21 | -0.020402 | 86.373 |
| w6 | 7 | 0.104203 | 123.592 |
| w7 | 4 | -0.031578 | 12.215 |
| w8 | 6 | 0.053015 | -1.008 |
| w9 | 4 | -0.116757 | -19.943 |
| w10 | 3 | -0.04686 | -4.187 |
| w11 | 12 | 0.107905 | 52.038 |
| w12 | 3 | 0.044482 | -1.091 |
| w13 | 14 | -0.037534 | 26.202 |
| w14 | 4 | 0.091742 | 40.367 |
| w15 | 15 | -0.005509 | 127.177 |
| w16 | 18 | 0.052632 | 23.198 |
| w17 | 8 | -0.019008 | -12.918 |
| w18 | 9 | 0.114609 | -2.086 |
| w19 | 12 | -0.07444 | -5.726 |
| w20 | 2 | -0.035822 | 0.655 |
| w21 | 4 | -0.203467 | -30.358 |
| w22 | 17 | 0.064053 | 59.244 |
| w23 | 3 | 0.098928 | 0.213 |
| w24 | 16 | 0.021361 | 86.92 |
| w25 | 14 | 0.10243 | 41.716 |
| w26 | 12 | 0.004011 | -25.232 |
| w27 | 14 | 0.072766 | 61.465 |
| w28 | 8 | -0.024736 | 7.157 |
| w29 | 12 | -0.064692 | 4.675 |
| w30 | 12 | -0.057119 | -33.705 |
| w31 | 7 | -0.005995 | -2.253 |
| w32 | 11 | 0.120121 | -5.285 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.022741 | -2.388 |
| w2 | 8 | -0.036412 | -30.149 |
| w3 | 7 | -0.085942 | -21.525 |
| w4 | 11 | 0.195944 | 144.639 |
| w5 | 11 | -0.083489 | 16.107 |
| w6 | 9 | 0.148255 | 143.261 |
| w7 | 7 | -0.038897 | 3.297 |
| w8 | 2 | -0.082828 | -25.769 |
| w9 | 6 | -0.113792 | -13.532 |
| w10 | 10 | -0.109537 | 1.843 |
| w11 | 7 | -0.105093 | 20.522 |
| w12 | 6 | 0.152139 | -24.054 |
| w13 | 9 | 0.054576 | 30.307 |
| w14 | 11 | 0.011592 | -8.399 |
| w15 | 11 | -0.053652 | 37.341 |
| w16 | 14 | -0.024056 | 35.222 |
| w17 | 10 | 0.04692 | 7.721 |
| w18 | 8 | -0.083571 | -26.285 |
| w19 | 10 | -0.002335 | -38.221 |
| w20 | 8 | -0.000295 | -6.31 |
| w21 | 7 | -0.053729 | 11.984 |
| w22 | 11 | -0.03371 | 14.107 |
| w23 | 8 | -0.116809 | -19.594 |
| w24 | 11 | -0.073533 | -4.173 |
| w25 | 7 | 0.010073 | 14.879 |
| w26 | 4 | 0.016439 | -7.834 |
| w27 | 11 | 0.014836 | 24.399 |
| w28 | 5 | -0.062898 | -13.656 |
| w29 | 11 | 0.000669 | 23.094 |
| w30 | 3 | -0.160778 | -30.871 |
| w31 | 0 | None | 0.0 |
| w32 | 17 | -0.040202 | -37.9 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 9 | 0.155494 | 111.129 |
| w7 | 9 | 0.144581 | 5.801 |
| w8 | 4 | 0.008115 | -11.854 |
| w9 | 6 | 0.155833 | 48.375 |
| w10 | 2 | -0.04871 | -9.734 |
| w11 | 4 | -0.058853 | -21.365 |
| w12 | 5 | 0.047058 | -21.71 |
| w13 | 7 | -0.009524 | 30.286 |
| w14 | 4 | 0.128559 | 44.824 |
| w15 | 8 | 0.258903 | 183.012 |
| w16 | 12 | 0.112609 | 127.88 |
| w17 | 6 | 0.061268 | 40.503 |
| w18 | 6 | 0.003367 | -27.421 |
| w19 | 2 | 0.077163 | 8.63 |
| w20 | 0 | -0.024905 | 0.0 |
| w21 | 6 | 0.015185 | 32.046 |
| w22 | 3 | -7.9e-05 | 20.121 |
| w23 | 5 | -0.051898 | 17.503 |
| w24 | 6 | 0.101249 | 36.251 |
| w25 | 6 | -0.081601 | 12.311 |
| w26 | 4 | 0.104795 | 24.216 |
| w27 | 7 | 0.361053 | 281.276 |
| w28 | 7 | -0.074944 | -23.989 |
| w29 | 8 | 0.095046 | 48.258 |
| w30 | 2 | -0.045391 | -13.95 |
| w31 | 6 | 0.032375 | -9.628 |
| w32 | 13 | 0.065612 | -18.011 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 5 | -0.053142 | -25.934 |
| w9 | 4 | -0.067867 | -44.82 |
| w10 | 6 | -0.009127 | -0.411 |
| w11 | 5 | 0.046482 | -1.563 |
| w12 | 5 | 0.053278 | 0.396 |
| w13 | 10 | 0.083022 | 46.935 |
| w14 | 5 | 0.138606 | 18.909 |
| w15 | 7 | -0.123664 | 3.962 |
| w16 | 9 | 0.108899 | 67.263 |
| w17 | 9 | 0.033655 | 15.063 |
| w18 | 6 | -0.14257 | -19.464 |
| w19 | 12 | 0.123634 | 9.428 |
| w20 | 3 | 0.03909 | 6.702 |
| w21 | 6 | -0.012264 | -11.375 |
| w22 | 14 | -0.028505 | -8.614 |
| w23 | 7 | 0.281835 | 88.358 |
| w24 | 11 | -0.174368 | -20.342 |
| w25 | 9 | 0.07223 | 41.576 |
| w26 | 4 | -0.003877 | -26.928 |
| w27 | 9 | -0.073473 | -2.809 |
| w28 | 4 | -0.088588 | -6.264 |
| w29 | 12 | -0.100897 | 6.995 |
| w30 | 13 | -0.185495 | -27.271 |
| w31 | 7 | -0.165973 | -26.073 |
| w32 | 6 | -0.039626 | -13.281 |

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
| w1 | 12 | 0.109562 | 144.34 |
| w2 | 6 | -0.098696 | -5.88 |
| w3 | 3 | -0.112277 | -12.165 |
| w4 | 14 | 0.150905 | 243.88 |
| w5 | 25 | 0.098327 | 99.337 |
| w6 | 5 | 0.045544 | 40.824 |
| w7 | 11 | 0.116551 | 40.504 |
| w8 | 6 | -0.070635 | -14.919 |
| w9 | 4 | 0.076215 | 7.568 |
| w10 | 7 | -0.027332 | -10.551 |
| w11 | 11 | 0.087254 | 60.196 |
| w12 | 5 | -0.098756 | -28.286 |
| w13 | 11 | 0.000283 | 67.019 |
| w14 | 7 | 0.072137 | 31.511 |
| w15 | 12 | -0.144515 | 17.61 |
| w16 | 22 | 0.04808 | 82.751 |
| w17 | 6 | 0.120975 | 7.945 |
| w18 | 11 | -0.088795 | -2.36 |
| w19 | 9 | 0.054685 | 12.127 |
| w20 | 5 | -0.030012 | -0.09 |
| w21 | 3 | 0.100695 | 11.62 |
| w22 | 10 | -0.04079 | 6.532 |
| w23 | 4 | -0.049556 | -1.027 |
| w24 | 11 | -0.154615 | 10.729 |
| w25 | 10 | 0.122765 | 43.571 |
| w26 | 6 | -0.001931 | -14.701 |
| w27 | 12 | -0.003206 | 18.481 |
| w28 | 2 | -0.115151 | -8.423 |
| w29 | 10 | 0.078335 | 96.999 |
| w30 | 6 | -0.113298 | -18.595 |
| w31 | 8 | -0.052758 | -3.275 |
| w32 | 8 | 0.037119 | -1.419 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 11 | 0.063363 | 43.378 |
| w11 | 4 | -0.078311 | -7.561 |
| w12 | 5 | -0.11031 | -33.219 |
| w13 | 13 | -0.003384 | 43.697 |
| w14 | 7 | -0.060549 | 57.52 |
| w15 | 9 | 0.026745 | 56.382 |
| w16 | 15 | 0.174651 | 80.459 |
| w17 | 13 | 0.019019 | 80.634 |
| w18 | 2 | -0.148207 | -25.531 |
| w19 | 2 | 0.068874 | -7.469 |
| w20 | 6 | 0.005431 | -32.174 |
| w21 | 4 | -0.084958 | -11.738 |
| w22 | 12 | -0.038367 | -2.195 |
| w23 | 6 | -0.191398 | -13.313 |
| w24 | 15 | 0.143969 | 128.701 |
| w25 | 5 | 0.031234 | 3.303 |
| w26 | 11 | -0.08126 | -26.276 |
| w27 | 14 | 0.298175 | 129.395 |
| w28 | 3 | -0.272904 | -29.668 |
| w29 | 4 | 0.045587 | 22.79 |
| w30 | 3 | -0.024337 | -14.577 |
| w31 | 6 | 0.043445 | -8.87 |
| w32 | 12 | -0.128606 | -53.392 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 4 | -0.156091 | -14.234 |
| w14 | 9 | 0.033778 | 60.221 |
| w15 | 4 | -0.126305 | -7.371 |
| w16 | 10 | 0.019927 | 73.171 |
| w17 | 12 | -0.060312 | 10.311 |
| w18 | 5 | -0.062481 | 44.65 |
| w19 | 3 | -0.068902 | 1.234 |
| w20 | 9 | -0.05637 | -5.751 |
| w21 | 4 | 0.065438 | -15.5 |
| w22 | 6 | -0.089486 | 0.887 |
| w23 | 2 | -0.040379 | 4.657 |
| w24 | 16 | -0.058808 | 79.06 |
| w25 | 7 | 0.078996 | -20.672 |
| w26 | 3 | -0.106229 | -27.401 |
| w27 | 14 | 0.131135 | 38.145 |
| w28 | 3 | 0.005779 | -12.887 |
| w29 | 11 | -0.042064 | 13.043 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.065487 | 0.317 |
| w32 | 14 | -0.018433 | -32.337 |

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
| w15 | 6 | -0.061325 | 3.929 |
| w16 | 13 | 0.028951 | 54.726 |
| w17 | 8 | -0.052426 | 12.573 |
| w18 | 5 | 0.137231 | 60.714 |
| w19 | 5 | 0.097824 | -21.344 |
| w20 | 5 | -0.063888 | -19.178 |
| w21 | 6 | -0.008603 | -34.14 |
| w22 | 8 | -0.06347 | -9.96 |
| w23 | 4 | 0.083816 | 0.381 |
| w24 | 15 | 0.054269 | 63.868 |
| w25 | 8 | 0.080496 | 17.515 |
| w26 | 7 | -0.053071 | -26.006 |
| w27 | 12 | 0.256938 | 137.31 |
| w28 | 4 | 0.008799 | 10.884 |
| w29 | 8 | 0.056569 | 31.548 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.015408 | -1.672 |
| w32 | 5 | -0.161902 | -40.521 |

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
| w15 | 5 | -0.008593 | -15.018 |
| w16 | 10 | 0.034131 | 112.42 |
| w17 | 9 | 0.112929 | 18.288 |
| w18 | 9 | -0.111929 | -23.532 |
| w19 | 8 | 0.000433 | -4.878 |
| w20 | 4 | -0.179451 | -16.589 |
| w21 | 2 | -0.031733 | 0.267 |
| w22 | 11 | -0.141304 | 6.969 |
| w23 | 12 | -0.128751 | -26.95 |
| w24 | 15 | -0.074108 | 13.934 |
| w25 | 14 | 0.092735 | 47.457 |
| w26 | 19 | 0.137169 | 80.461 |
| w27 | 4 | -0.123008 | -7.883 |
| w28 | 4 | -0.03124 | 5.932 |
| w29 | 14 | -0.033167 | 31.073 |
| w30 | 4 | -0.02752 | -2.391 |
| w31 | 6 | -0.092405 | 11.626 |
| w32 | 16 | -0.098203 | -14.776 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.109139 | -6.129 |
| w18 | 14 | -0.127203 | -24.083 |
| w19 | 7 | -0.007854 | -9.009 |
| w20 | 4 | 0.018072 | 2.062 |
| w21 | 2 | -0.076107 | -25.137 |
| w22 | 13 | -0.09341 | -4.836 |
| w23 | 4 | 0.082172 | -1.305 |
| w24 | 14 | 0.025042 | 41.411 |
| w25 | 5 | 0.073245 | 17.93 |
| w26 | 9 | -0.110231 | -32.471 |
| w27 | 12 | 0.136028 | 30.002 |
| w28 | 1 | -0.008942 | -4.335 |
| w29 | 9 | 0.00851 | 7.414 |
| w30 | 5 | -0.049948 | -35.936 |
| w31 | 4 | -0.087825 | -12.381 |
| w32 | 8 | -0.117519 | -31.517 |

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
| w20 | 4 | -0.01012 | -15.258 |
| w21 | 2 | 0.019731 | -33.07 |
| w22 | 9 | 0.02203 | -0.182 |
| w23 | 8 | -0.082299 | 0.667 |
| w24 | 20 | 0.145813 | 148.27 |
| w25 | 5 | -0.013159 | 15.688 |
| w26 | 8 | -0.061958 | -28.725 |
| w27 | 20 | -0.01723 | 7.719 |
| w28 | 4 | -0.055269 | -11.77 |
| w29 | 6 | -0.051383 | 14.354 |
| w30 | 2 | 0.10026 | 4.052 |
| w31 | 5 | -0.048974 | -24.355 |
| w32 | 6 | -0.004532 | -16.092 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 15 | 0.025372 | 5.263 |
| w23 | 7 | -0.006481 | -4.03 |
| w24 | 19 | -0.03445 | 123.328 |
| w25 | 7 | -0.060677 | 65.248 |
| w26 | 3 | 0.010935 | -8.591 |
| w27 | 12 | 0.054692 | 24.638 |
| w28 | 5 | 0.01219 | -12.866 |
| w29 | 9 | -0.044723 | -1.322 |
| w30 | 4 | -0.013258 | -19.372 |
| w31 | 7 | -0.110539 | 0.347 |
| w32 | 9 | 0.013489 | 19.704 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 9 | -0.048827 | 18.575 |
| w25 | 10 | -0.056383 | -10.868 |
| w26 | 6 | -0.025947 | -9.26 |
| w27 | 12 | 0.005274 | 74.129 |
| w28 | 2 | 0.018978 | -0.4 |
| w29 | 9 | -0.021101 | 14.109 |
| w30 | 7 | -0.02533 | -37.124 |
| w31 | 7 | 0.007018 | -3.365 |
| w32 | 3 | -0.018153 | -13.531 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | 0.111662 | 89.015 |
| w6 | 9 | 0.039236 | 18.824 |
| w7 | 10 | 0.075616 | -1.764 |
| w8 | 4 | -0.202035 | -32.194 |
| w9 | 9 | -0.083304 | -49.909 |
| w10 | 3 | 0.101506 | 45.175 |
| w11 | 12 | 0.005225 | 6.009 |
| w12 | 4 | 0.07098 | -12.597 |
| w13 | 15 | 0.053577 | 70.599 |
| w14 | 5 | -0.002479 | 34.231 |
| w15 | 4 | -0.148077 | 13.635 |
| w16 | 10 | 0.091442 | 77.889 |
| w17 | 10 | 0.058678 | -9.98 |
| w18 | 8 | -0.168152 | -14.529 |
| w19 | 7 | 0.045777 | 47.926 |
| w20 | 5 | 0.003747 | -0.992 |
| w21 | 4 | -0.03218 | 0.103 |
| w22 | 9 | -0.024482 | -12.234 |
| w23 | 6 | 0.093538 | 18.707 |
| w24 | 13 | -0.169609 | -30.939 |
| w25 | 10 | 0.147773 | 13.132 |
| w26 | 4 | 0.103729 | 36.546 |
| w27 | 12 | -0.086368 | 15.646 |
| w28 | 5 | -0.123384 | 12.891 |
| w29 | 6 | -0.059609 | 2.176 |
| w30 | 21 | 0.134606 | 279.591 |
| w31 | 3 | -0.103992 | -21.961 |
| w32 | 14 | 0.049677 | 53.841 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 16 | -0.040999 | 109.025 |
| w6 | 10 | 0.118853 | 91.131 |
| w7 | 10 | -0.00311 | 3.22 |
| w8 | 4 | -0.048444 | -15.855 |
| w9 | 6 | -0.060008 | -21.258 |
| w10 | 2 | 0.050485 | 6.602 |
| w11 | 7 | -0.018971 | 9.692 |
| w12 | 6 | 0.00782 | 5.555 |
| w13 | 13 | 0.008734 | 58.524 |
| w14 | 4 | -0.002533 | 29.765 |
| w15 | 10 | -0.151961 | 27.951 |
| w16 | 12 | -0.042159 | 50.065 |
| w17 | 12 | -0.082219 | -8.502 |
| w18 | 7 | 0.01518 | 13.549 |
| w19 | 11 | -0.188116 | -32.716 |
| w20 | 5 | 0.058474 | 15.017 |
| w21 | 6 | -0.065086 | -19.229 |
| w22 | 8 | -0.016339 | 6.107 |
| w23 | 3 | 0.223116 | 28.942 |
| w24 | 14 | -0.159793 | -22.803 |
| w25 | 9 | -0.07466 | -45.416 |
| w26 | 7 | -0.028648 | 15.523 |
| w27 | 8 | -0.10099 | 44.511 |
| w28 | 6 | 0.04413 | 11.23 |
| w29 | 11 | 0.127919 | 10.005 |
| w30 | 14 | -0.278416 | -12.617 |
| w31 | 4 | -0.084948 | -8.737 |
| w32 | 12 | 0.076157 | 44.78 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | -0.063849 | -16.977 |
| w18 | 8 | -0.227521 | -16.176 |
| w19 | 4 | -0.08963 | -26.858 |
| w20 | 2 | -0.02689 | 19.512 |
| w21 | 2 | -0.08757 | 2.277 |
| w22 | 5 | 0.097817 | 11.891 |
| w23 | 2 | 0.098582 | 22.088 |
| w24 | 8 | -0.027749 | 12.163 |
| w25 | 5 | 0.055539 | 31.232 |
| w26 | 9 | -0.007053 | -32.167 |
| w27 | 6 | 0.29475 | 181.403 |
| w28 | 4 | -0.082533 | 8.014 |
| w29 | 2 | 0.265914 | 69.184 |
| w30 | 4 | -0.023585 | -29.778 |
| w31 | 4 | 0.025919 | -12.24 |
| w32 | 8 | -0.2195 | -20.82 |

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
| w17 | 9 | -0.119681 | -17.85 |
| w18 | 2 | 0.027969 | 1.384 |
| w19 | 7 | 0.025766 | -18.821 |
| w20 | 5 | -0.078071 | -4.984 |
| w21 | 6 | -0.047486 | -39.602 |
| w22 | 7 | 0.056786 | 16.808 |
| w23 | 6 | 0.200053 | 41.804 |
| w24 | 11 | -0.02675 | 1.767 |
| w25 | 6 | -0.051423 | 20.191 |
| w26 | 9 | -0.152555 | -22.582 |
| w27 | 9 | 0.030877 | 40.677 |
| w28 | 2 | -0.031816 | -7.457 |
| w29 | 17 | -0.021752 | -3.662 |
| w30 | 5 | -0.057371 | -25.048 |
| w31 | 6 | 0.0112 | -21.063 |
| w32 | 5 | -0.009091 | 33.185 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | 0.053315 | 9.472 |
| w20 | 7 | -0.017511 | -1.811 |
| w21 | 2 | -0.075981 | -33.051 |
| w22 | 14 | -0.065949 | 123.34 |
| w23 | 4 | -0.012278 | -18.502 |
| w24 | 19 | 0.133133 | 267.107 |
| w25 | 4 | -0.211927 | -21.255 |
| w26 | 7 | -0.076626 | -21.972 |
| w27 | 10 | -0.007114 | -10.432 |
| w28 | 5 | -0.014753 | -6.759 |
| w29 | 11 | 0.000176 | 3.856 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.130384 | -30.231 |
| w32 | 8 | -0.067347 | 33.199 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 13 | 0.007305 | 31.647 |
| w23 | 5 | -0.123043 | -15.94 |
| w24 | 7 | -0.137909 | 6.199 |
| w25 | 7 | -0.044352 | -11.574 |
| w26 | 8 | -0.056182 | -34.687 |
| w27 | 10 | -0.035477 | -12.946 |
| w28 | 1 | -0.0104 | -1.867 |
| w29 | 9 | -0.007981 | 6.722 |
| w30 | 2 | -0.015458 | -2.112 |
| w31 | 8 | 0.012338 | 1.114 |
| w32 | 5 | 0.210179 | 46.314 |

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
| w27 | 7 | 0.047841 | 22.284 |
| w28 | 2 | -0.102893 | -11.38 |
| w29 | 7 | -0.040573 | 7.313 |
| w30 | 4 | 0.039043 | -4.601 |
| w31 | 3 | 0.012218 | -3.082 |
| w32 | 7 | -0.046022 | -1.589 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | 0.074341 | 24.71 |
| w18 | 3 | -0.126807 | -15.4 |
| w19 | 5 | 0.0222 | -5.304 |
| w20 | 1 | 0.046299 | 0.019 |
| w21 | 4 | -0.028486 | -26.779 |
| w22 | 10 | 0.011222 | 29.311 |
| w23 | 10 | -0.018675 | -41.155 |
| w24 | 13 | -0.092788 | 77.031 |
| w25 | 6 | 0.085912 | 12.091 |
| w26 | 3 | -0.016535 | -17.056 |
| w27 | 8 | 0.080554 | 6.236 |
| w28 | 4 | -0.133034 | -11.725 |
| w29 | 10 | -0.079415 | -7.991 |
| w30 | 4 | -0.160158 | -27.748 |
| w31 | 3 | -0.107372 | -13.481 |
| w32 | 4 | -0.105228 | -29.401 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 4 | -0.056382 | -13.752 |
| w19 | 5 | -0.017782 | -17.834 |
| w20 | 4 | -0.027244 | 2.926 |
| w21 | 4 | -0.167208 | -39.552 |
| w22 | 10 | 0.050294 | 72.394 |
| w23 | 5 | -0.182166 | -20.491 |
| w24 | 11 | 0.00364 | 69.237 |
| w25 | 6 | 0.112048 | 63.953 |
| w26 | 8 | -0.109279 | -22.407 |
| w27 | 11 | 0.064673 | 20.427 |
| w28 | 3 | 0.040015 | 0.307 |
| w29 | 8 | -0.007125 | 19.1 |
| w30 | 2 | -0.019882 | -8.054 |
| w31 | 3 | 0.014164 | -10.593 |
| w32 | 6 | -0.061566 | -51.091 |

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
| w28 | 3 | 0.11454 | -4.632 |
| w29 | 6 | -0.050442 | -20.511 |
| w30 | 6 | -0.14217 | 0.51 |
| w31 | 14 | 0.143961 | 13.493 |
| w32 | 10 | 0.000999 | -19.354 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 3 | 0.087978 | 15.751 |
| w15 | 7 | -0.001277 | 58.396 |
| w16 | 8 | 0.050227 | 202.071 |
| w17 | 9 | 0.048311 | 1.3 |
| w18 | 3 | -0.100877 | -6.968 |
| w19 | 5 | 0.000955 | -27.018 |
| w20 | 5 | -0.126963 | -18.047 |
| w21 | 4 | 0.083095 | 41.871 |
| w22 | 9 | -0.224035 | -20.332 |
| w23 | 4 | -0.170617 | 4.243 |
| w24 | 10 | -0.038927 | 44.694 |
| w25 | 12 | 0.137213 | 129.921 |
| w26 | 5 | -0.035858 | -1.994 |
| w27 | 7 | 0.210899 | 170.482 |
| w28 | 3 | -0.097375 | -11.341 |
| w29 | 4 | 0.083749 | 23.831 |
| w30 | 5 | 0.045122 | -20.761 |
| w31 | 6 | -0.046555 | -0.092 |
| w32 | 7 | 0.112665 | 1.863 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 8 | 0.295077 | 205.126 |
| w26 | 6 | 0.049863 | 18.868 |
| w27 | 10 | 0.118924 | 59.8 |
| w28 | 4 | -0.00326 | 8.651 |
| w29 | 5 | 0.038995 | -3.487 |
| w30 | 3 | 0.050872 | -11.411 |
| w31 | 5 | 0.102235 | 6.089 |
| w32 | 13 | -0.000239 | -35.038 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

