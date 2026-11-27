# Backtest of 031-01.g1.d2_wide-low-close-in-volatile-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.g1.d2_wide-low-close-in-volatile-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.183602 | 11.865 |
| w2 | 2 | 0.106044 | 7.662 |
| w3 | 1 | 0.0816 | 3.9 |
| w4 | 3 | 0.030167 | 3.802 |
| w5 | 2 | -0.018504 | 0.409 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | 0.051334 | 1.766 |
| w9 | 2 | -0.051617 | -7.77 |
| w10 | 3 | 0.073218 | 5.048 |
| w11 | 1 | -0.043451 | -1.325 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | 0.137308 | 9.182 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.087614 | 7.164 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.045643 | 2.187 |
| w18 | 2 | -0.064344 | -4.135 |
| w19 | 2 | -0.007352 | -1.164 |
| w20 | 3 | 0.070526 | 4.537 |
| w21 | 5 | 0.299194 | 26.988 |
| w22 | 2 | 0.065073 | 5.733 |
| w23 | 3 | 0.246759 | 14.046 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | 0.028278 | -0.955 |
| w26 | 1 | -0.040774 | -2.179 |
| w27 | 2 | 0.058809 | 4.546 |
| w28 | 1 | 0.041714 | 1.798 |
| w29 | 1 | -0.04916 | -1.717 |
| w30 | 2 | 0.007867 | -0.116 |
| w31 | 2 | 0.274086 | 17.104 |
| w32 | 3 | -0.076413 | -6.983 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.143159 | -7.973 |
| w2 | 2 | -0.038763 | -3.312 |
| w3 | 1 | -0.028892 | -1.856 |
| w4 | 5 | 0.010869 | 5.284 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.095899 | 8.528 |
| w7 | 1 | -0.019202 | -0.802 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | 0.022208 | -2.036 |
| w10 | 2 | -0.030089 | -0.743 |
| w11 | 1 | 0.067587 | 2.743 |
| w12 | 1 | 0.124235 | 4.587 |
| w13 | 4 | 0.162714 | 11.956 |
| w14 | 2 | 0.198566 | 14.886 |
| w15 | 3 | 0.159669 | 13.878 |
| w16 | 1 | -0.154593 | -6.849 |
| w17 | 1 | 0.048233 | 2.282 |
| w18 | 4 | 0.097102 | 8.099 |
| w19 | 2 | 0.049648 | 1.637 |
| w20 | 4 | 0.054833 | 3.317 |
| w21 | 4 | 0.122137 | 4.785 |
| w22 | 2 | 0.075215 | 4.783 |
| w23 | 1 | 0.016485 | 0.542 |
| w24 | 2 | 0.101408 | 6.39 |
| w25 | 2 | 0.109384 | 5.955 |
| w26 | 3 | -0.27254 | -24.433 |
| w27 | 3 | -0.100066 | -5.562 |
| w28 | 2 | -0.038137 | -2.476 |
| w29 | 3 | 0.025451 | 1.646 |
| w30 | 1 | -0.051334 | -2.39 |
| w31 | 1 | 0.288004 | 10.92 |
| w32 | 3 | 0.043987 | 2.585 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 2 | 0.007 | 1.597 |
| w7 | 1 | 0.079674 | 4.024 |
| w8 | 2 | 0.063185 | 3.176 |
| w9 | 4 | 0.222825 | 25.747 |
| w10 | 3 | 0.148105 | 10.487 |
| w11 | 1 | 0.089444 | 3.19 |
| w12 | 1 | 0.199959 | 9.78 |
| w13 | 3 | 0.136925 | 8.191 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.255141 | 15.133 |
| w16 | 2 | 0.075022 | 7.472 |
| w17 | 2 | 0.055302 | 1.509 |
| w18 | 1 | 0.046738 | 1.245 |
| w19 | 3 | 0.173731 | 11.103 |
| w20 | 1 | 0.131727 | 4.285 |
| w21 | 4 | 0.489467 | 60.066 |
| w22 | 3 | 0.108103 | 9.566 |
| w23 | 1 | -0.098886 | -11.382 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | 0.021266 | 1.536 |
| w27 | 2 | -0.112209 | -4.603 |
| w28 | 1 | 0.045154 | 1.642 |
| w29 | 1 | -0.00014 | 0.198 |
| w30 | 2 | 0.012482 | -0.731 |
| w31 | 3 | 0.285622 | 18.766 |
| w32 | 1 | -0.027478 | -1.842 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 1 | 0.043374 | 0.985 |
| w9 | 5 | -0.059334 | -12.317 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.077548 | 3.051 |
| w13 | 3 | 0.146471 | 9.418 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.010468 | -3.012 |
| w16 | 2 | 0.015143 | 1.926 |
| w17 | 1 | 0.017824 | 0.583 |
| w18 | 3 | -0.032793 | -4.193 |
| w19 | 3 | 0.102031 | 5.209 |
| w20 | 5 | 0.124337 | 9.535 |
| w21 | 3 | 0.121819 | 3.797 |
| w22 | 2 | -0.014191 | -1.75 |
| w23 | 2 | 0.535431 | 47.04 |
| w24 | 2 | -0.057787 | -3.696 |
| w25 | 2 | -0.025573 | -2.482 |
| w26 | 1 | -0.039621 | -2.428 |
| w27 | 4 | -0.009576 | 0.194 |
| w28 | 3 | 0.033013 | 1.708 |
| w29 | 1 | 0.018811 | 1.047 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.272113 | 14.756 |
| w32 | 4 | 0.070582 | 4.252 |

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
| w1 | 2 | 0.029019 | 4.308 |
| w2 | 3 | -0.050989 | -6.617 |
| w3 | 2 | 0.259862 | 16.458 |
| w4 | 2 | 0.280192 | 23.041 |
| w5 | 2 | 0.071115 | 4.056 |
| w6 | 2 | 0.00292 | 1.559 |
| w7 | 1 | 0.108069 | 5.4 |
| w8 | 1 | 0.063047 | 1.839 |
| w9 | 3 | 0.117481 | 5.13 |
| w10 | 2 | 0.053256 | 2.61 |
| w11 | 3 | 0.03968 | 2.773 |
| w12 | 1 | 0.056854 | 1.935 |
| w13 | 5 | 0.130132 | 12.572 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | 0.009093 | 0.76 |
| w16 | 1 | 0.152187 | 6.688 |
| w17 | 1 | -0.055766 | -3.026 |
| w18 | 2 | -0.089774 | -5.137 |
| w19 | 2 | -0.162311 | -9.612 |
| w20 | 5 | -0.030976 | -5.951 |
| w21 | 1 | 0.401754 | 15.456 |
| w22 | 3 | 0.031506 | 3.624 |
| w23 | 4 | 0.024071 | 1.386 |
| w24 | 2 | 0.056154 | 5.028 |
| w25 | 2 | 0.228278 | 16.148 |
| w26 | 3 | -0.146297 | -16.394 |
| w27 | 3 | -0.018367 | -1.078 |
| w28 | 4 | 0.08847 | 4.858 |
| w29 | 1 | 0.095428 | 5.104 |
| w30 | 1 | -0.096317 | -4.046 |
| w31 | 4 | 0.25201 | 23.044 |
| w32 | 1 | -0.030986 | -1.389 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 3 | 0.106681 | 6.84 |
| w11 | 1 | 0.11075 | 4.045 |
| w12 | 1 | 0.099583 | 3.424 |
| w13 | 3 | 0.174953 | 13.355 |
| w14 | 4 | 0.199104 | 18.951 |
| w15 | 3 | 0.099552 | 8.514 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.265705 | 22.586 |
| w18 | 2 | -0.175691 | -13.02 |
| w19 | 2 | -0.19711 | -14.01 |
| w20 | 5 | 0.050434 | 3.537 |
| w21 | 5 | 0.346373 | 31.105 |
| w22 | 1 | -0.039373 | -1.34 |
| w23 | 3 | -0.09744 | -10.506 |
| w24 | 2 | -0.03963 | -1.725 |
| w25 | 0 | None | 0.0 |
| w26 | 1 | -0.089325 | -4.958 |
| w27 | 2 | 0.016415 | 1.975 |
| w28 | 1 | 0.106381 | 3.501 |
| w29 | 3 | 0.071486 | 5.425 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | 0.294216 | 11.127 |
| w32 | 3 | -0.145387 | -15.831 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 1 | 0.177741 | 6.696 |
| w14 | 4 | 0.284337 | 32.872 |
| w15 | 1 | 0.170795 | 5.34 |
| w16 | 1 | 0.118449 | 6.42 |
| w17 | 1 | 0.027851 | 1.473 |
| w18 | 2 | -0.094657 | -5.589 |
| w19 | 1 | -0.104547 | -4.051 |
| w20 | 3 | 0.068953 | 5.321 |
| w21 | 2 | 0.304979 | 17.15 |
| w22 | 2 | 0.033431 | 1.639 |
| w23 | 1 | 0.019215 | -0.072 |
| w24 | 3 | -0.016867 | -2.122 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.065369 | -6.414 |
| w27 | 3 | 0.110656 | 9.015 |
| w28 | 3 | 0.098267 | 5.322 |
| w29 | 3 | -0.010501 | -1.664 |
| w30 | 3 | -0.067189 | -6.184 |
| w31 | 2 | 0.271982 | 14.484 |
| w32 | 0 | None | 0.0 |

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
| w15 | 2 | -0.039598 | -6.659 |
| w16 | 1 | -0.109767 | -3.541 |
| w17 | 2 | 0.081537 | 5.829 |
| w18 | 1 | 0.08637 | 5.821 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | 0.066815 | 4.691 |
| w21 | 5 | 0.337406 | 38.796 |
| w22 | 4 | 0.06185 | 4.634 |
| w23 | 1 | -0.027814 | -2.328 |
| w24 | 3 | 0.038041 | 3.011 |
| w25 | 1 | 0.061192 | 2.684 |
| w26 | 2 | 0.091677 | 4.167 |
| w27 | 2 | 0.096659 | 10.29 |
| w28 | 1 | 0.00811 | -0.019 |
| w29 | 4 | 0.053777 | 4.253 |
| w30 | 1 | 0.097004 | 3.557 |
| w31 | 2 | 0.148328 | 8.086 |
| w32 | 2 | 0.058696 | 2.771 |

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
| w15 | 1 | 0.062015 | 2.966 |
| w16 | 1 | 0.076635 | 3.948 |
| w17 | 1 | 0.038112 | 1.064 |
| w18 | 2 | 0.06109 | 3.568 |
| w19 | 5 | 0.117672 | 10.086 |
| w20 | 3 | 0.366539 | 26.465 |
| w21 | 3 | 0.207875 | 15.063 |
| w22 | 7 | 0.136999 | 13.491 |
| w23 | 3 | -0.112767 | -7.935 |
| w24 | 2 | 0.23244 | 13.976 |
| w25 | 2 | 0.120832 | 8.474 |
| w26 | 4 | -0.011857 | -0.946 |
| w27 | 3 | 0.008566 | 12.274 |
| w28 | 0 | None | 0.0 |
| w29 | 3 | -0.049814 | -2.763 |
| w30 | 1 | 0.097334 | 2.886 |
| w31 | 4 | -0.057712 | -3.963 |
| w32 | 4 | -0.045212 | -3.525 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | 0.094573 | 8.662 |
| w18 | 1 | -0.098078 | -4.21 |
| w19 | 3 | -0.044261 | -3.116 |
| w20 | 3 | 0.072918 | 3.795 |
| w21 | 1 | 0.280256 | 10.385 |
| w22 | 3 | 0.060631 | 5.237 |
| w23 | 1 | None | -0.429 |
| w24 | 1 | -0.085052 | -4.57 |
| w25 | 0 | None | 0.0 |
| w26 | 1 | -0.10538 | -8.176 |
| w27 | 5 | 0.092406 | 11.452 |
| w28 | 1 | -0.060486 | -2.696 |
| w29 | 4 | -0.010319 | -3.309 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.115886 | 6.909 |
| w32 | 3 | 0.08788 | 3.852 |

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
| w20 | 3 | 0.028395 | 0.87 |
| w21 | 1 | 0.411488 | 16.762 |
| w22 | 3 | 0.057652 | 5.427 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.004653 | 1.481 |
| w25 | 1 | 0.162874 | 7.601 |
| w26 | 2 | -0.101456 | -6.88 |
| w27 | 2 | 0.106028 | 8.223 |
| w28 | 1 | -0.072242 | -3.47 |
| w29 | 3 | -0.06994 | -6.472 |
| w30 | 1 | 0.038431 | 1.247 |
| w31 | 2 | 0.191946 | 9.734 |
| w32 | 3 | 0.001022 | -1.69 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.074375 | 7.321 |
| w23 | 1 | 0.004634 | -0.333 |
| w24 | 3 | 0.067791 | 8.252 |
| w25 | 3 | -0.008191 | -1.121 |
| w26 | 1 | -0.06968 | -3.111 |
| w27 | 1 | -0.081096 | -3.163 |
| w28 | 2 | -0.026246 | -2.604 |
| w29 | 2 | 0.047178 | 2.841 |
| w30 | 2 | -0.073433 | -3.881 |
| w31 | 1 | 0.235 | 10.822 |
| w32 | 4 | -0.173436 | -13.435 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 2 | 0.048749 | 3.371 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.068534 | -5.274 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.009901 | 0.753 |
| w29 | 2 | -0.0155 | -0.982 |
| w30 | 1 | 0.067765 | 1.824 |
| w31 | 1 | 0.323568 | 12.637 |
| w32 | 2 | 0.097059 | 7.147 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 1 | -0.076465 | -2.666 |
| w6 | 3 | 0.041051 | 3.665 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.19743 | 10.539 |
| w9 | 3 | -0.087582 | -11.31 |
| w10 | 2 | -0.121266 | -7.231 |
| w11 | 3 | 0.242836 | 18.574 |
| w12 | 3 | 0.027081 | -0.212 |
| w13 | 2 | 0.057673 | 3.464 |
| w14 | 3 | 0.117674 | 9.23 |
| w15 | 2 | -0.058687 | -4.824 |
| w16 | 2 | -0.003799 | 1.2 |
| w17 | 3 | 0.121256 | 12.753 |
| w18 | 3 | -0.000364 | -0.596 |
| w19 | 3 | -0.001279 | -0.867 |
| w20 | 1 | 0.013454 | 0.191 |
| w21 | 3 | 0.261238 | 17.581 |
| w22 | 1 | 0.047205 | 1.839 |
| w23 | 1 | -0.106245 | -4.461 |
| w24 | 3 | 0.111855 | 9.319 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.023631 | -0.796 |
| w27 | 2 | 0.040613 | 2.953 |
| w28 | 2 | -0.055191 | -3.803 |
| w29 | 2 | 0.072262 | 3.85 |
| w30 | 4 | 0.23446 | 28.73 |
| w31 | 1 | -0.07382 | -3.051 |
| w32 | 3 | -0.032781 | 0.179 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 1 | -0.12366 | -6.902 |
| w6 | 3 | 0.135496 | 10.206 |
| w7 | 1 | 0.057144 | 2.525 |
| w8 | 3 | 0.162196 | 10.739 |
| w9 | 4 | 0.020393 | -2.957 |
| w10 | 2 | 0.002932 | 0.246 |
| w11 | 3 | -0.01936 | -2.09 |
| w12 | 3 | 0.002683 | -2.099 |
| w13 | 5 | 0.069378 | 5.04 |
| w14 | 1 | 0.055143 | 2.739 |
| w15 | 2 | 0.129065 | 8.786 |
| w16 | 2 | 0.002548 | 3.068 |
| w17 | 2 | 0.358055 | 21.798 |
| w18 | 1 | -0.131003 | -5.773 |
| w19 | 2 | -0.073474 | -4.345 |
| w20 | 1 | -0.094895 | -4.626 |
| w21 | 5 | 0.254093 | 20.667 |
| w22 | 3 | 0.094707 | 6.696 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.006298 | 0.201 |
| w25 | 5 | 0.297148 | 31.977 |
| w26 | 3 | 0.068644 | 4.651 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.108558 | -7.548 |
| w30 | 1 | -0.133159 | -5.199 |
| w31 | 4 | 0.028649 | 0.44 |
| w32 | 4 | 0.010003 | 4.777 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | 0.084903 | 4.082 |
| w18 | 5 | -0.097068 | -7.201 |
| w19 | 2 | 0.048323 | 2.074 |
| w20 | 3 | -0.059427 | -5.883 |
| w21 | 1 | -0.035125 | -8.418 |
| w22 | 1 | -0.031023 | -1.006 |
| w23 | 4 | 0.172106 | 12.16 |
| w24 | 2 | -0.041525 | -2.499 |
| w25 | 1 | 0.347086 | 16.196 |
| w26 | 1 | -0.04507 | -1.994 |
| w27 | 1 | -0.011759 | 0.113 |
| w28 | 4 | 0.107037 | 7.838 |
| w29 | 4 | -0.024121 | -2.757 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | 0.287157 | 10.746 |
| w32 | 4 | -0.041837 | -4.691 |

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
| w17 | 2 | 0.110633 | 6.93 |
| w18 | 2 | -0.066257 | -4.661 |
| w19 | 1 | 0.260725 | 10.635 |
| w20 | 2 | -0.022924 | -1.528 |
| w21 | 2 | 0.258451 | 13.715 |
| w22 | 2 | 0.138721 | 9.379 |
| w23 | 2 | 0.160694 | 8.751 |
| w24 | 4 | 0.041671 | 8.218 |
| w25 | 1 | -0.010453 | -0.691 |
| w26 | 2 | -0.076233 | -6.0 |
| w27 | 2 | 0.164329 | 13.921 |
| w28 | 2 | 0.252888 | 13.701 |
| w29 | 2 | 0.002847 | 0.346 |
| w30 | 1 | -0.105933 | -5.216 |
| w31 | 2 | 0.044895 | 0.636 |
| w32 | 1 | -0.065321 | -3.085 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 2 | -0.145381 | -9.579 |
| w20 | 3 | -0.113486 | -10.338 |
| w21 | 3 | 0.040108 | -0.956 |
| w22 | 1 | 0.022911 | 2.244 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.022928 | 0.049 |
| w25 | 1 | 0.083901 | 3.497 |
| w26 | 2 | -0.118614 | -7.779 |
| w27 | 1 | 0.092525 | 4.283 |
| w28 | 3 | 0.016779 | -0.535 |
| w29 | 4 | -0.0474 | -4.664 |
| w30 | 1 | 0.043805 | 1.028 |
| w31 | 3 | 0.105651 | 5.065 |
| w32 | 2 | -0.063287 | -3.648 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.080933 | 5.36 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.037758 | 7.837 |
| w25 | 2 | -0.080192 | -3.647 |
| w26 | 2 | 0.00605 | -0.692 |
| w27 | 1 | -0.011356 | -0.233 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.065953 | -4.042 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.075285 | 3.419 |
| w32 | 3 | 0.034743 | 1.464 |

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
| w27 | 2 | 0.113489 | 7.799 |
| w28 | 1 | -0.024452 | -1.25 |
| w29 | 2 | 0.065636 | 3.839 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.225521 | 11.726 |
| w32 | 4 | 0.110457 | 10.542 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 1 | 0.076531 | 2.452 |
| w18 | 1 | -0.301408 | -14.282 |
| w19 | 6 | 0.092212 | 4.675 |
| w20 | 3 | -0.058852 | -5.696 |
| w21 | 2 | 0.161 | 7.887 |
| w22 | 4 | 0.075073 | 9.265 |
| w23 | 1 | 0.003222 | -0.429 |
| w24 | 4 | -0.108931 | -10.542 |
| w25 | 1 | 0.056172 | 2.29 |
| w26 | 1 | -0.035163 | -1.76 |
| w27 | 3 | 0.087018 | 8.34 |
| w28 | 2 | -0.040821 | -3.139 |
| w29 | 3 | 0.056987 | 2.693 |
| w30 | 2 | -0.040054 | -5.267 |
| w31 | 2 | 0.193176 | 9.874 |
| w32 | 2 | -0.066846 | -4.587 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 1 | 0.004274 | -0.012 |
| w19 | 3 | 0.240727 | 15.861 |
| w20 | 2 | -0.058926 | -4.094 |
| w21 | 3 | 0.262928 | 16.806 |
| w22 | 1 | -0.04436 | -2.369 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.004798 | 1.476 |
| w25 | 1 | -0.013378 | -0.549 |
| w26 | 1 | -0.045365 | -2.337 |
| w27 | 1 | -0.07361 | -3.261 |
| w28 | 3 | 0.054117 | 1.477 |
| w29 | 4 | 0.059651 | 3.886 |
| w30 | 2 | 0.118996 | 6.085 |
| w31 | 1 | 0.413139 | 14.919 |
| w32 | 2 | 0.092883 | 4.572 |

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
| w28 | 2 | -0.157797 | -11.218 |
| w29 | 2 | 0.072788 | 4.641 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.182054 | 11.925 |
| w32 | 3 | 0.117742 | 12.611 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.089567 | 1.86 |
| w16 | 2 | 0.028047 | 2.098 |
| w17 | 1 | -0.036875 | -2.513 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.053574 | 2.652 |
| w20 | 2 | -0.081223 | -9.376 |
| w21 | 1 | 0.104278 | 4.51 |
| w22 | 3 | 0.187701 | 15.078 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.02779 | 3.564 |
| w25 | 2 | 0.162731 | 14.523 |
| w26 | 0 | None | 0.0 |
| w27 | 1 | 0.067012 | 3.147 |
| w28 | 3 | 0.073847 | 3.906 |
| w29 | 5 | -0.143583 | -13.767 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.16717 | 9.433 |
| w32 | 3 | 0.072687 | 3.565 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 2 | 0.237765 | 18.387 |
| w26 | 1 | 0.070824 | 2.731 |
| w27 | 3 | 0.045397 | 3.213 |
| w28 | 1 | -0.037447 | -1.926 |
| w29 | 3 | 0.00279 | 0.05 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.018506 | 0.449 |
| w32 | 3 | 0.02071 | 0.577 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

