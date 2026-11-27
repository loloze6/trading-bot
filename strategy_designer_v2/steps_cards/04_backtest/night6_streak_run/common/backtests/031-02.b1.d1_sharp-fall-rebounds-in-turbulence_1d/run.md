# Backtest of 031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d

- Plan: `../../../../../03_test_plan/night6_streak_run/plans/031-02.b1.d1_sharp-fall-rebounds-in-turbulence_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.225151 | 17.477 |
| w2 | 30 | -0.018933 | 12.745 |
| w3 | 22 | -0.032778 | 22.386 |
| w4 | 17 | -0.092636 | -29.713 |
| w5 | 31 | 0.12163 | 30.712 |
| w6 | 28 | -0.061409 | 11.759 |
| w7 | 21 | 0.176607 | 16.507 |
| w8 | 24 | 0.111751 | 9.885 |
| w9 | 32 | 0.077009 | -21.174 |
| w10 | 12 | 0.130792 | 6.598 |
| w11 | 22 | 0.03474 | 18.181 |
| w12 | 25 | 0.02512 | 15.306 |
| w13 | 32 | 0.139403 | 6.714 |
| w14 | 15 | 0.107866 | 16.642 |
| w15 | 28 | 0.046215 | 30.117 |
| w16 | 28 | 0.114736 | 20.338 |
| w17 | 40 | 0.212862 | -9.797 |
| w18 | 25 | -0.001847 | 8.83 |
| w19 | 23 | -0.034674 | -4.076 |
| w20 | 43 | 0.155172 | -18.158 |
| w21 | 10 | -0.020934 | -11.092 |
| w22 | 26 | 0.127549 | 37.578 |
| w23 | 22 | 0.046628 | -2.729 |
| w24 | 18 | 0.137698 | 20.041 |
| w25 | 28 | 0.175078 | 14.188 |
| w26 | 30 | -0.064303 | -12.576 |
| w27 | 15 | -0.014181 | 3.697 |
| w28 | 29 | 0.103668 | 14.369 |
| w29 | 24 | -0.032779 | -10.879 |
| w30 | 28 | -0.044693 | -18.612 |
| w31 | 22 | -0.087916 | -35.352 |
| w32 | 15 | -0.066238 | 2.702 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.151992 | 4.41 |
| w2 | 27 | -0.123615 | -18.436 |
| w3 | 32 | 0.034125 | 9.113 |
| w4 | 24 | 0.031961 | 21.808 |
| w5 | 13 | 0.000759 | 4.038 |
| w6 | 37 | 0.05572 | 41.814 |
| w7 | 15 | 0.118792 | 5.405 |
| w8 | 29 | 0.185197 | -2.35 |
| w9 | 44 | 0.101843 | -17.48 |
| w10 | 16 | -0.002194 | -0.252 |
| w11 | 28 | 0.119929 | 25.337 |
| w12 | 24 | 0.012779 | -10.542 |
| w13 | 31 | 0.052344 | -4.368 |
| w14 | 28 | 0.137419 | 18.507 |
| w15 | 33 | 0.010099 | 7.914 |
| w16 | 24 | -0.107462 | -7.667 |
| w17 | 33 | 0.232916 | -2.006 |
| w18 | 27 | -0.07972 | -7.828 |
| w19 | 33 | -0.116523 | -18.831 |
| w20 | 31 | 0.193767 | -15.41 |
| w21 | 24 | 0.050117 | 1.713 |
| w22 | 38 | 0.085855 | 49.693 |
| w23 | 17 | 0.089599 | 43.562 |
| w24 | 27 | 0.031336 | 1.73 |
| w25 | 37 | 0.148548 | 4.008 |
| w26 | 23 | 0.066092 | -14.308 |
| w27 | 45 | -0.025947 | 11.987 |
| w28 | 24 | -0.070832 | -1.878 |
| w29 | 39 | 0.196572 | 23.696 |
| w30 | 11 | -0.016138 | 3.917 |
| w31 | 26 | 0.011569 | -19.106 |
| w32 | 18 | -0.076174 | -24.049 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 27 | 0.006506 | 33.584 |
| w7 | 8 | 0.096564 | 8.175 |
| w8 | 19 | 0.119292 | -9.041 |
| w9 | 35 | 0.092315 | -4.576 |
| w10 | 19 | 0.225692 | 13.42 |
| w11 | 9 | -0.000499 | 0.373 |
| w12 | 26 | 0.049147 | -4.121 |
| w13 | 37 | 0.072904 | -10.722 |
| w14 | 19 | 0.038997 | 3.005 |
| w15 | 25 | 0.147167 | 44.649 |
| w16 | 20 | 0.041176 | 11.704 |
| w17 | 19 | 0.187484 | 21.389 |
| w18 | 25 | -0.011134 | 4.021 |
| w19 | 27 | 0.071501 | 8.432 |
| w20 | 13 | 0.132801 | -17.656 |
| w21 | 12 | 0.273809 | 69.937 |
| w22 | 31 | 0.367582 | 53.643 |
| w23 | 20 | 0.031451 | 9.156 |
| w24 | 22 | 0.081622 | -1.859 |
| w25 | 29 | 0.214947 | 24.143 |
| w26 | 27 | 0.082573 | 24.953 |
| w27 | 22 | 0.037317 | 24.441 |
| w28 | 7 | 0.01223 | -0.2 |
| w29 | 33 | 0.00602 | 7.636 |
| w30 | 16 | -0.065924 | 1.003 |
| w31 | 19 | 0.200843 | -6.853 |
| w32 | 30 | -0.132455 | -31.054 |

- BCHUSD: 25 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w8 | 17 | 0.213565 | 4.651 |
| w9 | 34 | -0.089159 | -42.794 |
| w10 | 14 | 0.101752 | 8.73 |
| w11 | 21 | 0.117252 | 20.079 |
| w12 | 17 | 0.114811 | 3.608 |
| w13 | 25 | 0.226311 | 20.584 |
| w14 | 17 | 0.079608 | 2.233 |
| w15 | 28 | -0.008413 | -8.731 |
| w16 | 22 | 0.009576 | 11.905 |
| w17 | 28 | 0.160622 | -8.822 |
| w18 | 36 | -0.005284 | -5.137 |
| w19 | 37 | -0.000679 | -11.048 |
| w20 | 39 | 0.106288 | -15.503 |
| w21 | 9 | 0.095989 | -13.184 |
| w22 | 25 | 0.171934 | 34.34 |
| w23 | 29 | 0.115 | 35.814 |
| w24 | 23 | 0.035105 | -1.121 |
| w25 | 25 | -0.006628 | -6.28 |
| w26 | 26 | -0.039743 | -21.09 |
| w27 | 27 | -0.04105 | 0.19 |
| w28 | 30 | -0.036718 | 2.902 |
| w29 | 35 | 0.069445 | 13.011 |
| w30 | 37 | -0.005071 | 3.833 |
| w31 | 10 | 0.378375 | 13.912 |
| w32 | 36 | -0.126479 | -47.579 |

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
| w1 | 20 | -0.014135 | 33.365 |
| w2 | 28 | 0.025045 | 5.226 |
| w3 | 22 | 0.036654 | -5.089 |
| w4 | 23 | 0.003372 | 7.824 |
| w5 | 19 | -0.01655 | 7.414 |
| w6 | 27 | 0.128168 | 67.372 |
| w7 | 25 | 0.013238 | 1.22 |
| w8 | 23 | 0.162471 | -9.92 |
| w9 | 43 | 0.076488 | -7.85 |
| w10 | 12 | 0.12467 | 3.858 |
| w11 | 23 | 0.048933 | 16.279 |
| w12 | 30 | 0.002487 | -13.821 |
| w13 | 32 | 0.017654 | -5.486 |
| w14 | 21 | 0.101716 | 23.789 |
| w15 | 24 | -0.010104 | 2.785 |
| w16 | 19 | 0.140211 | 21.967 |
| w17 | 21 | 0.109431 | -10.574 |
| w18 | 32 | 0.06357 | 20.748 |
| w19 | 24 | -0.099553 | -8.409 |
| w20 | 42 | 0.097269 | -9.526 |
| w21 | 20 | 0.068791 | 10.99 |
| w22 | 37 | 0.149436 | 41.66 |
| w23 | 38 | -0.014566 | -2.307 |
| w24 | 34 | 0.068231 | 2.479 |
| w25 | 29 | -0.009679 | -4.643 |
| w26 | 27 | 0.033598 | -14.776 |
| w27 | 30 | -0.011677 | 2.342 |
| w28 | 30 | 0.115522 | -14.433 |
| w29 | 24 | 0.061852 | 15.434 |
| w30 | 17 | -0.04694 | -8.114 |
| w31 | 29 | -0.177021 | -39.726 |
| w32 | 13 | 0.076879 | 17.959 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 32 | 0.130847 | 28.082 |
| w11 | 21 | -0.025481 | -3.198 |
| w12 | 29 | 0.016172 | -8.578 |
| w13 | 37 | 0.091184 | 3.259 |
| w14 | 29 | 0.208798 | 24.753 |
| w15 | 34 | -0.007551 | 3.152 |
| w16 | 23 | 0.040544 | 12.039 |
| w17 | 26 | 0.240712 | 4.265 |
| w18 | 37 | 0.039448 | -4.91 |
| w19 | 24 | -0.015504 | -4.907 |
| w20 | 24 | 0.140535 | -11.224 |
| w21 | 24 | 0.132646 | 2.972 |
| w22 | 35 | 0.1595 | 43.697 |
| w23 | 20 | -0.002732 | -34.525 |
| w24 | 30 | 0.049044 | 71.419 |
| w25 | 33 | 0.130087 | 4.057 |
| w26 | 26 | 0.056943 | 5.285 |
| w27 | 15 | -0.069853 | -3.999 |
| w28 | 14 | 0.016132 | 2.663 |
| w29 | 32 | -0.031792 | -11.834 |
| w30 | 19 | -0.075818 | -11.925 |
| w31 | 27 | 0.156339 | 6.853 |
| w32 | 28 | -0.271479 | -43.197 |

- ATOMUSD: 20 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 23 | -0.066737 | -15.584 |
| w14 | 27 | 0.29033 | 95.303 |
| w15 | 16 | 0.245643 | 23.669 |
| w16 | 27 | 0.000102 | 14.245 |
| w17 | 25 | 0.21281 | -9.039 |
| w18 | 29 | 0.109101 | 54.943 |
| w19 | 20 | 0.079155 | -4.047 |
| w20 | 31 | 0.063131 | -17.14 |
| w21 | 18 | -0.003414 | -14.852 |
| w22 | 43 | 0.213616 | 34.343 |
| w23 | 24 | -0.006774 | -23.83 |
| w24 | 50 | 0.163334 | 37.94 |
| w25 | 28 | 0.200763 | 13.112 |
| w26 | 26 | -0.046301 | -21.224 |
| w27 | 24 | -0.039947 | -6.089 |
| w28 | 21 | -0.010357 | -10.511 |
| w29 | 37 | -0.076466 | -17.068 |
| w30 | 18 | -0.011121 | 10.876 |
| w31 | 30 | 0.117423 | 0.861 |
| w32 | 37 | 0.075217 | -5.92 |

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
| w15 | 30 | 0.245173 | 30.739 |
| w16 | 30 | -0.080583 | 17.58 |
| w17 | 29 | 0.340163 | 17.397 |
| w18 | 36 | 0.207378 | 87.782 |
| w19 | 20 | 0.035955 | -4.118 |
| w20 | 21 | 0.118571 | -2.733 |
| w21 | 27 | 0.014112 | -21.055 |
| w22 | 32 | 0.077783 | 32.37 |
| w23 | 32 | 0.010069 | -20.74 |
| w24 | 32 | 0.057556 | 14.675 |
| w25 | 26 | 0.087703 | 13.519 |
| w26 | 21 | -0.005103 | 4.548 |
| w27 | 28 | 0.01657 | 33.578 |
| w28 | 12 | -0.060811 | -4.21 |
| w29 | 28 | 0.031723 | 4.532 |
| w30 | 17 | -0.000989 | -5.543 |
| w31 | 29 | -0.003774 | -14.691 |
| w32 | 18 | -0.205021 | -31.085 |

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
| w15 | 27 | 0.056926 | 22.217 |
| w16 | 37 | -0.074204 | 2.755 |
| w17 | 16 | 0.201972 | 16.335 |
| w18 | 27 | 0.179217 | 15.636 |
| w19 | 31 | 0.016669 | -7.516 |
| w20 | 25 | 0.32861 | 22.635 |
| w21 | 22 | -0.042622 | -24.399 |
| w22 | 31 | 0.204282 | 35.872 |
| w23 | 26 | 0.020441 | -5.551 |
| w24 | 25 | 0.038261 | -0.169 |
| w25 | 20 | 0.159121 | 16.022 |
| w26 | 20 | -0.050984 | 1.522 |
| w27 | 20 | -0.030656 | 16.488 |
| w28 | 16 | -0.01391 | -6.62 |
| w29 | 27 | -0.012174 | -3.94 |
| w30 | 16 | 0.03683 | 7.81 |
| w31 | 22 | 0.021284 | 13.53 |
| w32 | 12 | -0.286154 | -20.908 |

- DOTUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 27 | 0.204084 | 0.008 |
| w18 | 36 | 0.025249 | 1.741 |
| w19 | 17 | -0.055051 | -8.142 |
| w20 | 25 | 0.095232 | -1.873 |
| w21 | 17 | 0.034249 | -9.762 |
| w22 | 36 | 0.094516 | 14.696 |
| w23 | 23 | 0.089759 | -2.37 |
| w24 | 45 | 0.032779 | 20.441 |
| w25 | 32 | 0.177394 | 11.345 |
| w26 | 19 | -0.080421 | -13.071 |
| w27 | 28 | -0.095528 | -7.26 |
| w28 | 22 | 0.030908 | 1.622 |
| w29 | 32 | -0.011605 | -8.283 |
| w30 | 15 | -0.154702 | -21.168 |
| w31 | 19 | 0.061146 | 1.36 |
| w32 | 20 | 0.032414 | -6.177 |

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
| w20 | 27 | -0.013216 | -22.006 |
| w21 | 20 | -0.020008 | -20.858 |
| w22 | 34 | 0.065389 | 34.183 |
| w23 | 26 | -0.023861 | -15.324 |
| w24 | 22 | -0.026221 | 51.06 |
| w25 | 24 | 0.182809 | 22.183 |
| w26 | 19 | -0.098707 | -16.618 |
| w27 | 31 | -0.012137 | 2.933 |
| w28 | 27 | 0.070846 | -6.105 |
| w29 | 35 | -0.049142 | 4.505 |
| w30 | 19 | -0.018552 | -5.677 |
| w31 | 25 | 0.055939 | -5.308 |
| w32 | 35 | 0.013408 | -16.101 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 35 | 0.057655 | 25.901 |
| w23 | 24 | -0.00325 | -12.065 |
| w24 | 34 | 0.055406 | 27.456 |
| w25 | 16 | 0.175898 | 37.285 |
| w26 | 19 | 0.000462 | -2.309 |
| w27 | 30 | -0.130498 | -7.321 |
| w28 | 32 | -0.027805 | -20.78 |
| w29 | 28 | -0.022242 | -6.173 |
| w30 | 20 | -0.100884 | -9.753 |
| w31 | 23 | 0.020093 | -6.916 |
| w32 | 28 | 0.033822 | 5.986 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 32 | 0.179598 | 25.647 |
| w25 | 32 | 0.050437 | 13.693 |
| w26 | 20 | 0.0579 | 23.472 |
| w27 | 28 | 0.071408 | 17.985 |
| w28 | 23 | 0.014347 | -1.542 |
| w29 | 25 | 0.034745 | 6.752 |
| w30 | 17 | -0.045217 | -8.776 |
| w31 | 20 | 0.247676 | 7.939 |
| w32 | 13 | -0.062387 | -17.982 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 16 | -0.063702 | -1.765 |
| w6 | 33 | 0.110889 | 30.713 |
| w7 | 23 | 0.101292 | 9.484 |
| w8 | 22 | 0.008722 | -11.72 |
| w9 | 29 | 0.023805 | -35.932 |
| w10 | 31 | 0.156798 | 18.72 |
| w11 | 33 | 0.149606 | 19.514 |
| w12 | 34 | -0.031883 | -14.835 |
| w13 | 19 | 0.156616 | 14.844 |
| w14 | 25 | -0.018242 | 8.748 |
| w15 | 26 | 0.049911 | 11.809 |
| w16 | 28 | -0.022453 | 16.06 |
| w17 | 29 | 0.22056 | 8.267 |
| w18 | 35 | 0.070699 | 35.671 |
| w19 | 29 | 0.136158 | 40.38 |
| w20 | 37 | 0.221459 | 7.514 |
| w21 | 15 | 0.073942 | -24.111 |
| w22 | 32 | 0.152492 | 36.814 |
| w23 | 28 | 0.035982 | 6.902 |
| w24 | 37 | 0.167386 | 17.673 |
| w25 | 37 | -0.023034 | -7.89 |
| w26 | 26 | -0.019545 | 26.34 |
| w27 | 40 | -0.079624 | 10.244 |
| w28 | 19 | -0.022484 | 1.982 |
| w29 | 25 | 0.123323 | 35.664 |
| w30 | 18 | 0.128756 | 30.517 |
| w31 | 23 | -0.091836 | -11.325 |
| w32 | 23 | -0.043572 | -1.341 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 33 | -0.017225 | 29.443 |
| w6 | 27 | 0.124605 | 38.858 |
| w7 | 26 | 0.174679 | 7.304 |
| w8 | 29 | 0.222004 | 11.993 |
| w9 | 38 | 0.073425 | -25.362 |
| w10 | 26 | 0.138497 | 13.65 |
| w11 | 29 | 0.094716 | 15.501 |
| w12 | 31 | -0.011136 | -10.796 |
| w13 | 39 | 0.09359 | -10.623 |
| w14 | 25 | 0.262694 | 27.737 |
| w15 | 29 | 0.001618 | 6.282 |
| w16 | 31 | 0.017087 | 22.61 |
| w17 | 27 | 0.244667 | -30.636 |
| w18 | 35 | 0.139016 | 28.365 |
| w19 | 27 | -0.120811 | -14.957 |
| w20 | 19 | 0.036503 | -24.493 |
| w21 | 18 | 0.098372 | 0.224 |
| w22 | 31 | 0.155004 | 51.433 |
| w23 | 22 | 0.035141 | -2.308 |
| w24 | 30 | 0.083166 | 3.1 |
| w25 | 29 | 0.176211 | 10.238 |
| w26 | 28 | 0.274934 | 44.938 |
| w27 | 27 | 0.084111 | 11.393 |
| w28 | 18 | 0.201575 | 23.95 |
| w29 | 36 | -0.109205 | -28.948 |
| w30 | 17 | -0.113912 | -6.243 |
| w31 | 30 | 0.107903 | 16.662 |
| w32 | 15 | 0.089979 | 16.57 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 23 | 0.067106 | -4.514 |
| w18 | 29 | -0.068055 | 21.195 |
| w19 | 23 | -0.054643 | -22.064 |
| w20 | 28 | 0.042409 | -20.323 |
| w21 | 20 | 0.025568 | -17.153 |
| w22 | 34 | 0.116201 | 30.892 |
| w23 | 27 | 0.207477 | -6.443 |
| w24 | 41 | 0.109155 | 14.37 |
| w25 | 32 | 0.11964 | 1.828 |
| w26 | 31 | 0.292474 | 8.163 |
| w27 | 20 | 0.229111 | 94.143 |
| w28 | 22 | 0.099727 | 3.545 |
| w29 | 25 | -0.051189 | -9.353 |
| w30 | 17 | -0.037564 | -4.478 |
| w31 | 29 | 0.112348 | -10.497 |
| w32 | 28 | -0.057879 | -9.517 |

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
| w17 | 21 | 0.102213 | 0.189 |
| w18 | 28 | -0.096756 | -26.708 |
| w19 | 31 | -0.066415 | -10.154 |
| w20 | 28 | 0.184702 | 12.634 |
| w21 | 15 | -0.030335 | -23.465 |
| w22 | 39 | 0.119677 | 29.851 |
| w23 | 25 | 0.12831 | 10.802 |
| w24 | 31 | -0.052689 | -3.715 |
| w25 | 35 | 0.045805 | 11.415 |
| w26 | 28 | -0.18447 | -20.28 |
| w27 | 34 | 0.074241 | 18.486 |
| w28 | 22 | 0.082486 | 23.231 |
| w29 | 26 | 0.012217 | 10.468 |
| w30 | 19 | -0.028785 | -4.173 |
| w31 | 18 | -0.071646 | -15.713 |
| w32 | 23 | 0.057835 | 8.937 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 20 | 0.076561 | 6.831 |
| w20 | 34 | 0.052631 | -17.646 |
| w21 | 17 | 0.060156 | -5.595 |
| w22 | 29 | 0.009861 | 61.426 |
| w23 | 14 | -0.041604 | -1.084 |
| w24 | 39 | 0.033813 | 28.298 |
| w25 | 27 | 0.130934 | 1.466 |
| w26 | 23 | -0.037793 | -4.455 |
| w27 | 32 | -0.089605 | -10.375 |
| w28 | 36 | 0.049093 | -11.178 |
| w29 | 33 | -0.081235 | -15.173 |
| w30 | 14 | 0.026098 | -0.09 |
| w31 | 29 | -0.023287 | -15.551 |
| w32 | 34 | 0.07646 | 4.764 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 35 | 0.218587 | 29.854 |
| w23 | 19 | -0.060585 | -6.035 |
| w24 | 29 | 0.131387 | 22.467 |
| w25 | 23 | -0.137361 | -25.122 |
| w26 | 31 | 0.006011 | -1.314 |
| w27 | 23 | -0.158745 | -22.424 |
| w28 | 33 | 0.068677 | -9.022 |
| w29 | 32 | -0.146756 | -9.944 |
| w30 | 19 | -0.034222 | -7.861 |
| w31 | 24 | 0.072488 | -2.071 |
| w32 | 23 | 0.016279 | 11.056 |

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
| w27 | 36 | 0.076309 | 13.867 |
| w28 | 16 | 0.001477 | 5.137 |
| w29 | 31 | -0.029967 | -9.449 |
| w30 | 18 | -0.01396 | -4.114 |
| w31 | 25 | 0.01178 | -7.895 |
| w32 | 35 | 0.022751 | 12.692 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 26 | 0.212493 | 7.271 |
| w18 | 29 | -0.112389 | -25.541 |
| w19 | 41 | 0.059128 | -10.53 |
| w20 | 19 | 0.043278 | -17.587 |
| w21 | 15 | -0.05055 | -19.494 |
| w22 | 32 | 0.117154 | 41.218 |
| w23 | 19 | -0.03732 | -17.739 |
| w24 | 38 | 0.00654 | 9.543 |
| w25 | 33 | 0.053041 | 2.888 |
| w26 | 26 | -0.094525 | -20.422 |
| w27 | 34 | -0.037448 | -2.256 |
| w28 | 19 | 0.052733 | 1.15 |
| w29 | 45 | -0.011391 | -9.474 |
| w30 | 16 | -0.104831 | -15.506 |
| w31 | 22 | 0.049472 | -9.318 |
| w32 | 28 | -0.081656 | -18.688 |

- GRTUSD: 15 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w18 | 42 | 0.06618 | 16.022 |
| w19 | 24 | 0.048839 | -8.454 |
| w20 | 32 | 0.044674 | -30.778 |
| w21 | 14 | 0.004806 | -26.757 |
| w22 | 17 | 0.073122 | 26.016 |
| w23 | 23 | -0.011051 | -16.079 |
| w24 | 22 | 0.173096 | 40.443 |
| w25 | 34 | 0.111633 | 20.052 |
| w26 | 20 | -0.022652 | -4.341 |
| w27 | 27 | -0.14825 | -1.957 |
| w28 | 27 | 0.019299 | -5.45 |
| w29 | 28 | 0.033149 | 3.513 |
| w30 | 12 | -0.073874 | -14.357 |
| w31 | 18 | 0.148475 | -0.42 |
| w32 | 34 | 0.071995 | -13.342 |

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
| w28 | 36 | 0.003335 | -13.688 |
| w29 | 31 | 0.112447 | 12.159 |
| w30 | 11 | -0.042133 | 22.596 |
| w31 | 35 | 0.036773 | -6.306 |
| w32 | 16 | 0.073096 | 22.483 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 9 | -0.115231 | -8.881 |
| w15 | 21 | 0.106034 | 58.276 |
| w16 | 18 | -0.004473 | 8.556 |
| w17 | 10 | 0.024096 | -1.85 |
| w18 | 19 | 0.209748 | 15.765 |
| w19 | 27 | -0.024897 | 1.573 |
| w20 | 28 | 0.193848 | -15.256 |
| w21 | 15 | -0.01869 | -2.979 |
| w22 | 32 | 0.010433 | 5.915 |
| w23 | 24 | 0.179594 | 28.632 |
| w24 | 22 | 0.083263 | 22.803 |
| w25 | 30 | 0.002843 | 1.321 |
| w26 | 19 | 0.079754 | 10.39 |
| w27 | 17 | -0.055317 | 11.306 |
| w28 | 33 | -0.002377 | -8.341 |
| w29 | 26 | 0.042548 | 7.617 |
| w30 | 10 | -0.144143 | -13.446 |
| w31 | 22 | -0.032397 | -3.381 |
| w32 | 23 | -0.063757 | -29.59 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 26 | 0.223361 | 32.325 |
| w26 | 26 | 0.074765 | 13.63 |
| w27 | 15 | -0.089644 | -8.335 |
| w28 | 35 | -0.044949 | -22.471 |
| w29 | 20 | -0.014816 | -3.018 |
| w30 | 20 | -0.026596 | -11.41 |
| w31 | 31 | -0.007311 | 0.845 |
| w32 | 32 | 0.031874 | -2.358 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

