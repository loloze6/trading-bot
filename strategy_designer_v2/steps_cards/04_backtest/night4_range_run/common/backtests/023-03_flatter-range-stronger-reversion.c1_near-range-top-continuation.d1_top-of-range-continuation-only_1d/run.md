# Backtest of 023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-03_flatter-range-stronger-reversion.c1_near-range-top-continuation.d1_top-of-range-continuation-only_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 19 | -0.027477 | -10.404 |
| w2 | 19 | 0.159631 | 89.833 |
| w3 | 35 | -0.0175 | 110.294 |
| w4 | 26 | 0.00664 | -36.49 |
| w5 | 28 | 0.026334 | 129.918 |
| w6 | 29 | 0.106144 | 120.715 |
| w7 | 8 | -0.052613 | -6.242 |
| w8 | 10 | 0.096189 | 4.779 |
| w9 | 15 | -0.106128 | -44.012 |
| w10 | 26 | 0.024784 | 40.627 |
| w11 | 27 | 0.027768 | 62.986 |
| w12 | 9 | 0.000412 | -17.257 |
| w13 | 25 | 0.034704 | 33.112 |
| w14 | 29 | -0.052419 | 11.796 |
| w15 | 28 | 0.125924 | 178.909 |
| w16 | 32 | -0.014399 | 29.765 |
| w17 | 20 | 0.095422 | 10.116 |
| w18 | 20 | 0.044743 | -7.788 |
| w19 | 20 | -0.044598 | -22.472 |
| w20 | 12 | 0.045838 | -12.051 |
| w21 | 10 | -0.048991 | -25.374 |
| w22 | 38 | -0.035137 | 77.618 |
| w23 | 14 | 0.066026 | 5.691 |
| w24 | 26 | -0.043589 | 76.347 |
| w25 | 29 | 0.071009 | 43.503 |
| w26 | 24 | -0.045514 | -25.808 |
| w27 | 32 | -0.020731 | 72.891 |
| w28 | 14 | 0.012886 | 1.361 |
| w29 | 25 | 0.061434 | 12.673 |
| w30 | 10 | -0.011739 | -22.904 |
| w31 | 24 | -0.019322 | -4.479 |
| w32 | 23 | 0.107521 | 21.616 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 16 | -0.085347 | 6.436 |
| w2 | 15 | 0.095854 | 29.136 |
| w3 | 16 | -0.202852 | -22.489 |
| w4 | 18 | 0.097038 | 151.738 |
| w5 | 25 | 0.006693 | 80.826 |
| w6 | 20 | 0.125695 | 80.43 |
| w7 | 11 | -0.073978 | -10.163 |
| w8 | 6 | 0.020061 | -17.287 |
| w9 | 7 | -0.202589 | -16.881 |
| w10 | 33 | -0.0043 | 38.6 |
| w11 | 13 | 0.073276 | 18.664 |
| w12 | 13 | -0.020874 | -33.417 |
| w13 | 24 | 0.040156 | 39.99 |
| w14 | 26 | -0.127291 | 16.804 |
| w15 | 14 | -0.047378 | 79.611 |
| w16 | 23 | 0.010349 | 16.95 |
| w17 | 22 | 0.06497 | 18.247 |
| w18 | 11 | 0.103761 | 7.899 |
| w19 | 12 | 0.026955 | -9.195 |
| w20 | 12 | -0.01395 | -4.553 |
| w21 | 19 | -0.074143 | -6.809 |
| w22 | 25 | -0.059172 | 4.508 |
| w23 | 13 | -0.115366 | -20.733 |
| w24 | 29 | -0.145577 | -22.348 |
| w25 | 20 | -0.063253 | 8.735 |
| w26 | 12 | -0.163181 | -31.624 |
| w27 | 29 | -0.031243 | 57.649 |
| w28 | 10 | -0.208393 | -33.208 |
| w29 | 18 | 0.044562 | 35.801 |
| w30 | 11 | -0.145747 | -33.998 |
| w31 | 19 | -0.041007 | -17.484 |
| w32 | 19 | 0.078337 | 2.235 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 16 | 0.150161 | 132.512 |
| w7 | 8 | 0.080273 | 7.358 |
| w8 | 5 | -0.021019 | -5.848 |
| w9 | 15 | 0.021649 | -2.874 |
| w10 | 9 | -0.198667 | -8.852 |
| w11 | 11 | -0.036843 | 11.604 |
| w12 | 7 | -0.035738 | -27.932 |
| w13 | 17 | 0.021518 | 19.461 |
| w14 | 23 | 0.097336 | 39.208 |
| w15 | 27 | 0.165716 | 175.497 |
| w16 | 21 | 0.007948 | 69.989 |
| w17 | 18 | -0.019868 | 15.299 |
| w18 | 15 | -0.110647 | -22.357 |
| w19 | 13 | -0.052086 | -14.508 |
| w20 | 9 | -0.017062 | -9.735 |
| w21 | 16 | -0.01799 | 12.993 |
| w22 | 24 | -0.140787 | 8.222 |
| w23 | 14 | -0.089499 | -0.622 |
| w24 | 18 | -0.004508 | 8.915 |
| w25 | 10 | -0.0421 | 18.481 |
| w26 | 19 | -0.05135 | -0.143 |
| w27 | 20 | 0.284734 | 279.054 |
| w28 | 13 | -0.052929 | -10.732 |
| w29 | 14 | 0.108962 | 54.718 |
| w30 | 10 | -0.084711 | -34.022 |
| w31 | 15 | -0.005252 | -14.236 |
| w32 | 10 | 0.061481 | -7.326 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.075784 | 14.609 |
| w8 | 9 | 0.049148 | -15.967 |
| w9 | 9 | -0.045088 | -30.405 |
| w10 | 23 | 0.073881 | 40.359 |
| w11 | 19 | -0.104593 | -5.651 |
| w12 | 14 | 0.027307 | -37.13 |
| w13 | 20 | 0.038207 | 61.856 |
| w14 | 20 | -0.151232 | -3.138 |
| w15 | 16 | -0.098278 | -9.62 |
| w16 | 19 | 0.10105 | 98.376 |
| w17 | 18 | -0.004127 | 8.951 |
| w18 | 15 | -0.020081 | -22.006 |
| w19 | 4 | 0.030122 | -11.911 |
| w20 | 8 | 0.018911 | 5.896 |
| w21 | 12 | -0.152918 | -26.484 |
| w22 | 29 | -0.016558 | 5.843 |
| w23 | 12 | 0.225529 | 96.665 |
| w24 | 19 | -0.151623 | -14.223 |
| w25 | 24 | 0.083722 | 43.906 |
| w26 | 10 | -0.037363 | -32.499 |
| w27 | 19 | -0.025846 | 36.165 |
| w28 | 8 | -0.043131 | -17.995 |
| w29 | 32 | -0.15863 | 23.65 |
| w30 | 14 | -0.177337 | -17.369 |
| w31 | 15 | -0.098165 | -19.802 |
| w32 | 10 | 0.145989 | -22.492 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 22 | 0.212887 | 251.748 |
| w2 | 27 | 0.005796 | 5.898 |
| w3 | 9 | 0.05933 | -4.951 |
| w4 | 38 | 0.072033 | 325.275 |
| w5 | 28 | 0.195994 | 170.87 |
| w6 | 20 | 0.051988 | 77.591 |
| w7 | 14 | 0.154951 | 35.718 |
| w8 | 8 | 0.082189 | -7.038 |
| w9 | 6 | -0.020491 | -13.072 |
| w10 | 16 | 0.01842 | 3.185 |
| w11 | 19 | 0.104095 | 42.363 |
| w12 | 10 | -0.023757 | -32.446 |
| w13 | 30 | 0.058018 | 71.622 |
| w14 | 29 | -0.083246 | 81.068 |
| w15 | 31 | -0.027919 | 28.119 |
| w16 | 34 | -0.06139 | 119.418 |
| w17 | 26 | 0.09914 | 43.326 |
| w18 | 24 | -0.004275 | -2.478 |
| w19 | 11 | 0.005124 | -6.812 |
| w20 | 12 | 0.117892 | 21.507 |
| w21 | 6 | -0.024582 | -9.214 |
| w22 | 37 | -0.110473 | 34.358 |
| w23 | 14 | -0.131816 | -17.201 |
| w24 | 22 | -0.052363 | 21.827 |
| w25 | 16 | 0.1264 | 48.828 |
| w26 | 16 | -0.034067 | -15.877 |
| w27 | 30 | -0.022596 | 9.128 |
| w28 | 1 | -0.013793 | -0.411 |
| w29 | 31 | 0.00205 | 82.822 |
| w30 | 14 | -0.135317 | -26.996 |
| w31 | 21 | -0.059736 | -15.128 |
| w32 | 23 | 0.017814 | 10.969 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 19 | 0.05137 | 50.326 |
| w11 | 12 | -0.129054 | -11.934 |
| w12 | 11 | -0.035522 | -35.217 |
| w13 | 20 | 0.090704 | 90.333 |
| w14 | 28 | -0.095472 | 63.961 |
| w15 | 22 | -0.039646 | 24.693 |
| w16 | 37 | 0.092998 | 133.204 |
| w17 | 13 | 0.074278 | 85.682 |
| w18 | 6 | -0.102318 | -24.313 |
| w19 | 10 | 0.036603 | -17.917 |
| w20 | 11 | -0.035204 | -21.793 |
| w21 | 5 | -0.142826 | -25.749 |
| w22 | 28 | -0.043697 | 16.136 |
| w23 | 5 | -0.068283 | -12.117 |
| w24 | 26 | 0.091443 | 164.862 |
| w25 | 18 | 0.082472 | 1.408 |
| w26 | 5 | -0.035891 | -16.384 |
| w27 | 18 | 0.237457 | 170.157 |
| w28 | 10 | -0.139274 | -20.379 |
| w29 | 15 | -0.018019 | 5.887 |
| w30 | 7 | -0.071554 | -22.552 |
| w31 | 4 | -0.149897 | -23.285 |
| w32 | 12 | 0.049582 | -16.124 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 12 | -0.109102 | 10.405 |
| w13 | 11 | -0.061985 | -20.191 |
| w14 | 19 | -0.027746 | 90.713 |
| w15 | 14 | -0.021051 | -4.042 |
| w16 | 21 | 0.025836 | 82.756 |
| w17 | 18 | 0.032901 | -5.923 |
| w18 | 10 | -0.129351 | 22.006 |
| w19 | 10 | -0.060264 | -24.684 |
| w20 | 12 | -0.016574 | 12.727 |
| w21 | 12 | -0.029925 | -10.698 |
| w22 | 21 | -0.043249 | 4.397 |
| w23 | 4 | -0.124536 | -8.406 |
| w24 | 24 | -0.137777 | 19.119 |
| w25 | 17 | 0.074916 | 0.716 |
| w26 | 3 | -0.086887 | -2.81 |
| w27 | 18 | 0.12379 | 50.966 |
| w28 | 9 | -0.09895 | -18.386 |
| w29 | 14 | -0.080415 | -17.075 |
| w30 | 7 | -0.020275 | -13.708 |
| w31 | 20 | -0.009061 | -16.096 |
| w32 | 13 | -0.052983 | -22.174 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | -0.133411 | -0.265 |
| w16 | 20 | 0.088585 | 120.837 |
| w17 | 14 | -0.045079 | -12.667 |
| w18 | 16 | -0.069896 | 36.252 |
| w19 | 9 | -0.006064 | -19.531 |
| w20 | 9 | -0.069727 | -28.296 |
| w21 | 9 | 0.063701 | -19.299 |
| w22 | 21 | -0.112407 | -18.438 |
| w23 | 3 | -0.056548 | -9.591 |
| w24 | 22 | -0.013742 | 92.855 |
| w25 | 11 | 0.090441 | 10.833 |
| w26 | 11 | -0.070906 | -28.897 |
| w27 | 16 | 0.151834 | 167.6 |
| w28 | 7 | 0.004 | -1.658 |
| w29 | 15 | 0.08089 | 9.42 |
| w30 | 0 | -0.169515 | 0.0 |
| w31 | 19 | 0.002334 | -18.166 |
| w32 | 12 | -0.048252 | -42.214 |

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
| w15 | 14 | -0.071023 | 6.48 |
| w16 | 27 | -0.006427 | 122.143 |
| w17 | 13 | 0.076328 | 18.447 |
| w18 | 11 | -0.114963 | -12.758 |
| w19 | 11 | 0.044743 | 0.136 |
| w20 | 29 | -0.103825 | -29.854 |
| w21 | 11 | -0.148325 | -44.459 |
| w22 | 33 | -0.102667 | 23.584 |
| w23 | 30 | -0.039381 | -9.764 |
| w24 | 51 | -0.126319 | 32.121 |
| w25 | 18 | 0.118556 | 47.203 |
| w26 | 40 | 0.049062 | 15.51 |
| w27 | 24 | 0.115618 | 132.115 |
| w28 | 15 | -0.222534 | -13.096 |
| w29 | 46 | -0.016983 | 42.859 |
| w30 | 7 | -0.068384 | -10.71 |
| w31 | 30 | 0.059832 | 28.651 |
| w32 | 27 | 0.043638 | 9.158 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 38 | 0.060306 | 46.004 |
| w17 | 19 | 0.042622 | -11.594 |
| w18 | 22 | -0.038547 | 1.001 |
| w19 | 7 | 0.051107 | -5.277 |
| w20 | 9 | 0.043071 | -2.81 |
| w21 | 5 | -0.098392 | -13.853 |
| w22 | 18 | -0.060864 | 12.682 |
| w23 | 11 | -0.090065 | -12.712 |
| w24 | 20 | 0.018977 | 61.811 |
| w25 | 19 | 0.117243 | 6.354 |
| w26 | 14 | -0.091919 | -20.409 |
| w27 | 11 | 0.148528 | 84.185 |
| w28 | 5 | -0.072861 | -9.075 |
| w29 | 19 | -0.006672 | -3.786 |
| w30 | 10 | -0.043594 | -42.305 |
| w31 | 14 | -0.15845 | -28.47 |
| w32 | 11 | 0.023343 | -15.605 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.072414 | 13.417 |
| w21 | 5 | -0.049057 | -27.973 |
| w22 | 23 | -0.021677 | 20.817 |
| w23 | 8 | -0.002283 | -1.597 |
| w24 | 23 | 0.182462 | 146.829 |
| w25 | 14 | 0.015522 | 17.354 |
| w26 | 10 | -0.04694 | -22.187 |
| w27 | 23 | 0.041731 | 28.204 |
| w28 | 4 | -0.031473 | -7.799 |
| w29 | 16 | -0.096053 | -11.851 |
| w30 | 6 | 0.114804 | 10.6 |
| w31 | 19 | -0.036581 | -22.167 |
| w32 | 16 | -0.015005 | -8.935 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 20 | -0.078086 | 3.321 |
| w23 | 4 | -0.034127 | -5.403 |
| w24 | 30 | 0.105167 | 129.657 |
| w25 | 20 | 0.045911 | 43.215 |
| w26 | 18 | 0.011602 | -12.302 |
| w27 | 19 | 0.039235 | 18.607 |
| w28 | 3 | -0.072667 | -8.696 |
| w29 | 14 | -0.026825 | -8.3 |
| w30 | 13 | -0.026516 | -25.091 |
| w31 | 20 | -0.080522 | -21.367 |
| w32 | 14 | 0.049181 | 29.748 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 16 | -0.068333 | 23.988 |
| w25 | 19 | -0.010239 | 28.353 |
| w26 | 15 | -0.095066 | -38.285 |
| w27 | 24 | -0.041413 | 99.17 |
| w28 | 6 | 0.078488 | 3.987 |
| w29 | 21 | 0.011028 | 1.025 |
| w30 | 5 | -0.043221 | -19.386 |
| w31 | 19 | 0.031161 | -15.513 |
| w32 | 14 | 0.090829 | -14.58 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 26 | 0.130391 | 115.973 |
| w6 | 14 | -0.001062 | 17.793 |
| w7 | 10 | -0.023489 | -13.291 |
| w8 | 11 | -0.066316 | -19.641 |
| w9 | 5 | 0.033868 | -22.664 |
| w10 | 18 | 0.012491 | 8.387 |
| w11 | 18 | 0.011435 | 6.829 |
| w12 | 8 | -0.117746 | -29.213 |
| w13 | 16 | 0.069161 | 83.43 |
| w14 | 22 | -0.149059 | 42.601 |
| w15 | 11 | -0.039305 | 2.964 |
| w16 | 21 | 0.031518 | 75.403 |
| w17 | 17 | 0.004954 | -22.448 |
| w18 | 21 | -0.04056 | 5.371 |
| w19 | 14 | 0.03476 | 14.74 |
| w20 | 10 | 0.085954 | 5.929 |
| w21 | 7 | -0.075322 | -13.608 |
| w22 | 18 | -0.126452 | -9.398 |
| w23 | 6 | -0.12753 | -16.614 |
| w24 | 25 | -0.09539 | -1.006 |
| w25 | 10 | 0.108034 | 20.922 |
| w26 | 29 | 0.085085 | 22.136 |
| w27 | 25 | -0.036548 | 27.56 |
| w28 | 6 | -0.163012 | -32.617 |
| w29 | 21 | -0.016599 | -3.668 |
| w30 | 27 | 0.104204 | 329.362 |
| w31 | 13 | -0.013159 | -10.366 |
| w32 | 19 | 0.056447 | 77.085 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 24 | 0.08811 | 139.84 |
| w6 | 24 | 0.114652 | 90.018 |
| w7 | 8 | -0.02514 | -2.447 |
| w8 | 5 | -0.121996 | -11.967 |
| w9 | 6 | -0.026797 | -33.474 |
| w10 | 16 | -0.153976 | 5.296 |
| w11 | 13 | 0.027712 | 16.701 |
| w12 | 10 | -0.025072 | -21.101 |
| w13 | 21 | 0.032275 | 44.415 |
| w14 | 31 | -0.155318 | 36.977 |
| w15 | 24 | -0.070755 | 32.806 |
| w16 | 18 | 0.04882 | 57.841 |
| w17 | 19 | 0.01999 | 4.021 |
| w18 | 13 | -0.253802 | -33.588 |
| w19 | 15 | -0.009168 | -15.599 |
| w20 | 16 | 0.042768 | -2.037 |
| w21 | 16 | -0.100478 | -16.38 |
| w22 | 18 | -0.048684 | 5.585 |
| w23 | 18 | 0.08524 | 9.002 |
| w24 | 35 | -0.132914 | -0.933 |
| w25 | 14 | -0.193412 | -46.288 |
| w26 | 23 | -0.049787 | 13.929 |
| w27 | 34 | -0.052956 | -4.595 |
| w28 | 24 | -0.030611 | 32.394 |
| w29 | 12 | 0.187129 | 54.168 |
| w30 | 35 | -0.106283 | 11.593 |
| w31 | 15 | 0.088948 | 14.716 |
| w32 | 25 | 0.031257 | 40.0 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | -0.158985 | -16.648 |
| w18 | 20 | -0.155328 | 19.078 |
| w19 | 8 | -0.050428 | -25.87 |
| w20 | 9 | -0.070095 | -0.233 |
| w21 | 6 | -0.186142 | -36.974 |
| w22 | 16 | 0.015806 | 27.796 |
| w23 | 11 | -0.004096 | -2.69 |
| w24 | 21 | -0.101966 | 4.042 |
| w25 | 12 | 0.091006 | 15.148 |
| w26 | 12 | -0.041132 | -17.375 |
| w27 | 20 | 0.145952 | 159.832 |
| w28 | 12 | -0.013832 | 5.773 |
| w29 | 14 | 0.120638 | 25.61 |
| w30 | 2 | -0.052599 | -6.16 |
| w31 | 13 | -0.044654 | -28.872 |
| w32 | 24 | 0.039408 | 16.811 |

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
| w17 | 22 | -0.070845 | -11.433 |
| w18 | 16 | -0.098855 | -33.458 |
| w19 | 6 | 0.0625 | -2.791 |
| w20 | 14 | -0.006054 | -1.756 |
| w21 | 7 | -0.02061 | -30.8 |
| w22 | 25 | -0.056007 | 5.504 |
| w23 | 6 | -0.050241 | 1.905 |
| w24 | 23 | -0.10655 | 39.055 |
| w25 | 11 | 0.019907 | 2.015 |
| w26 | 24 | 0.003192 | 5.865 |
| w27 | 27 | -0.030493 | 49.564 |
| w28 | 5 | -0.088665 | -9.399 |
| w29 | 22 | -0.096207 | 19.622 |
| w30 | 7 | -0.122917 | -22.74 |
| w31 | 7 | -0.228118 | -33.615 |
| w32 | 19 | 0.026308 | 16.35 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 9 | -0.056877 | -17.099 |
| w20 | 5 | 0.047081 | 7.55 |
| w21 | 7 | -0.046397 | -9.18 |
| w22 | 35 | 0.010075 | 168.397 |
| w23 | 16 | -0.051976 | -15.748 |
| w24 | 26 | 0.092229 | 330.783 |
| w25 | 5 | -0.050082 | -12.096 |
| w26 | 13 | -0.041725 | -27.863 |
| w27 | 17 | 0.02347 | 20.881 |
| w28 | 5 | -0.060963 | -10.054 |
| w29 | 28 | -0.051684 | -13.608 |
| w30 | 3 | -0.038958 | -16.754 |
| w31 | 11 | -0.026729 | -10.591 |
| w32 | 21 | 0.053278 | 43.389 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 20 | -0.038739 | 21.033 |
| w23 | 8 | -0.170765 | -27.866 |
| w24 | 19 | -0.12344 | 25.321 |
| w25 | 11 | -0.036029 | -13.462 |
| w26 | 9 | -0.012052 | -17.68 |
| w27 | 11 | -0.016216 | -5.403 |
| w28 | 4 | -0.114066 | -16.305 |
| w29 | 17 | 0.037028 | 6.473 |
| w30 | 2 | -0.107521 | -20.076 |
| w31 | 14 | -0.060498 | -15.736 |
| w32 | 18 | 0.061767 | 9.224 |

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
| w27 | 18 | 0.097222 | 47.794 |
| w28 | 8 | -0.042873 | -7.26 |
| w29 | 15 | 0.065782 | 2.891 |
| w30 | 3 | -0.007788 | -13.913 |
| w31 | 8 | -0.102988 | -11.95 |
| w32 | 17 | 0.003842 | 45.228 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 13 | 0.088565 | 20.394 |
| w18 | 4 | 0.119372 | -2.925 |
| w19 | 3 | -0.022057 | -16.048 |
| w20 | 8 | 0.183715 | 21.338 |
| w21 | 4 | -0.051559 | -26.779 |
| w22 | 19 | -0.032845 | 18.944 |
| w23 | 7 | -0.172748 | -13.463 |
| w24 | 28 | -0.058089 | 75.229 |
| w25 | 15 | 0.114708 | 20.645 |
| w26 | 9 | -0.118323 | -33.872 |
| w27 | 14 | 0.088794 | 54.969 |
| w28 | 6 | -0.070252 | -10.812 |
| w29 | 9 | -0.042485 | -13.092 |
| w30 | 5 | -0.097913 | -26.571 |
| w31 | 17 | -0.093829 | -26.216 |
| w32 | 8 | 0.129525 | -16.041 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 14 | 0.041759 | 5.997 |
| w18 | 14 | -0.008777 | 5.998 |
| w19 | 6 | -0.012516 | -12.976 |
| w20 | 7 | 0.061382 | 0.491 |
| w21 | 8 | -0.164983 | -44.819 |
| w22 | 24 | 0.061879 | 62.521 |
| w23 | 7 | -0.171398 | -25.596 |
| w24 | 24 | -0.043326 | 43.433 |
| w25 | 22 | 0.154868 | 49.154 |
| w26 | 11 | -0.034408 | -11.463 |
| w27 | 14 | 0.053008 | 29.763 |
| w28 | 4 | -0.039435 | -8.119 |
| w29 | 11 | 0.012048 | -1.583 |
| w30 | 6 | -0.063028 | -21.136 |
| w31 | 11 | -0.16446 | -28.592 |
| w32 | 10 | -0.009299 | -29.036 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 9 | 0.098206 | 3.178 |
| w29 | 18 | 0.017374 | -1.045 |
| w30 | 8 | -0.114922 | -12.25 |
| w31 | 18 | 0.109055 | 6.805 |
| w32 | 12 | -0.037916 | -2.546 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 19 | 0.085187 | 7.926 |
| w15 | 11 | 0.027123 | 61.845 |
| w16 | 32 | -0.023464 | 494.202 |
| w17 | 13 | 0.071074 | 9.913 |
| w18 | 10 | -0.101817 | -7.408 |
| w19 | 8 | 0.009415 | -9.007 |
| w20 | 10 | 0.046337 | -0.077 |
| w21 | 9 | 0.215687 | 47.301 |
| w22 | 24 | -0.044755 | -5.343 |
| w23 | 9 | 0.005957 | 4.755 |
| w24 | 21 | 0.042183 | 39.986 |
| w25 | 15 | 0.132446 | 95.677 |
| w26 | 10 | -0.04634 | -13.041 |
| w27 | 26 | 0.180959 | 185.792 |
| w28 | 8 | -0.067348 | -14.187 |
| w29 | 12 | 0.040735 | 19.311 |
| w30 | 8 | 0.050024 | -5.991 |
| w31 | 9 | -0.030628 | -12.12 |
| w32 | 13 | 0.131805 | 8.999 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 13 | 0.242488 | 244.362 |
| w26 | 19 | 0.07811 | -0.317 |
| w27 | 24 | 0.111838 | 53.414 |
| w28 | 6 | 0.010163 | -8.935 |
| w29 | 15 | 0.037611 | 24.045 |
| w30 | 3 | -0.0527 | -16.398 |
| w31 | 10 | 0.12375 | 7.027 |
| w32 | 16 | 0.093264 | 15.292 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

