# Backtest of 002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/002-01_sma-golden-cross-upward-drift.b1_momentum-inside-golden-cross-uptrends-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 62 | -0.05978 | -5.663 |
| w2 | 57 | 0.065382 | 41.24 |
| w3 | 57 | -0.047411 | 65.346 |
| w4 | 56 | -0.125264 | -30.043 |
| w5 | 48 | 0.060378 | 101.056 |
| w6 | 48 | 0.088258 | 114.64 |
| w7 | 32 | 0.019904 | 6.253 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | -0.175197 | -3.998 |
| w11 | 59 | 0.040643 | 40.106 |
| w12 | 21 | -0.021151 | -1.04 |
| w13 | 18 | -0.027937 | 3.908 |
| w14 | 42 | 0.032268 | 23.757 |
| w15 | 49 | 0.138533 | 155.709 |
| w16 | 50 | -0.056855 | 6.965 |
| w17 | 25 | 0.042413 | 10.885 |
| w18 | 49 | 0.027793 | 2.622 |
| w19 | 10 | 0.004951 | 0.976 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 45 | -0.18806 | -18.624 |
| w23 | 51 | -0.046832 | -12.639 |
| w24 | 28 | -0.030296 | 11.632 |
| w25 | 50 | 0.077307 | 43.63 |
| w26 | 65 | -0.087106 | -24.494 |
| w27 | 23 | 0.059562 | 41.695 |
| w28 | 59 | -0.071792 | -18.558 |
| w29 | 59 | -0.059658 | -8.668 |
| w30 | 58 | -0.078683 | -21.883 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.01245 | 0.0 |
| w2 | 55 | 0.072174 | 30.436 |
| w3 | 1 | 0.017031 | 0.377 |
| w4 | 50 | 0.141451 | 76.721 |
| w5 | 57 | 0.041891 | 30.009 |
| w6 | 41 | 0.064173 | 79.193 |
| w7 | 33 | -0.026974 | -3.894 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 19 | -0.0678 | -1.073 |
| w11 | 68 | 0.048144 | 6.907 |
| w12 | 0 | None | 0.0 |
| w13 | 16 | -0.020302 | -6.477 |
| w14 | 7 | -0.20963 | -10.335 |
| w15 | 51 | 0.012749 | 15.116 |
| w16 | 59 | -0.091033 | -1.298 |
| w17 | 33 | -0.079989 | -19.656 |
| w18 | 26 | -0.040249 | -10.596 |
| w19 | 4 | 0.059135 | 0.524 |
| w20 | 0 | None | 0.0 |
| w21 | 14 | -0.004955 | 0.63 |
| w22 | 71 | -0.079765 | -13.614 |
| w23 | 42 | -0.015115 | -9.006 |
| w24 | 0 | None | 0.0 |
| w25 | 36 | -0.01964 | 13.204 |
| w26 | 33 | 0.021117 | 9.975 |
| w27 | 13 | 0.070273 | 32.036 |
| w28 | 50 | -0.065427 | -12.75 |
| w29 | 17 | -0.084766 | -6.621 |
| w30 | 37 | -0.21311 | -38.875 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 26 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 17 | 0.014068 | 9.939 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 43 | -0.03574 | -6.544 |
| w12 | 0 | None | 0.0 |
| w13 | 12 | 0.095785 | 14.459 |
| w14 | 8 | -0.031975 | -1.795 |
| w15 | 49 | 0.185552 | 143.307 |
| w16 | 40 | -0.098725 | 13.98 |
| w17 | 31 | -0.03346 | -0.059 |
| w18 | 62 | -0.095469 | -16.365 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 17 | -0.06616 | 1.528 |
| w22 | 13 | 0.008071 | 2.409 |
| w23 | 46 | -0.077865 | -44.321 |
| w24 | 32 | -0.193463 | -23.215 |
| w25 | 45 | -0.003772 | 2.726 |
| w26 | 9 | -0.091498 | -3.91 |
| w27 | 48 | 0.258866 | 204.511 |
| w28 | 53 | -0.138752 | -23.294 |
| w29 | 27 | -0.173202 | -24.671 |
| w30 | 35 | -0.094235 | -7.893 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 106 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- BCHUSD: 23 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | -0.061447 | -0.841 |
| w11 | 63 | -0.046449 | -13.783 |
| w12 | 7 | -0.108375 | -4.551 |
| w13 | 26 | -0.024055 | -3.837 |
| w14 | 6 | -0.009453 | -0.839 |
| w15 | 41 | -0.09745 | -27.056 |
| w16 | 53 | 0.002187 | 37.688 |
| w17 | 27 | -0.066833 | -10.345 |
| w18 | 7 | 0.09736 | 15.59 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 54 | -0.17022 | -28.454 |
| w23 | 30 | 0.032389 | -5.216 |
| w24 | 72 | -0.187751 | -36.793 |
| w25 | 66 | 0.022664 | 42.811 |
| w26 | 37 | -0.023828 | 2.221 |
| w27 | 18 | 0.004578 | 2.453 |
| w28 | 21 | 0.038819 | 8.679 |
| w29 | 49 | -0.107117 | -8.693 |
| w30 | 76 | -0.211366 | -49.84 |
| w31 | 39 | -0.127122 | -20.826 |
| w32 | 0 | None | 0.0 |

