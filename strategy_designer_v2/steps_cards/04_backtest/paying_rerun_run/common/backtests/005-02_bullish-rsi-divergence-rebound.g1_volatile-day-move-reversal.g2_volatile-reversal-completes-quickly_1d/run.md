# Backtest of 005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d

- Plan: `../../../../../03_test_plan/night_005_run/plans/005-02_bullish-rsi-divergence-rebound.g1_volatile-day-move-reversal.g2_volatile-reversal-completes-quickly_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.128651 | 6.871 |
| w2 | 37 | -0.06469 | -27.961 |
| w3 | 12 | 0.093203 | 7.262 |
| w4 | 30 | 0.075549 | 9.901 |
| w5 | 31 | 0.135419 | 23.236 |
| w6 | 29 | 0.049393 | 1.438 |
| w7 | 32 | -0.072403 | -10.291 |
| w8 | 0 | -0.041632 | 0.0 |
| w9 | 22 | 0.093379 | 12.883 |
| w10 | 10 | 0.083435 | 4.956 |
| w11 | 38 | 0.10966 | 17.315 |
| w12 | 14 | -0.079606 | -6.599 |
| w13 | 24 | 0.191865 | 22.251 |
| w14 | 0 | None | 0.0 |
| w15 | 29 | 0.080507 | 10.819 |
| w16 | 28 | 0.012458 | -3.219 |
| w17 | 29 | 0.177136 | 27.573 |
| w18 | 9 | 0.071532 | 5.306 |
| w19 | 24 | 0.003471 | -1.029 |
| w20 | 25 | 0.212444 | 30.735 |
| w21 | 12 | 0.223808 | 16.837 |
| w22 | 27 | -0.006863 | -6.383 |
| w23 | 4 | -0.137113 | -5.722 |
| w24 | 23 | -0.017739 | -8.653 |
| w25 | 37 | 0.204903 | 39.444 |
| w26 | 18 | 0.109995 | 11.897 |
| w27 | 9 | 0.080004 | 5.774 |
| w28 | 25 | 0.111391 | 14.496 |
| w29 | 10 | 0.088568 | 5.864 |
| w30 | 35 | -0.120418 | -17.824 |
| w31 | 18 | -0.036832 | -19.564 |
| w32 | 16 | 0.06395 | 4.399 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.138625 | 6.437 |
| w2 | 28 | 0.04841 | -0.662 |
| w3 | 20 | -0.02292 | -4.507 |
| w4 | 39 | 0.014576 | -3.572 |
| w5 | 5 | -0.102896 | -2.516 |
| w6 | 31 | 0.020174 | -1.148 |
| w7 | 2 | -0.058703 | -1.975 |
| w8 | 8 | 0.003266 | -0.013 |
| w9 | 44 | 0.062191 | 6.243 |
| w10 | 19 | 0.05919 | 5.28 |
| w11 | 15 | 0.05607 | 4.165 |
| w12 | 0 | None | 0.0 |
| w13 | 41 | 0.113504 | 7.765 |
| w14 | 25 | 0.089523 | 11.422 |
| w15 | 37 | -0.030954 | -16.684 |
| w16 | 19 | 0.015359 | 0.47 |
| w17 | 24 | 0.270661 | 29.627 |
| w18 | 22 | -0.003623 | -3.129 |
| w19 | 0 | None | 0.0 |
| w20 | 24 | 0.27771 | 44.569 |
| w21 | 15 | -0.034318 | -5.579 |
| w22 | 16 | -0.057317 | -10.153 |
| w23 | 20 | 0.09514 | 8.724 |
| w24 | 6 | 0.019201 | -0.367 |
| w25 | 50 | 0.162106 | 39.941 |
| w26 | 8 | 0.131874 | 5.871 |
| w27 | 38 | 0.01973 | -2.122 |
| w28 | 2 | -0.13434 | -6.065 |
| w29 | 18 | -0.003604 | -3.86 |
| w30 | 25 | -0.085404 | -8.873 |
| w31 | 1 | -0.019487 | -0.644 |
| w32 | 21 | -0.040025 | -10.117 |

- XRPUSD: 26 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.077291 | 3.041 |
| w8 | 9 | 0.244226 | 19.058 |
| w9 | 18 | -0.030253 | -2.76 |
| w10 | 4 | 0.018945 | 0.248 |
| w11 | 18 | -0.058157 | -9.0 |
| w12 | 15 | 0.184351 | 20.553 |
| w13 | 45 | 0.176794 | 21.904 |
| w14 | 15 | 0.024736 | 0.975 |
| w15 | 30 | 0.107634 | 15.453 |
| w16 | 20 | -0.060036 | -4.857 |
| w17 | 11 | 0.11602 | 5.421 |
| w18 | 2 | -0.061153 | -3.48 |
| w19 | 22 | 0.043402 | 5.137 |
| w20 | 0 | 0.130423 | 0.0 |
| w21 | 28 | 0.258479 | 43.284 |
| w22 | 13 | 0.122479 | 9.722 |
| w23 | 13 | 0.069179 | 3.639 |
| w24 | 7 | 0.180345 | 14.749 |
| w25 | 27 | 0.179983 | 27.869 |
| w26 | 24 | -0.05289 | -13.049 |
| w27 | 24 | -0.368101 | -61.454 |
| w28 | 15 | 0.004146 | -0.77 |
| w29 | 19 | 0.08868 | 8.73 |
| w30 | 17 | -0.117983 | -10.789 |
| w31 | 12 | 0.311007 | 26.248 |
| w32 | 32 | -0.261782 | -45.163 |

- w6 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 106 warm-up bars -- required_bars=120. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 4 | 0.058037 | 1.306 |
| w9 | 32 | -0.219852 | -49.247 |
| w10 | 13 | 0.067332 | 3.214 |
| w11 | 1 | 0.065255 | 2.666 |
| w12 | 14 | 0.1355 | 9.622 |
| w13 | 34 | 0.178522 | 21.086 |
| w14 | 17 | 0.119933 | 8.377 |
| w15 | 26 | 0.049329 | -0.294 |
| w16 | 27 | 0.007899 | -2.5 |
| w17 | 22 | 0.323766 | 42.011 |
| w18 | 6 | 0.028316 | -0.169 |
| w19 | 12 | 0.107193 | 8.513 |
| w20 | 22 | 0.286605 | 40.268 |
| w21 | 7 | 0.100025 | 6.175 |
| w22 | 29 | 0.115931 | 5.74 |
| w23 | 14 | -0.028788 | -7.028 |
| w24 | 12 | 0.149815 | 10.122 |
| w25 | 37 | 0.133692 | 12.995 |
| w26 | 9 | 0.10273 | 5.24 |
| w27 | 21 | 0.048189 | 4.254 |
| w28 | 15 | -0.101445 | -11.764 |
| w29 | 10 | 0.055619 | 1.55 |
| w30 | 37 | 0.036035 | -3.608 |
| w31 | 9 | 0.206692 | 13.474 |
| w32 | 23 | 0.068521 | -1.182 |

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
| w1 | 21 | -0.033691 | -6.787 |
| w2 | 15 | 0.002145 | -3.631 |
| w3 | 17 | 0.072756 | 7.864 |
| w4 | 25 | -0.123523 | -47.793 |
| w5 | 18 | 0.10313 | 10.116 |
| w6 | 9 | -0.172257 | -24.709 |
| w7 | 27 | 0.040262 | 2.701 |
| w8 | 7 | 0.016218 | 0.042 |
| w9 | 42 | 0.135547 | 26.108 |
| w10 | 10 | 0.128118 | 5.537 |
| w11 | 30 | 0.039954 | 5.526 |
| w12 | 17 | 0.091109 | 8.832 |
| w13 | 53 | 0.147282 | 26.087 |
| w14 | 3 | -0.046979 | -4.588 |
| w15 | 23 | 0.087432 | 9.516 |
| w16 | 32 | 0.045978 | -3.189 |
| w17 | 24 | 0.167768 | 26.949 |
| w18 | 7 | -0.121009 | -9.454 |
| w19 | 12 | -0.005971 | -1.252 |
| w20 | 34 | 0.085889 | 16.744 |
| w21 | 10 | -0.02738 | -5.843 |
| w22 | 15 | 0.178804 | 12.396 |
| w23 | 0 | None | 0.0 |
| w24 | 22 | 0.211705 | 27.344 |
| w25 | 39 | 0.14509 | 22.723 |
| w26 | 17 | 0.188655 | 23.152 |
| w27 | 14 | 0.024289 | 0.953 |
| w28 | 23 | 0.180254 | 23.197 |
| w29 | 11 | 0.167917 | 17.889 |
| w30 | 12 | -0.05389 | -3.001 |
| w31 | 16 | -0.028561 | -10.183 |
| w32 | 27 | -0.109329 | -15.524 |

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 20 | 0.064449 | 7.383 |
| w12 | 21 | 0.153205 | 8.272 |
| w13 | 54 | 0.108907 | 4.166 |
| w14 | 2 | -0.032113 | -1.658 |
| w15 | 27 | 0.117133 | 15.403 |
| w16 | 23 | -0.11715 | -28.82 |
| w17 | 20 | 0.159642 | 18.844 |
| w18 | 15 | 0.043369 | 2.534 |
| w19 | 16 | -0.133952 | -13.57 |
| w20 | 23 | 0.160915 | 22.53 |
| w21 | 9 | 0.030185 | -2.477 |
| w22 | 18 | 0.082908 | 4.257 |
| w23 | 19 | 0.074884 | 2.108 |
| w24 | 42 | 0.036603 | -6.798 |
| w25 | 24 | 0.146272 | 14.576 |
| w26 | 15 | 0.003955 | -1.15 |
| w27 | 29 | -0.244281 | -44.214 |
| w28 | 15 | 0.109819 | 7.718 |
| w29 | 12 | 0.14009 | 10.385 |
| w30 | 20 | -0.035454 | -3.307 |
| w31 | 11 | 0.220998 | 15.129 |
| w32 | 23 | -0.06414 | -12.048 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=120. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 24 | 0.023484 | -9.266 |
| w14 | 18 | -0.009979 | -13.231 |
| w15 | 15 | 0.15404 | 7.506 |
| w16 | 34 | 0.054693 | -0.216 |
| w17 | 21 | 0.231316 | 24.392 |
| w18 | 19 | 0.145696 | 17.5 |
| w19 | 11 | 0.088107 | 4.154 |
| w20 | 14 | 0.1788 | 28.538 |
| w21 | 20 | 0.211519 | 20.1 |
| w22 | 2 | 0.047986 | 0.525 |
| w23 | 12 | 0.040092 | -0.258 |
| w24 | 49 | 0.193157 | 19.161 |
| w25 | 19 | 0.081293 | 5.122 |
| w26 | 20 | -0.016289 | -7.686 |
| w27 | 48 | -0.092446 | -29.247 |
| w28 | 1 | 0.002791 | 0.111 |
| w29 | 7 | 0.095486 | 6.308 |
| w30 | 19 | 0.00904 | -3.676 |
| w31 | 9 | -0.086113 | -6.866 |
| w32 | 27 | -0.106066 | -19.453 |

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
| w16 | 47 | 0.034199 | -3.831 |
| w17 | 16 | 0.227298 | 21.906 |
| w18 | 17 | -0.051559 | -5.577 |
| w19 | 5 | -0.002371 | -1.715 |
| w20 | 21 | 0.104569 | 12.64 |
| w21 | 19 | -0.066246 | -15.583 |
| w22 | 12 | 0.164103 | 7.609 |
| w23 | 10 | 0.13833 | 9.562 |
| w24 | 26 | -0.067456 | -20.892 |
| w25 | 30 | 0.142334 | 12.786 |
| w26 | 5 | -0.165559 | -10.119 |
| w27 | 31 | -0.089631 | -26.448 |
| w28 | 7 | -0.025418 | -2.52 |
| w29 | 21 | -0.007666 | -4.774 |
| w30 | 9 | -0.028751 | -1.865 |
| w31 | 17 | 0.188131 | 17.734 |
| w32 | 4 | 0.07279 | 4.477 |

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
| w15 | 18 | -0.012372 | -2.76 |
| w16 | 51 | 0.066223 | 7.587 |
| w17 | 12 | 0.282364 | 15.064 |
| w18 | 8 | -0.033974 | -2.64 |
| w19 | 14 | 0.168577 | 14.786 |
| w20 | 22 | 0.324656 | 33.889 |
| w21 | 14 | 0.209781 | 21.159 |
| w22 | 28 | 0.133277 | 9.591 |
| w23 | 0 | None | 0.0 |
| w24 | 20 | 0.005787 | -6.21 |
| w25 | 17 | 0.175602 | 14.13 |
| w26 | 21 | -0.078443 | -18.67 |
| w27 | 31 | -0.206972 | -79.017 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.097322 | 5.443 |
| w30 | 13 | 0.149473 | 8.634 |
| w31 | 11 | 0.0697 | 2.104 |
| w32 | 19 | -0.103987 | -8.979 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 27 | 0.165602 | 23.345 |
| w18 | 6 | -0.064947 | -4.584 |
| w19 | 0 | 0.079406 | 0.0 |
| w20 | 21 | 0.146509 | 18.063 |
| w21 | 11 | -0.003568 | -5.604 |
| w22 | 19 | 0.0353 | -0.181 |
| w23 | 4 | 0.100618 | 3.283 |
| w24 | 55 | 0.109739 | 1.742 |
| w25 | 26 | 0.179041 | 19.52 |
| w26 | 9 | -0.067367 | -3.937 |
| w27 | 41 | -0.175582 | -44.269 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.061684 | 2.539 |
| w30 | 17 | -0.103528 | -11.353 |
| w31 | 11 | 0.056213 | 4.963 |
| w32 | 11 | 0.065124 | 1.842 |

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
| w20 | 25 | 0.17339 | 29.03 |
| w21 | 12 | -0.008366 | -6.812 |
| w22 | 12 | 0.166356 | 14.229 |
| w23 | 13 | -0.003338 | -2.934 |
| w24 | 26 | -0.147474 | -41.963 |
| w25 | 23 | 0.214491 | 25.256 |
| w26 | 19 | 0.072302 | 6.495 |
| w27 | 36 | -0.104088 | -18.612 |
| w28 | 13 | -0.017841 | -4.587 |
| w29 | 10 | 0.057706 | 3.446 |
| w30 | 22 | 0.035566 | 2.158 |
| w31 | 16 | 0.156161 | 10.398 |
| w32 | 20 | 0.085473 | 8.51 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.112058 | 8.219 |
| w23 | 7 | -0.089462 | -7.612 |
| w24 | 39 | 0.028431 | -5.271 |
| w25 | 28 | 0.150019 | 17.009 |
| w26 | 10 | -0.030614 | -2.389 |
| w27 | 31 | 0.021793 | 0.872 |
| w28 | 17 | -0.040398 | -6.692 |
| w29 | 9 | 0.102345 | 7.64 |
| w30 | 29 | -0.223078 | -27.129 |
| w31 | 14 | -0.001631 | -0.668 |
| w32 | 22 | 0.093938 | 11.324 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 26 | 0.123277 | 17.373 |
| w25 | 27 | 0.099566 | 10.846 |
| w26 | 17 | 0.015683 | 1.546 |
| w27 | 14 | -0.046376 | -9.588 |
| w28 | 31 | 0.000357 | -1.288 |
| w29 | 2 | -0.047926 | -2.048 |
| w30 | 22 | -0.089969 | -10.526 |
| w31 | 15 | 0.223633 | 15.816 |
| w32 | 17 | -0.028833 | -5.478 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 20 | -0.019724 | -7.104 |
| w6 | 14 | 0.130123 | 12.4 |
| w7 | 8 | -0.098814 | -7.409 |
| w8 | 15 | 0.062167 | 2.791 |
| w9 | 26 | -0.054261 | -18.746 |
| w10 | 2 | 0.087453 | 1.417 |
| w11 | 42 | 0.023092 | -3.285 |
| w12 | 14 | 0.121927 | 15.522 |
| w13 | 26 | 0.171351 | 27.573 |
| w14 | 15 | -0.002269 | -1.475 |
| w15 | 16 | 0.030989 | 0.183 |
| w16 | 31 | -0.023063 | -8.752 |
| w17 | 23 | 0.311406 | 34.638 |
| w18 | 23 | -0.032684 | -9.898 |
| w19 | 19 | -0.010991 | -1.805 |
| w20 | 20 | 0.135949 | 12.873 |
| w21 | 10 | -0.120929 | -15.877 |
| w22 | 27 | 0.182325 | 18.84 |
| w23 | 16 | 0.179415 | 19.397 |
| w24 | 32 | 0.105233 | 11.255 |
| w25 | 38 | 0.024501 | -2.981 |
| w26 | 17 | -0.023795 | -7.234 |
| w27 | 40 | -0.046925 | -17.429 |
| w28 | 0 | None | 0.0 |
| w29 | 19 | -0.006916 | -2.425 |
| w30 | 33 | 0.034284 | -14.307 |
| w31 | 0 | None | 0.0 |
| w32 | 27 | -0.111635 | -12.773 |

- XMRUSD: 27 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 15 | 0.096878 | 6.88 |
| w7 | 27 | -0.12748 | -15.072 |
| w8 | 12 | 0.050583 | 3.415 |
| w9 | 40 | 0.144309 | 18.31 |
| w10 | 10 | 0.165899 | 7.663 |
| w11 | 35 | 0.090945 | 8.539 |
| w12 | 2 | 0.080123 | 3.521 |
| w13 | 45 | 0.137245 | 14.994 |
| w14 | 13 | 0.23163 | 25.092 |
| w15 | 13 | 0.024144 | -2.814 |
| w16 | 28 | 0.110631 | 18.187 |
| w17 | 23 | 0.193589 | 18.68 |
| w18 | 4 | -0.038608 | -3.304 |
| w19 | 27 | -0.047839 | -10.684 |
| w20 | 18 | -0.037771 | -6.156 |
| w21 | 10 | 0.233079 | 15.921 |
| w22 | 16 | 0.049916 | 1.216 |
| w23 | 13 | -0.070592 | -9.326 |
| w24 | 14 | 0.055006 | 1.291 |
| w25 | 33 | 0.227255 | 49.196 |
| w26 | 10 | 0.114631 | 7.901 |
| w27 | 37 | 0.119114 | -3.388 |
| w28 | 0 | None | 0.0 |
| w29 | 24 | -0.176696 | -22.983 |
| w30 | 23 | -0.115532 | -16.11 |
| w31 | 25 | 0.043731 | 0.28 |
| w32 | 19 | 0.049601 | 8.652 |

- w5 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 119 warm-up bars -- required_bars=120. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- CRVUSD: 15 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 15 | -0.060525 | -7.424 |
| w19 | 1 | None | -0.167 |
| w20 | 26 | -0.06238 | -10.513 |
| w21 | 13 | -0.030184 | -10.062 |
| w22 | 8 | -0.070837 | -5.148 |
| w23 | 24 | 0.025716 | -2.74 |
| w24 | 21 | 0.167877 | 22.756 |
| w25 | 35 | 0.128449 | 13.817 |
| w26 | 25 | 0.010598 | -1.729 |
| w27 | 27 | -0.260256 | -46.32 |
| w28 | 7 | -0.044369 | -4.173 |
| w29 | 21 | -0.03436 | -5.863 |
| w30 | 12 | -0.075861 | -10.698 |
| w31 | 12 | 0.018701 | 0.143 |
| w32 | 26 | -0.033799 | -14.202 |

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

- AAVEUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 25 | 0.262757 | 44.644 |
| w18 | 10 | -0.190376 | -23.424 |
| w19 | 26 | 0.111907 | 11.646 |
| w20 | 20 | 0.166863 | 16.599 |
| w21 | 12 | -0.029052 | -6.547 |
| w22 | 3 | 0.061068 | 2.228 |
| w23 | 27 | 0.090945 | 6.557 |
| w24 | 32 | 0.062335 | 1.63 |
| w25 | 43 | -0.000188 | -5.44 |
| w26 | 23 | -0.014182 | -4.643 |
| w27 | 40 | 0.144944 | 22.128 |
| w28 | 17 | 0.085012 | 5.853 |
| w29 | 7 | 0.047938 | 2.195 |
| w30 | 30 | -0.027375 | -7.403 |
| w31 | 12 | 0.04898 | 2.245 |
| w32 | 19 | -0.032247 | -7.248 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 23 | 0.058535 | 3.74 |
| w20 | 21 | 0.056691 | 3.758 |
| w21 | 19 | 0.029724 | -2.307 |
| w22 | 6 | -0.056326 | -2.182 |
| w23 | 0 | None | 0.0 |
| w24 | 51 | 0.115255 | -3.358 |
| w25 | 17 | 0.148116 | 11.429 |
| w26 | 13 | 0.012684 | 0.006 |
| w27 | 28 | -0.088174 | -15.177 |
| w28 | 22 | -0.11877 | -15.424 |
| w29 | 8 | 0.083675 | 5.168 |
| w30 | 16 | 0.018801 | -0.484 |
| w31 | 6 | -0.017291 | -2.705 |
| w32 | 29 | 0.110678 | 8.819 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 3 | -0.059029 | -3.069 |
| w23 | 1 | -0.032677 | -0.606 |
| w24 | 33 | 0.201699 | 19.232 |
| w25 | 36 | -0.008012 | -6.373 |
| w26 | 15 | -0.02524 | -3.362 |
| w27 | 26 | -0.012594 | -5.565 |
| w28 | 13 | -0.053801 | -4.434 |
| w29 | 8 | 0.002935 | -0.627 |
| w30 | 10 | -0.048427 | -4.913 |
| w31 | 23 | 0.059045 | 4.131 |
| w32 | 10 | 0.103043 | 5.454 |

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
| w27 | 37 | 0.023959 | -5.587 |
| w28 | 17 | -0.01535 | -2.207 |
| w29 | 12 | 0.052627 | 3.674 |
| w30 | 25 | -0.053404 | -8.457 |
| w31 | 13 | 0.190676 | 15.185 |
| w32 | 23 | 0.016481 | 0.654 |

- FILUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 4 | -0.043739 | -2.922 |
| w19 | 29 | 0.122512 | 11.83 |
| w20 | 27 | 0.08338 | 6.191 |
| w21 | 12 | 0.211095 | 16.071 |
| w22 | 21 | 0.046434 | 2.348 |
| w23 | 4 | 0.090123 | 3.746 |
| w24 | 50 | 0.135913 | 10.042 |
| w25 | 34 | 0.172644 | 24.237 |
| w26 | 10 | 0.054983 | 2.453 |
| w27 | 39 | -0.109563 | -27.269 |
| w28 | 1 | -0.03667 | -1.737 |
| w29 | 11 | 0.059603 | 2.869 |
| w30 | 27 | -0.276598 | -50.472 |
| w31 | 5 | 0.104881 | 2.984 |
| w32 | 15 | 0.017199 | -0.926 |

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
| w18 | 10 | 0.089421 | 7.045 |
| w19 | 12 | 0.091209 | 5.602 |
| w20 | 17 | -0.100403 | -13.816 |
| w21 | 16 | 0.177008 | 13.492 |
| w22 | 11 | 0.101749 | 8.543 |
| w23 | 10 | 0.013321 | -0.839 |
| w24 | 24 | 0.135195 | 3.287 |
| w25 | 27 | 0.165126 | 21.721 |
| w26 | 9 | -0.07967 | -3.806 |
| w27 | 36 | -0.009366 | -6.24 |
| w28 | 8 | -0.057834 | -4.479 |
| w29 | 5 | 0.10817 | 5.873 |
| w30 | 26 | -0.012369 | -7.659 |
| w31 | 5 | 0.069307 | 2.735 |
| w32 | 27 | 0.092431 | 6.034 |

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
| w28 | 44 | -0.01317 | -2.545 |
| w29 | 2 | 0.083125 | 3.885 |
| w30 | 17 | -0.128755 | -16.605 |
| w31 | 21 | -0.054323 | -9.002 |
| w32 | 5 | -0.100007 | -4.197 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 13 | -0.235366 | -55.809 |
| w15 | 20 | 0.135623 | 10.193 |
| w16 | 28 | -0.013946 | -47.413 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | 0.051031 | 1.765 |
| w19 | 8 | 0.198983 | 15.413 |
| w20 | 24 | 0.233596 | 20.389 |
| w21 | 19 | 0.024121 | 1.109 |
| w22 | 17 | -0.014347 | -0.623 |
| w23 | 3 | 0.072443 | 1.634 |
| w24 | 30 | 0.06597 | 4.901 |
| w25 | 35 | 0.09037 | 6.772 |
| w26 | 8 | -0.014338 | -2.382 |
| w27 | 25 | -0.410382 | -51.014 |
| w28 | 14 | -0.001876 | -1.073 |
| w29 | 11 | 0.079257 | 7.055 |
| w30 | 8 | -0.086183 | -5.033 |
| w31 | 14 | 0.184582 | 17.905 |
| w32 | 16 | -0.022623 | -4.419 |

- PEPEUSD: 7 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 5 | -0.035721 | -2.385 |
| w27 | 16 | 0.048224 | 2.36 |
| w28 | 14 | -0.038505 | -5.372 |
| w29 | 5 | 0.129709 | 7.855 |
| w30 | 13 | -0.030522 | -3.433 |
| w31 | 14 | 0.091597 | 6.241 |
| w32 | 15 | -0.161895 | -24.506 |

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

