# Backtest of 020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b1_resistance-breakout-all-coins.b1_resistance-breakout-in-uptrend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | -0.047932 | 9.534 |
| w2 | 12 | 0.1345 | 35.711 |
| w3 | 30 | -0.00325 | 64.398 |
| w4 | 22 | 0.042255 | -8.658 |
| w5 | 16 | -0.0844 | 13.155 |
| w6 | 19 | 0.048571 | 33.564 |
| w7 | 10 | -0.066246 | -9.72 |
| w8 | 9 | 0.176891 | 8.551 |
| w9 | 5 | 0.012177 | -7.644 |
| w10 | 18 | 0.037956 | 17.49 |
| w11 | 16 | 0.075897 | 53.393 |
| w12 | 3 | 0.095667 | 1.332 |
| w13 | 14 | 0.007934 | 25.49 |
| w14 | 22 | 0.042255 | 12.985 |
| w15 | 28 | 0.098353 | 94.059 |
| w16 | 15 | -0.046437 | 13.796 |
| w17 | 17 | 0.104829 | 7.834 |
| w18 | 14 | -0.058064 | 12.752 |
| w19 | 13 | 0.07935 | -9.325 |
| w20 | 9 | 0.01066 | -3.994 |
| w21 | 12 | 0.046278 | -28.594 |
| w22 | 24 | 0.268525 | 111.417 |
| w23 | 14 | -0.006493 | 1.403 |
| w24 | 29 | -0.098952 | 63.57 |
| w25 | 22 | 0.042681 | 34.013 |
| w26 | 20 | -0.077936 | -25.865 |
| w27 | 25 | 0.084278 | 48.761 |
| w28 | 18 | -0.069347 | -10.668 |
| w29 | 30 | 0.115683 | 10.119 |
| w30 | 10 | 0.049161 | -8.918 |
| w31 | 22 | 0.052174 | -20.084 |
| w32 | 24 | 0.010608 | 16.382 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.007975 | 21.081 |
| w2 | 12 | 0.098959 | -17.122 |
| w3 | 29 | -0.102321 | -17.04 |
| w4 | 24 | -0.063534 | 78.196 |
| w5 | 19 | -0.061175 | 35.018 |
| w6 | 17 | 0.039451 | 134.86 |
| w7 | 8 | -0.107429 | -13.296 |
| w8 | 4 | 0.100475 | -4.067 |
| w9 | 5 | -0.014844 | -12.197 |
| w10 | 20 | 0.040192 | 36.004 |
| w11 | 16 | 0.167505 | 26.018 |
| w12 | 4 | -0.036117 | -9.15 |
| w13 | 22 | -0.06513 | 6.609 |
| w14 | 21 | 0.035753 | 14.548 |
| w15 | 12 | -0.019887 | 42.206 |
| w16 | 28 | 0.007144 | 33.891 |
| w17 | 13 | 0.000162 | -14.078 |
| w18 | 24 | 0.071081 | -15.551 |
| w19 | 11 | -0.105347 | -18.798 |
| w20 | 10 | 0.028798 | 7.199 |
| w21 | 14 | 0.103749 | 27.494 |
| w22 | 20 | -0.183651 | -8.612 |
| w23 | 16 | -0.160055 | -31.647 |
| w24 | 29 | 0.021734 | -5.491 |
| w25 | 16 | -0.095673 | 7.264 |
| w26 | 5 | -0.037114 | -2.552 |
| w27 | 24 | -0.121289 | 36.173 |
| w28 | 12 | -0.05791 | -11.816 |
| w29 | 19 | 0.022508 | 32.631 |
| w30 | 15 | -0.285724 | -31.97 |
| w31 | 11 | -0.010022 | -6.076 |
| w32 | 19 | -0.037864 | -8.034 |