- w7 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w8 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w9 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ETHUSD: 31 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 69 | -0.102498 | -17.743 |
| w3 | 33 | -0.015518 | 2.132 |
| w4 | 22 | 0.176032 | 199.029 |
| w5 | 40 | 0.1383 | 98.662 |
| w6 | 50 | 0.057651 | 60.204 |
| w7 | 40 | 0.092834 | 33.606 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 6 | -0.072764 | -5.474 |
| w11 | 55 | 0.054453 | 14.802 |
| w12 | 3 | -0.080301 | -2.243 |
| w13 | 25 | -0.013011 | -4.768 |
| w14 | 47 | 0.075061 | 56.701 |
| w15 | 66 | 0.011339 | 25.012 |
| w16 | 48 | 0.015644 | 64.216 |
| w17 | 50 | -0.04542 | -4.654 |
| w18 | 75 | -0.072657 | -16.364 |
| w19 | 11 | 0.12893 | 30.252 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 40 | -0.155065 | -14.148 |
| w23 | 66 | -0.162277 | -32.117 |
| w24 | 20 | -0.037781 | 1.568 |
| w25 | 55 | 0.060918 | 29.782 |
| w26 | 40 | -0.044906 | -15.582 |
| w27 | 14 | -0.020147 | -0.838 |
| w28 | 31 | -0.02769 | 8.615 |
| w29 | 25 | -0.024433 | 27.767 |
| w30 | 46 | -0.018682 | 8.765 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | None | -0.071 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 142 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 59 | -0.058781 | -12.384 |
| w12 | 0 | None | 0.0 |
| w13 | 19 | 0.007138 | -1.487 |
| w14 | 43 | -0.028642 | 18.769 |
| w15 | 65 | 0.03828 | 11.322 |
| w16 | 36 | 0.129718 | 101.479 |
| w17 | 60 | 0.034655 | 36.184 |
| w18 | 39 | 0.019772 | 18.45 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 33 | -0.042172 | -3.435 |
| w23 | 23 | 0.110003 | 28.667 |
| w24 | 15 | 0.067547 | 34.603 |
| w25 | 59 | 0.037645 | 5.097 |
| w26 | 5 | -0.034376 | -0.832 |
| w27 | 8 | 0.130153 | 40.869 |
| w28 | 42 | -0.108275 | -22.185 |
| w29 | 10 | -0.104511 | -7.181 |
| w30 | 40 | -0.023232 | 10.487 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 18 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 76 | -0.073166 | -21.451 |
| w16 | 48 | -0.010385 | 33.283 |
| w17 | 34 | -0.11871 | -30.163 |
| w18 | 63 | -0.023678 | -12.835 |
| w19 | 27 | -0.053222 | -11.101 |
| w20 | 0 | None | 0.0 |
| w21 | 32 | -0.096128 | -16.911 |
| w22 | 38 | -0.09285 | -14.332 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.041646 | 0.275 |
| w25 | 64 | 0.043201 | 13.763 |
| w26 | 5 | 0.012222 | -0.148 |
| w27 | 14 | -0.05836 | -7.097 |
| w28 | 16 | -0.067787 | -5.598 |
| w29 | 10 | -0.041887 | -3.751 |
| w30 | 22 | -0.12544 | -11.736 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w12 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w13 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w14 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 16 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 40 | -0.157488 | -28.329 |
| w18 | 56 | -0.105171 | -29.286 |
| w19 | 14 | 0.115698 | 9.077 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.104934 | 38.723 |
| w25 | 61 | 0.070359 | 17.157 |
| w26 | 13 | -0.143937 | -5.634 |
| w27 | 10 | 0.082863 | 28.048 |
| w28 | 24 | 0.006944 | 5.491 |
| w29 | 12 | -0.088651 | -3.292 |
| w30 | 30 | -0.170201 | -9.882 |
| w31 | 0 | None | 0.0 |
| w32 | 13 | 0.042703 | 6.548 |

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

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 17 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 59 | -0.034417 | 45.966 |
| w17 | 27 | -0.127083 | -6.617 |
| w18 | 66 | -0.074365 | -19.754 |
| w19 | 6 | 0.144829 | 7.714 |
| w20 | 37 | -0.061686 | -8.466 |
| w21 | 0 | None | 0.0 |
| w22 | 52 | -0.2194 | -32.084 |
| w23 | 67 | -0.051008 | -7.894 |
| w24 | 66 | -0.123623 | 13.514 |
| w25 | 53 | 0.065085 | 29.044 |
| w26 | 56 | -0.036028 | -6.223 |
| w27 | 55 | 0.054815 | 214.946 |
| w28 | 71 | -0.15297 | -25.424 |
| w29 | 67 | -0.044887 | 24.047 |
| w30 | 43 | -0.024771 | 0.313 |
| w31 | 16 | -0.003376 | 1.464 |
| w32 | 64 | 0.064021 | 12.968 |

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 180 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOTUSD: 14 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | -0.171211 | -3.532 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 45 | -0.111471 | -15.512 |
| w23 | 12 | -0.005921 | 2.134 |
| w24 | 12 | 0.08879 | 29.876 |
| w25 | 54 | 0.062395 | 14.908 |
| w26 | 11 | -0.150427 | -4.63 |
| w27 | 11 | -0.071766 | -7.895 |
| w28 | 19 | -0.054893 | -3.128 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | 0.010673 | 5.159 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w18 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AVAXUSD: 12 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 40 | -0.048703 | -6.964 |
| w23 | 19 | 0.007597 | 6.902 |
| w24 | 14 | 0.012238 | 32.017 |
| w25 | 53 | 0.061849 | 15.907 |
| w26 | 12 | -0.097161 | -4.977 |
| w27 | 10 | 0.103182 | 32.912 |
| w28 | 22 | 0.002804 | 6.36 |
| w29 | 9 | -0.024587 | -2.354 |
| w30 | 31 | 0.082597 | 27.01 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 131 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- NEARUSD: 10 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 18 | 0.143414 | 44.66 |
| w25 | 53 | 0.070525 | 31.701 |
| w26 | 50 | 0.017895 | 3.076 |
| w27 | 17 | 0.006224 | -1.789 |
| w28 | 19 | 0.100422 | 12.337 |
| w29 | 7 | -0.012887 | -0.789 |
| w30 | 45 | -0.013571 | -5.085 |
| w31 | 0 | None | 0.0 |
| w32 | 54 | -0.075808 | -19.267 |

