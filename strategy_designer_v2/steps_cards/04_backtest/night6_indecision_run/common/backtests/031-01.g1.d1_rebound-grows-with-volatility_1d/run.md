# Backtest of 031-01.g1.d1_rebound-grows-with-volatility_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d1_rebound-grows-with-volatility_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.12825 | 6.968 |
| w2 | 2 | 0.0913 | 7.662 |
| w3 | 1 | 0.0816 | 3.9 |
| w4 | 4 | 0.052171 | 5.131 |
| w5 | 3 | -0.054197 | -1.687 |
| w6 | 3 | 0.074871 | 2.441 |
| w7 | 2 | 0.080879 | 2.609 |
| w8 | 3 | 0.09517 | 4.014 |
| w9 | 5 | -0.062019 | -9.533 |
| w10 | 5 | 0.045779 | 2.765 |
| w11 | 3 | -0.010211 | 0.112 |
| w12 | 3 | 0.039282 | 0.697 |
| w13 | 5 | 0.158706 | 9.426 |
| w14 | 2 | 0.071645 | 1.506 |
| w15 | 2 | 0.081005 | 5.353 |
| w16 | 3 | -0.032812 | -0.42 |
| w17 | 3 | 0.021559 | 0.643 |
| w18 | 3 | -0.07729 | -4.197 |
| w19 | 8 | -0.079511 | -6.607 |
| w20 | 5 | 0.061875 | 3.052 |
| w21 | 7 | 0.302953 | 24.916 |
| w22 | 5 | 0.07584 | 7.489 |
| w23 | 6 | 0.229366 | 9.514 |
| w24 | 1 | -0.030349 | -0.272 |
| w25 | 2 | 0.157087 | 6.465 |
| w26 | 2 | -0.046941 | -3.071 |
| w27 | 5 | 0.001633 | 1.549 |
| w28 | 6 | 0.012168 | -0.122 |
| w29 | 5 | -0.010735 | -0.69 |
| w30 | 4 | -0.040691 | -2.452 |
| w31 | 3 | 0.296208 | 18.904 |
| w32 | 5 | -0.15945 | -15.496 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.08703 | -5.529 |
| w2 | 4 | -0.031065 | -2.634 |
| w3 | 2 | -0.029922 | -2.371 |
| w4 | 5 | 0.019303 | 6.093 |
| w5 | 2 | -0.104916 | -0.435 |
| w6 | 3 | 0.097068 | 8.839 |
| w7 | 2 | 0.061427 | 2.254 |
| w8 | 4 | -0.120492 | -5.934 |
| w9 | 6 | 0.015494 | -3.199 |
| w10 | 2 | -0.007336 | 0.298 |
| w11 | 4 | 0.025328 | 0.705 |
| w12 | 2 | 0.154928 | 5.106 |
| w13 | 6 | 0.233074 | 12.577 |
| w14 | 4 | 0.197552 | 17.184 |
| w15 | 4 | 0.129398 | 8.518 |
| w16 | 3 | -0.138546 | -5.203 |
| w17 | 3 | 0.091964 | 5.971 |
| w18 | 6 | 0.109681 | 7.802 |
| w19 | 9 | -0.06642 | -5.913 |
| w20 | 8 | 0.062263 | 3.299 |
| w21 | 5 | 0.135211 | 6.16 |
| w22 | 5 | 0.010412 | 0.218 |
| w23 | 3 | 0.012719 | 0.35 |
| w24 | 3 | 0.128322 | 7.662 |
| w25 | 3 | 0.107034 | 4.484 |
| w26 | 3 | -0.302576 | -24.133 |
| w27 | 4 | -0.089286 | -3.951 |
| w28 | 6 | -0.08179 | -3.032 |
| w29 | 6 | 0.171596 | 14.15 |
| w30 | 2 | -0.036902 | -0.962 |
| w31 | 3 | 0.240198 | 8.933 |
| w32 | 4 | 0.035656 | 1.442 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 4 | -0.042534 | -2.392 |
| w7 | 2 | 0.076076 | 3.988 |
| w8 | 5 | 0.022868 | -2.023 |
| w9 | 5 | 0.229682 | 25.598 |
| w10 | 7 | 0.237446 | 16.68 |
| w11 | 3 | 0.116028 | 5.319 |
| w12 | 2 | 0.064622 | 1.182 |
| w13 | 5 | 0.215171 | 10.115 |
| w14 | 1 | 0.122727 | 1.045 |
| w15 | 3 | 0.227621 | 10.832 |
| w16 | 3 | 0.117775 | 8.045 |
| w17 | 3 | 0.008791 | -0.801 |
| w18 | 4 | 0.106671 | 4.665 |
| w19 | 7 | 0.15797 | 9.882 |
| w20 | 3 | 0.117291 | 3.829 |
| w21 | 6 | 0.4891 | 59.779 |
| w22 | 5 | 0.119278 | 10.224 |
| w23 | 1 | -0.098886 | -8.101 |
| w24 | 1 | 0.009882 | 0.198 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.050273 | -8.798 |
| w27 | 4 | -0.133402 | -6.286 |
| w28 | 5 | 0.067219 | 3.16 |
| w29 | 3 | 0.02041 | 1.314 |
| w30 | 3 | 0.04502 | 0.795 |
| w31 | 5 | 0.291658 | 16.954 |
| w32 | 2 | -0.024517 | -1.917 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 2 | 0.060173 | 0.891 |
| w9 | 6 | -0.069743 | -11.363 |
| w10 | 2 | 0.042786 | 1.226 |
| w11 | 3 | 0.078077 | 2.824 |
| w12 | 2 | 0.083297 | 2.417 |
| w13 | 7 | 0.148949 | 7.669 |
| w14 | 3 | 0.162118 | 7.86 |
| w15 | 4 | -0.020112 | -4.738 |
| w16 | 4 | 0.041577 | 4.909 |
| w17 | 2 | 0.057493 | 4.938 |
| w18 | 4 | -0.033673 | -3.742 |
| w19 | 6 | 0.019375 | -1.415 |
| w20 | 10 | 0.080309 | 2.871 |
| w21 | 8 | 0.163378 | 5.694 |
| w22 | 4 | -0.051119 | -4.112 |
| w23 | 4 | 0.491878 | 51.939 |
| w24 | 5 | -0.01787 | -1.878 |
| w25 | 4 | -0.000236 | 0.695 |
| w26 | 1 | -0.039621 | -2.428 |
| w27 | 5 | 0.053549 | 4.682 |
| w28 | 7 | 0.028252 | 0.314 |
| w29 | 2 | -0.007707 | -0.012 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.266717 | 14.171 |
| w32 | 6 | 0.057752 | 1.178 |

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
| w1 | 5 | 0.048797 | 7.804 |
| w2 | 5 | -0.055327 | -6.458 |
| w3 | 3 | 0.250703 | 16.442 |
| w4 | 2 | 0.294472 | 21.793 |
| w5 | 2 | 0.133781 | 5.281 |
| w6 | 4 | 0.103623 | 7.93 |
| w7 | 3 | 0.111229 | 5.384 |
| w8 | 6 | 0.001223 | -2.525 |
| w9 | 5 | 0.147504 | 8.146 |
| w10 | 2 | 0.046012 | 1.386 |
| w11 | 5 | 0.055838 | 3.002 |
| w12 | 5 | -0.083347 | -5.966 |
| w13 | 7 | 0.170156 | 13.02 |
| w14 | 2 | 0.02569 | 1.059 |
| w15 | 2 | 0.040679 | 2.817 |
| w16 | 3 | 0.163755 | 8.647 |
| w17 | 3 | -0.04956 | -2.728 |
| w18 | 6 | -0.017997 | -1.162 |
| w19 | 6 | -0.09152 | -4.763 |
| w20 | 8 | -0.030314 | -5.889 |
| w21 | 6 | 0.359014 | 20.068 |
| w22 | 6 | 0.005784 | 1.653 |
| w23 | 4 | 0.03409 | 1.231 |
| w24 | 2 | 0.042179 | 4.46 |
| w25 | 3 | 0.286871 | 17.303 |
| w26 | 5 | -0.179751 | -15.822 |
| w27 | 4 | -0.054524 | -2.549 |
| w28 | 8 | 0.139975 | 7.67 |
| w29 | 4 | 0.013678 | 1.847 |
| w30 | 4 | -0.092672 | -3.694 |
| w31 | 4 | 0.280232 | 21.352 |
| w32 | 2 | -0.075327 | -4.867 |