- XRPUSD: 26 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 5 | 0.074863 | 7.545 |
| w8 | 4 | -0.036324 | -5.328 |
| w9 | 13 | 0.088051 | -2.99 |
| w10 | 8 | -0.295153 | -21.451 |
| w11 | 9 | 0.15162 | -8.495 |
| w12 | 16 | -0.082946 | -17.863 |
| w13 | 11 | 0.051415 | 4.516 |
| w14 | 15 | -0.102274 | 29.386 |
| w15 | 12 | 0.009993 | 224.478 |
| w16 | 17 | 0.126535 | 62.024 |
| w17 | 9 | 0.012279 | 18.994 |
| w18 | 14 | 0.10228 | -11.045 |
| w19 | 11 | -0.074076 | -18.18 |
| w20 | 0 | -0.034407 | 0.0 |
| w21 | 12 | -0.044818 | -0.87 |
| w22 | 18 | -0.215661 | -14.877 |
| w23 | 13 | -0.131994 | -9.968 |
| w24 | 12 | 0.204881 | 15.383 |
| w25 | 20 | -0.10045 | -0.118 |
| w26 | 13 | 0.297464 | -4.264 |
| w27 | 14 | 0.228798 | 167.872 |
| w28 | 8 | 0.003501 | -4.342 |
| w29 | 20 | -0.005021 | 12.971 |
| w30 | 6 | -0.132633 | -11.824 |
| w31 | 11 | -0.021418 | -29.76 |
| w32 | 15 | 0.075238 | 1.74 |

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 106 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 6 | 0.032762 | -11.019 |
| w9 | 3 | -0.02136 | -16.358 |
| w10 | 19 | 0.038236 | 19.82 |
| w11 | 15 | -0.003783 | 0.312 |
| w12 | 8 | -0.074253 | -3.764 |
| w13 | 14 | -0.096336 | 42.229 |
| w14 | 19 | -0.045928 | 21.166 |
| w15 | 24 | 0.01143 | -4.979 |
| w16 | 24 | 0.179347 | 79.095 |
| w17 | 15 | -0.026268 | -13.198 |
| w18 | 13 | 0.058313 | 5.016 |
| w19 | 12 | 0.040638 | -1.251 |
| w20 | 8 | -0.116422 | -8.067 |
| w21 | 8 | -0.139149 | -19.558 |
| w22 | 29 | -0.100651 | -24.678 |
| w23 | 4 | 0.094913 | 50.92 |
| w24 | 20 | -0.158184 | 8.518 |
| w25 | 26 | -0.039116 | 50.4 |
| w26 | 15 | 0.16572 | -11.286 |
| w27 | 22 | -0.004918 | 6.971 |
| w28 | 12 | -0.07725 | -16.905 |
| w29 | 27 | -0.123425 | 14.12 |
| w30 | 29 | -0.153971 | -3.196 |
| w31 | 6 | -0.011995 | -3.986 |
| w32 | 7 | -0.070049 | -21.88 |

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
| w1 | 17 | -0.038902 | 169.096 |
| w2 | 21 | 0.182999 | 47.307 |
| w3 | 8 | 0.033831 | -2.778 |
| w4 | 31 | 0.004871 | 205.17 |
| w5 | 21 | 0.260081 | 76.794 |
| w6 | 17 | 0.186232 | 61.124 |
| w7 | 10 | 0.144988 | -3.633 |
| w8 | 8 | -0.018382 | -16.163 |
| w9 | 5 | 0.050969 | -4.79 |
| w10 | 19 | -0.155924 | -2.329 |
| w11 | 13 | -0.007955 | 26.721 |
| w12 | 17 | -0.029946 | -16.424 |
| w13 | 13 | -0.05645 | 28.491 |
| w14 | 20 | 0.11147 | 78.029 |
| w15 | 18 | -0.058557 | 13.489 |
| w16 | 23 | 0.154004 | 94.607 |
| w17 | 13 | -0.035922 | 2.896 |
| w18 | 17 | -0.027306 | 12.281 |
| w19 | 11 | 0.032724 | -8.91 |
| w20 | 10 | -0.014914 | 11.245 |
| w21 | 10 | 0.037596 | -30.525 |
| w22 | 28 | -0.06208 | 5.923 |
| w23 | 12 | -0.219359 | -23.212 |
| w24 | 21 | 0.040839 | -0.021 |
| w25 | 12 | 0.015697 | 9.896 |
| w26 | 14 | -0.018943 | -6.872 |
| w27 | 13 | -0.051356 | 30.244 |
| w28 | 2 | -0.047881 | -1.411 |
| w29 | 21 | -0.011326 | 12.76 |
| w30 | 8 | -0.109746 | -13.739 |
| w31 | 20 | -0.014838 | -34.905 |
| w32 | 17 | 0.009331 | 26.525 |

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 20 | 0.002565 | -5.373 |
| w12 | 9 | -0.03933 | -15.956 |
| w13 | 12 | 0.058537 | 50.754 |
| w14 | 19 | -0.105185 | 20.294 |
| w15 | 17 | 0.01017 | 7.732 |
| w16 | 28 | -0.032869 | 40.616 |
| w17 | 15 | -0.037749 | 37.765 |
| w18 | 3 | -0.058388 | -15.935 |
| w19 | 9 | -0.000332 | -24.493 |
| w20 | 9 | 0.016442 | -5.789 |
| w21 | 0 | None | 0.0 |
| w22 | 24 | 0.108884 | 18.78 |
| w23 | 5 | -0.191929 | -0.39 |
| w24 | 21 | -0.111176 | 83.175 |
| w25 | 14 | 0.084868 | -9.412 |
| w26 | 8 | -0.108524 | -11.613 |
| w27 | 26 | 0.046181 | 51.27 |
| w28 | 8 | -0.144394 | -15.567 |
| w29 | 20 | 0.094944 | 15.354 |
| w30 | 8 | 0.07815 | -0.15 |
| w31 | 2 | -0.103491 | -8.015 |
| w32 | 21 | 0.156742 | 8.468 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=112. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 17 | -0.050981 | -23.839 |
| w14 | 23 | 0.133083 | 61.691 |
| w15 | 17 | -0.038991 | -7.562 |
| w16 | 26 | 0.002602 | 61.949 |
| w17 | 17 | -0.03252 | 10.653 |
| w18 | 15 | 0.01765 | 17.878 |
| w19 | 7 | -0.132926 | -14.401 |
| w20 | 16 | 0.062137 | 6.88 |
| w21 | 13 | 0.144527 | -26.458 |
| w22 | 15 | -0.083652 | 11.597 |
| w23 | 4 | -0.059485 | -8.325 |
| w24 | 19 | -0.111648 | -2.863 |
| w25 | 11 | 0.049831 | 38.341 |
| w26 | 5 | 0.043641 | 0.785 |
| w27 | 22 | 0.170992 | 41.731 |
| w28 | 4 | -0.049364 | -12.608 |
| w29 | 25 | -0.011971 | -23.324 |
| w30 | 4 | -0.081101 | -11.568 |
| w31 | 14 | -0.066517 | -6.654 |
| w32 | 11 | 0.036497 | -12.492 |