- w22 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 199 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- SUIUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 55 | 0.067429 | 22.548 |
| w26 | 13 | -0.009153 | 0.444 |
| w27 | 44 | -0.143759 | 7.533 |
| w28 | 40 | -0.008777 | -3.724 |
| w29 | 29 | -0.106922 | -11.339 |
| w30 | 33 | -0.094193 | -11.963 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w24 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 121 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 27 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 63 | -0.088701 | -12.512 |
| w7 | 40 | 0.074768 | 24.697 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 50 | 0.088364 | 21.14 |
| w12 | 0 | None | 0.0 |
| w13 | 20 | 0.055975 | 3.961 |
| w14 | 57 | -0.052593 | 6.341 |
| w15 | 73 | -0.050307 | -19.109 |
| w16 | 50 | -0.171722 | -11.371 |
| w17 | 34 | -0.113816 | -20.276 |
| w18 | 30 | -0.025853 | -5.79 |
| w19 | 17 | 0.160553 | 14.946 |
| w20 | 7 | 0.028 | 2.562 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 23 | 0.000543 | -3.696 |
| w25 | 25 | 0.051024 | 13.555 |
| w26 | 15 | -0.032458 | -0.673 |
| w27 | 61 | -0.058041 | -1.085 |
| w28 | 19 | -0.053561 | -3.431 |
| w29 | 40 | -0.069831 | -14.247 |
| w30 | 43 | 0.144669 | 200.411 |
| w31 | 33 | -0.0456 | -6.701 |
| w32 | 53 | 0.05251 | 35.377 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 184 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XMRUSD: 27 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 23 | 0.096669 | 98.232 |
| w7 | 45 | -0.01319 | -0.374 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 72 | -0.045154 | -15.194 |
| w12 | 13 | -0.041704 | -3.7 |
| w13 | 21 | -0.019429 | -4.446 |
| w14 | 57 | 0.000321 | 21.206 |
| w15 | 72 | -0.059016 | -1.719 |
| w16 | 64 | -0.028261 | 17.854 |
| w17 | 37 | -0.106212 | -18.144 |
| w18 | 18 | -0.057582 | -6.568 |
| w19 | 5 | -0.088534 | -2.584 |
| w20 | 29 | -0.05766 | -12.726 |
| w21 | 0 | None | 0.0 |
| w22 | 74 | -0.053027 | -16.266 |
| w23 | 41 | -0.039141 | -5.932 |
| w24 | 38 | -0.123826 | -18.17 |
| w25 | 24 | -0.132118 | -42.329 |
| w26 | 42 | -0.12304 | -22.468 |
| w27 | 60 | -0.056931 | -24.242 |
| w28 | 82 | 0.012991 | -0.436 |
| w29 | 53 | 0.090386 | 34.782 |
| w30 | 55 | -0.116176 | -3.695 |
| w31 | 30 | 0.013615 | -4.839 |
| w32 | 5 | 0.124478 | 40.59 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 119 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- CRVUSD: 14 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 24 | -0.068182 | -5.536 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 37 | -0.116439 | -14.411 |
| w23 | 27 | -0.063706 | -4.813 |
| w24 | 8 | -0.065365 | -3.656 |
| w25 | 56 | 0.015492 | -0.584 |
| w26 | 2 | -0.048239 | -1.335 |
| w27 | 8 | 0.05942 | 32.847 |
| w28 | 25 | 0.004992 | -0.805 |
| w29 | 33 | -0.003973 | -4.081 |
| w30 | 27 | -0.106147 | -7.752 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | -0.082948 | -7.424 |

