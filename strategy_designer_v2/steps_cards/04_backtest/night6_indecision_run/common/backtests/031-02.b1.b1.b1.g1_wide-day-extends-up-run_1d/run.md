# Backtest of 031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g1_wide-day-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 62 | -0.017136 | -3.821 |
| w2 | 54 | 0.150256 | 46.068 |
| w3 | 72 | 0.06586 | 67.029 |
| w4 | 59 | -0.210656 | -26.31 |
| w5 | 64 | -0.024872 | 70.578 |
| w6 | 57 | 0.102085 | 74.247 |
| w7 | 39 | 0.001491 | -5.052 |
| w8 | 37 | 0.209126 | 30.655 |
| w9 | 44 | 0.062693 | -10.811 |
| w10 | 56 | -0.019622 | 19.098 |
| w11 | 57 | 0.07006 | 48.809 |
| w12 | 41 | -0.001223 | -12.476 |
| w13 | 60 | -0.001593 | 10.857 |
| w14 | 51 | -0.015406 | 16.745 |
| w15 | 64 | -0.051463 | 61.774 |
| w16 | 55 | -0.036358 | 19.219 |
| w17 | 49 | 0.009725 | -1.758 |
| w18 | 46 | -0.013691 | -4.414 |
| w19 | 41 | 0.051193 | 1.145 |
| w20 | 41 | -0.022307 | -21.143 |
| w21 | 47 | -0.086168 | -18.824 |
| w22 | 56 | 0.086092 | 69.545 |
| w23 | 48 | -0.056685 | -17.007 |
| w24 | 70 | -0.068299 | 48.51 |
| w25 | 55 | 0.006647 | 24.033 |
| w26 | 48 | -0.003764 | -4.193 |
| w27 | 62 | 0.019352 | 51.465 |
| w28 | 52 | -0.169435 | -25.516 |
| w29 | 57 | 0.031865 | 13.049 |
| w30 | 46 | 0.040735 | -11.143 |
| w31 | 52 | 0.021792 | 1.68 |
| w32 | 48 | 0.191001 | 32.68 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 53 | -0.021697 | 4.267 |
| w2 | 51 | -0.06159 | -21.707 |
| w3 | 52 | 0.083986 | 10.865 |
| w4 | 52 | -0.111482 | -6.052 |
| w5 | 55 | 0.052464 | 39.745 |
| w6 | 45 | 0.173896 | 102.714 |
| w7 | 33 | -0.043953 | -5.787 |
| w8 | 35 | -0.039249 | -17.521 |
| w9 | 34 | -0.01564 | -22.474 |
| w10 | 54 | -0.038803 | 29.552 |
| w11 | 43 | -0.022601 | -2.204 |
| w12 | 40 | 0.048445 | -6.969 |
| w13 | 60 | 0.001751 | 14.333 |
| w14 | 50 | 0.004984 | 13.363 |
| w15 | 57 | 0.002749 | 28.971 |
| w16 | 46 | 0.045326 | 26.304 |
| w17 | 45 | 0.103253 | 27.396 |
| w18 | 55 | 0.023148 | 3.929 |
| w19 | 42 | 0.062936 | -5.782 |
| w20 | 35 | -0.086869 | -31.654 |
| w21 | 51 | 0.021352 | 6.322 |
| w22 | 60 | -0.182188 | -15.366 |
| w23 | 36 | -0.048095 | -10.075 |
| w24 | 51 | -0.052916 | -4.288 |
| w25 | 52 | 0.01034 | 5.123 |
| w26 | 37 | -0.016285 | -13.193 |
| w27 | 66 | -0.019006 | 27.807 |
| w28 | 37 | -0.0679 | -15.999 |
| w29 | 46 | 0.087209 | 18.338 |
| w30 | 42 | -0.181434 | -34.426 |
| w31 | 42 | -0.083526 | -16.249 |
| w32 | 37 | 0.13844 | 13.042 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 56 | 0.054943 | 87.78 |
| w7 | 34 | 0.093321 | 12.367 |
| w8 | 37 | 0.010787 | -18.242 |
| w9 | 33 | 0.215219 | 47.225 |
| w10 | 41 | -0.144471 | -16.057 |
| w11 | 45 | 0.005117 | 14.797 |
| w12 | 41 | -0.065705 | -12.993 |
| w13 | 58 | -0.031146 | 11.99 |
| w14 | 46 | 0.176513 | 56.983 |
| w15 | 44 | 0.173356 | 100.473 |
| w16 | 45 | 0.128865 | 68.952 |
| w17 | 40 | 0.151643 | 37.835 |
| w18 | 40 | 0.004804 | -3.383 |
| w19 | 41 | 0.03918 | 4.347 |
| w20 | 21 | -0.05388 | -17.854 |
| w21 | 35 | -0.024772 | 12.693 |
| w22 | 55 | -0.016914 | -1.925 |
| w23 | 43 | -0.003122 | 18.107 |
| w24 | 56 | 0.032003 | 30.107 |
| w25 | 37 | -0.082789 | -25.254 |
| w26 | 48 | 0.037212 | -0.212 |
| w27 | 53 | 0.200142 | 164.475 |
| w28 | 37 | -0.03045 | -11.836 |
| w29 | 42 | 0.128416 | 27.516 |
| w30 | 31 | 0.027689 | -5.656 |
| w31 | 41 | 0.005601 | -2.545 |
| w32 | 37 | 0.217705 | 40.431 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 33 | 0.088944 | 22.708 |
| w8 | 33 | -0.039553 | -20.796 |
| w9 | 21 | 0.308673 | 51.222 |
| w10 | 45 | 0.029063 | 16.599 |
| w11 | 45 | -0.139298 | -14.281 |
| w12 | 39 | 0.075129 | 3.492 |
| w13 | 50 | -0.03247 | 25.574 |
| w14 | 50 | -0.013617 | 8.824 |
| w15 | 54 | -0.117449 | -34.043 |
| w16 | 54 | 0.104801 | 56.091 |
| w17 | 48 | 0.134764 | 33.07 |
| w18 | 47 | -0.000282 | -19.096 |
| w19 | 47 | 0.117283 | 0.358 |
| w20 | 33 | 0.073274 | -1.869 |
| w21 | 47 | -0.019363 | -20.294 |
| w22 | 46 | 0.02717 | 13.522 |
| w23 | 44 | 0.223253 | 51.57 |
| w24 | 53 | -0.025242 | 0.326 |
| w25 | 45 | 0.095469 | 46.408 |
| w26 | 40 | -0.022001 | -15.863 |
| w27 | 45 | -0.012937 | 18.802 |
| w28 | 48 | -0.053078 | -12.206 |
| w29 | 48 | -0.17969 | -12.63 |
| w30 | 43 | -0.006958 | 0.141 |
| w31 | 44 | -0.149662 | -22.403 |
| w32 | 31 | 0.223188 | 34.515 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | 0.128476 | 106.173 |
| w2 | 43 | -0.054375 | -4.786 |
| w3 | 36 | -0.018783 | -13.38 |
| w4 | 50 | 0.176224 | 220.657 |
| w5 | 55 | -0.002813 | 74.598 |
| w6 | 55 | 0.017891 | 47.179 |
| w7 | 39 | 0.149328 | 38.619 |
| w8 | 34 | -0.017062 | -14.659 |
| w9 | 39 | 0.137022 | 12.028 |
| w10 | 44 | -0.062745 | 2.312 |
| w11 | 47 | 0.024057 | 21.3 |
| w12 | 39 | -0.00322 | -8.157 |
| w13 | 64 | 0.015009 | 48.987 |
| w14 | 54 | 0.091533 | 51.657 |
| w15 | 61 | -0.051481 | 19.395 |
| w16 | 62 | 0.039846 | 67.773 |
| w17 | 42 | 0.10669 | 40.82 |
| w18 | 54 | -0.043826 | -2.68 |
| w19 | 43 | 0.100465 | -3.023 |
| w20 | 30 | 0.012309 | -13.539 |
| w21 | 52 | 0.044176 | 3.719 |
| w22 | 56 | 0.043904 | 37.919 |
| w23 | 46 | -0.155446 | -22.549 |
| w24 | 60 | -0.00099 | 17.051 |
| w25 | 54 | 0.157384 | 37.665 |
| w26 | 38 | 0.068531 | -3.503 |
| w27 | 52 | -0.037348 | 24.364 |
| w28 | 39 | -0.178487 | -33.286 |
| w29 | 59 | 0.036473 | 47.199 |
| w30 | 37 | -0.053721 | -13.047 |
| w31 | 54 | -0.076241 | -24.158 |
| w32 | 53 | 0.210616 | 42.716 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 45 | 0.044931 | 26.672 |
| w11 | 39 | -0.064685 | -9.391 |
| w12 | 49 | -0.064297 | -13.335 |
| w13 | 66 | 0.049356 | 35.163 |
| w14 | 49 | 0.058372 | 40.586 |
| w15 | 47 | -0.005272 | 11.328 |
| w16 | 56 | 0.073512 | 88.967 |
| w17 | 48 | 0.126789 | 78.218 |
| w18 | 36 | -0.228101 | -35.817 |
| w19 | 31 | 0.08369 | -0.63 |
| w20 | 42 | -0.060753 | -37.076 |
| w21 | 33 | 0.001448 | -24.915 |
| w22 | 58 | 0.007031 | 16.287 |
| w23 | 30 | -0.029352 | -11.053 |
| w24 | 62 | 0.136658 | 153.198 |
| w25 | 42 | 0.103796 | 3.116 |
| w26 | 34 | -0.00714 | -10.134 |
| w27 | 50 | 0.211365 | 97.126 |
| w28 | 40 | -0.090851 | -12.116 |
| w29 | 40 | 0.155543 | 23.793 |
| w30 | 38 | -0.096834 | -24.129 |
| w31 | 39 | -0.082704 | -22.245 |
| w32 | 43 | 0.247649 | 52.841 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 54 | -0.020099 | 23.873 |
| w13 | 47 | 0.020323 | -9.181 |
| w14 | 52 | 0.11359 | 88.092 |
| w15 | 44 | 0.023991 | 10.243 |
| w16 | 53 | 0.00445 | 24.007 |
| w17 | 60 | 0.069828 | 23.257 |
| w18 | 49 | -0.12737 | -10.044 |
| w19 | 29 | 0.002617 | -5.349 |
| w20 | 38 | 0.023666 | -4.498 |
| w21 | 46 | -0.02706 | -8.667 |
| w22 | 54 | 0.001516 | 13.031 |
| w23 | 32 | -0.099498 | -30.934 |
| w24 | 51 | -0.072502 | 2.231 |
| w25 | 46 | 0.137529 | 14.091 |
| w26 | 34 | -0.125085 | -31.326 |
| w27 | 40 | 0.121861 | 37.985 |
| w28 | 38 | -0.233384 | -26.322 |
| w29 | 43 | 0.069223 | 0.114 |
| w30 | 21 | -0.031213 | -6.695 |
| w31 | 51 | 0.048984 | 1.969 |
| w32 | 38 | 0.007956 | 3.864 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 33 | -0.077681 | -15.905 |
| w16 | 47 | 0.039283 | 40.299 |
| w17 | 52 | -0.034354 | -4.313 |
| w18 | 55 | 0.10041 | 41.356 |
| w19 | 33 | 0.09095 | -14.297 |
| w20 | 37 | -0.086423 | -24.903 |
| w21 | 38 | 0.037428 | -8.918 |
| w22 | 52 | -0.032422 | -5.072 |
| w23 | 33 | -0.087597 | -36.144 |
| w24 | 53 | 0.002547 | 47.411 |
| w25 | 43 | 0.189536 | 25.299 |
| w26 | 38 | -0.000444 | -3.173 |
| w27 | 52 | 0.154274 | 52.027 |
| w28 | 39 | -0.05935 | -18.647 |
| w29 | 41 | 0.04365 | 12.999 |
| w30 | 30 | -0.037017 | -11.709 |
| w31 | 42 | 0.054576 | -4.064 |
| w32 | 40 | 0.058212 | -1.392 |

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
| w15 | 44 | -0.121367 | -24.729 |
| w16 | 57 | -0.109392 | 35.475 |
| w17 | 43 | 0.103409 | 11.233 |
| w18 | 39 | -0.108151 | -21.134 |
| w19 | 46 | 0.010296 | -5.178 |
| w20 | 41 | 0.008462 | -0.428 |
| w21 | 53 | -0.115198 | -22.72 |
| w22 | 60 | -0.125692 | 1.081 |
| w23 | 54 | 0.024885 | -0.893 |
| w24 | 75 | 0.080769 | 51.715 |
| w25 | 52 | 0.038225 | 14.288 |
| w26 | 66 | 0.19707 | 49.338 |
| w27 | 59 | 0.042314 | 85.606 |
| w28 | 51 | -0.17135 | -17.152 |
| w29 | 66 | -0.079104 | 12.308 |
| w30 | 46 | -0.05886 | -8.684 |
| w31 | 65 | -0.122538 | 13.867 |
| w32 | 61 | 0.117592 | 12.871 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 54 | 0.053049 | 33.119 |
| w17 | 61 | 0.112547 | 41.405 |
| w18 | 39 | -0.071517 | -12.436 |
| w19 | 44 | 0.089525 | -12.817 |
| w20 | 33 | 0.038736 | -3.888 |
| w21 | 40 | -0.223669 | -34.87 |
| w22 | 49 | 0.027015 | 15.374 |
| w23 | 43 | -0.04752 | -12.974 |
| w24 | 44 | -0.002597 | 48.33 |
| w25 | 45 | 0.108994 | 6.495 |
| w26 | 44 | -0.035022 | -18.036 |
| w27 | 46 | 0.123287 | 48.321 |
| w28 | 35 | -0.172266 | -20.855 |
| w29 | 37 | 0.08652 | 7.488 |
| w30 | 34 | -0.008406 | -10.506 |
| w31 | 33 | -0.116859 | -22.3 |
| w32 | 38 | 0.15898 | 5.334 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 34 | 0.073906 | -8.761 |
| w21 | 43 | -0.034745 | -15.209 |
| w22 | 61 | 0.086652 | 38.864 |
| w23 | 27 | -0.009932 | -14.669 |
| w24 | 51 | 0.205146 | 152.594 |
| w25 | 46 | 0.064802 | 14.872 |
| w26 | 44 | 0.067691 | 1.715 |
| w27 | 51 | 0.104277 | 40.657 |
| w28 | 36 | -0.09915 | -21.405 |
| w29 | 48 | -0.01541 | -4.705 |
| w30 | 43 | 0.048281 | -13.509 |
| w31 | 41 | -0.097572 | -22.414 |
| w32 | 46 | 0.098869 | 1.706 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 47 | 0.012485 | 20.077 |
| w23 | 36 | 0.062265 | -5.239 |
| w24 | 54 | 0.154137 | 132.473 |
| w25 | 50 | 0.124591 | 54.684 |
| w26 | 43 | -0.002246 | -11.06 |
| w27 | 45 | 0.118392 | 33.27 |
| w28 | 31 | -0.067787 | -17.124 |
| w29 | 34 | -0.006326 | 1.452 |
| w30 | 36 | 0.070561 | 0.571 |
| w31 | 38 | -0.002737 | -8.406 |
| w32 | 31 | 0.028927 | 44.307 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 46 | -0.03386 | 15.31 |
| w25 | 47 | -0.032792 | 5.561 |
| w26 | 30 | 0.034551 | -1.334 |
| w27 | 63 | 0.059456 | 83.61 |
| w28 | 31 | -0.027139 | -9.182 |
| w29 | 42 | -0.0335 | -5.653 |
| w30 | 35 | -0.006403 | -13.563 |
| w31 | 41 | 0.018287 | -3.83 |
| w32 | 47 | 0.17183 | 37.724 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 55 | 0.143651 | 106.954 |
| w6 | 40 | -0.008172 | 16.255 |
| w7 | 34 | 0.077209 | 1.338 |
| w8 | 33 | 0.076736 | 6.809 |
| w9 | 38 | 0.056144 | -14.901 |
| w10 | 41 | -0.024276 | 6.807 |
| w11 | 33 | 0.012787 | 10.978 |
| w12 | 31 | -0.127856 | -25.027 |
| w13 | 56 | 0.125451 | 79.481 |
| w14 | 57 | -0.127359 | 4.78 |
| w15 | 47 | -0.156548 | -26.785 |
| w16 | 49 | 0.106708 | 62.136 |
| w17 | 43 | 0.130064 | 29.018 |
| w18 | 36 | -0.044766 | 3.146 |
| w19 | 42 | 0.056117 | 12.106 |
| w20 | 33 | -0.031241 | -14.719 |
| w21 | 43 | -0.195973 | -32.647 |
| w22 | 50 | -0.170007 | -2.815 |
| w23 | 40 | 0.015612 | -21.936 |
| w24 | 58 | -0.021682 | 1.424 |
| w25 | 40 | 0.163669 | 19.657 |
| w26 | 52 | 0.089544 | 10.899 |
| w27 | 48 | 0.010426 | 23.658 |
| w28 | 43 | -0.090437 | -15.387 |
| w29 | 40 | 0.021166 | 9.171 |
| w30 | 55 | 0.184533 | 185.06 |
| w31 | 39 | 0.051138 | 1.91 |
| w32 | 42 | 0.187635 | 74.159 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 60 | 0.108188 | 143.332 |
| w6 | 38 | 0.072886 | 67.59 |
| w7 | 36 | 0.010212 | 0.083 |
| w8 | 35 | 0.0449 | -2.671 |
| w9 | 42 | 0.087172 | -5.42 |
| w10 | 43 | -0.098927 | 7.216 |
| w11 | 51 | 0.014302 | 6.089 |
| w12 | 34 | -0.134501 | -20.71 |
| w13 | 60 | 0.025798 | 28.406 |
| w14 | 64 | -0.183823 | 2.076 |
| w15 | 60 | -0.185025 | -3.816 |
| w16 | 54 | 0.011511 | 49.704 |
| w17 | 47 | 0.072728 | 12.69 |
| w18 | 40 | -0.098567 | -27.373 |
| w19 | 51 | -0.043323 | -8.493 |
| w20 | 47 | -0.029241 | -16.391 |
| w21 | 55 | -0.124398 | -9.736 |
| w22 | 61 | -0.118539 | -19.239 |
| w23 | 35 | 0.033614 | -1.962 |
| w24 | 56 | -0.074265 | -2.048 |
| w25 | 51 | -0.026687 | -10.843 |
| w26 | 51 | 0.116672 | 25.226 |
| w27 | 44 | -0.078878 | 7.004 |
| w28 | 55 | -0.014791 | 22.69 |
| w29 | 41 | -0.012965 | 1.003 |
| w30 | 51 | -0.068523 | 17.345 |
| w31 | 40 | 0.011755 | 6.483 |
| w32 | 60 | -0.104229 | -5.71 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 51 | -0.023922 | 2.879 |
| w18 | 44 | -0.02962 | 19.062 |
| w19 | 51 | 0.045005 | -9.201 |
| w20 | 49 | -0.135412 | -24.037 |
| w21 | 40 | -0.107549 | -34.802 |
| w22 | 56 | 0.047674 | 19.816 |
| w23 | 38 | -0.011112 | -13.186 |
| w24 | 59 | 0.072779 | 23.771 |
| w25 | 45 | 0.185401 | 28.587 |
| w26 | 41 | 0.034965 | -7.354 |
| w27 | 48 | 0.118564 | 57.249 |
| w28 | 36 | -0.09797 | -10.018 |
| w29 | 39 | 0.092548 | 19.011 |
| w30 | 37 | -0.086097 | -15.249 |
| w31 | 41 | -0.008643 | -12.489 |
| w32 | 51 | 0.068813 | 27.732 |

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
| w17 | 37 | 0.066206 | 12.877 |
| w18 | 49 | -0.022179 | -18.965 |
| w19 | 40 | 0.123629 | 7.348 |
| w20 | 38 | 0.049645 | -2.021 |
| w21 | 52 | -0.124152 | -37.745 |
| w22 | 49 | 0.06192 | 23.869 |
| w23 | 44 | -0.072583 | -14.471 |
| w24 | 53 | 0.029192 | 63.815 |
| w25 | 51 | 0.123091 | 10.818 |
| w26 | 42 | 0.029552 | 15.147 |
| w27 | 59 | -0.03803 | 20.761 |
| w28 | 35 | -0.056419 | -11.633 |
| w29 | 61 | 0.010561 | 35.109 |
| w30 | 34 | -0.028217 | -20.852 |
| w31 | 38 | -0.106817 | -18.011 |
| w32 | 34 | 0.103389 | 49.475 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 38 | 0.032992 | 3.152 |
| w20 | 36 | 0.015329 | -18.877 |
| w21 | 43 | -0.01954 | -0.675 |
| w22 | 60 | -0.028389 | 87.118 |
| w23 | 42 | 0.111018 | 6.758 |
| w24 | 61 | 0.131422 | 166.602 |
| w25 | 38 | -0.083208 | -18.245 |
| w26 | 39 | -0.039508 | -12.753 |
| w27 | 48 | 0.064623 | 25.261 |
| w28 | 37 | -0.087111 | -17.567 |
| w29 | 54 | -0.064912 | -19.254 |
| w30 | 30 | -0.070816 | -16.188 |
| w31 | 42 | -0.019272 | -3.302 |
| w32 | 46 | -0.048095 | 13.684 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 48 | -0.031606 | 4.91 |
| w23 | 40 | -0.047114 | -9.376 |
| w24 | 54 | -0.119481 | 9.626 |
| w25 | 40 | -0.014391 | -12.553 |
| w26 | 42 | 0.1227 | 5.397 |
| w27 | 49 | -0.113144 | -5.558 |
| w28 | 39 | -0.009713 | -7.078 |
| w29 | 43 | 0.071958 | 17.403 |
| w30 | 33 | -0.076485 | -11.857 |
| w31 | 44 | 0.000125 | -13.904 |
| w32 | 43 | 0.212 | 46.31 |

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
| w27 | 45 | 0.085222 | 42.497 |
| w28 | 44 | -0.187395 | -17.656 |
| w29 | 48 | 0.059945 | -5.863 |
| w30 | 23 | 0.02514 | -10.384 |
| w31 | 44 | -0.073159 | -16.06 |
| w32 | 50 | 0.12983 | 73.545 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 42 | 0.065397 | 6.719 |
| w18 | 33 | -0.089421 | -27.67 |
| w19 | 32 | 0.088657 | -5.794 |
| w20 | 22 | 0.134296 | 17.494 |
| w21 | 41 | -0.026391 | -19.488 |
| w22 | 51 | 0.078488 | 44.817 |
| w23 | 40 | -0.086206 | -16.144 |
| w24 | 53 | -0.078017 | 20.348 |
| w25 | 40 | 0.164309 | 23.382 |
| w26 | 43 | -0.034854 | -22.403 |
| w27 | 53 | -0.006772 | 10.134 |
| w28 | 43 | -0.130767 | -28.749 |
| w29 | 36 | -0.0026 | -21.117 |
| w30 | 32 | 0.098552 | -3.015 |
| w31 | 37 | -0.108134 | -26.857 |
| w32 | 30 | 0.094088 | 5.89 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 40 | 0.123816 | 16.7 |
| w18 | 45 | -0.138054 | -20.254 |
| w19 | 40 | 0.054243 | -15.036 |
| w20 | 35 | 0.03059 | -10.613 |
| w21 | 41 | 0.049866 | -4.171 |
| w22 | 50 | 0.044263 | 73.472 |
| w23 | 35 | 0.05504 | -15.849 |
| w24 | 51 | 0.010361 | 54.697 |
| w25 | 43 | 0.110478 | 50.33 |
| w26 | 41 | 0.121127 | 10.158 |
| w27 | 47 | 0.109206 | 26.567 |
| w28 | 28 | -0.022269 | -13.954 |
| w29 | 37 | 0.021403 | -2.398 |
| w30 | 21 | -0.074446 | -16.69 |
| w31 | 43 | -0.161832 | -36.83 |
| w32 | 38 | 0.195119 | 20.633 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 44 | -0.004887 | -6.129 |
| w29 | 42 | 0.080737 | 0.627 |
| w30 | 38 | 0.043882 | 3.653 |
| w31 | 44 | 0.118273 | 21.977 |
| w32 | 41 | 0.077047 | 18.911 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 43 | 0.123869 | 65.486 |
| w15 | 48 | 0.166254 | 64.947 |
| w16 | 48 | 0.022021 | 192.823 |
| w17 | 38 | -0.009306 | -0.448 |
| w18 | 30 | -0.146832 | -27.599 |
| w19 | 38 | -0.031832 | -10.529 |
| w20 | 37 | 0.010705 | -12.386 |
| w21 | 35 | 0.206238 | 97.197 |
| w22 | 49 | 0.028642 | 8.034 |
| w23 | 55 | 0.054191 | -4.782 |
| w24 | 51 | 0.021341 | 34.563 |
| w25 | 41 | 0.133275 | 48.384 |
| w26 | 39 | 0.014415 | -1.989 |
| w27 | 53 | 0.109979 | 88.903 |
| w28 | 32 | -0.148942 | -23.696 |
| w29 | 42 | 0.050168 | 19.063 |
| w30 | 30 | 0.0373 | -6.638 |
| w31 | 44 | -0.107212 | -15.231 |
| w32 | 36 | 0.136203 | 11.527 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 45 | 0.330517 | 177.4 |
| w26 | 49 | 0.107989 | 25.033 |
| w27 | 42 | 0.179084 | 71.401 |
| w28 | 38 | -0.172161 | -21.639 |
| w29 | 37 | 0.05846 | 5.381 |
| w30 | 37 | -0.000607 | -14.751 |
| w31 | 45 | -0.029036 | 2.474 |
| w32 | 47 | 0.206605 | 33.195 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

