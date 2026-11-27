# Backtest of 020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d

- Plan: `../../../../../03_test_plan/night3_levels_run/plans/020-03_resistance-breakout-continues-up.b2_breakout-after-a-run.b1_resistance-breakout-all-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | 0.000174 | 5.713 |
| w2 | 9 | 0.150772 | 40.115 |
| w3 | 26 | 0.030921 | 67.928 |
| w4 | 25 | 0.113842 | 3.134 |
| w5 | 15 | -0.059277 | 16.559 |
| w6 | 23 | 0.054398 | 44.486 |
| w7 | 6 | -0.008899 | -2.339 |
| w8 | 12 | 0.210467 | 4.357 |
| w9 | 14 | 0.03557 | -17.913 |
| w10 | 16 | 0.047308 | 27.539 |
| w11 | 19 | 0.091924 | 57.792 |
| w12 | 7 | 0.065697 | -0.224 |
| w13 | 18 | 0.001483 | 32.107 |
| w14 | 19 | 0.024317 | 11.132 |
| w15 | 30 | 0.08044 | 94.846 |
| w16 | 19 | -0.042529 | 8.354 |
| w17 | 15 | 0.050539 | -5.158 |
| w18 | 20 | 0.010421 | 11.845 |
| w19 | 11 | 0.011112 | -14.647 |
| w20 | 10 | 0.037537 | -9.127 |
| w21 | 16 | 0.003857 | -46.054 |
| w22 | 21 | 0.131911 | 59.573 |
| w23 | 17 | -0.019471 | -14.662 |
| w24 | 26 | -0.067873 | 72.737 |
| w25 | 20 | 0.130861 | 46.685 |
| w26 | 18 | -0.066614 | -29.405 |
| w27 | 25 | 0.110908 | 29.895 |
| w28 | 21 | -0.066484 | -9.845 |
| w29 | 36 | 0.173283 | 5.918 |
| w30 | 13 | 0.030693 | -11.761 |
| w31 | 22 | 0.06844 | -6.076 |
| w32 | 20 | 0.036517 | 30.274 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 17 | 0.037691 | 21.914 |
| w2 | 14 | 0.161694 | -10.907 |
| w3 | 26 | -0.069498 | -31.311 |
| w4 | 21 | -0.065736 | 110.549 |
| w5 | 26 | -0.045268 | 41.116 |
| w6 | 14 | 0.056941 | 139.041 |
| w7 | 11 | -0.012389 | -4.059 |
| w8 | 7 | 0.045686 | -8.952 |
| w9 | 7 | -0.165989 | -27.864 |
| w10 | 22 | 0.10972 | 52.185 |
| w11 | 18 | 0.113533 | 17.504 |
| w12 | 6 | 0.036085 | -3.167 |
| w13 | 22 | -0.041024 | 20.86 |
| w14 | 18 | -0.030239 | 28.292 |
| w15 | 15 | -0.016225 | 30.864 |
| w16 | 19 | 0.03652 | 17.966 |
| w17 | 12 | 0.007045 | -12.584 |
| w18 | 21 | 0.09011 | -7.549 |
| w19 | 11 | -0.031985 | -18.486 |
| w20 | 8 | 0.03754 | 1.099 |
| w21 | 16 | 0.099693 | 23.638 |
| w22 | 20 | -0.162082 | -8.356 |
| w23 | 14 | -0.052913 | -8.599 |
| w24 | 30 | -0.087259 | -18.975 |
| w25 | 19 | -0.097264 | 3.486 |
| w26 | 10 | -0.083999 | -22.458 |
| w27 | 24 | -0.121147 | 19.199 |
| w28 | 16 | -0.087805 | -16.962 |
| w29 | 17 | 0.053643 | 37.916 |
| w30 | 16 | -0.204397 | -34.437 |
| w31 | 18 | -0.001812 | -17.739 |
| w32 | 19 | 0.103436 | 17.741 |

- XRPUSD: 26 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 5 | 0.168904 | 18.655 |
| w8 | 3 | -0.027311 | -8.308 |
| w9 | 13 | 0.099008 | -2.042 |
| w10 | 12 | -0.21166 | -12.971 |
| w11 | 10 | 0.265607 | -2.385 |
| w12 | 11 | -0.075183 | -16.325 |
| w13 | 19 | 0.020556 | 0.214 |
| w14 | 16 | -0.137982 | 27.365 |
| w15 | 15 | 0.002106 | 234.534 |
| w16 | 16 | 0.041893 | 41.405 |
| w17 | 6 | 0.013307 | 26.038 |
| w18 | 17 | 0.079369 | -15.416 |
| w19 | 12 | -0.051044 | -19.507 |
| w20 | 0 | -0.061408 | 0.0 |
| w21 | 14 | -0.008887 | 7.286 |
| w22 | 18 | -0.176459 | 18.987 |
| w23 | 9 | -0.125027 | -10.941 |
| w24 | 16 | 0.194327 | 8.136 |
| w25 | 14 | -0.073909 | 0.361 |
| w26 | 12 | 0.156875 | -16.018 |
| w27 | 16 | 0.238382 | 158.233 |
| w28 | 13 | -0.056123 | -11.107 |
| w29 | 17 | 0.055043 | 16.59 |
| w30 | 7 | -0.15331 | -21.51 |
| w31 | 17 | 0.005333 | -29.121 |
| w32 | 14 | 0.307437 | 27.356 |

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
| w8 | 8 | 0.078991 | -3.631 |
| w9 | 9 | 0.100789 | -14.395 |
| w10 | 15 | -0.004912 | 11.19 |
| w11 | 18 | -0.066224 | -4.032 |
| w12 | 12 | -0.080892 | -3.1 |
| w13 | 18 | -0.077909 | 55.529 |
| w14 | 11 | -0.088955 | 32.665 |
| w15 | 23 | -0.055687 | -23.341 |
| w16 | 21 | 0.184202 | 76.41 |
| w17 | 14 | -0.026501 | -11.841 |
| w18 | 13 | 0.031555 | -13.433 |
| w19 | 8 | -0.041458 | -11.397 |
| w20 | 6 | -0.160316 | -9.366 |
| w21 | 14 | -0.175354 | -29.514 |
| w22 | 27 | -0.221838 | -23.565 |
| w23 | 5 | 0.087045 | 49.127 |
| w24 | 22 | -0.124909 | -9.284 |
| w25 | 22 | -0.052553 | 58.712 |
| w26 | 11 | 0.187732 | -7.314 |
| w27 | 25 | -0.058071 | -3.947 |
| w28 | 15 | -0.060591 | -8.516 |
| w29 | 28 | -0.127032 | 15.088 |
| w30 | 23 | -0.258194 | -22.791 |
| w31 | 9 | -0.067514 | -9.57 |
| w32 | 11 | 0.206063 | 4.627 |

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
| w1 | 15 | -0.010017 | 197.322 |
| w2 | 19 | 0.117088 | 14.855 |
| w3 | 10 | 0.072999 | -2.891 |
| w4 | 29 | 0.010898 | 196.428 |
| w5 | 19 | 0.224947 | 101.953 |
| w6 | 22 | 0.198049 | 67.102 |
| w7 | 12 | 0.167677 | 3.895 |
| w8 | 9 | 0.007659 | -13.833 |
| w9 | 11 | 0.025672 | -5.337 |
| w10 | 21 | -0.110861 | 3.933 |
| w11 | 14 | -0.01251 | 28.893 |
| w12 | 15 | -0.015427 | -28.741 |
| w13 | 18 | -0.06238 | 60.877 |
| w14 | 25 | 0.076375 | 82.559 |
| w15 | 15 | -0.072625 | 8.587 |
| w16 | 23 | 0.202469 | 96.903 |
| w17 | 8 | 0.023681 | 11.995 |
| w18 | 18 | -0.01588 | 8.536 |
| w19 | 10 | 0.0574 | -0.12 |
| w20 | 6 | -0.04879 | 5.623 |
| w21 | 13 | 0.066589 | -34.161 |
| w22 | 32 | -0.09836 | 3.876 |
| w23 | 13 | -0.133349 | -17.853 |
| w24 | 22 | -0.012545 | 0.922 |
| w25 | 10 | 0.003144 | 8.709 |
| w26 | 14 | 0.003087 | -14.49 |
| w27 | 21 | -0.078083 | 14.564 |
| w28 | 4 | -0.111568 | -11.1 |
| w29 | 28 | -0.016935 | 9.47 |
| w30 | 4 | -0.07337 | -21.423 |
| w31 | 26 | -0.023033 | -22.127 |
| w32 | 19 | 0.071208 | 23.439 |

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 19 | -0.018265 | -2.494 |
| w12 | 9 | -0.026311 | -13.304 |
| w13 | 19 | 0.055106 | 62.979 |
| w14 | 16 | -0.067827 | 36.297 |
| w15 | 19 | 0.072834 | 15.429 |
| w16 | 28 | -0.021142 | 25.639 |
| w17 | 15 | 0.000431 | 35.194 |
| w18 | 6 | -0.081076 | -15.258 |
| w19 | 10 | -0.049724 | -32.631 |
| w20 | 13 | -0.047929 | -11.329 |
| w21 | 7 | -0.052173 | -22.17 |
| w22 | 24 | 0.078619 | 26.648 |
| w23 | 7 | -0.173934 | -15.122 |
| w24 | 18 | -0.128767 | 66.045 |
| w25 | 11 | 0.081227 | -4.861 |
| w26 | 16 | 0.021687 | -13.16 |
| w27 | 25 | 0.08304 | 78.945 |
| w28 | 12 | -0.133297 | -15.62 |
| w29 | 19 | 0.125075 | 10.612 |
| w30 | 5 | 0.015604 | -9.265 |
| w31 | 5 | -0.045186 | -18.15 |
| w32 | 19 | 0.228293 | 19.791 |

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
| w13 | 20 | -0.056464 | -19.45 |
| w14 | 19 | 0.178078 | 71.714 |
| w15 | 16 | -0.034047 | -6.568 |
| w16 | 26 | 0.024658 | 53.781 |
| w17 | 19 | 0.058335 | 20.261 |
| w18 | 16 | -0.00034 | 7.917 |
| w19 | 15 | -0.112557 | -12.691 |
| w20 | 15 | 0.082208 | 8.324 |
| w21 | 13 | 0.188246 | -30.436 |
| w22 | 25 | -0.106173 | 13.897 |
| w23 | 5 | -0.016017 | -11.582 |
| w24 | 21 | -0.141021 | -18.937 |
| w25 | 9 | 0.053673 | 41.586 |
| w26 | 9 | -0.011007 | -21.344 |
| w27 | 21 | 0.103158 | 17.816 |
| w28 | 10 | 0.022228 | -12.481 |
| w29 | 22 | 0.063857 | -19.835 |
| w30 | 5 | -0.048987 | -8.726 |
| w31 | 15 | -0.068224 | -13.202 |
| w32 | 11 | 0.064692 | -12.915 |

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
| w16 | 21 | -0.019626 | 69.147 |
| w17 | 19 | -0.116715 | -15.48 |
| w18 | 12 | -0.064574 | 24.794 |
| w19 | 11 | -0.049511 | -22.386 |
| w20 | 11 | -0.095221 | -19.988 |
| w21 | 11 | 0.087335 | -8.75 |
| w22 | 16 | -0.0483 | -16.587 |
| w23 | 2 | -0.050415 | -16.984 |
| w24 | 33 | 0.00127 | 14.207 |
| w25 | 19 | 0.193136 | 0.14 |
| w26 | 15 | 0.08381 | -19.066 |
| w27 | 21 | 0.234513 | 91.896 |
| w28 | 9 | 0.010763 | -10.847 |
| w29 | 13 | 0.098453 | 44.277 |
| w30 | 1 | -0.116756 | -4.589 |
| w31 | 13 | 0.05829 | -5.777 |
| w32 | 14 | 0.106912 | -6.491 |

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
| w15 | 9 | 0.094348 | -3.0 |
| w16 | 22 | 0.026277 | 76.411 |
| w17 | 6 | -0.059106 | 13.088 |
| w18 | 19 | 0.040753 | 1.668 |
| w19 | 14 | -0.029351 | -2.974 |
| w20 | 18 | -0.071393 | 4.705 |
| w21 | 15 | -0.088435 | -34.091 |
| w22 | 31 | -0.154851 | 5.447 |
| w23 | 24 | 0.008371 | -6.528 |
| w24 | 28 | -0.016851 | 34.855 |
| w25 | 15 | 0.076118 | 4.488 |
| w26 | 18 | 0.119325 | 23.685 |
| w27 | 24 | 0.298744 | 133.682 |
| w28 | 24 | -0.117167 | -19.831 |
| w29 | 31 | -0.026869 | 26.331 |
| w30 | 8 | -0.107375 | -15.236 |
| w31 | 33 | -0.046611 | 23.279 |
| w32 | 25 | 0.097187 | -2.885 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | -0.101332 | -7.626 |
| w18 | 18 | -0.027533 | 4.917 |
| w19 | 13 | -0.060248 | -19.781 |
| w20 | 14 | -0.013019 | -7.142 |
| w21 | 10 | -0.131356 | -31.393 |
| w22 | 17 | -0.170208 | 14.672 |
| w23 | 15 | -0.056308 | -22.133 |
| w24 | 12 | 0.004255 | 24.332 |
| w25 | 17 | 0.088279 | 6.589 |
| w26 | 10 | 0.017538 | -15.195 |
| w27 | 14 | 0.220984 | 40.044 |
| w28 | 11 | -0.106922 | -24.44 |
| w29 | 19 | 0.033347 | -21.124 |
| w30 | 11 | 0.01706 | -24.806 |
| w31 | 14 | -0.014492 | -24.402 |
| w32 | 11 | -0.004097 | -19.383 |

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
| w20 | 17 | 0.133718 | 11.618 |
| w21 | 10 | -0.042881 | -22.041 |
| w22 | 23 | -0.060936 | 32.61 |
| w23 | 6 | -0.004008 | 0.09 |
| w24 | 21 | 0.127882 | 143.968 |
| w25 | 12 | 0.061492 | 25.731 |
| w26 | 14 | 0.066135 | -15.807 |
| w27 | 24 | 0.068445 | 21.197 |
| w28 | 8 | 0.005426 | -11.093 |
| w29 | 25 | 0.036843 | 6.785 |
| w30 | 7 | 0.107246 | 11.414 |
| w31 | 20 | -0.016341 | -23.282 |
| w32 | 17 | 0.174172 | 6.96 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.17001 | -10.439 |
| w23 | 8 | -0.044522 | -18.288 |
| w24 | 14 | 0.142901 | 240.836 |
| w25 | 10 | -0.082306 | 64.807 |
| w26 | 12 | -0.075732 | -12.886 |
| w27 | 13 | 0.028672 | 2.264 |
| w28 | 8 | -0.057884 | -16.2 |
| w29 | 21 | 0.10703 | -10.156 |
| w30 | 16 | -0.046444 | -29.674 |
| w31 | 12 | -0.104042 | -10.963 |
| w32 | 12 | -0.121242 | 55.509 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 19 | -0.111794 | 25.116 |
| w25 | 21 | -0.027442 | -2.754 |
| w26 | 10 | -0.081417 | -17.15 |
| w27 | 20 | 0.009909 | 33.687 |
| w28 | 10 | 0.109976 | -4.448 |
| w29 | 16 | 0.105766 | -0.935 |
| w30 | 8 | -0.080738 | -24.937 |
| w31 | 15 | -0.006131 | -18.21 |
| w32 | 21 | 0.301212 | 21.467 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 19 | 0.09304 | 55.76 |
| w6 | 23 | -0.163544 | -14.273 |
| w7 | 14 | 0.005357 | 1.102 |
| w8 | 7 | 0.071707 | -1.846 |
| w9 | 5 | -0.024904 | -10.328 |
| w10 | 18 | -0.013872 | 21.608 |
| w11 | 15 | -0.084967 | 27.519 |
| w12 | 9 | -0.00783 | -15.616 |
| w13 | 20 | 0.221796 | 62.18 |
| w14 | 20 | -0.138001 | 0.392 |
| w15 | 15 | -0.005312 | 1.956 |
| w16 | 19 | -0.014934 | 38.345 |
| w17 | 15 | -0.090266 | -17.533 |
| w18 | 14 | 0.171437 | 27.5 |
| w19 | 4 | -0.051892 | 21.086 |
| w20 | 7 | 0.100979 | -2.657 |
| w21 | 10 | 0.086988 | -30.488 |
| w22 | 22 | -0.044957 | -9.154 |
| w23 | 10 | 0.092027 | -9.976 |
| w24 | 19 | 0.138235 | 5.759 |
| w25 | 11 | 0.039277 | 8.796 |
| w26 | 16 | 0.072405 | 31.975 |
| w27 | 17 | 0.106248 | 63.261 |
| w28 | 10 | 0.03104 | -22.825 |
| w29 | 21 | 0.139196 | 24.107 |
| w30 | 22 | 0.075484 | 154.023 |
| w31 | 12 | 0.063199 | -0.445 |
| w32 | 14 | -0.023083 | 47.88 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 15 | 0.026123 | 157.816 |
| w6 | 12 | 0.034482 | 96.702 |
| w7 | 8 | -0.038018 | -4.441 |
| w8 | 7 | -0.034922 | -15.365 |
| w9 | 10 | -0.115039 | -22.019 |
| w10 | 27 | -0.07321 | 19.351 |
| w11 | 13 | -0.033642 | 13.076 |
| w12 | 9 | -0.088375 | -19.012 |
| w13 | 16 | 0.063751 | 19.905 |
| w14 | 27 | -0.1664 | 33.896 |
| w15 | 27 | -0.204962 | -0.076 |
| w16 | 18 | -0.110441 | 31.3 |
| w17 | 19 | -0.071567 | -23.92 |
| w18 | 17 | 0.030864 | -8.307 |
| w19 | 17 | -0.080708 | -16.295 |
| w20 | 7 | -0.037598 | -1.972 |
| w21 | 23 | 0.011037 | -11.694 |
| w22 | 19 | -0.031399 | 8.528 |
| w23 | 12 | 0.071683 | 10.48 |
| w24 | 27 | 0.076738 | 7.785 |
| w25 | 7 | -0.063355 | -55.402 |
| w26 | 24 | -0.036054 | 8.01 |
| w27 | 23 | -0.017437 | 1.913 |
| w28 | 24 | -0.054004 | 22.451 |
| w29 | 16 | -0.01067 | -3.904 |
| w30 | 38 | -0.058468 | 15.749 |
| w31 | 20 | 0.067505 | 33.899 |
| w32 | 26 | -0.022181 | 50.136 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 15 | -0.093196 | -14.108 |
| w18 | 25 | 0.032302 | 27.183 |
| w19 | 8 | 0.094868 | -12.799 |
| w20 | 13 | -0.066048 | -24.099 |
| w21 | 7 | -0.093411 | -46.307 |
| w22 | 25 | -0.015053 | 12.418 |
| w23 | 4 | -0.052556 | -13.809 |
| w24 | 16 | -0.073138 | -2.607 |
| w25 | 10 | -0.016089 | 41.81 |
| w26 | 16 | -0.020522 | -27.111 |
| w27 | 10 | 0.044492 | 162.038 |
| w28 | 12 | -0.102773 | -7.18 |
| w29 | 14 | 0.222612 | 33.863 |
| w30 | 4 | -0.070785 | -19.358 |
| w31 | 17 | 0.019733 | -16.358 |
| w32 | 18 | 0.136044 | 29.973 |

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
| w17 | 18 | -0.190489 | -21.388 |
| w18 | 15 | -0.116154 | -25.499 |
| w19 | 11 | 0.018417 | 7.987 |
| w20 | 10 | -0.038988 | -4.585 |
| w21 | 15 | 0.13612 | -20.066 |
| w22 | 22 | -0.088659 | 11.223 |
| w23 | 9 | 0.031315 | 0.311 |
| w24 | 27 | 0.04751 | 0.101 |
| w25 | 13 | 0.06375 | -11.05 |
| w26 | 23 | 0.020387 | 25.796 |
| w27 | 22 | -0.012244 | 66.779 |
| w28 | 8 | 0.013716 | -5.61 |
| w29 | 21 | -0.008076 | 26.098 |
| w30 | 5 | -0.106411 | -4.327 |
| w31 | 9 | -0.097076 | -29.47 |
| w32 | 16 | -0.037829 | 0.46 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 12 | -0.134652 | -22.225 |
| w20 | 11 | 0.012324 | -0.246 |
| w21 | 15 | -0.031916 | 17.363 |
| w22 | 24 | -0.014092 | 126.784 |
| w23 | 16 | 0.133435 | -9.619 |
| w24 | 26 | -0.091881 | 57.612 |
| w25 | 13 | -0.08196 | -23.381 |
| w26 | 16 | 0.002419 | -36.939 |
| w27 | 19 | 0.118129 | -2.119 |
| w28 | 7 | -0.102987 | -8.854 |
| w29 | 27 | -0.041619 | -14.124 |
| w30 | 6 | 0.017385 | -4.836 |
| w31 | 15 | -0.009116 | -16.862 |
| w32 | 18 | -0.038684 | 29.555 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 22 | 0.034685 | 28.728 |
| w23 | 14 | -0.00188 | -19.691 |
| w24 | 25 | -0.096982 | -7.71 |
| w25 | 16 | -0.000286 | -20.537 |
| w26 | 7 | 0.033924 | -7.003 |
| w27 | 20 | -0.001888 | -11.814 |
| w28 | 10 | -0.001221 | -11.656 |
| w29 | 20 | 0.109951 | 18.161 |
| w30 | 3 | -0.070191 | -14.739 |
| w31 | 14 | 0.034113 | -21.308 |
| w32 | 16 | 0.062082 | 2.185 |

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
| w27 | 14 | -0.00182 | 39.152 |
| w28 | 10 | -0.041585 | -7.71 |
| w29 | 19 | 0.023963 | 2.736 |
| w30 | 7 | 0.131812 | -5.146 |
| w31 | 15 | -0.072536 | -29.148 |
| w32 | 14 | -0.072846 | 19.31 |

- FILUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 8 | 0.122036 | -13.272 |
| w19 | 7 | 0.05623 | -18.391 |
| w20 | 12 | 0.173091 | 9.988 |
| w21 | 7 | -0.01011 | -22.806 |
| w22 | 19 | -0.034097 | 20.988 |
| w23 | 10 | -0.183801 | -28.63 |
| w24 | 26 | -0.054625 | 13.476 |
| w25 | 17 | 0.027387 | 13.843 |
| w26 | 16 | 0.047293 | -23.374 |
| w27 | 19 | 0.085995 | 36.982 |
| w28 | 8 | -0.149521 | -16.578 |
| w29 | 21 | 0.010631 | -25.769 |
| w30 | 9 | 0.290895 | 13.533 |
| w31 | 17 | -0.064905 | -29.434 |
| w32 | 11 | 0.054296 | 1.364 |

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
| w18 | 12 | -0.016489 | -4.877 |
| w19 | 6 | -0.062395 | -18.223 |
| w20 | 5 | 0.029629 | 1.66 |
| w21 | 9 | 0.096661 | -4.054 |
| w22 | 18 | 0.015401 | 102.769 |
| w23 | 7 | 0.077381 | -5.617 |
| w24 | 23 | -0.141723 | 50.453 |
| w25 | 15 | 0.075687 | 42.431 |
| w26 | 11 | -0.051253 | -17.028 |
| w27 | 13 | 0.036577 | 24.094 |
| w28 | 5 | 0.079015 | -5.128 |
| w29 | 14 | 0.07992 | -3.785 |
| w30 | 9 | -0.010573 | -15.583 |
| w31 | 10 | -0.040722 | -21.452 |
| w32 | 13 | -0.017103 | 9.257 |

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
| w28 | 12 | 0.045738 | -5.659 |
| w29 | 17 | -0.050261 | -9.66 |
| w30 | 12 | 0.077478 | -13.927 |
| w31 | 11 | 0.202691 | 28.347 |
| w32 | 12 | 0.000902 | 2.243 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 20 | 0.24956 | 36.882 |
| w15 | 11 | 0.152123 | 108.257 |
| w16 | 14 | 0.040368 | 224.211 |
| w17 | 7 | 0.031465 | 25.009 |
| w18 | 7 | -0.040396 | -1.663 |
| w19 | 6 | -0.15554 | 8.696 |
| w20 | 10 | -0.073344 | -21.19 |
| w21 | 7 | -0.044427 | 87.757 |
| w22 | 19 | -0.055206 | 6.106 |
| w23 | 11 | -0.068089 | 1.163 |
| w24 | 14 | 0.10702 | 17.753 |
| w25 | 15 | 0.161739 | 87.531 |
| w26 | 11 | 0.037471 | -14.743 |
| w27 | 20 | -0.022329 | 91.079 |
| w28 | 8 | 0.025817 | -2.869 |
| w29 | 22 | 0.077495 | 37.271 |
| w30 | 6 | 0.04416 | 0.845 |
| w31 | 12 | 0.029113 | -7.132 |
| w32 | 10 | 0.217041 | 11.462 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 16 | 0.150004 | 91.052 |
| w26 | 14 | 0.163199 | 8.195 |
| w27 | 23 | 0.009222 | 46.566 |
| w28 | 11 | -0.013959 | -12.717 |
| w29 | 15 | 0.00683 | -8.141 |
| w30 | 4 | -0.008406 | -11.121 |
| w31 | 16 | 0.008481 | -7.557 |
| w32 | 18 | 0.249034 | 11.53 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