- ADAUSD: 22 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 5 | 0.182023 | 8.725 |
| w12 | 4 | 0.180452 | 8.663 |
| w13 | 5 | 0.204054 | 13.798 |
| w14 | 4 | 0.199685 | 14.703 |
| w15 | 5 | 0.120223 | 9.836 |
| w16 | 1 | 0.035285 | 0.579 |
| w17 | 4 | 0.260688 | 22.628 |
| w18 | 3 | -0.165891 | -12.066 |
| w19 | 6 | -0.104841 | -5.375 |
| w20 | 8 | 0.025433 | 0.144 |
| w21 | 10 | 0.369925 | 30.337 |
| w22 | 4 | -0.082365 | -2.811 |
| w23 | 4 | -0.084998 | -10.399 |
| w24 | 3 | -0.038972 | -1.417 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.075796 | -5.127 |
| w27 | 3 | -0.028432 | -1.45 |
| w28 | 4 | 0.085518 | 3.072 |
| w29 | 4 | 0.109163 | 6.821 |
| w30 | 1 | 0.002559 | -0.175 |
| w31 | 3 | 0.171828 | 4.607 |
| w32 | 6 | -0.265172 | -27.389 |

- w10 not run: the engine stopped.

```
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^
  File "/home/user/trading-bot/trading-bot/core/backtester.py", line 368, in simulate_on_loaded_data
    raise AssertionError(bot.warmup_not_ready)
AssertionError: warmup_prefetch: strategy not ready after 95 warm-up bars -- required_bars=100. 2x-required_bars was insufficient for this config; investigate before proceeding.
```

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 4 | 0.209181 | 11.183 |
| w14 | 6 | 0.262748 | 33.017 |
| w15 | 5 | 0.173091 | 9.066 |
| w16 | 2 | 0.124096 | 6.844 |
| w17 | 4 | 0.006635 | 0.538 |
| w18 | 3 | -0.09385 | -5.233 |
| w19 | 5 | -0.000241 | -0.353 |
| w20 | 4 | 0.057966 | 3.685 |
| w21 | 4 | 0.317526 | 17.586 |
| w22 | 4 | 0.033754 | 1.577 |
| w23 | 4 | 0.064668 | 0.793 |
| w24 | 5 | -0.027143 | -2.785 |
| w25 | 2 | 0.095708 | 1.671 |
| w26 | 3 | -0.127849 | -8.612 |
| w27 | 4 | 0.138226 | 8.268 |
| w28 | 7 | 0.163284 | 7.314 |
| w29 | 5 | 0.046607 | 2.198 |
| w30 | 4 | -0.04288 | -3.633 |
| w31 | 3 | 0.235708 | 11.184 |
| w32 | 3 | 0.018924 | -0.213 |

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
| w15 | 3 | -0.08838 | -7.561 |
| w16 | 4 | -0.092786 | -2.74 |
| w17 | 6 | 0.113511 | 8.716 |
| w18 | 3 | 0.095058 | 6.105 |
| w19 | 3 | -0.05829 | -4.738 |
| w20 | 8 | 0.081029 | 5.222 |
| w21 | 8 | 0.353418 | 34.537 |
| w22 | 7 | 0.050406 | 2.638 |
| w23 | 1 | -0.026699 | -1.744 |
| w24 | 4 | 0.060331 | 4.832 |
| w25 | 2 | 0.108524 | 5.495 |
| w26 | 2 | 0.102527 | 4.413 |
| w27 | 3 | 0.078759 | 8.62 |
| w28 | 6 | 0.087151 | 2.925 |
| w29 | 6 | 0.021519 | 1.088 |
| w30 | 3 | 0.070079 | 0.057 |
| w31 | 3 | 0.165044 | 8.203 |
| w32 | 6 | 0.035047 | 0.541 |

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
| w15 | 2 | 0.044543 | 2.076 |
| w16 | 5 | 0.052114 | 3.364 |
| w17 | 4 | -0.044428 | -2.433 |
| w18 | 4 | 0.066134 | 3.038 |
| w19 | 11 | 0.038105 | 1.406 |
| w20 | 7 | 0.327817 | 33.015 |
| w21 | 8 | 0.197394 | 13.74 |
| w22 | 7 | 0.216209 | 18.163 |
| w23 | 4 | -0.138716 | -9.781 |
| w24 | 4 | 0.28603 | 21.509 |
| w25 | 5 | 0.184864 | 9.917 |
| w26 | 6 | 3.9e-05 | -1.021 |
| w27 | 4 | 0.009412 | 13.424 |
| w28 | 2 | 0.089251 | 2.791 |
| w29 | 4 | -0.091016 | -4.756 |
| w30 | 2 | 0.057182 | 0.504 |
| w31 | 6 | -0.015775 | -3.024 |
| w32 | 6 | -0.038778 | -3.223 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.088188 | 9.888 |
| w18 | 3 | -0.068672 | -3.548 |
| w19 | 6 | 0.055807 | 1.692 |
| w20 | 4 | 0.057668 | 2.1 |
| w21 | 6 | 0.272458 | 12.254 |
| w22 | 5 | 0.054537 | 3.369 |
| w23 | 1 | None | -0.247 |
| w24 | 1 | -0.085052 | -3.327 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.104373 | -7.054 |
| w27 | 7 | 0.074609 | 7.802 |
| w28 | 7 | 0.010129 | -1.136 |
| w29 | 6 | 0.055715 | 2.485 |
| w30 | 2 | -0.005869 | -0.425 |
| w31 | 2 | 0.083853 | 4.203 |
| w32 | 5 | 0.132932 | 6.663 |

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
| w20 | 5 | 0.037113 | 1.263 |
| w21 | 5 | 0.370289 | 20.994 |
| w22 | 8 | 0.068535 | 6.127 |
| w23 | 1 | 0.0606 | 0.775 |
| w24 | 4 | 0.011438 | 1.918 |
| w25 | 1 | 0.162874 | 7.601 |
| w26 | 2 | -0.105695 | -5.73 |
| w27 | 3 | 0.091084 | 7.506 |
| w28 | 6 | -0.034609 | -2.995 |
| w29 | 5 | -0.037432 | -3.348 |
| w30 | 4 | 0.013565 | -0.471 |
| w31 | 5 | 0.210641 | 9.273 |
| w32 | 5 | 0.006332 | -1.561 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | 0.085529 | 5.056 |
| w23 | 2 | 0.024441 | 0.244 |
| w24 | 4 | 0.038263 | 4.532 |
| w25 | 4 | -0.000963 | -0.342 |
| w26 | 3 | -0.061673 | -2.811 |
| w27 | 2 | -0.052763 | -1.365 |
| w28 | 6 | -0.076168 | -5.567 |
| w29 | 3 | 0.073799 | 4.337 |
| w30 | 6 | -0.065313 | -3.533 |
| w31 | 2 | 0.152784 | 7.048 |
| w32 | 5 | -0.1788 | -13.636 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 4 | -0.023635 | -0.804 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.027871 | -2.788 |
| w27 | 1 | 0.075635 | 0.803 |
| w28 | 5 | -0.029839 | -1.558 |
| w29 | 4 | 0.001408 | -0.027 |
| w30 | 5 | 0.059643 | 1.587 |
| w31 | 2 | 0.293075 | 9.015 |
| w32 | 5 | 0.115448 | 9.395 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 2 | -0.069876 | -2.278 |
| w6 | 6 | 0.068871 | 5.812 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.200074 | 10.792 |
| w9 | 7 | -0.138221 | -17.944 |
| w10 | 5 | -0.110786 | -7.405 |
| w11 | 6 | 0.206376 | 9.78 |
| w12 | 5 | 0.005962 | -1.563 |
| w13 | 5 | 0.032563 | 1.817 |
| w14 | 3 | 0.11584 | 6.381 |
| w15 | 7 | -0.001855 | -1.391 |
| w16 | 3 | 0.07144 | 5.095 |
| w17 | 7 | 0.144565 | 17.674 |
| w18 | 5 | -0.006159 | -1.107 |
| w19 | 6 | -0.036593 | -2.568 |
| w20 | 4 | 0.066554 | 1.735 |
| w21 | 6 | 0.309261 | 18.267 |
| w22 | 4 | 0.079102 | 3.014 |
| w23 | 2 | -0.117407 | -5.359 |
| w24 | 4 | 0.098597 | 7.641 |
| w25 | 2 | -0.066263 | -0.78 |
| w26 | 3 | 0.002991 | 0.76 |
| w27 | 2 | 0.044974 | 3.154 |
| w28 | 5 | -0.01832 | -2.034 |
| w29 | 3 | 0.138908 | 7.421 |
| w30 | 6 | 0.253287 | 28.002 |
| w31 | 2 | 0.140003 | 5.899 |
| w32 | 3 | -0.054089 | -1.021 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 3 | -0.099401 | -4.473 |
| w6 | 3 | 0.10026 | 7.372 |
| w7 | 2 | 0.069568 | 2.252 |
| w8 | 4 | 0.135202 | 7.783 |
| w9 | 5 | 0.020247 | -3.026 |
| w10 | 4 | 0.03037 | 1.024 |
| w11 | 5 | 0.006365 | -0.002 |
| w12 | 8 | 0.069159 | 0.888 |
| w13 | 5 | 0.108011 | 6.347 |
| w14 | 3 | 0.068756 | 4.154 |
| w15 | 6 | 0.164242 | 11.128 |
| w16 | 5 | 0.042221 | 4.797 |
| w17 | 4 | 0.322308 | 23.439 |
| w18 | 4 | -0.092951 | -5.678 |
| w19 | 5 | -0.060023 | -3.633 |
| w20 | 4 | -0.067325 | -2.962 |
| w21 | 7 | 0.227784 | 17.931 |
| w22 | 6 | 0.073285 | 4.37 |
| w23 | 1 | 0.019445 | 0.218 |
| w24 | 2 | 0.04615 | 1.589 |
| w25 | 5 | 0.320901 | 29.995 |
| w26 | 7 | 0.159596 | 10.751 |
| w27 | 4 | 0.133695 | 6.581 |
| w28 | 7 | 0.126983 | 5.051 |
| w29 | 4 | -0.089825 | -6.732 |
| w30 | 2 | -0.073166 | -2.05 |
| w31 | 6 | 0.03857 | 2.178 |
| w32 | 6 | 0.022887 | 6.745 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.08674 | 4.079 |
| w18 | 6 | -0.029427 | -0.718 |
| w19 | 4 | 0.101807 | 4.177 |
| w20 | 4 | -0.06938 | -6.284 |
| w21 | 5 | 0.03213 | -5.725 |
| w22 | 3 | -0.024282 | -1.015 |
| w23 | 5 | 0.205945 | 12.904 |
| w24 | 2 | -0.040627 | -2.071 |
| w25 | 3 | 0.372411 | 19.073 |
| w26 | 3 | -0.126766 | -5.524 |
| w27 | 2 | -0.044907 | -1.274 |
| w28 | 9 | 0.058082 | 2.456 |
| w29 | 4 | -0.017773 | -1.817 |
| w30 | 1 | -0.034102 | -0.344 |
| w31 | 3 | 0.201422 | 7.424 |
| w32 | 4 | -0.055307 | -5.771 |

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
| w17 | 4 | 0.09981 | 6.504 |
| w18 | 4 | -0.037711 | -2.51 |
| w19 | 6 | 0.191955 | 7.877 |
| w20 | 6 | -0.024225 | -1.527 |
| w21 | 8 | 0.303475 | 19.192 |
| w22 | 4 | 0.099872 | 6.115 |
| w23 | 4 | 0.14438 | 7.246 |
| w24 | 5 | 0.042347 | 7.033 |
| w25 | 4 | -0.101906 | -4.157 |
| w26 | 3 | -0.077494 | -4.014 |
| w27 | 4 | 0.131911 | 11.0 |
| w28 | 5 | 0.235402 | 9.807 |
| w29 | 2 | 0.010429 | 0.823 |
| w30 | 2 | -0.062551 | -2.562 |
| w31 | 4 | 0.037459 | -0.646 |
| w32 | 6 | -0.083573 | -5.071 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | -0.163043 | -11.143 |
| w20 | 5 | -0.149567 | -12.591 |
| w21 | 7 | 0.125952 | 5.389 |
| w22 | 5 | 0.000193 | 1.55 |
| w23 | 3 | 0.037109 | 0.979 |
| w24 | 5 | -0.029461 | -0.635 |
| w25 | 2 | 0.136199 | 6.186 |
| w26 | 3 | -0.085323 | -4.918 |
| w27 | 2 | 0.050535 | 2.711 |
| w28 | 5 | 0.004031 | -1.223 |
| w29 | 6 | -0.058261 | -4.434 |
| w30 | 5 | 0.04416 | 0.172 |
| w31 | 3 | 0.113879 | 3.939 |
| w32 | 2 | -0.064232 | -3.643 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.07083 | 4.014 |
| w23 | 2 | 0.203023 | 4.486 |
| w24 | 5 | 0.02257 | 5.593 |
| w25 | 3 | -0.076706 | -2.766 |
| w26 | 3 | 0.053422 | 1.539 |
| w27 | 2 | -0.073287 | -3.539 |
| w28 | 5 | -0.04751 | -2.351 |
| w29 | 5 | 0.009648 | 0.89 |
| w30 | 5 | 0.033006 | 0.276 |
| w31 | 5 | 0.071785 | 3.044 |
| w32 | 4 | 0.056166 | 2.411 |

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
| w27 | 3 | 0.057703 | 3.183 |
| w28 | 6 | 0.016389 | 0.18 |
| w29 | 4 | 0.063308 | 3.158 |
| w30 | 1 | -0.058212 | -1.232 |
| w31 | 3 | 0.217528 | 8.504 |
| w32 | 6 | 0.111594 | 10.703 |

- FILUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 3 | -0.255956 | -15.466 |
| w19 | 6 | 0.105479 | 5.36 |
| w20 | 4 | -0.074421 | -5.84 |
| w21 | 5 | 0.183322 | 8.9 |
| w22 | 4 | 0.061024 | 6.226 |
| w23 | 1 | 0.003222 | -0.429 |
| w24 | 4 | -0.116186 | -8.924 |
| w25 | 1 | 0.056172 | 1.559 |
| w26 | 1 | -0.035163 | -0.774 |
| w27 | 4 | 0.054974 | 5.369 |
| w28 | 8 | -0.003861 | -1.926 |
| w29 | 5 | 0.06263 | 2.233 |
| w30 | 3 | -0.017992 | -1.581 |
| w31 | 4 | 0.183834 | 8.501 |
| w32 | 6 | 0.004067 | -1.196 |

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
| w18 | 5 | 0.227173 | 10.158 |
| w19 | 8 | 0.215376 | 10.403 |
| w20 | 5 | -0.042621 | -3.176 |
| w21 | 4 | 0.290069 | 16.821 |
| w22 | 5 | -0.036413 | -1.197 |
| w23 | 2 | 0.027889 | 0.216 |
| w24 | 4 | -0.001078 | 1.89 |
| w25 | 3 | -0.005919 | -0.336 |
| w26 | 3 | -0.081053 | -4.148 |
| w27 | 1 | -0.07361 | -1.822 |
| w28 | 7 | 0.008861 | -2.096 |
| w29 | 7 | 0.101276 | 6.76 |
| w30 | 5 | 0.13826 | 4.994 |
| w31 | 2 | 0.352059 | 11.637 |
| w32 | 3 | 0.091041 | 3.928 |

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
| w28 | 4 | -0.091372 | -5.678 |
| w29 | 4 | 0.149663 | 8.411 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.090762 | 5.936 |
| w32 | 6 | 0.136206 | 12.657 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 2 | 0.0309 | 1.924 |
| w15 | 6 | 0.045404 | 0.241 |
| w16 | 2 | 0.028016 | 2.098 |
| w17 | 5 | 0.0156 | 1.453 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.075187 | 4.603 |
| w20 | 9 | -0.026409 | -5.46 |
| w21 | 6 | 0.085087 | 5.093 |
| w22 | 6 | 0.157087 | 11.623 |
| w23 | 1 | -0.278682 | -3.415 |
| w24 | 3 | 0.044262 | 3.476 |
| w25 | 2 | 0.230064 | 16.49 |
| w26 | 2 | -0.021859 | -1.129 |
| w27 | 3 | 0.010096 | 0.232 |
| w28 | 7 | 0.046302 | 1.187 |
| w29 | 7 | -0.117764 | -9.563 |
| w30 | 1 | -0.06556 | -0.679 |
| w31 | 3 | 0.158428 | 8.455 |
| w32 | 4 | 0.077601 | 4.007 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.228326 | 23.097 |
| w26 | 1 | 0.070824 | 1.342 |
| w27 | 4 | 0.011039 | 0.726 |
| w28 | 4 | -0.064428 | -4.59 |
| w29 | 5 | 0.034961 | 2.612 |
| w30 | 3 | 0.191154 | 3.742 |
| w31 | 4 | 0.088566 | 4.054 |
| w32 | 5 | 0.028569 | 0.821 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