- w16 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w18 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 13 | -0.105649 | -8.791 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 48 | -0.108808 | -18.359 |
| w23 | 9 | 0.029097 | 5.454 |
| w24 | 28 | -0.081475 | 0.448 |
| w25 | 63 | 0.042764 | 15.949 |
| w26 | 11 | -0.106534 | -9.85 |
| w27 | 70 | -0.095668 | -3.384 |
| w28 | 33 | -0.055885 | -3.806 |
| w29 | 43 | -0.106897 | -19.654 |
| w30 | 35 | -0.111503 | -7.566 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.035861 | -2.055 |

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 137 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 13 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 20 | -0.127477 | -19.934 |
| w22 | 39 | -0.11109 | 8.901 |
| w23 | 48 | -0.02565 | -3.771 |
| w24 | 46 | 0.026101 | 80.743 |
| w25 | 64 | -0.040011 | -9.486 |
| w26 | 6 | -0.043863 | -2.107 |
| w27 | 18 | 0.014675 | -0.533 |
| w28 | 15 | -0.130807 | -7.252 |
| w29 | 22 | -0.16038 | -11.194 |
| w30 | 28 | -0.050626 | 2.224 |
| w31 | 0 | None | 0.0 |
| w32 | 54 | -0.131547 | -28.768 |

