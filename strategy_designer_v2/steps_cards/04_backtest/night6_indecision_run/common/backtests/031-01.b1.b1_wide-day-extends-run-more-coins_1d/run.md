# Backtest of 031-01.b1.b1_wide-day-extends-run-more-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b1_wide-day-extends-run-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 49 | -0.07933 | -6.613 |
| w2 | 54 | 0.115673 | 46.603 |
| w3 | 70 | 0.05739 | 66.053 |
| w4 | 57 | -0.116401 | -14.982 |
| w5 | 58 | 0.055549 | 80.907 |
| w6 | 53 | 0.051577 | 59.62 |
| w7 | 39 | 0.007792 | 6.095 |
| w8 | 42 | 0.151116 | 13.342 |
| w9 | 41 | -0.014186 | -15.249 |
| w10 | 59 | -0.010372 | 17.342 |
| w11 | 56 | 0.060966 | 39.93 |
| w12 | 40 | 0.022651 | -17.203 |
| w13 | 58 | 0.015608 | 19.753 |
| w14 | 53 | -0.07584 | 8.822 |
| w15 | 62 | 0.048243 | 71.833 |
| w16 | 57 | -0.034315 | 19.579 |
| w17 | 45 | -0.003238 | -2.571 |
| w18 | 46 | 0.006847 | -5.613 |
| w19 | 41 | -0.113795 | -13.899 |
| w20 | 45 | -0.001778 | -22.338 |
| w21 | 43 | -0.092632 | -21.136 |
| w22 | 53 | 0.153968 | 99.772 |
| w23 | 48 | -0.134916 | -21.059 |
| w24 | 68 | -0.026552 | 48.233 |
| w25 | 53 | 0.020626 | 28.789 |
| w26 | 50 | -0.016624 | -1.024 |
| w27 | 66 | 0.03289 | 27.442 |
| w28 | 50 | -0.083755 | -17.511 |
| w29 | 61 | 0.002997 | -0.335 |
| w30 | 52 | 0.11911 | -1.091 |
| w31 | 46 | -0.023699 | -3.627 |
| w32 | 46 | 0.202424 | 32.059 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 52 | -0.078279 | 10.009 |
| w2 | 49 | -0.095133 | -27.875 |
| w3 | 60 | -0.120249 | -18.625 |
| w4 | 48 | -0.072394 | 2.231 |
| w5 | 59 | 0.052084 | 41.79 |
| w6 | 47 | 0.159912 | 91.673 |
| w7 | 40 | -0.048338 | -1.563 |
| w8 | 31 | 0.056697 | -15.833 |
| w9 | 34 | -0.000338 | -14.491 |
| w10 | 52 | -0.026509 | 14.13 |
| w11 | 44 | 0.074279 | 4.513 |
| w12 | 49 | 0.018204 | -10.234 |
| w13 | 60 | 0.010387 | 19.78 |
| w14 | 54 | 0.02189 | 15.249 |
| w15 | 59 | 0.012612 | 33.784 |
| w16 | 49 | 0.03603 | 28.943 |
| w17 | 45 | 0.098392 | 21.551 |
| w18 | 54 | -0.005222 | 0.911 |
| w19 | 39 | -0.042882 | -11.586 |
| w20 | 37 | -0.04173 | -12.022 |
| w21 | 45 | 0.015443 | 4.882 |
| w22 | 65 | -0.056417 | -0.889 |
| w23 | 46 | -0.052463 | -15.418 |
| w24 | 51 | -0.078479 | -5.599 |
| w25 | 55 | 0.01161 | 17.19 |
| w26 | 43 | -0.066413 | -16.98 |
| w27 | 65 | -0.039225 | 26.29 |
| w28 | 41 | -0.017148 | -15.452 |
| w29 | 45 | 0.054446 | 17.801 |
| w30 | 42 | -0.163891 | -33.786 |
| w31 | 44 | -0.06604 | -18.797 |
| w32 | 43 | 0.11179 | -6.422 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 52 | 0.090973 | 113.977 |
| w7 | 33 | 0.097469 | 11.456 |
| w8 | 34 | -0.024982 | -25.064 |
| w9 | 40 | 0.145971 | 35.634 |
| w10 | 44 | -0.080861 | -15.722 |
| w11 | 42 | 0.017205 | 4.559 |
| w12 | 34 | -0.02922 | -8.897 |
| w13 | 53 | -0.055004 | -1.069 |
| w14 | 50 | 0.202729 | 61.067 |
| w15 | 49 | 0.192193 | 104.566 |
| w16 | 58 | 0.104535 | 73.138 |
| w17 | 42 | 0.081535 | 29.756 |
| w18 | 48 | -0.067076 | -11.942 |
| w19 | 36 | -0.043366 | -1.683 |
| w20 | 21 | 0.031681 | -3.725 |
| w21 | 34 | 0.052659 | 21.286 |
| w22 | 63 | -0.048252 | 13.294 |
| w23 | 43 | 0.015384 | 28.588 |
| w24 | 57 | 0.009948 | 30.344 |
| w25 | 44 | -0.009515 | -5.364 |
| w26 | 51 | 0.019393 | -4.673 |
| w27 | 54 | 0.228771 | 192.357 |
| w28 | 36 | -0.033902 | -8.763 |
| w29 | 46 | 0.123398 | 31.29 |
| w30 | 36 | -0.027649 | -12.382 |
| w31 | 34 | -0.022014 | -9.169 |
| w32 | 39 | 0.194661 | 32.014 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 40 | 0.111209 | 20.876 |
| w8 | 31 | 0.015174 | -12.567 |
| w9 | 23 | 0.274737 | 36.529 |
| w10 | 49 | -0.008872 | 5.145 |
| w11 | 44 | -0.153552 | -15.627 |
| w12 | 41 | 0.026753 | -6.204 |
| w13 | 56 | -0.016035 | 30.202 |
| w14 | 49 | -0.05564 | 4.617 |
| w15 | 51 | -0.08126 | -27.851 |
| w16 | 55 | 0.081561 | 54.177 |
| w17 | 43 | 0.058737 | 26.579 |
| w18 | 42 | 0.007292 | -21.463 |
| w19 | 41 | 0.040199 | -21.151 |
| w20 | 32 | 0.028528 | -14.347 |
| w21 | 43 | -0.102664 | -23.833 |
| w22 | 48 | 0.04308 | 18.428 |
| w23 | 49 | 0.177601 | 48.737 |
| w24 | 50 | -0.034463 | 0.782 |
| w25 | 45 | 0.068574 | 52.307 |
| w26 | 46 | 0.055112 | -4.064 |
| w27 | 46 | -0.003884 | 4.412 |
| w28 | 44 | -0.049832 | -3.226 |
| w29 | 55 | -0.157143 | -8.995 |
| w30 | 48 | -0.166339 | -10.466 |
| w31 | 37 | -0.19792 | -35.119 |
| w32 | 37 | 0.235583 | 32.677 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | 0.142995 | 107.915 |
| w2 | 49 | 0.043227 | 7.826 |
| w3 | 39 | 0.066145 | -8.25 |
| w4 | 55 | 0.202559 | 223.305 |
| w5 | 63 | -0.021727 | 66.271 |
| w6 | 54 | 0.082206 | 34.69 |
| w7 | 43 | 0.11477 | 33.523 |
| w8 | 37 | 0.019248 | -11.283 |
| w9 | 43 | -0.025482 | -21.856 |
| w10 | 51 | -0.009504 | 5.705 |
| w11 | 50 | 0.04631 | 17.307 |
| w12 | 38 | -0.006811 | -13.698 |
| w13 | 68 | -0.014833 | 37.867 |
| w14 | 61 | 0.112908 | 60.531 |
| w15 | 55 | -0.047454 | 16.71 |
| w16 | 59 | 0.010192 | 53.371 |
| w17 | 49 | 0.057226 | 26.608 |
| w18 | 50 | -0.071541 | -9.502 |
| w19 | 44 | -0.001029 | -13.52 |
| w20 | 33 | 0.012658 | -10.886 |
| w21 | 49 | -0.014224 | -5.177 |
| w22 | 50 | 0.091291 | 46.137 |
| w23 | 46 | -0.182994 | -20.153 |
| w24 | 59 | -0.048874 | 10.257 |
| w25 | 53 | 0.102711 | 44.864 |
| w26 | 41 | 0.070218 | 0.275 |
| w27 | 55 | -0.114471 | 5.354 |
| w28 | 41 | -0.203738 | -41.112 |
| w29 | 56 | 0.036735 | 43.922 |
| w30 | 32 | -0.067725 | -24.643 |
| w31 | 49 | -0.101014 | -26.639 |
| w32 | 42 | 0.176571 | 38.531 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 46 | 0.072422 | 30.473 |
| w11 | 42 | -0.090078 | -14.382 |
| w12 | 50 | -0.064712 | -18.694 |
| w13 | 68 | 0.064436 | 44.957 |
| w14 | 53 | 0.032143 | 42.96 |
| w15 | 51 | -0.047256 | 6.86 |
| w16 | 59 | 0.053567 | 75.692 |
| w17 | 48 | 0.051051 | 69.926 |
| w18 | 35 | -0.112375 | -31.847 |
| w19 | 27 | 0.027246 | -2.566 |
| w20 | 44 | -0.037751 | -18.709 |
| w21 | 31 | 0.041545 | -14.951 |
| w22 | 64 | 0.062036 | 26.796 |
| w23 | 30 | -0.02775 | -5.352 |
| w24 | 60 | 0.1405 | 145.593 |
| w25 | 44 | 0.129803 | 8.323 |
| w26 | 38 | -0.023389 | -14.419 |
| w27 | 56 | 0.215337 | 96.996 |
| w28 | 35 | -0.095001 | -12.822 |
| w29 | 42 | 0.106153 | 29.296 |
| w30 | 37 | -0.077651 | -29.485 |
| w31 | 38 | -0.184106 | -31.493 |
| w32 | 44 | 0.260485 | 54.76 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 55 | -0.00336 | 19.503 |
| w13 | 52 | -0.036746 | -14.958 |
| w14 | 56 | 0.093067 | 82.712 |
| w15 | 47 | 0.011076 | 12.701 |
| w16 | 56 | -0.035293 | 36.852 |
| w17 | 59 | 0.086756 | 31.756 |
| w18 | 49 | -0.116465 | -13.751 |
| w19 | 34 | -0.005699 | -12.858 |
| w20 | 40 | -0.018872 | -20.435 |
| w21 | 45 | 0.01547 | -2.571 |
| w22 | 53 | 0.087233 | 22.011 |
| w23 | 31 | -0.084982 | -25.115 |
| w24 | 47 | 0.052974 | 20.643 |
| w25 | 42 | 0.120587 | 15.794 |
| w26 | 38 | -0.049971 | -27.311 |
| w27 | 44 | 0.064323 | 18.44 |
| w28 | 42 | -0.189191 | -28.333 |
| w29 | 40 | 0.073098 | 0.464 |
| w30 | 23 | -0.031196 | -16.372 |
| w31 | 48 | 0.063713 | -2.134 |
| w32 | 40 | 0.091829 | 3.648 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 40 | -0.013031 | -6.309 |
| w16 | 48 | 0.047977 | 34.005 |
| w17 | 40 | -0.010293 | -2.685 |
| w18 | 56 | 0.084784 | 35.501 |
| w19 | 32 | 0.068369 | -11.399 |
| w20 | 36 | -0.042077 | -19.176 |
| w21 | 38 | 0.052058 | -0.414 |
| w22 | 51 | -0.0125 | -10.128 |
| w23 | 35 | -0.140807 | -38.955 |
| w24 | 54 | 0.069905 | 52.45 |
| w25 | 47 | 0.143636 | 8.103 |
| w26 | 40 | 0.034851 | -14.821 |
| w27 | 52 | 0.150093 | 67.937 |
| w28 | 40 | -0.005939 | -15.279 |
| w29 | 36 | 0.072827 | 16.49 |
| w30 | 32 | -0.124354 | -23.198 |
| w31 | 39 | 0.055737 | -5.203 |
| w32 | 38 | 0.145061 | 11.375 |

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
| w15 | 40 | -0.062492 | -23.152 |
| w16 | 59 | -0.067614 | 37.918 |
| w17 | 39 | 0.055946 | 13.944 |
| w18 | 39 | -0.120699 | -20.655 |
| w19 | 44 | 0.066041 | 6.684 |
| w20 | 45 | -0.011903 | -3.244 |
| w21 | 48 | -0.169666 | -31.046 |
| w22 | 59 | -0.137276 | -0.913 |
| w23 | 53 | -0.043107 | -11.101 |
| w24 | 72 | 0.062299 | 45.885 |
| w25 | 53 | -0.00279 | 3.61 |
| w26 | 59 | 0.186446 | 39.554 |
| w27 | 60 | 0.053078 | 97.073 |
| w28 | 41 | -0.170706 | -18.56 |
| w29 | 58 | -0.124591 | 10.223 |
| w30 | 53 | -0.067178 | -10.971 |
| w31 | 67 | -0.076736 | 18.248 |
| w32 | 59 | 0.130975 | 12.636 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 59 | 0.048162 | 31.807 |
| w17 | 56 | 0.077587 | 25.527 |
| w18 | 37 | -0.054452 | -16.477 |
| w19 | 49 | 0.03458 | -16.45 |
| w20 | 38 | -0.025815 | -21.371 |
| w21 | 41 | -0.140651 | -30.28 |
| w22 | 49 | 0.053412 | 21.127 |
| w23 | 39 | -0.131 | -23.415 |
| w24 | 49 | -0.004394 | 43.473 |
| w25 | 44 | 0.127648 | 11.71 |
| w26 | 40 | -0.072346 | -27.185 |
| w27 | 50 | 0.120744 | 40.855 |
| w28 | 41 | -0.089702 | -26.335 |
| w29 | 37 | 0.062929 | -0.362 |
| w30 | 36 | -0.085187 | -22.346 |
| w31 | 26 | -0.107764 | -20.933 |
| w32 | 37 | 0.169795 | 7.333 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 34 | 0.031267 | -15.093 |
| w21 | 43 | -0.073243 | -28.517 |
| w22 | 58 | 0.094704 | 47.483 |
| w23 | 25 | -0.003363 | -16.222 |
| w24 | 56 | 0.200294 | 152.442 |
| w25 | 43 | 0.094984 | 10.211 |
| w26 | 44 | 0.017164 | -3.097 |
| w27 | 52 | 0.033512 | 26.161 |
| w28 | 36 | -0.086307 | -14.694 |
| w29 | 52 | -0.036123 | -2.999 |
| w30 | 43 | 0.035382 | -18.961 |
| w31 | 39 | -0.104733 | -24.306 |
| w32 | 41 | 0.008966 | 0.974 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 51 | -0.017041 | 26.608 |
| w23 | 36 | -0.0356 | -25.183 |
| w24 | 49 | 0.13255 | 99.987 |
| w25 | 52 | 0.079991 | 36.795 |
| w26 | 47 | -0.022055 | -7.235 |
| w27 | 52 | 0.075117 | 17.167 |
| w28 | 33 | -0.047165 | -17.593 |
| w29 | 38 | 0.007457 | -3.739 |
| w30 | 40 | 0.011056 | -8.518 |
| w31 | 37 | -0.020432 | -8.841 |
| w32 | 33 | 0.082552 | 54.995 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 47 | 0.030485 | 32.864 |
| w25 | 46 | -0.008278 | 27.146 |
| w26 | 35 | 0.034672 | 0.072 |
| w27 | 60 | 0.088502 | 74.158 |
| w28 | 35 | 0.039932 | 2.419 |
| w29 | 48 | 0.004366 | -4.415 |
| w30 | 34 | -0.009357 | -16.086 |
| w31 | 35 | -0.011303 | -12.633 |
| w32 | 49 | 0.199361 | 45.137 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 47 | 0.094113 | 90.133 |
| w6 | 43 | -0.023719 | 9.408 |
| w7 | 33 | 0.118583 | 11.992 |
| w8 | 31 | 0.049215 | 3.247 |
| w9 | 38 | 0.056411 | -21.144 |
| w10 | 38 | 0.034576 | 9.817 |
| w11 | 38 | 0.053653 | 19.619 |
| w12 | 31 | -0.072823 | -21.136 |
| w13 | 55 | 0.115625 | 67.315 |
| w14 | 52 | -0.10007 | 6.789 |
| w15 | 46 | -0.002654 | -17.057 |
| w16 | 49 | 0.109091 | 67.052 |
| w17 | 47 | 0.110628 | 23.413 |
| w18 | 39 | -0.015643 | 10.968 |
| w19 | 42 | 0.050531 | 10.717 |
| w20 | 37 | -0.018754 | -15.684 |
| w21 | 44 | -0.130706 | -35.855 |
| w22 | 55 | -0.119961 | -9.336 |
| w23 | 39 | 0.042802 | -10.069 |
| w24 | 58 | -0.007703 | 8.604 |
| w25 | 44 | 0.176297 | 22.944 |
| w26 | 54 | 0.095838 | 9.834 |
| w27 | 49 | -0.011774 | 17.483 |
| w28 | 39 | -0.069235 | -12.216 |
| w29 | 44 | 0.034852 | 9.821 |
| w30 | 56 | 0.121648 | 164.415 |
| w31 | 36 | 0.014354 | -4.103 |
| w32 | 48 | 0.223431 | 103.52 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 54 | 0.08499 | 121.182 |
| w6 | 41 | 0.046397 | 38.411 |
| w7 | 31 | 0.027009 | -7.599 |
| w8 | 35 | 0.072432 | -5.523 |
| w9 | 33 | 0.070718 | -6.628 |
| w10 | 45 | -0.096501 | 0.935 |
| w11 | 50 | 0.047535 | 9.678 |
| w12 | 39 | -0.168347 | -24.52 |
| w13 | 57 | 0.039277 | 39.987 |
| w14 | 66 | -0.188119 | 3.089 |
| w15 | 62 | -0.04813 | 3.177 |
| w16 | 59 | 0.033106 | 63.977 |
| w17 | 48 | 0.040791 | 9.792 |
| w18 | 39 | -0.105374 | -25.529 |
| w19 | 45 | -0.114574 | -14.329 |
| w20 | 43 | -0.078945 | -12.563 |
| w21 | 51 | -0.140564 | -7.189 |
| w22 | 56 | -0.08059 | -9.866 |
| w23 | 40 | 0.016717 | -18.256 |
| w24 | 50 | -0.012275 | 6.481 |
| w25 | 46 | -0.059862 | -12.682 |
| w26 | 52 | 0.055165 | 14.329 |
| w27 | 41 | -0.079677 | 12.372 |
| w28 | 52 | -0.016446 | 5.101 |
| w29 | 45 | -0.114089 | -12.779 |
| w30 | 49 | -0.200785 | -4.395 |
| w31 | 39 | 0.041218 | 3.346 |
| w32 | 61 | -0.138243 | -9.053 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 45 | -0.072244 | -6.259 |
| w18 | 48 | 0.017165 | 19.122 |
| w19 | 51 | 0.076949 | -4.949 |
| w20 | 46 | -0.079937 | -20.135 |
| w21 | 35 | -0.116499 | -32.037 |
| w22 | 52 | 0.046 | 20.076 |
| w23 | 37 | -0.098998 | -19.807 |
| w24 | 56 | 0.029534 | 10.391 |
| w25 | 47 | 0.156675 | 22.784 |
| w26 | 45 | -0.016285 | -18.16 |
| w27 | 50 | 0.144341 | 82.62 |
| w28 | 40 | -0.188013 | -17.765 |
| w29 | 33 | 0.147409 | 29.785 |
| w30 | 35 | -0.10902 | -17.802 |
| w31 | 37 | -0.062304 | -16.307 |
| w32 | 48 | 0.172 | 69.227 |

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
| w17 | 42 | 0.060533 | 14.522 |
| w18 | 48 | 0.016119 | -19.085 |
| w19 | 43 | 0.054745 | 5.478 |
| w20 | 40 | -0.020629 | -8.251 |
| w21 | 56 | -0.136621 | -38.43 |
| w22 | 44 | 0.053001 | 26.675 |
| w23 | 49 | 0.023478 | -3.48 |
| w24 | 52 | 0.021791 | 68.262 |
| w25 | 47 | 0.021466 | 8.017 |
| w26 | 43 | 0.017887 | 10.813 |
| w27 | 59 | 0.016502 | 35.568 |
| w28 | 37 | -0.054054 | -10.999 |
| w29 | 57 | -0.003077 | 31.265 |
| w30 | 32 | -0.101042 | -25.046 |
| w31 | 34 | -0.083326 | -10.601 |
| w32 | 38 | 0.108528 | 51.87 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 37 | 0.012379 | 5.174 |
| w20 | 35 | -0.030803 | -17.383 |
| w21 | 47 | -0.074935 | -3.421 |
| w22 | 61 | -0.009194 | 71.964 |
| w23 | 44 | 0.130401 | 7.147 |
| w24 | 60 | 0.195504 | 176.842 |
| w25 | 39 | -0.062753 | -16.519 |
| w26 | 43 | -0.03726 | -21.393 |
| w27 | 54 | 0.020652 | 12.218 |
| w28 | 43 | -0.120306 | -22.601 |
| w29 | 51 | -0.054429 | -5.357 |
| w30 | 33 | -0.06896 | -18.606 |
| w31 | 36 | -0.045771 | -14.071 |
| w32 | 48 | -0.054315 | 5.625 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 45 | -0.019374 | 6.326 |
| w23 | 45 | -0.014445 | -9.945 |
| w24 | 48 | -0.127724 | 2.329 |
| w25 | 45 | -0.076464 | -24.133 |
| w26 | 39 | 0.008271 | -5.65 |
| w27 | 48 | -0.100301 | -12.512 |
| w28 | 37 | -0.040245 | -8.656 |
| w29 | 45 | 0.026431 | 13.485 |
| w30 | 39 | 0.019446 | -8.782 |
| w31 | 46 | -0.061254 | -18.717 |
| w32 | 43 | 0.138524 | 30.872 |

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
| w27 | 47 | 0.087284 | 44.382 |
| w28 | 43 | -0.134328 | -19.319 |
| w29 | 46 | -0.009139 | -11.882 |
| w30 | 30 | 0.031023 | -11.817 |
| w31 | 39 | -0.167014 | -30.719 |
| w32 | 41 | 0.11813 | 70.481 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 44 | 0.024009 | 5.786 |
| w18 | 37 | -0.04698 | -23.999 |
| w19 | 38 | 0.027339 | -19.162 |
| w20 | 28 | 0.088619 | 13.679 |
| w21 | 41 | -0.042094 | -17.397 |
| w22 | 55 | 0.052718 | 37.13 |
| w23 | 42 | -0.029353 | -21.297 |
| w24 | 60 | -0.103438 | 9.137 |
| w25 | 37 | 0.149808 | 22.058 |
| w26 | 47 | 0.016155 | -12.591 |
| w27 | 57 | -0.062738 | -7.364 |
| w28 | 43 | -0.15465 | -31.117 |
| w29 | 41 | -0.053561 | -20.894 |
| w30 | 28 | 0.106605 | -4.361 |
| w31 | 40 | -0.0947 | -20.56 |
| w32 | 36 | 0.044191 | 10.54 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 36 | 0.054046 | 4.824 |
| w18 | 48 | -0.158468 | -25.831 |
| w19 | 41 | 0.045088 | -18.35 |
| w20 | 37 | 0.028053 | -4.125 |
| w21 | 41 | 0.043914 | -8.897 |
| w22 | 44 | 0.059698 | 61.577 |
| w23 | 36 | 0.046309 | -21.947 |
| w24 | 52 | 0.017645 | 47.879 |
| w25 | 49 | 0.110844 | 51.676 |
| w26 | 41 | 0.012928 | -2.119 |
| w27 | 50 | 0.099785 | 22.651 |
| w28 | 36 | -0.022638 | -19.164 |
| w29 | 40 | 0.02601 | -12.808 |
| w30 | 29 | -0.08091 | -20.755 |
| w31 | 36 | -0.143918 | -32.841 |
| w32 | 36 | 0.203409 | 12.036 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 43 | 0.032998 | 2.936 |
| w29 | 40 | -0.015303 | 10.611 |
| w30 | 35 | -0.022178 | -7.357 |
| w31 | 48 | 0.069574 | 14.277 |
| w32 | 41 | 0.108121 | 29.815 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 44 | 0.089643 | 51.097 |
| w15 | 48 | 0.038729 | 35.436 |
| w16 | 39 | 0.017741 | 248.213 |
| w17 | 36 | 0.008276 | 3.627 |
| w18 | 38 | -0.131785 | -31.67 |
| w19 | 38 | -0.030295 | -10.028 |
| w20 | 40 | -0.015556 | -7.736 |
| w21 | 31 | 0.239914 | 100.565 |
| w22 | 54 | 0.120557 | 19.371 |
| w23 | 47 | -0.064314 | -9.54 |
| w24 | 52 | -0.002664 | 23.592 |
| w25 | 47 | 0.163472 | 64.09 |
| w26 | 42 | 0.027573 | -2.857 |
| w27 | 51 | 0.14713 | 90.93 |
| w28 | 35 | -0.071571 | -18.288 |
| w29 | 45 | 0.0584 | 23.415 |
| w30 | 30 | 0.025483 | -11.621 |
| w31 | 48 | -0.088839 | -18.092 |
| w32 | 33 | 0.101564 | 5.066 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 41 | 0.287654 | 219.961 |
| w26 | 42 | 0.078706 | 9.926 |
| w27 | 44 | 0.105626 | 38.087 |
| w28 | 44 | -0.110989 | -22.16 |
| w29 | 39 | 0.074429 | 7.658 |
| w30 | 37 | -0.012277 | -12.365 |
| w31 | 38 | -0.024002 | -0.385 |
| w32 | 51 | 0.180888 | 25.953 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

