# Backtest of 030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d

- Plan: `../../../../../03_test_plan/brief_absorption_run/plans/030-03_heavy-flat-high-close-reverses.b1_heavy-volume-high-close-continuation.b2_heavy-low-close-next-day-rebound.d1_heavy-volume-bottom-close-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 13 | -0.039402 | -3.61 |
| w2 | 9 | -0.20893 | -12.401 |
| w3 | 6 | 0.178911 | 15.054 |
| w4 | 8 | -0.017446 | -2.893 |
| w5 | 7 | -9.4e-05 | 1.688 |
| w6 | 6 | 0.02764 | 1.993 |
| w7 | 9 | 0.133705 | 8.509 |
| w8 | 5 | 0.164195 | 6.452 |
| w9 | 11 | -0.007422 | -7.968 |
| w10 | 3 | 0.049382 | 1.825 |
| w11 | 6 | 0.256178 | 19.245 |
| w12 | 7 | -0.020401 | -1.679 |
| w13 | 5 | 0.234974 | 9.362 |
| w14 | 4 | 0.065805 | 4.027 |
| w15 | 6 | 0.060596 | 8.221 |
| w16 | 5 | -0.039362 | -1.116 |
| w17 | 5 | 0.108653 | 2.281 |
| w18 | 6 | 0.00143 | -0.506 |
| w19 | 4 | 0.019626 | 0.091 |
| w20 | 8 | 0.056208 | 0.479 |
| w21 | 8 | 0.224783 | 9.649 |
| w22 | 4 | 0.129423 | 10.297 |
| w23 | 3 | 0.238102 | 5.388 |
| w24 | 8 | 0.065095 | 4.86 |
| w25 | 8 | -0.195335 | -9.62 |
| w26 | 4 | 0.036752 | 0.452 |
| w27 | 3 | 0.053836 | 0.759 |
| w28 | 9 | 0.086649 | 6.291 |
| w29 | 7 | 0.01026 | 0.81 |
| w30 | 4 | 0.02016 | 0.532 |
| w31 | 6 | 0.100602 | -0.862 |
| w32 | 6 | -0.090564 | -6.033 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 9 | 0.086826 | 4.752 |
| w2 | 12 | -0.105124 | -8.819 |
| w3 | 9 | 0.119223 | 5.784 |
| w4 | 10 | -0.036221 | -4.325 |
| w5 | 4 | -0.015258 | 1.235 |
| w6 | 5 | 0.139266 | 9.991 |
| w7 | 7 | 0.101115 | 4.297 |
| w8 | 4 | 0.118017 | 3.159 |
| w9 | 9 | 0.003807 | -2.268 |
| w10 | 4 | 0.003115 | 0.541 |
| w11 | 10 | -0.06135 | -3.409 |
| w12 | 7 | 0.292049 | 12.975 |
| w13 | 6 | 0.273113 | 15.415 |
| w14 | 9 | 0.190198 | 17.518 |
| w15 | 10 | 0.144935 | 12.685 |
| w16 | 5 | -0.009832 | 0.738 |
| w17 | 4 | 0.213735 | 5.552 |
| w18 | 8 | 0.068115 | 5.457 |
| w19 | 11 | 0.104097 | 5.215 |
| w20 | 11 | 0.118195 | 7.754 |
| w21 | 4 | 0.108677 | 4.887 |
| w22 | 8 | 0.044853 | 2.38 |
| w23 | 9 | -0.00999 | -0.815 |
| w24 | 7 | 0.068651 | 3.969 |
| w25 | 6 | -0.045135 | -3.941 |
| w26 | 6 | 0.114771 | 2.348 |
| w27 | 6 | 0.001208 | -1.058 |
| w28 | 6 | -0.05536 | -3.502 |
| w29 | 11 | 0.218647 | 19.251 |
| w30 | 8 | 0.005031 | -0.126 |
| w31 | 7 | -0.045715 | -3.565 |
| w32 | 7 | 0.118982 | 5.093 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 6 | -0.071544 | -3.44 |
| w7 | 6 | 0.022838 | 0.666 |
| w8 | 4 | 0.113123 | 3.193 |
| w9 | 10 | 0.126249 | 9.964 |
| w10 | 7 | 0.141341 | 4.749 |
| w11 | 7 | 0.069757 | 3.316 |
| w12 | 3 | -0.000335 | -2.574 |
| w13 | 4 | 0.252887 | 8.398 |
| w14 | 7 | 0.04079 | 1.423 |
| w15 | 14 | 0.074238 | 9.702 |
| w16 | 4 | -0.042501 | -0.285 |
| w17 | 6 | 0.117219 | 8.757 |
| w18 | 4 | 0.090915 | 2.918 |
| w19 | 5 | -0.023527 | -3.564 |
| w20 | 5 | 0.039592 | -0.874 |
| w21 | 14 | 0.26667 | 26.658 |
| w22 | 8 | -0.003223 | -0.736 |
| w23 | 13 | -0.094598 | -7.352 |
| w24 | 7 | -0.173425 | -6.532 |
| w25 | 6 | 0.039075 | 2.395 |
| w26 | 3 | -0.019724 | -0.976 |
| w27 | 8 | 0.012686 | 4.802 |
| w28 | 2 | 0.055057 | 1.728 |
| w29 | 4 | 0.008012 | 0.18 |
| w30 | 0 | -0.04617 | 0.0 |
| w31 | 5 | 0.145529 | 2.334 |
| w32 | 8 | -0.024539 | -3.0 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 5 | -0.036178 | -2.167 |
| w8 | 3 | 0.14751 | 4.197 |
| w9 | 13 | -0.099839 | -15.736 |
| w10 | 7 | 0.06705 | 4.129 |
| w11 | 9 | 0.072554 | 2.59 |
| w12 | 7 | 0.170922 | 7.39 |
| w13 | 6 | 0.139885 | 7.059 |
| w14 | 7 | 0.215413 | 10.658 |
| w15 | 10 | 0.071794 | 3.778 |
| w16 | 5 | -0.029742 | 0.542 |
| w17 | 2 | 0.109816 | 1.598 |
| w18 | 5 | 0.091253 | 4.136 |
| w19 | 6 | -0.155429 | -8.01 |
| w20 | 13 | 0.064644 | 0.694 |
| w21 | 11 | 0.069086 | 2.338 |
| w22 | 9 | -0.085377 | -5.78 |
| w23 | 14 | 0.346198 | 39.54 |
| w24 | 6 | -0.046969 | -3.072 |
| w25 | 9 | 0.031239 | 6.144 |
| w26 | 6 | 0.040535 | 0.451 |
| w27 | 9 | 0.049749 | 2.581 |
| w28 | 13 | -0.065307 | -7.063 |
| w29 | 6 | -0.084408 | -5.364 |
| w30 | 6 | 0.082158 | 2.625 |
| w31 | 5 | 0.399129 | 17.781 |
| w32 | 11 | 0.026747 | -2.095 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 7 | 0.099235 | 8.097 |
| w2 | 6 | 0.077689 | 3.823 |
| w3 | 8 | 0.183065 | 3.71 |
| w4 | 3 | -0.202455 | -1.768 |
| w5 | 10 | 0.241239 | 14.644 |
| w6 | 7 | 0.17718 | 10.54 |
| w7 | 12 | 0.083557 | 4.606 |
| w8 | 8 | 0.114181 | 3.535 |
| w9 | 16 | 0.051128 | 0.54 |
| w10 | 3 | 0.045943 | 1.27 |
| w11 | 8 | 0.103822 | 8.915 |
| w12 | 7 | 0.022699 | -0.663 |
| w13 | 4 | 0.254524 | 11.915 |
| w14 | 2 | 0.042549 | 0.912 |
| w15 | 8 | -0.037869 | -2.812 |
| w16 | 6 | -0.036058 | -0.09 |
| w17 | 2 | 0.302156 | 6.91 |
| w18 | 5 | 0.222154 | 14.779 |
| w19 | 3 | -0.085193 | -3.395 |
| w20 | 8 | -0.023042 | -3.946 |
| w21 | 6 | 0.220387 | 8.089 |
| w22 | 5 | 0.004334 | 1.263 |
| w23 | 3 | 0.099322 | 2.305 |
| w24 | 4 | -0.103221 | -4.395 |
| w25 | 5 | 0.093674 | 4.145 |
| w26 | 1 | 0.045047 | -0.048 |
| w27 | 3 | -0.01378 | -0.946 |
| w28 | 5 | 0.025511 | 0.511 |
| w29 | 6 | 0.060788 | 2.379 |
| w30 | 5 | 0.19353 | 5.365 |
| w31 | 4 | 0.231375 | 11.521 |
| w32 | 2 | -0.080157 | -3.396 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | 0.020264 | 0.83 |
| w11 | 7 | 0.022598 | -0.272 |
| w12 | 6 | 0.197132 | 5.758 |
| w13 | 9 | 0.206776 | 16.184 |
| w14 | 8 | 0.224971 | 12.238 |
| w15 | 4 | -0.015692 | -0.728 |
| w16 | 4 | 0.025785 | 0.759 |
| w17 | 6 | 0.129979 | 3.757 |
| w18 | 3 | 0.043536 | 1.082 |
| w19 | 3 | 0.057879 | 1.331 |
| w20 | 8 | 0.008747 | -2.378 |
| w21 | 7 | 0.255805 | 11.179 |
| w22 | 6 | -0.043684 | -1.639 |
| w23 | 8 | -0.051462 | -6.14 |
| w24 | 7 | -0.108688 | -8.58 |
| w25 | 5 | -0.012231 | 0.101 |
| w26 | 5 | 0.026129 | -0.468 |
| w27 | 7 | -0.07389 | -2.587 |
| w28 | 4 | 0.085376 | 2.697 |
| w29 | 6 | 0.039545 | 1.205 |
| w30 | 11 | -0.023644 | -4.603 |
| w31 | 5 | 0.312106 | 10.617 |
| w32 | 8 | -0.316904 | -24.901 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 8 | 0.092493 | 8.496 |
| w13 | 9 | 0.159834 | 6.193 |
| w14 | 12 | 0.168572 | 22.132 |
| w15 | 6 | 0.008771 | -1.108 |
| w16 | 6 | -0.054819 | -1.885 |
| w17 | 7 | 0.221698 | 7.946 |
| w18 | 8 | 0.09271 | 4.629 |
| w19 | 11 | 0.000872 | -1.948 |
| w20 | 8 | -0.072861 | -6.46 |
| w21 | 3 | 0.185682 | 3.348 |
| w22 | 5 | 0.089803 | 6.652 |
| w23 | 6 | 0.099706 | 2.066 |
| w24 | 8 | -0.042303 | -4.118 |
| w25 | 5 | 0.039311 | 0.328 |
| w26 | 7 | -0.100435 | -9.474 |
| w27 | 9 | 0.082793 | 5.321 |
| w28 | 9 | 0.100861 | 5.64 |
| w29 | 7 | 0.079139 | 3.965 |
| w30 | 6 | 0.081214 | 2.704 |
| w31 | 6 | 0.145041 | 5.752 |
| w32 | 6 | 0.01995 | -0.18 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 6 | -0.103243 | -6.341 |
| w16 | 2 | -0.102362 | -0.909 |
| w17 | 6 | 0.040066 | 1.118 |
| w18 | 7 | 0.123369 | 8.954 |
| w19 | 6 | -0.084779 | -6.241 |
| w20 | 11 | -0.116838 | -8.762 |
| w21 | 16 | 0.213986 | 14.774 |
| w22 | 4 | -0.077959 | -4.764 |
| w23 | 8 | 0.058639 | -0.174 |
| w24 | 8 | 0.00109 | 2.845 |
| w25 | 5 | -0.055556 | -2.52 |
| w26 | 6 | 0.01172 | -0.643 |
| w27 | 9 | -0.036676 | -1.285 |
| w28 | 9 | 0.232333 | 8.886 |
| w29 | 10 | 0.158133 | 10.641 |
| w30 | 9 | 0.112343 | 2.146 |
| w31 | 5 | 0.118866 | 3.456 |
| w32 | 3 | 0.072313 | 1.088 |

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
| w15 | 11 | -0.028516 | -1.832 |
| w16 | 14 | -0.005542 | 2.236 |
| w17 | 8 | 0.105896 | 7.233 |
| w18 | 4 | -0.06415 | -0.937 |
| w19 | 6 | 0.049025 | 3.178 |
| w20 | 16 | 0.204915 | 22.221 |
| w21 | 8 | 0.226256 | 8.95 |
| w22 | 9 | 0.06227 | 2.56 |
| w23 | 5 | -0.046984 | -3.43 |
| w24 | 5 | 0.077237 | 5.0 |
| w25 | 7 | 0.10325 | 4.747 |
| w26 | 7 | 0.071763 | 6.261 |
| w27 | 4 | 0.02272 | 13.575 |
| w28 | 3 | 0.02803 | 1.056 |
| w29 | 10 | -0.165988 | -9.744 |
| w30 | 5 | 0.11604 | 2.143 |
| w31 | 7 | -0.075332 | -4.794 |
| w32 | 8 | -0.126404 | -8.017 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 6 | 0.012339 | 2.103 |
| w17 | 7 | 0.049103 | 3.837 |
| w18 | 5 | 0.040251 | 1.084 |
| w19 | 4 | -0.017976 | -0.951 |
| w20 | 7 | 0.088271 | 3.768 |
| w21 | 11 | 0.137722 | 3.634 |
| w22 | 4 | -0.094255 | -5.448 |
| w23 | 6 | 0.064539 | -0.25 |
| w24 | 5 | -0.0461 | -3.168 |
| w25 | 6 | -0.010683 | -0.181 |
| w26 | 8 | -0.030189 | -3.457 |
| w27 | 5 | -0.161543 | -9.608 |
| w28 | 5 | 0.092867 | 1.952 |
| w29 | 5 | 0.126001 | 7.284 |
| w30 | 13 | 0.113899 | 2.576 |
| w31 | 5 | 0.129414 | 4.485 |
| w32 | 7 | 0.101247 | 1.314 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | 0.042426 | 1.523 |
| w21 | 5 | 0.067868 | -0.433 |
| w22 | 9 | -0.075348 | -1.757 |
| w23 | 7 | -0.242542 | -13.067 |
| w24 | 14 | 5e-06 | 4.032 |
| w25 | 10 | 0.164374 | 12.007 |
| w26 | 7 | -0.040919 | -2.214 |
| w27 | 5 | -0.005222 | -0.792 |
| w28 | 6 | 0.112105 | 5.141 |
| w29 | 6 | 0.035302 | 1.66 |
| w30 | 10 | 0.028895 | -0.617 |
| w31 | 5 | 0.269895 | 10.951 |
| w32 | 9 | -0.067627 | -5.428 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.010132 | -0.001 |
| w23 | 12 | 0.005133 | -2.587 |
| w24 | 11 | -0.022415 | 0.977 |
| w25 | 1 | -0.129451 | -3.088 |
| w26 | 7 | -0.054798 | -2.804 |
| w27 | 7 | 0.089553 | 2.333 |
| w28 | 5 | 0.174591 | 5.497 |
| w29 | 5 | 0.050923 | 1.822 |
| w30 | 9 | 0.116281 | 7.784 |
| w31 | 7 | 0.101354 | 4.549 |
| w32 | 15 | -0.016992 | 2.93 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 12 | -0.11833 | -5.603 |
| w25 | 1 | -0.160242 | -2.848 |
| w26 | 13 | 0.078006 | 3.246 |
| w27 | 4 | 0.075096 | 2.468 |
| w28 | 2 | -0.020871 | -0.901 |
| w29 | 2 | -0.053097 | -0.979 |
| w30 | 3 | -0.108999 | -2.918 |
| w31 | 6 | 0.298635 | 12.501 |
| w32 | 4 | 0.083573 | 0.829 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 9 | 0.026428 | 1.565 |
| w6 | 7 | 0.002413 | 0.775 |
| w7 | 5 | -0.050016 | -1.45 |
| w8 | 4 | 0.138725 | 5.451 |
| w9 | 9 | -0.054247 | -6.519 |
| w10 | 8 | -0.10154 | -4.949 |
| w11 | 12 | 0.139206 | 14.02 |
| w12 | 11 | 0.057334 | 1.225 |
| w13 | 8 | 0.031285 | 3.045 |
| w14 | 9 | 0.075299 | 4.946 |
| w15 | 9 | 0.158628 | 5.894 |
| w16 | 8 | 0.052576 | 5.944 |
| w17 | 11 | 0.11845 | 14.754 |
| w18 | 10 | -0.005997 | -1.653 |
| w19 | 8 | -0.112621 | -9.04 |
| w20 | 5 | -0.090944 | -5.621 |
| w21 | 8 | 0.004373 | -2.337 |
| w22 | 7 | 0.184833 | 10.366 |
| w23 | 9 | 0.013256 | -0.416 |
| w24 | 12 | 0.083052 | 6.335 |
| w25 | 13 | 0.014601 | -0.313 |
| w26 | 8 | 0.063969 | 3.376 |
| w27 | 9 | -0.088004 | -5.386 |
| w28 | 4 | -0.030922 | -2.245 |
| w29 | 7 | 0.070662 | 5.298 |
| w30 | 9 | 0.114241 | 10.692 |
| w31 | 4 | 0.27085 | 8.638 |
| w32 | 5 | -0.098534 | -0.33 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | -0.070025 | 0.636 |
| w6 | 3 | -0.027535 | -0.545 |
| w7 | 5 | 0.166369 | 6.157 |
| w8 | 8 | 0.132861 | 4.509 |
| w9 | 9 | 0.065033 | 1.935 |
| w10 | 6 | -0.033629 | -2.483 |
| w11 | 9 | -0.15791 | -9.824 |
| w12 | 10 | 0.058273 | 0.106 |
| w13 | 9 | 0.085672 | 5.879 |
| w14 | 7 | -0.006127 | 0.97 |
| w15 | 6 | -0.033749 | -0.906 |
| w16 | 8 | 0.049861 | 7.055 |
| w17 | 8 | 0.159453 | 11.914 |
| w18 | 4 | -0.119257 | -6.248 |
| w19 | 5 | 0.01109 | 0.411 |
| w20 | 9 | -0.03884 | -3.213 |
| w21 | 8 | 0.042125 | -0.115 |
| w22 | 7 | -0.017044 | -2.172 |
| w23 | 7 | 0.027013 | -0.957 |
| w24 | 4 | 0.071286 | 2.779 |
| w25 | 7 | 0.151751 | 0.001 |
| w26 | 4 | -0.079171 | -4.03 |
| w27 | 5 | -0.04314 | -2.827 |
| w28 | 4 | 0.153253 | 5.515 |
| w29 | 7 | -0.028765 | -2.078 |
| w30 | 5 | -0.059022 | -1.105 |
| w31 | 5 | 0.002053 | -0.817 |
| w32 | 11 | 0.113012 | 13.501 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | 0.022459 | -0.235 |
| w18 | 10 | -0.079638 | -3.529 |
| w19 | 3 | 0.15089 | 4.654 |
| w20 | 11 | -0.065056 | -5.635 |
| w21 | 6 | 0.173184 | 5.688 |
| w22 | 8 | -0.038708 | -2.276 |
| w23 | 7 | 0.017233 | -0.948 |
| w24 | 6 | 0.190762 | 13.005 |
| w25 | 7 | 0.238339 | 17.017 |
| w26 | 14 | 0.098866 | 7.11 |
| w27 | 9 | 0.035378 | 3.856 |
| w28 | 4 | 0.142893 | 3.897 |
| w29 | 5 | 0.045377 | 0.675 |
| w30 | 5 | 0.111169 | 2.672 |
| w31 | 6 | 0.169461 | 6.257 |
| w32 | 8 | 0.004314 | -1.505 |

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
| w17 | 5 | 0.0705 | 5.622 |
| w18 | 7 | -0.051438 | -4.839 |
| w19 | 4 | -0.061971 | -2.845 |
| w20 | 9 | 0.091483 | 4.636 |
| w21 | 11 | 0.032842 | -1.25 |
| w22 | 10 | 0.006785 | 0.87 |
| w23 | 7 | 0.001791 | 0.994 |
| w24 | 13 | -0.004384 | 4.759 |
| w25 | 8 | 0.008023 | 3.378 |
| w26 | 13 | -0.16737 | -11.712 |
| w27 | 4 | 0.130658 | 8.633 |
| w28 | 5 | 0.230569 | 9.368 |
| w29 | 4 | -0.091528 | -2.204 |
| w30 | 8 | 0.095267 | 3.344 |
| w31 | 6 | 0.09266 | 2.354 |
| w32 | 8 | -0.028736 | -0.947 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 7 | -0.177472 | -11.622 |
| w20 | 16 | -0.245798 | -12.023 |
| w21 | 14 | -0.044036 | -3.65 |
| w22 | 13 | -0.042991 | 0.317 |
| w23 | 5 | 0.045174 | 0.861 |
| w24 | 14 | 0.140941 | 24.545 |
| w25 | 2 | 0.00458 | -0.204 |
| w26 | 7 | -0.037967 | -3.54 |
| w27 | 5 | -0.03954 | -1.721 |
| w28 | 6 | -0.011672 | -1.851 |
| w29 | 4 | -0.130041 | -4.242 |
| w30 | 7 | 0.116324 | 4.007 |
| w31 | 10 | 0.101471 | 3.325 |
| w32 | 7 | -0.020328 | -0.981 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | -0.03307 | -1.184 |
| w23 | 7 | 0.279623 | 6.112 |
| w24 | 14 | 0.102594 | 12.337 |
| w25 | 6 | 0.008424 | -1.36 |
| w26 | 7 | 0.147133 | 6.52 |
| w27 | 11 | -0.06308 | -3.157 |
| w28 | 3 | 0.088525 | 2.81 |
| w29 | 6 | 0.113812 | 7.617 |
| w30 | 10 | 0.16457 | 9.721 |
| w31 | 7 | 0.141034 | 5.832 |
| w32 | 8 | -0.028241 | -1.017 |

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
| w27 | 7 | 0.101197 | 6.309 |
| w28 | 8 | -0.08164 | -5.07 |
| w29 | 9 | 0.118805 | 6.158 |
| w30 | 6 | 0.125604 | 1.885 |
| w31 | 7 | 0.042691 | 1.702 |
| w32 | 7 | 0.047086 | 6.986 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.163117 | 5.002 |
| w18 | 9 | -0.085884 | -7.376 |
| w19 | 10 | 0.033409 | -1.485 |
| w20 | 8 | -0.129067 | -9.556 |
| w21 | 9 | -0.074764 | -6.133 |
| w22 | 7 | 0.332147 | 26.3 |
| w23 | 5 | -0.026984 | -1.526 |
| w24 | 12 | -0.077916 | -5.711 |
| w25 | 8 | 0.028958 | 0.809 |
| w26 | 5 | 0.085986 | 1.434 |
| w27 | 10 | 0.098872 | 8.618 |
| w28 | 2 | -0.038454 | -3.475 |
| w29 | 15 | 0.053596 | 0.823 |
| w30 | 12 | -0.057822 | -8.123 |
| w31 | 5 | 0.008149 | -0.983 |
| w32 | 7 | -0.140694 | -5.052 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 10 | 0.079689 | 2.301 |
| w18 | 10 | 0.172198 | 7.152 |
| w19 | 7 | 0.059458 | 0.955 |
| w20 | 8 | 0.044212 | 1.443 |
| w21 | 9 | 0.164468 | 5.698 |
| w22 | 8 | -0.069726 | -3.744 |
| w23 | 9 | -0.003262 | -2.839 |
| w24 | 8 | 0.079076 | 6.408 |
| w25 | 5 | 0.018443 | 0.638 |
| w26 | 2 | -0.065406 | -2.025 |
| w27 | 8 | 0.001744 | -0.031 |
| w28 | 7 | -0.077226 | -6.686 |
| w29 | 7 | 0.005575 | -1.064 |
| w30 | 6 | 0.077784 | 2.901 |
| w31 | 8 | 0.144195 | 3.459 |
| w32 | 5 | 0.12841 | 2.952 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 6 | 0.137146 | 7.279 |
| w29 | 5 | 0.158983 | 9.058 |
| w30 | 3 | 0.011391 | 2.537 |
| w31 | 7 | 0.085988 | 4.035 |
| w32 | 6 | 0.086816 | 3.8 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 4 | -0.147939 | -3.552 |
| w15 | 14 | 0.236842 | 16.51 |
| w16 | 9 | -0.038258 | 0.376 |
| w17 | 9 | 0.082292 | 4.227 |
| w18 | 5 | 0.179238 | 4.162 |
| w19 | 8 | 0.029661 | 1.328 |
| w20 | 6 | -0.06993 | -5.521 |
| w21 | 12 | 0.027287 | 5.117 |
| w22 | 3 | -0.016991 | -0.312 |
| w23 | 12 | 0.189555 | 8.866 |
| w24 | 14 | 0.044023 | 5.522 |
| w25 | 9 | 0.041907 | 2.444 |
| w26 | 0 | 0.039278 | 0.0 |
| w27 | 4 | 0.053977 | 1.348 |
| w28 | 5 | -0.037189 | -3.182 |
| w29 | 9 | 0.071176 | 3.136 |
| w30 | 4 | 0.268167 | 7.051 |
| w31 | 6 | 0.246101 | 6.292 |
| w32 | 3 | 0.075479 | 0.13 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 14 | 0.176263 | 17.319 |
| w26 | 2 | 0.070467 | 0.541 |
| w27 | 4 | 0.107153 | 2.833 |
| w28 | 5 | 0.166922 | 5.631 |
| w29 | 7 | 0.05415 | 1.319 |
| w30 | 5 | 0.20513 | 6.669 |
| w31 | 5 | 0.136143 | 4.361 |
| w32 | 7 | -0.080294 | -4.581 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