- w19 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 144 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LDOUSD: 9 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 21 | -0.094764 | -6.803 |
| w25 | 70 | -0.01098 | -12.796 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.107397 | -5.559 |
| w28 | 39 | -0.063882 | -5.601 |
| w29 | 7 | -0.034187 | -3.449 |
| w30 | 43 | -0.115307 | -7.956 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.066137 | -4.307 |

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w22 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w23 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ONDOUSD: 5 of 6 windows run. w1 to w26 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 40 | -0.020938 | -1.832 |
| w29 | 10 | -0.031757 | -1.753 |
| w30 | 35 | -0.08288 | -7.237 |
| w31 | 0 | None | 0.0 |
| w32 | 47 | -0.077474 | -18.569 |

- w27 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 143 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- FILUSD: 14 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 41 | -0.199851 | -16.936 |
| w23 | 12 | 0.032346 | 8.079 |
| w24 | 24 | -0.03436 | 0.823 |
| w25 | 58 | 0.081719 | 21.433 |
| w26 | 9 | -0.133413 | -4.894 |
| w27 | 12 | -0.060864 | -10.277 |
| w28 | 21 | -0.035516 | 0.06 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w18 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- GRTUSD: 13 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 33 | -0.036452 | -2.435 |
| w23 | 21 | -0.020921 | -3.999 |
| w24 | 18 | -0.021587 | 3.122 |
| w25 | 61 | 0.158657 | 72.707 |
| w26 | 35 | 0.043219 | 10.221 |
| w27 | 12 | -0.080566 | -10.545 |
| w28 | 18 | -0.028443 | 3.918 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w18 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w19 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 4 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w29 | 40 | -0.054545 | -11.996 |
| w30 | 34 | -0.023931 | -6.067 |
| w31 | 2 | 0.039413 | 0.387 |
| w32 | 27 | -0.054042 | -10.526 |

- w28 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 184 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 33 | 0.002948 | -5.349 |
| w16 | 15 | -0.060392 | 145.135 |
| w17 | 37 | 0.076906 | 13.31 |
| w18 | 16 | -0.03127 | 0.744 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 23 | -0.033186 | -5.047 |
| w22 | 39 | -0.047989 | -8.154 |
| w23 | 0 | None | 0.0 |
| w24 | 25 | 0.019105 | 8.033 |
| w25 | 56 | 0.110423 | 67.157 |
| w26 | 41 | -0.022636 | 0.057 |
| w27 | 10 | 0.21263 | 83.47 |
| w28 | 29 | 0.017734 | 14.906 |
| w29 | 13 | -0.094427 | -5.216 |
| w30 | 52 | -0.088654 | -11.382 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 134 warm-up bars -- required_bars=200. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- PEPEUSD: 6 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w27 | 16 | -0.098925 | -7.324 |
| w28 | 25 | 0.065331 | 18.816 |
| w29 | 39 | -0.066306 | -13.351 |
| w30 | 21 | -0.216221 | -19.266 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w25 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w26 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

