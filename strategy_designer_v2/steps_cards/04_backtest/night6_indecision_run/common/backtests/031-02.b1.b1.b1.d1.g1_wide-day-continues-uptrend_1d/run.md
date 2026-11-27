# Backtest of 031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1.g1_wide-day-continues-uptrend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.03428 | -1.637 |
| w2 | 12 | 0.12505 | 39.365 |
| w3 | 27 | 0.103612 | 43.19 |
| w4 | 22 | -0.208943 | -24.516 |
| w5 | 31 | 0.040784 | 39.86 |
| w6 | 30 | 0.08438 | 45.013 |
| w7 | 2 | -0.063291 | -9.077 |
| w8 | 6 | 0.163151 | 6.537 |
| w9 | 6 | -0.080929 | -10.868 |
| w10 | 13 | -0.013068 | 0.884 |
| w11 | 24 | 0.006395 | 15.918 |
| w12 | 5 | 0.183265 | 5.639 |
| w13 | 25 | -0.064113 | 5.061 |
| w14 | 15 | 0.044635 | 12.475 |
| w15 | 20 | 0.016864 | 26.844 |
| w16 | 18 | -0.049767 | 3.598 |
| w17 | 7 | 0.102593 | 5.952 |
| w18 | 10 | -0.098486 | -8.278 |
| w19 | 2 | -0.120275 | -6.646 |
| w20 | 9 | 0.10233 | -2.918 |
| w21 | 9 | -0.008697 | -4.233 |
| w22 | 23 | 0.134736 | 50.343 |
| w23 | 10 | 0.044323 | 2.756 |
| w24 | 20 | 0.063389 | 37.565 |
| w25 | 21 | -0.064411 | 7.064 |
| w26 | 13 | -0.071831 | -13.222 |
| w27 | 24 | 0.06742 | 25.956 |
| w28 | 11 | 0.008662 | -3.069 |
| w29 | 19 | -0.027646 | -7.429 |
| w30 | 6 | 0.079189 | -5.387 |
| w31 | 9 | -0.023445 | -0.265 |
| w32 | 9 | 0.235795 | 31.865 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 14 | 0.159071 | 34.651 |
| w2 | 17 | -0.152105 | -32.88 |
| w3 | 14 | -0.104436 | -16.877 |
| w4 | 23 | -0.087303 | 6.319 |
| w5 | 22 | -0.010016 | 17.496 |
| w6 | 28 | 0.188917 | 73.344 |
| w7 | 5 | 0.074009 | 3.203 |
| w8 | 3 | -0.082717 | -8.845 |
| w9 | 8 | -0.093643 | -10.664 |
| w10 | 18 | 0.040494 | 22.503 |
| w11 | 11 | -0.147283 | -4.02 |
| w12 | 4 | 0.088712 | 1.749 |
| w13 | 21 | -0.052817 | 7.045 |
| w14 | 19 | 0.005778 | 19.397 |
| w15 | 27 | 0.115762 | 27.223 |
| w16 | 21 | -0.193501 | -4.515 |
| w17 | 11 | 0.121622 | 0.548 |
| w18 | 14 | 0.073824 | -3.138 |
| w19 | 4 | -0.028454 | -4.119 |
| w20 | 6 | 0.069115 | -0.359 |
| w21 | 14 | -0.063587 | 2.669 |
| w22 | 15 | -0.105829 | -0.95 |
| w23 | 5 | 0.031378 | -2.608 |
| w24 | 16 | -0.080061 | -9.037 |
| w25 | 15 | 0.022647 | 5.561 |
| w26 | 5 | -0.091423 | -10.893 |
| w27 | 27 | -0.01565 | 19.188 |
| w28 | 7 | -0.004514 | -2.428 |
| w29 | 16 | 0.203865 | 18.135 |
| w30 | 5 | -0.239044 | -19.605 |
| w31 | 4 | -0.120717 | -5.363 |
| w32 | 11 | 0.07799 | 11.914 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 20 | 0.135302 | 72.35 |
| w7 | 10 | 0.013924 | 4.779 |
| w8 | 1 | 0.000631 | -0.598 |
| w9 | 16 | 0.19613 | 12.296 |
| w10 | 9 | 0.049594 | 4.122 |
| w11 | 10 | -0.149402 | 10.018 |
| w12 | 7 | 0.006923 | -1.2 |
| w13 | 16 | -0.081181 | -9.184 |
| w14 | 22 | 0.152713 | 23.117 |
| w15 | 22 | 0.225763 | 59.739 |
| w16 | 13 | -0.104373 | -0.135 |
| w17 | 14 | 0.07133 | 19.587 |
| w18 | 7 | 0.013428 | -1.71 |
| w19 | 10 | 0.152227 | 2.962 |
| w20 | 1 | -0.041414 | -2.328 |
| w21 | 7 | 0.184268 | 15.625 |
| w22 | 11 | -0.145059 | -6.265 |
| w23 | 11 | -0.115119 | -7.202 |
| w24 | 20 | -0.051288 | -13.186 |
| w25 | 10 | -0.035029 | -2.961 |
| w26 | 8 | -0.007401 | 7.977 |
| w27 | 18 | 0.213505 | 85.505 |
| w28 | 13 | -0.131727 | -8.83 |
| w29 | 14 | 0.083445 | 15.761 |
| w30 | 6 | -0.186389 | -5.355 |
| w31 | 7 | -0.167835 | -18.115 |
| w32 | 9 | 0.395167 | 46.247 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | 0.16519 | 20.008 |
| w8 | 5 | 0.012487 | -3.306 |
| w9 | 18 | 0.081463 | 3.267 |
| w10 | 19 | 0.083669 | 6.212 |
| w11 | 17 | -0.018204 | 0.001 |
| w12 | 5 | 0.017079 | -0.817 |
| w13 | 14 | -0.103966 | 11.257 |
| w14 | 18 | 0.148431 | 15.283 |
| w15 | 23 | -0.082275 | -16.553 |
| w16 | 21 | -0.087414 | -0.525 |
| w17 | 14 | 0.05566 | 4.86 |
| w18 | 6 | -0.119399 | -17.861 |
| w19 | 5 | -0.058322 | -6.992 |
| w20 | 3 | -0.064556 | -7.655 |
| w21 | 6 | 0.10394 | -14.065 |
| w22 | 15 | 0.015752 | 8.103 |
| w23 | 10 | 0.317367 | 60.892 |
| w24 | 20 | -0.077825 | 6.589 |
| w25 | 18 | -0.123258 | -4.116 |
| w26 | 5 | 0.003769 | -4.548 |
| w27 | 15 | -0.035 | 7.193 |
| w28 | 4 | -0.020915 | 2.56 |
| w29 | 14 | -0.11186 | -0.581 |
| w30 | 10 | -0.04277 | 0.698 |
| w31 | 6 | -0.003734 | -4.997 |
| w32 | 10 | 0.241273 | 33.201 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.093104 | 52.216 |
| w2 | 20 | -0.171653 | -9.034 |
| w3 | 7 | -0.05305 | -2.679 |
| w4 | 26 | 0.14014 | 91.009 |
| w5 | 24 | -0.028327 | 22.737 |
| w6 | 25 | 0.117623 | 36.623 |
| w7 | 12 | -0.03499 | 0.995 |
| w8 | 4 | -0.009717 | -0.388 |
| w9 | 10 | -0.096204 | -11.119 |
| w10 | 14 | -0.051587 | -3.396 |
| w11 | 15 | 0.008864 | 9.907 |
| w12 | 6 | -0.176151 | -12.86 |
| w13 | 25 | -0.041195 | 18.969 |
| w14 | 25 | 0.091848 | 37.166 |
| w15 | 23 | -0.003126 | 13.592 |
| w16 | 25 | -0.036943 | 24.52 |
| w17 | 13 | -0.023231 | -8.067 |
| w18 | 11 | 0.078965 | -0.289 |
| w19 | 7 | -0.016436 | -4.912 |
| w20 | 6 | 0.012432 | 11.497 |
| w21 | 9 | -0.138391 | 3.92 |
| w22 | 18 | 0.083291 | 27.447 |
| w23 | 11 | -0.131708 | -7.643 |
| w24 | 25 | -0.11395 | -1.26 |
| w25 | 17 | 0.020132 | 13.501 |
| w26 | 10 | 0.090048 | 6.65 |
| w27 | 15 | -0.036859 | 13.702 |
| w28 | 2 | -0.081286 | -2.132 |
| w29 | 27 | 0.181746 | 25.12 |
| w30 | 4 | -0.058073 | -8.605 |
| w31 | 9 | -0.090603 | -12.724 |
| w32 | 6 | 0.149995 | 12.884 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 20 | 0.055499 | 2.334 |
| w11 | 9 | -0.136338 | 4.314 |
| w12 | 8 | 0.051856 | -4.999 |
| w13 | 27 | 0.00106 | 19.068 |
| w14 | 22 | 0.12039 | 27.356 |
| w15 | 19 | 0.025281 | 1.679 |
| w16 | 23 | -0.034446 | 19.86 |
| w17 | 20 | 0.229576 | 39.405 |
| w18 | 4 | -0.128687 | -10.064 |
| w19 | 6 | 0.027275 | -2.231 |
| w20 | 7 | -0.027092 | -9.789 |
| w21 | 6 | -0.220921 | -8.131 |
| w22 | 18 | 0.084551 | 14.765 |
| w23 | 5 | -0.139579 | -15.935 |
| w24 | 24 | 0.130992 | 49.837 |
| w25 | 12 | 0.111811 | 3.879 |
| w26 | 5 | -0.022015 | -3.082 |
| w27 | 22 | 0.152472 | 40.931 |
| w28 | 7 | -0.109582 | -7.515 |
| w29 | 21 | 0.090977 | 12.06 |
| w30 | 2 | -0.092916 | -7.958 |
| w31 | 3 | -0.111757 | -9.029 |
| w32 | 19 | 0.153571 | 12.989 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 12 | 0.091922 | 14.47 |
| w13 | 19 | -0.045718 | -8.312 |
| w14 | 25 | 0.218987 | 55.206 |
| w15 | 9 | -0.045229 | 3.135 |
| w16 | 19 | -0.018778 | 8.068 |
| w17 | 13 | 0.123552 | -2.606 |
| w18 | 9 | -0.122217 | 9.082 |
| w19 | 11 | 0.004761 | 1.451 |
| w20 | 9 | -0.070706 | -4.365 |
| w21 | 15 | -0.119319 | 1.755 |
| w22 | 18 | 0.046048 | 12.626 |
| w23 | 3 | 0.02691 | -0.489 |
| w24 | 26 | -0.011177 | -2.833 |
| w25 | 7 | 0.144954 | 15.415 |
| w26 | 2 | -0.040478 | -5.53 |
| w27 | 17 | -0.041209 | 0.162 |
| w28 | 2 | 0.015179 | 0.255 |
| w29 | 17 | 0.155435 | 11.042 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.190202 | -11.6 |
| w32 | 13 | 0.043164 | -3.119 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 8 | -0.024163 | -7.241 |
| w16 | 25 | -0.111662 | 6.781 |
| w17 | 12 | 0.149585 | 3.282 |
| w18 | 11 | 0.224791 | 28.266 |
| w19 | 7 | 0.01088 | -3.783 |
| w20 | 8 | 0.01152 | -6.783 |
| w21 | 10 | -0.130194 | -13.688 |
| w22 | 16 | 0.081458 | 16.159 |
| w23 | 0 | None | 0.0 |
| w24 | 17 | 0.016986 | 40.563 |
| w25 | 19 | 0.192788 | 20.017 |
| w26 | 2 | -0.014554 | -1.869 |
| w27 | 20 | 0.069571 | 46.902 |
| w28 | 6 | -0.117307 | -6.742 |
| w29 | 14 | 0.010662 | 14.306 |
| w30 | 3 | -0.006477 | -1.625 |
| w31 | 10 | 0.159617 | 11.251 |
| w32 | 11 | 0.09624 | 5.188 |

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
| w15 | 14 | -0.118103 | 11.342 |
| w16 | 26 | -0.069525 | 17.117 |
| w17 | 6 | 0.044202 | 6.496 |
| w18 | 16 | 0.09171 | -1.524 |
| w19 | 11 | 0.124827 | 5.418 |
| w20 | 11 | 0.020851 | 6.891 |
| w21 | 13 | -0.000104 | -8.12 |
| w22 | 12 | 0.007903 | 11.834 |
| w23 | 19 | -0.01307 | -15.587 |
| w24 | 22 | 0.122069 | 30.421 |
| w25 | 12 | -0.05196 | -5.978 |
| w26 | 11 | 0.136248 | 16.534 |
| w27 | 21 | -0.017803 | 49.26 |
| w28 | 11 | -0.103295 | 0.295 |
| w29 | 25 | -0.08453 | -10.925 |
| w30 | 0 | None | 0.0 |
| w31 | 27 | -0.281458 | -3.003 |
| w32 | 15 | 0.053612 | -0.859 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 28 | 0.034751 | 16.799 |
| w17 | 15 | 0.088808 | 15.531 |
| w18 | 16 | 0.049385 | 6.244 |
| w19 | 9 | 0.089347 | -1.53 |
| w20 | 6 | -0.026568 | -2.028 |
| w21 | 8 | -0.327034 | -14.597 |
| w22 | 16 | -0.061362 | 0.322 |
| w23 | 3 | 0.033751 | -0.374 |
| w24 | 20 | -0.063593 | -0.235 |
| w25 | 16 | 0.148259 | 14.1 |
| w26 | 5 | -0.009707 | -5.161 |
| w27 | 16 | 0.058228 | 7.323 |
| w28 | 1 | -0.291029 | -5.325 |
| w29 | 18 | 0.15622 | 9.764 |
| w30 | 7 | 0.013548 | -12.921 |
| w31 | 7 | -0.102613 | -11.916 |
| w32 | 9 | 0.160036 | 5.941 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | 0.028479 | 7.197 |
| w21 | 5 | -0.203991 | -16.24 |
| w22 | 18 | 0.102861 | 7.978 |
| w23 | 6 | 0.088963 | -0.676 |
| w24 | 20 | 0.094004 | 44.627 |
| w25 | 8 | 0.143121 | 11.386 |
| w26 | 6 | -0.051944 | -12.377 |
| w27 | 18 | -0.003487 | 7.379 |
| w28 | 4 | 0.055548 | -0.243 |
| w29 | 15 | 0.05601 | 8.965 |
| w30 | 9 | -0.005634 | -5.908 |
| w31 | 10 | -0.046912 | -10.52 |
| w32 | 10 | 0.109708 | 2.648 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 14 | 0.072122 | 21.579 |
| w23 | 5 | 0.103713 | -0.734 |
| w24 | 29 | 0.213964 | 55.304 |
| w25 | 19 | 0.026242 | 39.824 |
| w26 | 8 | 0.065038 | -3.179 |
| w27 | 13 | -0.112159 | 4.3 |
| w28 | 1 | -0.000537 | -4.259 |
| w29 | 10 | -0.013213 | 3.86 |
| w30 | 13 | 0.064273 | 4.419 |
| w31 | 5 | -0.117417 | -6.024 |
| w32 | 16 | -0.07581 | 34.398 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 20 | -0.056451 | 0.802 |
| w25 | 13 | 0.040961 | 7.923 |
| w26 | 6 | -0.091349 | -14.062 |
| w27 | 30 | 0.051308 | 39.02 |
| w28 | 13 | 0.132177 | 10.033 |
| w29 | 12 | -0.009476 | -2.424 |
| w30 | 7 | 0.064535 | -3.677 |
| w31 | 6 | -0.029246 | -0.476 |
| w32 | 8 | 0.263694 | 45.254 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | 0.152354 | 34.531 |
| w6 | 18 | 0.040717 | 3.705 |
| w7 | 10 | 0.033608 | -5.256 |
| w8 | 7 | 4.7e-05 | -3.178 |
| w9 | 4 | -0.111085 | -12.386 |
| w10 | 12 | -0.029183 | -6.512 |
| w11 | 12 | 0.019171 | 7.895 |
| w12 | 8 | -0.038095 | -6.93 |
| w13 | 27 | -0.008572 | 33.682 |
| w14 | 18 | -0.101838 | -8.074 |
| w15 | 12 | 0.022045 | 4.631 |
| w16 | 24 | -0.023702 | 9.221 |
| w17 | 14 | 0.124238 | 1.726 |
| w18 | 15 | 0.098409 | 8.395 |
| w19 | 9 | 0.026984 | 6.946 |
| w20 | 5 | 0.059052 | 0.514 |
| w21 | 7 | 0.067079 | -4.449 |
| w22 | 9 | -0.025821 | -2.941 |
| w23 | 5 | -0.077855 | -14.265 |
| w24 | 13 | -0.052487 | 5.356 |
| w25 | 13 | 0.03903 | 10.217 |
| w26 | 14 | 0.032971 | -0.737 |
| w27 | 25 | -0.044592 | 10.179 |
| w28 | 7 | 0.015429 | -5.692 |
| w29 | 12 | 0.046431 | 16.144 |
| w30 | 28 | 0.235711 | 107.51 |
| w31 | 7 | -0.014493 | -4.859 |
| w32 | 23 | 0.148909 | 46.243 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 22 | 0.020289 | 54.548 |
| w6 | 24 | 0.024576 | 21.3 |
| w7 | 7 | -0.029067 | -7.276 |
| w8 | 2 | -0.064369 | -2.238 |
| w9 | 8 | 0.020608 | -15.334 |
| w10 | 20 | -0.065116 | 10.612 |
| w11 | 18 | -0.116667 | -8.846 |
| w12 | 5 | -0.03953 | -5.724 |
| w13 | 22 | -0.003093 | 16.062 |
| w14 | 18 | -0.039027 | -1.995 |
| w15 | 13 | -0.140948 | 0.307 |
| w16 | 19 | -0.06872 | 14.286 |
| w17 | 7 | 0.05497 | -3.281 |
| w18 | 4 | -0.133216 | -14.87 |
| w19 | 15 | -0.181272 | -19.786 |
| w20 | 8 | 0.078923 | 3.476 |
| w21 | 5 | -0.038662 | -2.673 |
| w22 | 15 | 0.031701 | 3.984 |
| w23 | 6 | 0.042605 | -6.196 |
| w24 | 21 | 0.012274 | 1.763 |
| w25 | 4 | 0.055264 | 4.256 |
| w26 | 17 | 0.26392 | 21.866 |
| w27 | 7 | -0.044046 | 7.543 |
| w28 | 10 | -0.03448 | 5.215 |
| w29 | 8 | -0.167542 | -6.132 |
| w30 | 15 | -0.087248 | -8.241 |
| w31 | 11 | -0.02544 | 2.955 |
| w32 | 16 | -0.045847 | 8.6 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | 0.073745 | 5.669 |
| w18 | 15 | 0.005294 | 23.308 |
| w19 | 9 | 0.03524 | -2.263 |
| w20 | 12 | -0.064022 | -1.132 |
| w21 | 5 | -0.182178 | -14.232 |
| w22 | 18 | 0.069641 | 16.235 |
| w23 | 6 | 0.09354 | -1.788 |
| w24 | 19 | 0.131252 | 29.411 |
| w25 | 12 | 0.131502 | 22.959 |
| w26 | 10 | 0.073086 | -2.825 |
| w27 | 15 | 0.088713 | 63.721 |
| w28 | 9 | -0.070097 | 4.323 |
| w29 | 9 | 0.260102 | 29.084 |
| w30 | 1 | -0.068748 | -4.213 |
| w31 | 7 | -0.097734 | -8.517 |
| w32 | 17 | 0.105463 | 31.843 |

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
| w17 | 14 | 0.089271 | 3.809 |
| w18 | 13 | 0.032408 | 1.211 |
| w19 | 8 | 0.022206 | 2.822 |
| w20 | 10 | 0.051003 | -2.834 |
| w21 | 11 | -0.103206 | -26.312 |
| w22 | 16 | 0.157374 | 28.158 |
| w23 | 8 | -0.138846 | -16.143 |
| w24 | 26 | 0.012213 | 27.533 |
| w25 | 12 | 0.299188 | 37.273 |
| w26 | 12 | -0.083548 | -6.292 |
| w27 | 20 | 0.051944 | 17.808 |
| w28 | 4 | 0.127903 | 1.595 |
| w29 | 20 | 0.027144 | 5.299 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.055816 | -10.87 |
| w32 | 12 | 0.109409 | 5.08 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | -0.214761 | -14.225 |
| w20 | 9 | 0.029072 | -5.867 |
| w21 | 13 | 0.033685 | -1.491 |
| w22 | 27 | -0.03652 | 33.356 |
| w23 | 11 | 0.157444 | -2.428 |
| w24 | 30 | 0.212049 | 72.189 |
| w25 | 12 | 0.018473 | -7.775 |
| w26 | 10 | -0.096329 | -15.609 |
| w27 | 12 | -0.050628 | 1.067 |
| w28 | 9 | 0.029815 | -1.628 |
| w29 | 18 | -0.073332 | -4.638 |
| w30 | 1 | 0.009782 | -3.577 |
| w31 | 8 | -0.098985 | -22.023 |
| w32 | 16 | -0.011837 | 17.158 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.00828 | 28.541 |
| w23 | 11 | 0.001536 | -8.05 |
| w24 | 21 | -0.06654 | -1.534 |
| w25 | 10 | -0.048553 | -5.684 |
| w26 | 8 | 0.05109 | 2.155 |
| w27 | 18 | -0.107054 | 3.638 |
| w28 | 4 | -0.116233 | -9.304 |
| w29 | 22 | 0.109166 | 13.509 |
| w30 | 3 | -0.011647 | -3.038 |
| w31 | 18 | -0.033847 | -9.929 |
| w32 | 7 | -0.035782 | -5.637 |

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
| w27 | 17 | 0.132268 | 25.45 |
| w28 | 7 | -0.099779 | -5.674 |
| w29 | 14 | -0.011602 | -7.561 |
| w30 | 4 | 0.08064 | 0.462 |
| w31 | 5 | -0.195429 | -14.703 |
| w32 | 20 | 0.152867 | 38.862 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.040205 | 4.351 |
| w18 | 8 | 0.043122 | -12.913 |
| w19 | 10 | 0.180835 | 7.525 |
| w20 | 3 | 0.038909 | -1.44 |
| w21 | 9 | 0.017603 | -7.041 |
| w22 | 18 | 0.009389 | 12.115 |
| w23 | 5 | -0.116024 | -8.04 |
| w24 | 17 | -0.142204 | -0.323 |
| w25 | 15 | 0.151452 | 22.695 |
| w26 | 6 | -0.012978 | -10.257 |
| w27 | 21 | -0.010174 | 2.452 |
| w28 | 3 | -0.147105 | -4.273 |
| w29 | 12 | -0.026121 | -9.966 |
| w30 | 7 | 0.361959 | 19.7 |
| w31 | 12 | -0.036728 | -17.152 |
| w32 | 8 | 0.037055 | 5.219 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | 0.109975 | 13.055 |
| w18 | 9 | -0.11365 | -15.367 |
| w19 | 9 | 0.150388 | -11.581 |
| w20 | 7 | 0.055374 | -5.606 |
| w21 | 7 | 0.013831 | -3.202 |
| w22 | 18 | -0.0571 | 39.408 |
| w23 | 9 | 0.117409 | 2.099 |
| w24 | 22 | 0.045729 | 18.902 |
| w25 | 18 | 0.183439 | 27.607 |
| w26 | 7 | -0.016286 | -3.617 |
| w27 | 13 | -0.107514 | 8.769 |
| w28 | 2 | 0.064295 | -0.872 |
| w29 | 13 | 0.085776 | -5.063 |
| w30 | 5 | -0.057411 | -4.276 |
| w31 | 7 | -0.209867 | -10.526 |
| w32 | 13 | 0.115818 | 7.193 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 4 | -0.041356 | -7.588 |
| w29 | 12 | 0.038397 | -1.418 |
| w30 | 5 | 0.091916 | 3.46 |
| w31 | 11 | -0.102683 | -5.628 |
| w32 | 14 | 0.135264 | 19.632 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 11 | 0.292914 | 71.828 |
| w15 | 21 | 0.064355 | 43.766 |
| w16 | 23 | 0.048438 | 196.141 |
| w17 | 12 | -0.011113 | 2.9 |
| w18 | 8 | -0.026601 | 0.791 |
| w19 | 12 | -0.053674 | -5.145 |
| w20 | 4 | -0.105573 | -6.472 |
| w21 | 11 | 0.284617 | 67.531 |
| w22 | 13 | 0.14582 | 10.036 |
| w23 | 6 | 0.032128 | 3.412 |
| w24 | 22 | -0.033033 | 3.794 |
| w25 | 17 | 0.174192 | 40.424 |
| w26 | 7 | 0.083522 | -4.04 |
| w27 | 23 | 0.170798 | 53.58 |
| w28 | 5 | -0.128289 | -4.757 |
| w29 | 19 | 0.029244 | 19.741 |
| w30 | 5 | -0.033918 | -6.574 |
| w31 | 9 | -0.076778 | -9.069 |
| w32 | 6 | 0.386879 | 38.305 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 18 | 0.295421 | 102.944 |
| w26 | 9 | 0.097896 | 9.889 |
| w27 | 17 | 0.221015 | 33.605 |
| w28 | 6 | -0.119067 | -8.07 |
| w29 | 16 | 0.176143 | 10.755 |
| w30 | 4 | 0.049488 | -0.998 |
| w31 | 22 | 0.035838 | 0.291 |
| w32 | 8 | 0.260602 | 22.989 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