- w12 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 17 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 22 | -0.021617 | 73.616 |
| w17 | 13 | 0.012504 | 9.408 |
| w18 | 14 | -0.081621 | 18.072 |
| w19 | 5 | -0.101751 | -21.049 |
| w20 | 5 | -0.036489 | 1.571 |
| w21 | 11 | 0.091803 | -20.279 |
| w22 | 17 | -0.069642 | -8.793 |
| w23 | 5 | -0.172691 | -13.893 |
| w24 | 25 | -0.001955 | 20.93 |
| w25 | 15 | 0.215614 | 10.397 |
| w26 | 9 | 0.000805 | -13.637 |
| w27 | 19 | 0.244328 | 75.397 |
| w28 | 8 | 0.081725 | -4.968 |
| w29 | 16 | 0.122587 | 27.336 |
| w30 | 2 | -0.158217 | -17.901 |
| w31 | 18 | 0.109501 | -7.645 |
| w32 | 14 | -0.043477 | -31.248 |

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w15 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 18 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 14 | 0.028325 | -6.001 |
| w16 | 20 | 0.018223 | 79.837 |
| w17 | 7 | -0.043357 | 11.795 |
| w18 | 20 | 0.058552 | 5.534 |
| w19 | 18 | -0.125202 | -6.208 |
| w20 | 19 | -0.214911 | -16.619 |
| w21 | 13 | -0.087598 | -32.266 |
| w22 | 25 | -0.114222 | 9.504 |
| w23 | 22 | -0.029882 | -8.083 |
| w24 | 24 | -0.021294 | 40.473 |
| w25 | 14 | 0.112968 | 10.039 |
| w26 | 17 | 0.061796 | 4.058 |
| w27 | 19 | 0.323202 | 144.582 |
| w28 | 16 | -0.087675 | -7.497 |
| w29 | 29 | -0.019761 | 37.559 |
| w30 | 16 | -0.099558 | -22.606 |
| w31 | 30 | -0.06971 | 29.476 |
| w32 | 26 | 0.002854 | -4.56 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | -0.112223 | -7.771 |
| w18 | 13 | -0.047861 | 16.379 |
| w19 | 11 | -0.070599 | -15.398 |
| w20 | 12 | -0.035656 | -11.582 |
| w21 | 7 | -0.143959 | -20.845 |
| w22 | 16 | -0.18051 | 7.896 |
| w23 | 10 | -0.098739 | -16.161 |
| w24 | 13 | 0.011388 | 29.459 |
| w25 | 16 | 0.087723 | -3.161 |
| w26 | 13 | -0.018157 | -13.944 |
| w27 | 13 | 0.283089 | 78.056 |
| w28 | 1 | -0.037928 | -2.348 |
| w29 | 23 | 0.013979 | -23.264 |
| w30 | 16 | 0.03426 | -27.335 |
| w31 | 6 | 0.029504 | -12.549 |
| w32 | 12 | -0.061047 | -16.407 |

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
| w20 | 12 | 0.101519 | 13.508 |
| w21 | 5 | -0.041901 | -16.935 |
| w22 | 20 | -0.072776 | 7.76 |
| w23 | 7 | -0.017124 | -9.264 |
| w24 | 21 | 0.170108 | 183.225 |
| w25 | 13 | 0.041553 | 26.135 |
| w26 | 7 | 0.001617 | -8.752 |
| w27 | 24 | 0.094131 | 40.031 |
| w28 | 3 | 0.050533 | 8.705 |
| w29 | 25 | 0.034215 | 10.621 |
| w30 | 8 | 0.080974 | -0.518 |
| w31 | 10 | -0.0474 | -18.569 |
| w32 | 15 | 0.142395 | 14.636 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 14 | -0.20307 | -9.071 |
| w23 | 4 | -0.018772 | -7.566 |
| w24 | 13 | 0.103748 | 202.764 |
| w25 | 7 | -0.083705 | 61.029 |
| w26 | 12 | -0.102208 | -12.823 |
| w27 | 22 | 0.01506 | 7.079 |
| w28 | 2 | -0.082437 | -6.15 |
| w29 | 15 | 0.102636 | -1.577 |
| w30 | 17 | -0.107467 | -39.171 |
| w31 | 12 | -0.060665 | -10.054 |
| w32 | 13 | -0.109814 | 45.743 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 15 | -0.084761 | 24.011 |
| w25 | 20 | -0.07799 | -3.894 |
| w26 | 12 | -0.100038 | -11.953 |
| w27 | 20 | 0.043229 | 46.958 |
| w28 | 13 | 0.13937 | -2.797 |
| w29 | 17 | 0.071395 | -7.493 |
| w30 | 6 | -0.077116 | -20.398 |
| w31 | 10 | -0.078684 | -14.616 |
| w32 | 13 | 0.183079 | 6.766 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 13 | 0.122413 | 52.879 |
| w6 | 25 | -0.159309 | -6.35 |
| w7 | 11 | -0.00531 | -5.61 |
| w8 | 7 | 0.120318 | -11.74 |
| w9 | 5 | -0.085441 | -5.503 |
| w10 | 18 | 0.005078 | 33.311 |
| w11 | 17 | -0.147012 | 13.395 |
| w12 | 4 | -0.029339 | -6.212 |
| w13 | 19 | 0.202322 | 36.417 |
| w14 | 21 | -0.121655 | 1.283 |
| w15 | 17 | 0.009574 | -0.169 |
| w16 | 27 | 0.037972 | 75.034 |
| w17 | 11 | -0.017968 | -1.561 |
| w18 | 11 | 0.179201 | 18.521 |
| w19 | 6 | -0.067027 | 21.621 |
| w20 | 7 | 0.01969 | -2.004 |
| w21 | 3 | -0.007167 | -4.11 |
| w22 | 17 | -0.123975 | -4.36 |
| w23 | 5 | 0.02137 | -1.046 |
| w24 | 23 | 0.133418 | 0.4 |
| w25 | 11 | 0.036523 | 5.511 |
| w26 | 15 | 0.070021 | 30.444 |
| w27 | 18 | 0.144319 | 89.535 |
| w28 | 10 | -0.06136 | -25.182 |
| w29 | 13 | 0.107502 | 25.203 |
| w30 | 22 | 0.07721 | 182.394 |
| w31 | 8 | 0.138584 | 13.735 |
| w32 | 15 | -0.05928 | 34.858 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 17 | 0.070562 | 141.057 |
| w6 | 13 | 0.012614 | 88.329 |
| w7 | 10 | -0.036712 | -11.662 |
| w8 | 6 | 0.104006 | -4.322 |
| w9 | 8 | -0.048684 | -13.372 |
| w10 | 21 | -0.063462 | 14.778 |
| w11 | 18 | 0.053914 | 15.186 |
| w12 | 3 | 0.042003 | -6.111 |
| w13 | 11 | 0.071 | 25.972 |
| w14 | 25 | -0.178784 | 28.98 |
| w15 | 29 | -0.237017 | -6.414 |
| w16 | 27 | -0.143607 | 39.93 |
| w17 | 15 | -0.066514 | -23.549 |
| w18 | 10 | -0.135652 | -26.441 |
| w19 | 21 | -0.010665 | -15.746 |
| w20 | 9 | -0.056452 | -9.943 |
| w21 | 21 | -0.005015 | -17.985 |
| w22 | 21 | -0.020439 | 7.721 |
| w23 | 9 | 0.029543 | 2.614 |
| w24 | 28 | 0.138758 | 18.736 |
| w25 | 7 | -0.063001 | -38.183 |
| w26 | 20 | -0.022718 | 0.921 |
| w27 | 22 | -0.006782 | 2.736 |
| w28 | 25 | -0.078556 | 8.557 |
| w29 | 11 | -0.041897 | -7.965 |
| w30 | 39 | -0.052422 | 13.364 |
| w31 | 22 | 0.103546 | 38.29 |
| w32 | 25 | -0.052042 | 41.975 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | -0.130838 | -18.227 |
| w18 | 25 | 0.065257 | 39.815 |
| w19 | 14 | 0.145686 | -5.815 |
| w20 | 9 | -0.056382 | -18.881 |
| w21 | 2 | -0.043489 | -30.125 |
| w22 | 17 | -0.062344 | 3.102 |
| w23 | 4 | -0.222595 | -23.169 |
| w24 | 17 | -0.080857 | -10.364 |
| w25 | 12 | -0.005792 | 25.103 |
| w26 | 17 | -0.020025 | -20.986 |
| w27 | 14 | 0.026309 | 160.512 |
| w28 | 14 | -0.06302 | -8.327 |
| w29 | 14 | 0.212208 | 17.507 |
| w30 | 1 | -0.168191 | -6.503 |
| w31 | 6 | -0.052099 | -15.065 |
| w32 | 13 | 0.199513 | 56.884 |

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
| w17 | 18 | -0.222083 | -13.119 |
| w18 | 13 | -0.147475 | -29.881 |
| w19 | 11 | -0.010966 | 9.281 |
| w20 | 10 | -0.048226 | 1.692 |
| w21 | 9 | 0.082197 | -22.423 |
| w22 | 22 | -0.153923 | -2.895 |
| w23 | 9 | 0.003552 | -4.067 |
| w24 | 32 | 0.116247 | 22.314 |
| w25 | 16 | 0.094947 | 25.348 |
| w26 | 21 | -0.030745 | 13.346 |
| w27 | 21 | -0.007358 | 72.388 |
| w28 | 3 | -0.036436 | -3.503 |
| w29 | 24 | 0.019857 | 10.528 |
| w30 | 6 | -0.013329 | -18.018 |
| w31 | 3 | -0.001672 | -14.693 |
| w32 | 15 | -0.03113 | -0.283 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 15 | -0.10885 | -19.661 |
| w20 | 9 | 0.03258 | 3.895 |
| w21 | 12 | -0.031018 | 14.821 |
| w22 | 25 | -0.005694 | 110.214 |
| w23 | 12 | 0.123074 | -3.555 |
| w24 | 24 | -0.121944 | 46.945 |
| w25 | 13 | -0.117459 | -24.738 |
| w26 | 10 | -0.023458 | -25.897 |
| w27 | 28 | 0.134889 | 12.689 |
| w28 | 2 | 0.0278 | -5.698 |
| w29 | 27 | -0.01851 | -10.901 |
| w30 | 5 | -0.039307 | -8.442 |
| w31 | 11 | -0.055253 | -9.569 |
| w32 | 19 | -0.032831 | 28.636 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 19 | 0.030315 | 29.1 |
| w23 | 10 | -0.054392 | -21.123 |
| w24 | 23 | -0.087391 | -4.376 |
| w25 | 21 | 0.055951 | -24.199 |
| w26 | 6 | 0.054858 | 2.071 |
| w27 | 21 | -0.066921 | -19.527 |
| w28 | 6 | 0.012722 | -5.619 |
| w29 | 17 | 0.083492 | 36.575 |
| w30 | 6 | -0.062431 | -15.062 |
| w31 | 9 | 0.004363 | -18.818 |
| w32 | 15 | 0.051313 | -5.303 |

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
| w27 | 19 | -0.002777 | 31.442 |
| w28 | 7 | -0.063979 | -5.569 |
| w29 | 22 | 0.021512 | 7.573 |
| w30 | 9 | 0.029666 | -22.676 |
| w31 | 9 | 0.008748 | -10.8 |
| w32 | 11 | -0.014375 | 20.439 |

- FILUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 5 | 0.269892 | -4.9 |
| w19 | 10 | 0.041235 | -10.274 |
| w20 | 8 | 0.199425 | 14.603 |
| w21 | 5 | 0.086129 | -14.756 |
| w22 | 21 | -0.01945 | 5.376 |
| w23 | 4 | -0.122361 | -11.137 |
| w24 | 20 | -0.007055 | 11.543 |
| w25 | 16 | 0.016439 | 18.452 |
| w26 | 5 | -0.085201 | -19.736 |
| w27 | 18 | 0.118455 | 28.95 |
| w28 | 1 | -0.146407 | -5.863 |
| w29 | 19 | 0.024886 | -15.819 |
| w30 | 10 | -0.121613 | -38.243 |
| w31 | 11 | -0.107833 | -18.378 |
| w32 | 13 | -0.012613 | -5.016 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 14 | -0.031525 | -18.052 |
| w19 | 9 | -0.088902 | -12.397 |
| w20 | 12 | 0.065801 | -5.837 |
| w21 | 4 | 0.147569 | 0.836 |
| w22 | 15 | 0.05063 | 118.099 |
| w23 | 6 | -0.183692 | -15.656 |
| w24 | 20 | -0.125963 | 53.603 |
| w25 | 17 | 0.081003 | 37.889 |
| w26 | 6 | -0.048271 | -9.632 |
| w27 | 17 | 0.034757 | 34.309 |
| w28 | 1 | -0.120805 | -4.566 |
| w29 | 13 | 0.044893 | -5.684 |
| w30 | 5 | -0.056631 | -16.843 |
| w31 | 7 | -0.188194 | -19.739 |
| w32 | 16 | -0.090412 | -22.269 |

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
| w28 | 11 | 0.115202 | 12.177 |
| w29 | 17 | -0.03277 | -9.053 |
| w30 | 16 | 0.030129 | -17.869 |
| w31 | 9 | 0.293205 | 18.365 |
| w32 | 11 | -0.017754 | -6.279 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 15 | 0.193764 | 29.365 |
| w15 | 11 | 0.174394 | 119.492 |
| w16 | 15 | 0.032391 | 214.523 |
| w17 | 9 | 0.055221 | 25.062 |
| w18 | 7 | -0.075411 | -7.078 |
| w19 | 11 | -0.200363 | -15.457 |
| w20 | 9 | -0.017454 | -12.995 |
| w21 | 8 | 0.008691 | 100.612 |
| w22 | 18 | -0.101456 | -11.475 |
| w23 | 7 | -0.058169 | 9.529 |
| w24 | 15 | 0.181944 | 36.495 |
| w25 | 12 | 0.191109 | 89.345 |
| w26 | 9 | 0.061877 | -7.655 |
| w27 | 24 | -0.028723 | 86.222 |
| w28 | 4 | -0.067119 | -8.089 |
| w29 | 25 | 0.098695 | 27.861 |
| w30 | 8 | -0.019346 | -21.539 |
| w31 | 9 | 0.012501 | -7.488 |
| w32 | 14 | 0.178016 | 2.131 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 11 | 0.159064 | 72.576 |
| w26 | 8 | 0.174209 | 15.692 |
| w27 | 19 | 0.012739 | 43.611 |
| w28 | 7 | 0.033765 | -9.917 |
| w29 | 14 | 0.016007 | -1.314 |
| w30 | 4 | -0.032372 | -27.456 |
| w31 | 10 | 0.007535 | -8.198 |
| w32 | 23 | 0.131257 | -5.139 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

