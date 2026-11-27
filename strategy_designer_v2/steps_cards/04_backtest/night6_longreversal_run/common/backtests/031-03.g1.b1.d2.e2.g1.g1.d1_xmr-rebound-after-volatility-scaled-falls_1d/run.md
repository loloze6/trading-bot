# Backtest of 031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d

- Plan: `../../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g1.d1_xmr-rebound-after-volatility-scaled-falls_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.16818 | 13.393 |
| w2 | 45 | -0.057643 | -8.949 |
| w3 | 40 | -0.015493 | 8.735 |
| w4 | 29 | -0.090797 | -20.285 |
| w5 | 44 | 0.0677 | 34.823 |
| w6 | 39 | -0.07919 | -1.001 |
| w7 | 53 | -0.001247 | -3.983 |
| w8 | 44 | 0.086141 | 5.463 |
| w9 | 50 | 0.090326 | -17.609 |
| w10 | 37 | 0.102483 | 13.028 |
| w11 | 47 | -0.063894 | 2.001 |
| w12 | 51 | 0.030232 | -7.32 |
| w13 | 47 | 0.188747 | 29.579 |
| w14 | 39 | 0.073721 | 14.303 |
| w15 | 40 | -0.037633 | 9.924 |
| w16 | 45 | 0.037462 | 17.049 |
| w17 | 54 | 0.256002 | 37.338 |
| w18 | 47 | -0.05771 | -11.63 |
| w19 | 51 | 0.006182 | -8.464 |
| w20 | 53 | 0.053434 | -15.047 |
| w21 | 49 | -0.005528 | -14.333 |
| w22 | 47 | -0.033109 | 8.82 |
| w23 | 52 | 0.052991 | -4.418 |
| w24 | 45 | 0.150853 | 38.676 |
| w25 | 45 | 0.104893 | 25.991 |
| w26 | 50 | 0.027209 | -2.73 |
| w27 | 46 | -0.070693 | 2.721 |
| w28 | 48 | 0.101556 | 8.434 |
| w29 | 49 | 0.013256 | 0.925 |
| w30 | 56 | -0.085687 | -29.807 |
| w31 | 53 | -0.046218 | -26.702 |
| w32 | 48 | -0.144759 | -20.284 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | 0.32593 | 0.0 |
| w2 | 42 | -0.103625 | -25.423 |
| w3 | 52 | 0.062439 | 15.441 |
| w4 | 52 | 0.003926 | 11.764 |
| w5 | 41 | -0.001209 | 10.564 |
| w6 | 39 | 0.145347 | 38.452 |
| w7 | 55 | 0.034114 | 5.787 |
| w8 | 50 | 0.145633 | 1.524 |
| w9 | 54 | 0.184557 | 8.702 |
| w10 | 49 | 0.049583 | 14.095 |
| w11 | 53 | 0.00698 | -3.468 |
| w12 | 51 | -0.020206 | -17.835 |
| w13 | 44 | 0.102597 | 13.119 |
| w14 | 51 | 0.193429 | 30.206 |
| w15 | 41 | 0.076775 | 28.201 |
| w16 | 47 | -0.063804 | -1.229 |
| w17 | 46 | 0.213668 | 31.668 |
| w18 | 49 | -0.097379 | -20.907 |
| w19 | 56 | 0.046006 | -8.324 |
| w20 | 55 | 0.109756 | 4.763 |
| w21 | 51 | 0.022518 | 2.859 |
| w22 | 49 | 0.022668 | 1.115 |
| w23 | 43 | -0.048513 | -11.359 |
| w24 | 50 | 0.069237 | 7.387 |
| w25 | 42 | 0.085614 | 14.464 |
| w26 | 46 | 0.073356 | -8.137 |
| w27 | 50 | -0.008209 | 4.36 |
| w28 | 48 | -0.10303 | -15.392 |
| w29 | 43 | 0.121302 | 16.882 |
| w30 | 53 | 0.008066 | -8.344 |
| w31 | 51 | 0.094588 | -2.162 |
| w32 | 55 | -0.095837 | -30.617 |

- XRPUSD: 25 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 49 | 0.056591 | -13.617 |
| w9 | 56 | 0.040537 | 4.977 |
| w10 | 47 | 0.215662 | 16.555 |
| w11 | 55 | 0.051574 | 4.859 |
| w12 | 61 | -0.006942 | -15.475 |
| w13 | 48 | 0.042347 | -4.95 |
| w14 | 43 | 0.136087 | 20.518 |
| w15 | 48 | -0.002716 | 7.585 |
| w16 | 41 | 3.3e-05 | 14.76 |
| w17 | 40 | 0.216951 | 20.776 |
| w18 | 45 | 0.083652 | 3.492 |
| w19 | 50 | 0.042743 | -8.741 |
| w20 | 5 | 0.085521 | -3.641 |
| w21 | 0 | 0.204775 | 0.0 |
| w22 | 41 | 0.276655 | 53.238 |
| w23 | 50 | 0.018566 | 37.004 |
| w24 | 38 | 0.137224 | 17.911 |
| w25 | 50 | 0.095056 | 16.865 |
| w26 | 46 | -0.043532 | -11.121 |
| w27 | 45 | -0.087793 | 8.512 |
| w28 | 46 | 0.049885 | 4.169 |
| w29 | 49 | 0.14449 | 19.984 |
| w30 | 57 | -0.060769 | -25.86 |
| w31 | 60 | -0.05104 | -23.075 |
| w32 | 56 | -0.149044 | -30.67 |

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 106 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 228 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- BCHUSD: 22 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 43 | 0.070064 | 0.417 |
| w12 | 53 | -0.124765 | -36.512 |
| w13 | 45 | 0.113392 | 29.331 |
| w14 | 41 | 0.224132 | 19.515 |
| w15 | 44 | 0.021046 | -7.946 |
| w16 | 46 | 0.046189 | 18.741 |
| w17 | 47 | 0.293558 | 41.25 |
| w18 | 49 | 0.028031 | -10.388 |
| w19 | 58 | -0.014013 | -26.586 |
| w20 | 55 | 0.071662 | -12.487 |
| w21 | 47 | 0.182793 | 7.87 |
| w22 | 43 | 0.028615 | -1.874 |
| w23 | 52 | 0.122004 | 48.658 |
| w24 | 50 | 0.142238 | 13.962 |
| w25 | 48 | 0.063469 | 14.519 |
| w26 | 53 | -0.013727 | -13.783 |
| w27 | 47 | 0.010447 | 4.175 |
| w28 | 49 | -0.033631 | -15.473 |
| w29 | 51 | 0.05332 | 7.076 |
| w30 | 53 | 0.063806 | 0.191 |
| w31 | 47 | 0.224648 | 13.402 |
| w32 | 56 | -0.098515 | -46.203 |

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

- w10 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_BCHUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ETHUSD: 31 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w2 | 47 | 0.003826 | -0.432 |
| w3 | 48 | 0.118928 | 5.064 |
| w4 | 41 | -0.087338 | 9.092 |
| w5 | 44 | -0.021707 | 8.74 |
| w6 | 42 | 0.173014 | 29.416 |
| w7 | 51 | -0.080506 | -10.082 |
| w8 | 51 | 0.10412 | -3.108 |
| w9 | 53 | 0.092674 | -4.59 |
| w10 | 49 | 0.143752 | 12.891 |
| w11 | 51 | -0.016775 | -1.742 |
| w12 | 51 | -0.019957 | -15.704 |
| w13 | 50 | 0.060091 | 9.151 |
| w14 | 43 | 0.136178 | 20.805 |
| w15 | 42 | 0.062622 | 14.681 |
| w16 | 37 | 0.077549 | 28.082 |
| w17 | 43 | 0.119874 | 26.115 |
| w18 | 48 | 0.100167 | 12.263 |
| w19 | 50 | -0.078652 | -20.741 |
| w20 | 52 | 0.0188 | -18.8 |
| w21 | 43 | 0.117005 | 6.144 |
| w22 | 47 | 0.085227 | 21.622 |
| w23 | 56 | 0.113874 | 5.426 |
| w24 | 49 | 0.155168 | 36.436 |
| w25 | 45 | -0.018992 | -2.366 |
| w26 | 51 | 0.043934 | -7.045 |
| w27 | 51 | -0.061543 | -2.647 |
| w28 | 56 | 0.119516 | 3.022 |
| w29 | 39 | -0.012594 | 10.032 |
| w30 | 54 | -0.045607 | -17.374 |
| w31 | 52 | -0.103121 | -30.812 |
| w32 | 45 | -0.099607 | -16.192 |

- w1 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 142 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ADAUSD: 21 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 51 | -0.042836 | -17.066 |
| w13 | 44 | 0.071483 | 8.344 |
| w14 | 40 | 0.227721 | 35.971 |
| w15 | 51 | 0.106232 | 19.545 |
| w16 | 44 | 0.077677 | 27.498 |
| w17 | 41 | 0.242161 | 51.842 |
| w18 | 52 | 0.095299 | -7.175 |
| w19 | 55 | -0.031691 | -18.144 |
| w20 | 54 | 0.109647 | 2.615 |
| w21 | 51 | 0.05446 | -10.375 |
| w22 | 51 | 0.152875 | 35.678 |
| w23 | 56 | 0.08543 | -1.864 |
| w24 | 42 | 0.028833 | 21.398 |
| w25 | 57 | 0.127261 | 7.15 |
| w26 | 54 | 0.048522 | -6.057 |
| w27 | 42 | -0.129524 | -8.669 |
| w28 | 48 | -0.011444 | -5.215 |
| w29 | 45 | 0.048019 | 4.621 |
| w30 | 58 | -0.014079 | -30.238 |
| w31 | 54 | 0.083533 | -0.811 |
| w32 | 54 | -0.256446 | -47.935 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w11 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 215 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 17 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 54 | 0.051488 | 20.631 |
| w17 | 43 | 0.161262 | 31.606 |
| w18 | 50 | 0.113117 | 17.462 |
| w19 | 54 | 0.188441 | 4.368 |
| w20 | 56 | -0.004622 | -14.066 |
| w21 | 48 | 0.054748 | -2.836 |
| w22 | 51 | 0.188699 | 26.18 |
| w23 | 54 | -0.006665 | -31.827 |
| w24 | 52 | 0.068565 | 12.158 |
| w25 | 51 | 0.002126 | -11.184 |
| w26 | 55 | -0.005812 | -27.439 |
| w27 | 52 | -0.078944 | -11.981 |
| w28 | 51 | -0.063723 | -14.974 |
| w29 | 53 | -0.08508 | -16.499 |
| w30 | 55 | -0.01301 | -30.217 |
| w31 | 53 | 0.013059 | -8.949 |
| w32 | 61 | 0.010315 | -15.559 |

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

- w15 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ATOMUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ALGOUSD: 15 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 49 | 0.172081 | 44.704 |
| w19 | 45 | -0.001152 | -25.903 |
| w20 | 54 | 0.084468 | -3.328 |
| w21 | 49 | 0.009909 | -10.688 |
| w22 | 46 | -0.006568 | -7.395 |
| w23 | 55 | -0.044201 | -28.387 |
| w24 | 44 | 0.04024 | 22.083 |
| w25 | 50 | 0.024593 | -7.291 |
| w26 | 52 | -0.045546 | -20.098 |
| w27 | 53 | -0.04673 | -3.247 |
| w28 | 48 | -0.001775 | -9.536 |
| w29 | 49 | 0.031486 | 0.48 |
| w30 | 53 | -0.012718 | -24.722 |
| w31 | 54 | -0.06825 | -17.862 |
| w32 | 52 | -0.173939 | -30.785 |

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

- w17 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_ALGOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TRXUSD: 17 of 18 windows run. w1 to w14 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 53 | -0.06901 | 11.035 |
| w17 | 41 | 0.305308 | 26.879 |
| w18 | 45 | 0.131186 | 15.565 |
| w19 | 51 | 0.042732 | -4.516 |
| w20 | 48 | 0.298273 | 49.086 |
| w21 | 48 | 0.093866 | -3.83 |
| w22 | 44 | 0.101457 | 15.743 |
| w23 | 45 | -0.025884 | -2.973 |
| w24 | 40 | 0.05799 | 14.645 |
| w25 | 44 | -0.04607 | -16.971 |
| w26 | 49 | -0.095183 | -9.509 |
| w27 | 47 | -0.087999 | -9.999 |
| w28 | 42 | 0.046821 | 3.176 |
| w29 | 36 | -0.003205 | 4.194 |
| w30 | 52 | 0.077582 | -10.071 |
| w31 | 50 | 0.039235 | 3.48 |
| w32 | 39 | -0.227582 | -24.937 |

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 180 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOTUSD: 13 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 56 | 0.086555 | -6.974 |
| w21 | 53 | 0.142602 | -2.593 |
| w22 | 47 | 0.113823 | 18.765 |
| w23 | 52 | 0.042238 | -17.584 |
| w24 | 48 | 0.00133 | 1.299 |
| w25 | 49 | 0.078205 | -1.688 |
| w26 | 50 | -0.176108 | -34.243 |
| w27 | 53 | -0.094189 | -13.625 |
| w28 | 51 | -0.084912 | -19.13 |
| w29 | 50 | -0.01436 | -10.94 |
| w30 | 56 | -0.08053 | -31.512 |
| w31 | 52 | 0.009222 | -9.544 |
| w32 | 59 | -0.077911 | -28.734 |

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

- w19 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AVAXUSD: 11 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 48 | -0.036084 | 0.988 |
| w23 | 59 | 0.077418 | -10.731 |
| w24 | 41 | -0.122101 | -2.516 |
| w25 | 52 | 0.123311 | 13.211 |
| w26 | 51 | -0.090214 | -20.97 |
| w27 | 56 | -0.050738 | 1.364 |
| w28 | 50 | -0.034516 | -14.889 |
| w29 | 46 | -0.061848 | -9.764 |
| w30 | 54 | -0.062234 | -20.697 |
| w31 | 53 | 0.04935 | -4.774 |
| w32 | 53 | 0.022011 | -15.711 |

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 131 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w21 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 254 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- NEARUSD: 10 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 53 | -0.058721 | -21.03 |
| w24 | 42 | 0.079896 | 33.956 |
| w25 | 54 | 0.088716 | 25.849 |
| w26 | 46 | -0.098487 | -17.133 |
| w27 | 50 | -0.079521 | -7.584 |
| w28 | 50 | -0.001433 | -16.704 |
| w29 | 51 | -0.029549 | -6.751 |
| w30 | 52 | -0.107804 | -21.853 |
| w31 | 57 | -0.038807 | -11.804 |
| w32 | 53 | -0.008345 | 11.957 |

- w22 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 199 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- SUIUSD: 7 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 55 | -0.059263 | -15.807 |
| w27 | 46 | 0.092739 | 30.561 |
| w28 | 53 | 0.026348 | 1.743 |
| w29 | 50 | 0.081192 | 11.175 |
| w30 | 59 | 0.032442 | -16.311 |
| w31 | 50 | -0.035639 | -14.473 |
| w32 | 51 | -0.043062 | -5.189 |

- w24 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 121 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w25 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 243 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ZECUSD: 27 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 45 | 0.150958 | 34.516 |
| w7 | 57 | 0.092904 | 9.573 |
| w8 | 53 | 0.161872 | 10.258 |
| w9 | 55 | 0.114972 | -8.039 |
| w10 | 52 | 0.221154 | 18.874 |
| w11 | 56 | 0.04747 | -0.775 |
| w12 | 50 | -0.019125 | -19.17 |
| w13 | 49 | -0.000338 | 6.979 |
| w14 | 48 | 0.059256 | 13.756 |
| w15 | 46 | 0.087774 | 6.708 |
| w16 | 42 | -0.011223 | 14.557 |
| w17 | 44 | 0.265562 | 41.52 |
| w18 | 50 | 0.012875 | 3.927 |
| w19 | 52 | -0.006962 | -4.653 |
| w20 | 54 | 0.136136 | 5.804 |
| w21 | 44 | 0.108205 | 1.822 |
| w22 | 51 | 0.077957 | 6.594 |
| w23 | 45 | -0.003535 | -11.289 |
| w24 | 45 | 0.158319 | 24.553 |
| w25 | 55 | 0.028014 | -10.664 |
| w26 | 46 | -0.100072 | -6.823 |
| w27 | 55 | -0.078454 | -3.55 |
| w28 | 48 | -0.07967 | -16.869 |
| w29 | 53 | 0.021098 | 3.546 |
| w30 | 44 | -0.047152 | 26.134 |
| w31 | 51 | -0.036038 | -7.086 |
| w32 | 48 | 0.025747 | 14.043 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 184 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- XMRUSD: 26 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 51 | 0.142923 | 22.889 |
| w8 | 57 | 0.196571 | 13.624 |
| w9 | 55 | 0.148018 | 1.78 |
| w10 | 47 | 0.202261 | 23.769 |
| w11 | 49 | -0.034966 | -8.379 |
| w12 | 58 | 0.046762 | -10.372 |
| w13 | 55 | 0.120237 | 14.371 |
| w14 | 40 | 0.307542 | 41.783 |
| w15 | 45 | 0.164023 | 36.133 |
| w16 | 40 | 0.023959 | 21.186 |
| w17 | 46 | 0.260478 | 44.904 |
| w18 | 43 | 0.02451 | -5.822 |
| w19 | 53 | -0.009149 | -12.48 |
| w20 | 48 | 0.089518 | 3.796 |
| w21 | 40 | 0.137112 | 4.557 |
| w22 | 47 | 0.154908 | 17.657 |
| w23 | 50 | 0.051878 | -11.991 |
| w24 | 51 | 0.174362 | 16.919 |
| w25 | 52 | 0.216445 | 22.529 |
| w26 | 36 | 0.252907 | 27.671 |
| w27 | 44 | 0.046613 | 2.582 |
| w28 | 40 | 0.108027 | 17.334 |
| w29 | 56 | -0.095333 | -21.976 |
| w30 | 43 | -0.084968 | -5.695 |
| w31 | 41 | 0.077664 | 7.968 |
| w32 | 40 | 0.109552 | 27.963 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 119 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 242 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- CRVUSD: 13 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 51 | -0.000106 | -10.811 |
| w21 | 54 | 0.158687 | 0.985 |
| w22 | 45 | 0.095054 | 19.066 |
| w23 | 54 | 0.206357 | 9.812 |
| w24 | 52 | 0.124264 | 22.393 |
| w25 | 51 | 0.122415 | 7.039 |
| w26 | 56 | 0.10521 | 2.022 |
| w27 | 49 | 0.033256 | 27.832 |
| w28 | 49 | 0.018025 | 0.222 |
| w29 | 53 | -0.036225 | -6.392 |
| w30 | 59 | -0.058907 | -24.86 |
| w31 | 53 | 0.07824 | -7.529 |
| w32 | 49 | -0.025262 | -5.005 |

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

- w19 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_CRVUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- AAVEUSD: 14 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 58 | -0.033394 | -17.473 |
| w20 | 60 | 0.042913 | -0.891 |
| w21 | 39 | 0.090857 | -0.966 |
| w22 | 47 | 0.076307 | 16.154 |
| w23 | 52 | -0.020531 | -12.625 |
| w24 | 53 | -0.028524 | 4.681 |
| w25 | 51 | 0.074972 | 6.199 |
| w26 | 52 | -0.10226 | -10.561 |
| w27 | 52 | 0.017845 | 19.604 |
| w28 | 49 | 0.107769 | 5.205 |
| w29 | 49 | 0.029388 | 11.78 |
| w30 | 50 | 0.005935 | -18.439 |
| w31 | 48 | 0.045815 | -5.435 |
| w32 | 58 | -0.078093 | -7.092 |

- w17 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 137 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w18 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 260 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 13 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 54 | 0.108101 | 3.605 |
| w21 | 50 | 0.170409 | 16.872 |
| w22 | 44 | -0.022211 | 26.772 |
| w23 | 53 | 0.067377 | -0.865 |
| w24 | 46 | 0.046056 | 32.655 |
| w25 | 49 | 0.098871 | -3.237 |
| w26 | 51 | -0.000519 | -9.565 |
| w27 | 53 | -0.008507 | -4.392 |
| w28 | 52 | -0.014278 | -17.111 |
| w29 | 51 | -0.106205 | -14.37 |
| w30 | 58 | 0.027306 | -20.405 |
| w31 | 52 | 0.056023 | -3.039 |
| w32 | 62 | -0.003877 | 0.948 |

- w19 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 144 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- LDOUSD: 8 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 53 | -0.086962 | -25.594 |
| w26 | 58 | 0.018238 | -9.62 |
| w27 | 49 | -0.096111 | -9.519 |
| w28 | 55 | 0.03107 | -8.008 |
| w29 | 54 | -0.1324 | -16.132 |
| w30 | 55 | 0.120403 | 1.476 |
| w31 | 54 | 0.025024 | -9.643 |
| w32 | 50 | -0.089511 | -14.727 |

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

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_LDOUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- ONDOUSD: 5 of 6 windows run. w1 to w26 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 56 | 0.113091 | 6.161 |
| w29 | 47 | 0.009353 | -1.636 |
| w30 | 62 | -0.002848 | -26.279 |
| w31 | 51 | 0.043096 | -5.26 |
| w32 | 55 | 0.009523 | 4.727 |

- w27 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 143 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- FILUSD: 13 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 56 | 0.010058 | -15.562 |
| w21 | 46 | 0.037153 | -12.908 |
| w22 | 50 | 0.111755 | 28.224 |
| w23 | 53 | -0.010958 | -18.831 |
| w24 | 42 | 0.001339 | 6.973 |
| w25 | 51 | -0.033065 | -15.174 |
| w26 | 48 | 0.115285 | -1.736 |
| w27 | 47 | -0.065442 | -6.949 |
| w28 | 51 | -0.032084 | -15.721 |
| w29 | 55 | 0.00489 | -10.481 |
| w30 | 56 | -0.131102 | -29.319 |
| w31 | 49 | 0.071463 | -4.637 |
| w32 | 55 | 0.083306 | 2.709 |

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

- w19 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- GRTUSD: 12 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 45 | 0.019755 | -13.859 |
| w22 | 48 | 0.038566 | 21.839 |
| w23 | 49 | -0.068247 | -18.302 |
| w24 | 48 | 0.07102 | 23.748 |
| w25 | 60 | 0.030054 | 4.951 |
| w26 | 57 | 0.005019 | -13.5 |
| w27 | 50 | -0.126559 | -16.761 |
| w28 | 51 | -0.032562 | -19.729 |
| w29 | 50 | -0.018517 | -9.327 |
| w30 | 57 | -0.00049 | -28.306 |
| w31 | 49 | 0.061473 | -7.243 |
| w32 | 65 | -0.001039 | -22.798 |

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

- w20 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 4 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w29 | 53 | 0.117221 | 10.092 |
| w30 | 57 | -0.057952 | -13.495 |
| w31 | 52 | -0.021976 | -4.149 |
| w32 | 54 | 0.04055 | 6.003 |

- w28 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 184 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 17 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 44 | 0.289083 | 139.029 |
| w17 | 26 | 0.225384 | 10.245 |
| w18 | 50 | 0.138978 | 12.015 |
| w19 | 54 | 0.043917 | 2.306 |
| w20 | 53 | 0.092865 | -3.255 |
| w21 | 51 | 0.019641 | 6.581 |
| w22 | 52 | 0.038689 | 6.814 |
| w23 | 49 | 0.061735 | 0.863 |
| w24 | 44 | 0.074182 | 19.616 |
| w25 | 46 | -0.036787 | -1.215 |
| w26 | 53 | -0.033492 | -10.181 |
| w27 | 43 | -0.136997 | -3.009 |
| w28 | 51 | -0.006737 | -11.328 |
| w29 | 45 | -0.018298 | -2.215 |
| w30 | 55 | 0.03719 | -8.591 |
| w31 | 53 | -0.006328 | -4.931 |
| w32 | 53 | -0.107638 | -29.445 |

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 134 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 257 warm-up bars -- required_bars=262. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- PEPEUSD: 5 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 49 | 0.025321 | -11.716 |
| w29 | 51 | -0.095238 | -12.319 |
| w30 | 54 | 0.043975 | -16.233 |
| w31 | 52 | 0.032499 | -0.939 |
| w32 | 74 | -0.129526 | -30.911 |

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

- w27 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

