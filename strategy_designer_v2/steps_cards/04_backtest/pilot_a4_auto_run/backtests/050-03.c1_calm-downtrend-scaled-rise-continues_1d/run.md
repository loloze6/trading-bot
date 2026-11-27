# Backtest of 050-03.c1_calm-downtrend-scaled-rise-continues_1d

- Plan: `../../../../03_test_plan/pilot_a4_auto_run/plans/050-03.c1_calm-downtrend-scaled-rise-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, DOT, XMR, INJ, GRT, TAO, DOGE, FIL as BTCUSD, DOTUSD, XMRUSD, INJUSD, GRTUSD, TAOUSD, DOGEUSD, FILUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.118317 | 4.777 |
| w2 | 0 | None | 0.0 |
| w3 | 5 | 0.01824 | 0.434 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 7 | 0.050209 | 7.584 |
| w8 | 8 | 0.067878 | 13.563 |
| w9 | 7 | -0.015677 | -1.243 |
| w10 | 0 | -0.103907 | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 9 | -0.062113 | 0.29 |
| w13 | 7 | 0.20443 | 17.482 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.115526 | -5.657 |
| w19 | 4 | 0.056934 | -1.616 |
| w20 | 13 | 0.107895 | 4.162 |
| w21 | 8 | 0.075806 | -2.181 |
| w22 | 2 | -0.026277 | 4.271 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.0327 | 2.559 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.034457 | -0.013 |
| w31 | 4 | 0.060015 | 7.118 |
| w32 | 9 | -0.075889 | 2.605 |

- DOTUSD: 11 of 32 windows run. 15 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 11 | 0.101872 | 27.65 |
| w23 | 12 | 0.023069 | 4.278 |
| w24 | 6 | -0.002372 | 8.405 |
| w25 | 4 | 0.063789 | 9.6 |
| w26 | 0 | 0.016607 | 0.0 |
| w27 | 7 | -0.100755 | -5.355 |
| w28 | 5 | 0.05668 | 0.578 |
| w29 | 13 | 0.082896 | 14.057 |
| w30 | 0 | None | 0.0 |
| w31 | 7 | 0.003781 | -8.074 |
| w32 | 11 | -0.165681 | -17.718 |

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

- w20 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_DOTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- XMRUSD: 25 of 32 windows run. 4 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 10 | 0.015383 | -6.757 |
| w9 | 8 | 0.147457 | -10.983 |
| w10 | 3 | -0.147172 | -2.316 |
| w11 | 0 | -0.011217 | 0.0 |
| w12 | 16 | 0.019942 | -0.918 |
| w13 | 8 | 0.159656 | 25.984 |
| w14 | 2 | -0.075063 | -0.573 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.046913 | 10.562 |
| w18 | 6 | 0.033373 | 5.993 |
| w19 | 3 | -0.046254 | -18.896 |
| w20 | 9 | 0.064063 | 8.329 |
| w21 | 5 | 0.01322 | -0.416 |
| w22 | 9 | 0.13444 | 2.291 |
| w23 | 1 | None | -0.032 |
| w24 | 6 | 0.056565 | -0.569 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | 0.015292 | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | 0.00568 | 12.3 |
| w29 | 3 | -0.08269 | -0.823 |
| w30 | 2 | -0.008963 | 9.737 |
| w31 | 5 | -0.052891 | -3.08 |
| w32 | 7 | 0.016113 | 6.81 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 119 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 242 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w7 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 364 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- INJUSD: 11 of 32 windows run. 18 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.004143 | 57.162 |
| w23 | 4 | 0.067432 | 18.847 |
| w24 | 7 | -0.11818 | 2.744 |
| w25 | 2 | -0.063022 | 5.749 |
| w26 | 8 | -0.045106 | -9.344 |
| w27 | 5 | 0.077389 | 5.927 |
| w28 | 6 | 0.09481 | 8.245 |
| w29 | 3 | -0.077907 | 12.221 |
| w30 | 3 | -0.384045 | -10.576 |
| w31 | 17 | 0.009402 | -7.761 |
| w32 | 1 | -0.081962 | -1.617 |

- w19 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 144 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w20 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 264 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w21 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 387 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- GRTUSD: 10 of 32 windows run. 16 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 6 | 0.132796 | -6.152 |
| w24 | 8 | -0.12469 | -4.423 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.016971 | -10.792 |
| w27 | 5 | 0.076334 | 15.851 |
| w28 | 3 | 0.118508 | 5.586 |
| w29 | 9 | 0.041973 | 25.944 |
| w30 | 6 | -0.081223 | -17.541 |
| w31 | 15 | -0.010896 | -14.331 |
| w32 | 2 | 0.422981 | 6.731 |

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

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w22 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_GRTUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- TAOUSD: 3 of 32 windows run. 27 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19, w20, w21, w22, w23, w24, w25, w26, w27 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w30 | 11 | -0.145535 | 11.547 |
| w31 | 14 | 0.165149 | 30.986 |
| w32 | 7 | 0.016879 | 14.203 |

- w28 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 184 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w29 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 304 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- DOGEUSD: 16 of 32 windows run. 13 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.041218 | 10.694 |
| w18 | 15 | -0.021724 | 0.822 |
| w19 | 10 | 0.010161 | -9.719 |
| w20 | 9 | 0.042096 | 5.067 |
| w21 | 4 | 0.054905 | 0.146 |
| w22 | 14 | 0.053313 | -1.04 |
| w23 | 3 | -0.038987 | -1.179 |
| w24 | 2 | -0.09154 | -3.899 |
| w25 | 7 | 0.014391 | 38.015 |
| w26 | 1 | -0.112238 | -1.909 |
| w27 | 9 | -0.013059 | 11.282 |
| w28 | 2 | -0.053522 | -3.213 |
| w29 | 8 | 0.022509 | 34.059 |
| w30 | 0 | None | 0.0 |
| w31 | 15 | 0.02858 | -4.92 |
| w32 | 5 | 0.196976 | 28.29 |

- w14 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 134 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w15 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 257 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- w16 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 379 warm-up bars -- required_bars=395. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- FILUSD: 11 of 32 windows run. 16 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.00485 | 8.316 |
| w23 | 10 | 0.060432 | -5.913 |
| w24 | 11 | -0.143774 | -5.26 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | -0.100898 | -7.288 |
| w27 | 11 | -0.0039 | 5.669 |
| w28 | 2 | 0.092614 | 2.748 |
| w29 | 8 | 0.037731 | 17.546 |
| w30 | 9 | -0.158683 | -32.943 |
| w31 | 8 | 0.046175 | -12.302 |
| w32 | 8 | -0.023126 | 1.894 |

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

- w20 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

- w21 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_FILUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

