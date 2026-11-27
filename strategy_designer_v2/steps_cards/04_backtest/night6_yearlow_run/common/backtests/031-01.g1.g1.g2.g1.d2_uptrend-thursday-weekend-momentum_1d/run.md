# Backtest of 031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.g2.g1.d2_uptrend-thursday-weekend-momentum_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | 0.024946 | -0.669 |
| w2 | 9 | 0.10877 | 27.055 |
| w3 | 19 | 0.183521 | 35.825 |
| w4 | 20 | -0.11275 | -15.936 |
| w5 | 20 | -0.072043 | 4.785 |
| w6 | 21 | 0.061489 | 26.413 |
| w7 | 0 | 0.181777 | 0.0 |
| w8 | 3 | 0.094019 | 4.511 |
| w9 | 0 | -0.016136 | 0.0 |
| w10 | 12 | 0.071569 | 6.739 |
| w11 | 15 | 0.088477 | 28.87 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.01185 | 0.636 |
| w14 | 9 | -0.093904 | 6.392 |
| w15 | 16 | 0.010967 | 16.736 |
| w16 | 13 | 0.001831 | 3.589 |
| w17 | 12 | 0.234157 | 23.071 |
| w18 | 8 | 0.109454 | 8.123 |
| w19 | 4 | 0.053803 | 1.148 |
| w20 | 1 | -0.233728 | -1.792 |
| w21 | 4 | 0.155306 | 6.879 |
| w22 | 14 | 0.144298 | 36.481 |
| w23 | 5 | 0.066807 | 2.212 |
| w24 | 14 | 0.011421 | 8.977 |
| w25 | 11 | -0.026497 | -5.276 |
| w26 | 2 | -0.004913 | 0.772 |
| w27 | 11 | 0.05043 | 4.297 |
| w28 | 5 | 0.005447 | -1.508 |
| w29 | 15 | -0.103249 | -7.13 |
| w30 | 3 | -0.267042 | -16.617 |
| w31 | 8 | 0.055403 | -0.034 |
| w32 | 7 | 0.089728 | 1.129 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | 0.003823 | -6.326 |
| w2 | 11 | 0.184994 | 20.361 |
| w3 | 11 | -0.042726 | -0.936 |
| w4 | 9 | -0.165165 | -15.239 |
| w5 | 13 | -0.078684 | -2.293 |
| w6 | 17 | 0.03589 | 46.1 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 16 | 0.066324 | 18.145 |
| w11 | 13 | 0.108248 | 9.61 |
| w12 | 0 | None | 0.0 |
| w13 | 6 | 0.014132 | 2.038 |
| w14 | 8 | -0.06449 | 10.285 |
| w15 | 15 | 0.180173 | 26.486 |
| w16 | 17 | 0.101265 | 24.131 |
| w17 | 5 | 0.02818 | -2.428 |
| w18 | 8 | -0.052433 | 0.525 |
| w19 | 3 | -0.022679 | -1.003 |
| w20 | 0 | -0.165426 | 0.0 |
| w21 | 8 | 0.041912 | 13.057 |
| w22 | 15 | 0.079179 | 3.175 |
| w23 | 7 | -0.070328 | -2.962 |
| w24 | 11 | -0.084933 | -0.727 |
| w25 | 5 | -0.011471 | 16.2 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.064729 | 33.276 |
| w28 | 8 | 0.074002 | -1.415 |
| w29 | 14 | 0.006663 | 18.236 |
| w30 | 3 | -0.489538 | -33.001 |
| w31 | 4 | 0.023543 | -2.66 |
| w32 | 5 | 0.162885 | 2.515 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 14 | -0.064324 | 0.659 |
| w7 | 4 | 0.029874 | 0.7 |
| w8 | 1 | -0.004071 | -0.321 |
| w9 | 6 | -0.014905 | 1.087 |
| w10 | 3 | 0.177351 | 5.266 |
| w11 | 5 | -0.072927 | -8.604 |
| w12 | 5 | -0.070004 | -4.024 |
| w13 | 6 | -0.007156 | -9.491 |
| w14 | 11 | 0.015831 | 24.39 |
| w15 | 5 | 0.018319 | 99.674 |
| w16 | 9 | -0.031109 | 14.491 |
| w17 | 7 | 0.125826 | 16.432 |
| w18 | 2 | -0.036699 | -0.568 |
| w19 | 3 | -0.024004 | -0.024 |
| w20 | 1 | 0.003836 | -0.088 |
| w21 | 3 | 0.055374 | -1.666 |
| w22 | 13 | 0.043169 | 3.013 |
| w23 | 5 | -0.086254 | -11.304 |
| w24 | 8 | -0.047613 | -1.787 |
| w25 | 4 | -0.112683 | -11.819 |
| w26 | 4 | -0.018777 | 1.56 |
| w27 | 10 | 0.426789 | 121.602 |
| w28 | 4 | -0.036509 | -1.796 |
| w29 | 11 | 0.042943 | 6.48 |
| w30 | 0 | 0.067272 | 0.0 |
| w31 | 2 | -0.004156 | -1.272 |
| w32 | 5 | 0.123619 | 5.901 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 1 | -0.073239 | -1.476 |
| w8 | 2 | -0.002843 | 7.149 |
| w9 | 1 | -0.051917 | -2.938 |
| w10 | 11 | 0.060489 | 9.411 |
| w11 | 7 | -0.080309 | -1.391 |
| w12 | 2 | -0.051237 | -2.035 |
| w13 | 7 | 0.048834 | -4.153 |
| w14 | 7 | 0.010424 | 7.318 |
| w15 | 9 | 0.001919 | 3.669 |
| w16 | 12 | 0.095062 | 30.816 |
| w17 | 5 | -0.035741 | -4.04 |
| w18 | 3 | -0.064636 | -2.503 |
| w19 | 4 | -0.028788 | -4.528 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | -0.013649 | -1.245 |
| w22 | 10 | 0.126536 | 10.829 |
| w23 | 7 | 0.485352 | 69.085 |
| w24 | 10 | -0.127727 | 1.024 |
| w25 | 15 | -0.003422 | 45.771 |
| w26 | 2 | 0.063458 | 0.042 |
| w27 | 15 | 0.025084 | 9.739 |
| w28 | 6 | 0.097031 | 0.222 |
| w29 | 20 | -0.072189 | -18.184 |
| w30 | 11 | -0.16977 | -16.084 |
| w31 | 4 | 0.05448 | 4.284 |
| w32 | 3 | 0.006825 | 2.791 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.00619 | 26.511 |
| w2 | 5 | -0.319024 | -34.475 |
| w3 | 6 | 0.05484 | -1.565 |
| w4 | 19 | 0.081836 | 11.601 |
| w5 | 14 | -0.073014 | 3.068 |
| w6 | 13 | -0.016247 | 16.68 |
| w7 | 6 | 0.033708 | 11.232 |
| w8 | 1 | -0.118222 | -0.625 |
| w9 | 1 | -0.008464 | -0.001 |
| w10 | 10 | 0.078422 | 9.645 |
| w11 | 11 | -0.012412 | 7.008 |
| w12 | 3 | -0.029061 | -0.701 |
| w13 | 7 | 0.066711 | 2.715 |
| w14 | 14 | -0.026168 | 42.131 |
| w15 | 13 | -0.011167 | 16.234 |
| w16 | 20 | -0.061317 | 1.387 |
| w17 | 9 | 0.125276 | 24.942 |
| w18 | 12 | -0.03095 | -3.448 |
| w19 | 4 | 0.077969 | 3.921 |
| w20 | 3 | -0.148247 | -4.123 |
| w21 | 3 | 0.071288 | 6.383 |
| w22 | 15 | 0.098603 | 18.304 |
| w23 | 7 | -0.074119 | -5.365 |
| w24 | 11 | -0.102184 | -5.467 |
| w25 | 13 | -0.049257 | -4.45 |
| w26 | 5 | 0.004455 | 2.557 |
| w27 | 9 | 0.071976 | 21.219 |
| w28 | 0 | 0.107311 | 0.0 |
| w29 | 15 | -0.010174 | 12.204 |
| w30 | 2 | -0.331452 | -12.315 |
| w31 | 5 | 0.066973 | 1.203 |
| w32 | 3 | 0.109971 | 2.351 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 13 | 0.233431 | 45.382 |
| w11 | 7 | -0.039578 | -3.288 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | -0.007726 | -5.527 |
| w14 | 14 | -0.128428 | 11.488 |
| w15 | 10 | -0.037139 | 24.29 |
| w16 | 18 | 0.03522 | 38.69 |
| w17 | 11 | 0.148682 | 28.773 |
| w18 | 2 | 0.020457 | -1.29 |
| w19 | 3 | -0.002415 | 2.434 |
| w20 | 5 | 0.001152 | -0.052 |
| w21 | 2 | 0.143614 | 1.099 |
| w22 | 9 | 0.154856 | 15.259 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.080244 | 33.736 |
| w25 | 6 | -0.027532 | -3.863 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.490447 | 96.597 |
| w28 | 4 | 0.111411 | 0.815 |
| w29 | 12 | 0.02135 | 2.381 |
| w30 | 4 | -0.262794 | -9.548 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | -0.068162 | -11.034 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 10 | -0.040113 | 0.794 |
| w13 | 7 | 0.032982 | -10.029 |
| w14 | 17 | -0.051663 | 10.909 |
| w15 | 6 | -0.023504 | 4.742 |
| w16 | 14 | 0.168622 | 17.863 |
| w17 | 10 | 0.182666 | 35.953 |
| w18 | 10 | 0.004226 | 3.35 |
| w19 | 5 | 0.015314 | -4.318 |
| w20 | 6 | -0.05395 | -6.901 |
| w21 | 10 | 0.333988 | 16.476 |
| w22 | 10 | 0.196047 | 17.025 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | -0.069633 | 8.684 |
| w25 | 6 | -0.132654 | -13.936 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.332487 | 56.703 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.2372 | -11.168 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | 0.088031 | 0.527 |
| w32 | 4 | -0.100781 | 1.82 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 2 | -0.054001 | 0.017 |
| w16 | 15 | 0.292621 | 50.97 |
| w17 | 6 | 0.136398 | 8.384 |
| w18 | 5 | -0.137163 | -4.326 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.026463 | 0.64 |
| w21 | 7 | 0.219747 | 19.966 |
| w22 | 6 | 0.12597 | 3.381 |
| w23 | 1 | 0.005153 | 0.348 |
| w24 | 15 | 0.0589 | 31.082 |
| w25 | 4 | -0.094244 | -18.029 |
| w26 | 2 | 0.168118 | 4.097 |
| w27 | 11 | 0.604635 | 122.335 |
| w28 | 5 | 0.044298 | -0.307 |
| w29 | 7 | -0.13798 | -7.615 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | 0.183821 | 4.496 |
| w32 | 5 | -0.033123 | -7.244 |

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
| w15 | 7 | -0.159861 | -19.466 |
| w16 | 14 | 0.022359 | 27.257 |
| w17 | 5 | 0.071253 | 6.087 |
| w18 | 9 | -0.125132 | -2.392 |
| w19 | 4 | -0.05985 | -4.931 |
| w20 | 6 | 0.045217 | 1.269 |
| w21 | 1 | 0.038607 | 2.226 |
| w22 | 14 | 0.087108 | 12.467 |
| w23 | 16 | 0.215451 | 32.0 |
| w24 | 19 | 0.06357 | 18.671 |
| w25 | 10 | 0.089866 | 10.223 |
| w26 | 15 | 0.076161 | 15.862 |
| w27 | 11 | 0.020671 | 29.961 |
| w28 | 10 | -0.114979 | -3.59 |
| w29 | 18 | 0.011353 | -1.358 |
| w30 | 1 | -0.094091 | -1.042 |
| w31 | 15 | -0.097606 | 3.377 |
| w32 | 10 | 0.043775 | 0.784 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 19 | -0.001394 | 26.776 |
| w17 | 7 | 0.087618 | 3.242 |
| w18 | 11 | 0.013759 | 0.097 |
| w19 | 3 | -0.014406 | 0.982 |
| w20 | 2 | 0.052204 | 0.444 |
| w21 | 0 | None | 0.0 |
| w22 | 9 | 0.060274 | 1.016 |
| w23 | 4 | 0.006138 | -3.504 |
| w24 | 10 | -0.070051 | 19.131 |
| w25 | 7 | -0.047675 | -16.369 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | 0.219287 | 73.751 |
| w28 | 0 | 0.18124 | 0.0 |
| w29 | 5 | -0.076756 | -2.46 |
| w30 | 5 | -0.233909 | -16.423 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.108015 | -5.818 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 3 | 0.023165 | -0.081 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | 0.147104 | 14.342 |
| w23 | 0 | None | 0.0 |
| w24 | 13 | 0.066923 | 58.698 |
| w25 | 5 | 0.052808 | -4.33 |
| w26 | 2 | 0.107761 | 2.595 |
| w27 | 15 | 0.306868 | 34.935 |
| w28 | 0 | 0.112349 | 0.0 |
| w29 | 9 | -0.125606 | -1.348 |
| w30 | 4 | -0.051218 | -3.098 |
| w31 | 4 | 0.010431 | -4.499 |
| w32 | 5 | 0.107275 | 0.111 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 7 | 0.185487 | 5.879 |
| w23 | 0 | None | 0.0 |
| w24 | 15 | -0.036753 | 33.35 |
| w25 | 11 | -0.122762 | -3.077 |
| w26 | 5 | 0.147429 | 0.899 |
| w27 | 10 | 0.091449 | 13.971 |
| w28 | 0 | 0.130938 | 0.0 |
| w29 | 5 | -0.099607 | -0.997 |
| w30 | 4 | -0.096444 | -6.024 |
| w31 | 4 | -0.030435 | -4.331 |
| w32 | 10 | -0.033438 | 7.446 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 10 | 0.06165 | 2.851 |
| w25 | 15 | 0.055809 | -0.835 |
| w26 | 0 | None | 0.0 |
| w27 | 18 | 0.057915 | 17.356 |
| w28 | 6 | 0.166866 | 3.172 |
| w29 | 7 | -0.116504 | -5.113 |
| w30 | 2 | 0.037045 | 0.707 |
| w31 | 5 | 0.008992 | -4.993 |
| w32 | 7 | -0.048469 | -3.902 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | -0.086297 | -5.611 |
| w6 | 10 | -0.257551 | -20.172 |
| w7 | 3 | -0.008898 | 1.475 |
| w8 | 1 | -0.031486 | -1.379 |
| w9 | 1 | -0.019877 | -2.819 |
| w10 | 8 | 0.171292 | 6.921 |
| w11 | 13 | 0.088552 | 4.086 |
| w12 | 0 | None | 0.0 |
| w13 | 7 | 0.114577 | -1.344 |
| w14 | 14 | -0.012744 | 30.154 |
| w15 | 7 | -0.065522 | 5.903 |
| w16 | 21 | 0.024645 | 26.632 |
| w17 | 10 | 0.121501 | 5.519 |
| w18 | 5 | -0.172409 | -21.253 |
| w19 | 7 | 0.054494 | 2.907 |
| w20 | 2 | -0.088935 | -5.256 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.023814 | 0.982 |
| w23 | 1 | -0.085931 | -2.298 |
| w24 | 10 | -0.029626 | 4.539 |
| w25 | 5 | 0.014425 | 3.071 |
| w26 | 11 | 0.078712 | 15.152 |
| w27 | 9 | -0.052042 | 5.517 |
| w28 | 5 | 0.056801 | -1.033 |
| w29 | 8 | -0.213454 | -6.315 |
| w30 | 17 | 0.064914 | 41.048 |
| w31 | 4 | -0.037204 | -3.153 |
| w32 | 9 | 0.059496 | 20.714 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 16 | 0.036133 | 12.662 |
| w6 | 14 | -0.115706 | 9.882 |
| w7 | 2 | 0.111966 | 0.718 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.019579 | -1.368 |
| w10 | 13 | 0.134388 | 7.704 |
| w11 | 12 | 0.004147 | 6.275 |
| w12 | 0 | None | 0.0 |
| w13 | 8 | 0.041304 | 0.611 |
| w14 | 16 | -0.084681 | 10.343 |
| w15 | 17 | -0.09061 | 7.528 |
| w16 | 20 | 0.098526 | 37.65 |
| w17 | 7 | 0.137067 | 8.519 |
| w18 | 3 | 0.007502 | 0.226 |
| w19 | 7 | -0.050541 | -0.288 |
| w20 | 0 | -0.191821 | 0.0 |
| w21 | 5 | -0.001117 | -0.367 |
| w22 | 9 | 0.129949 | 16.385 |
| w23 | 5 | 0.10904 | 4.428 |
| w24 | 12 | -0.032993 | -4.812 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | -0.138099 | 8.668 |
| w27 | 10 | 0.077875 | 9.376 |
| w28 | 9 | -0.003572 | -5.884 |
| w29 | 6 | 0.143954 | 22.04 |
| w30 | 15 | -0.166272 | -3.721 |
| w31 | 8 | -0.13222 | -14.766 |
| w32 | 9 | -0.004135 | 12.821 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.161546 | 2.631 |
| w18 | 12 | -0.210182 | -16.795 |
| w19 | 1 | -0.123142 | -2.727 |
| w20 | 4 | -0.062479 | -6.101 |
| w21 | 0 | -0.070096 | 0.0 |
| w22 | 11 | 0.361445 | 26.257 |
| w23 | 1 | -0.060025 | -2.697 |
| w24 | 11 | 0.071376 | 14.03 |
| w25 | 2 | -0.136325 | -15.156 |
| w26 | 0 | None | 0.0 |
| w27 | 11 | 0.21286 | 71.194 |
| w28 | 4 | 0.013882 | 0.338 |
| w29 | 9 | 0.048889 | 7.484 |
| w30 | 0 | 0.036085 | 0.0 |
| w31 | 1 | -0.055756 | -3.555 |
| w32 | 11 | -0.070507 | -17.539 |

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
| w17 | 8 | 0.079823 | 5.687 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.080568 | 2.118 |
| w20 | 4 | -0.070604 | -2.797 |
| w21 | 2 | 0.071055 | 3.904 |
| w22 | 9 | 0.118687 | 12.018 |
| w23 | 6 | 0.167852 | 3.266 |
| w24 | 15 | -0.11805 | -9.929 |
| w25 | 5 | -0.106372 | -17.246 |
| w26 | 10 | 0.035104 | -7.375 |
| w27 | 18 | 0.089608 | 17.157 |
| w28 | 1 | 0.019092 | -0.77 |
| w29 | 16 | -0.038419 | -2.393 |
| w30 | 0 | -0.015832 | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | 0.072841 | 8.395 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 3 | 0.006593 | -0.046 |
| w20 | 2 | -0.093071 | -8.754 |
| w21 | 8 | 0.100378 | 10.676 |
| w22 | 15 | -0.02269 | 2.049 |
| w23 | 12 | 0.073154 | 5.424 |
| w24 | 16 | 0.046151 | 31.767 |
| w25 | 5 | 0.010897 | -10.255 |
| w26 | 5 | 0.013329 | -3.406 |
| w27 | 12 | 0.178877 | 18.884 |
| w28 | 0 | None | 0.0 |
| w29 | 11 | -0.151672 | -1.372 |
| w30 | 0 | 0.04311 | 0.0 |
| w31 | 2 | -0.020946 | -6.392 |
| w32 | 15 | -0.026183 | -4.133 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 14 | 0.126299 | 10.875 |
| w23 | 2 | 0.062055 | 0.964 |
| w24 | 13 | 0.07277 | 9.433 |
| w25 | 7 | 0.095806 | -8.379 |
| w26 | 4 | -0.238823 | -10.068 |
| w27 | 10 | 0.087373 | 8.863 |
| w28 | 7 | 0.130875 | 1.963 |
| w29 | 9 | 0.068165 | 8.996 |
| w30 | 1 | -0.095472 | -1.282 |
| w31 | 2 | -0.057388 | -13.215 |
| w32 | 7 | -0.006266 | -8.597 |

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
| w27 | 13 | 0.184157 | 25.164 |
| w28 | 3 | -0.04284 | -4.404 |
| w29 | 7 | -0.095806 | -2.502 |
| w30 | 3 | -0.047454 | -4.522 |
| w31 | 0 | None | 0.0 |
| w32 | 7 | 0.080292 | 0.368 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.059508 | 3.72 |
| w18 | 5 | -0.067298 | 2.18 |
| w19 | 4 | 0.026569 | -3.522 |
| w20 | 4 | 0.08621 | 8.891 |
| w21 | 0 | None | 0.0 |
| w22 | 10 | -0.09296 | -6.24 |
| w23 | 3 | -0.126747 | -5.563 |
| w24 | 13 | -0.185644 | 2.297 |
| w25 | 12 | 0.017811 | 6.706 |
| w26 | 0 | None | 0.0 |
| w27 | 12 | 0.234445 | 58.256 |
| w28 | 2 | 0.163245 | -0.206 |
| w29 | 5 | -0.124242 | -1.563 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.018981 | -5.216 |
| w32 | 3 | 0.250133 | 2.954 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.081268 | 1.329 |
| w18 | 6 | 0.021666 | -3.295 |
| w19 | 3 | -0.070914 | -1.818 |
| w20 | 2 | 0.050089 | 0.17 |
| w21 | 1 | -0.038574 | 0.006 |
| w22 | 13 | 0.119317 | 37.301 |
| w23 | 2 | -0.061009 | -1.669 |
| w24 | 12 | -0.001924 | 9.819 |
| w25 | 9 | 0.028005 | 18.28 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | 0.177645 | 22.666 |
| w28 | 0 | 0.192613 | 0.0 |
| w29 | 4 | -0.133948 | -3.222 |
| w30 | 2 | 0.029593 | 0.233 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | -0.095947 | -17.32 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 3 | -0.020691 | -2.331 |
| w29 | 6 | 0.028822 | -0.622 |
| w30 | 5 | 0.120549 | 7.97 |
| w31 | 4 | -0.136321 | -8.375 |
| w32 | 5 | -0.14594 | -12.864 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 10 | -0.166502 | -0.506 |
| w15 | 10 | 0.038533 | 50.52 |
| w16 | 13 | 0.064695 | 27.603 |
| w17 | 6 | 0.14813 | 1.653 |
| w18 | 3 | -0.059987 | -6.926 |
| w19 | 0 | None | 0.0 |
| w20 | 3 | -0.131369 | -3.199 |
| w21 | 7 | 0.077452 | 63.225 |
| w22 | 5 | 0.065212 | 2.062 |
| w23 | 2 | -0.010365 | 3.585 |
| w24 | 12 | 0.072742 | 1.553 |
| w25 | 7 | 0.098883 | 11.17 |
| w26 | 0 | None | 0.0 |
| w27 | 14 | 0.052952 | 28.175 |
| w28 | 2 | 0.272415 | 1.003 |
| w29 | 9 | -0.055846 | 1.898 |
| w30 | 4 | -0.206032 | -11.009 |
| w31 | 3 | 0.032604 | 0.385 |
| w32 | 5 | -0.075468 | -10.57 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 6 | 0.303006 | 25.399 |
| w26 | 9 | 0.051994 | 1.644 |
| w27 | 11 | 0.091873 | 2.349 |
| w28 | 2 | 0.088423 | 0.374 |
| w29 | 4 | -0.036337 | 1.347 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | 0.01205 | -2.814 |
| w32 | 5 | 0.318826 | 17.796 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

