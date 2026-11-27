# Backtest of 031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b2.e2_short-rise-in-uptrend-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.118297 | -11.315 |
| w2 | 30 | 0.13469 | 65.753 |
| w3 | 37 | 0.016008 | 49.04 |
| w4 | 50 | -0.058729 | -15.313 |
| w5 | 52 | -0.032818 | 53.547 |
| w6 | 51 | 0.123044 | 89.738 |
| w7 | 6 | 0.02087 | -0.662 |
| w8 | 17 | 0.050606 | 3.715 |
| w9 | 15 | -0.047755 | -9.715 |
| w10 | 28 | -0.013468 | 10.825 |
| w11 | 46 | 0.0944 | 61.809 |
| w12 | 3 | -0.066257 | -5.007 |
| w13 | 20 | -0.040373 | -8.356 |
| w14 | 43 | 0.020236 | 19.163 |
| w15 | 44 | 0.042923 | 39.587 |
| w16 | 47 | 0.080528 | 48.839 |
| w17 | 20 | -0.02744 | -16.419 |
| w18 | 33 | 0.076613 | -6.749 |
| w19 | 10 | 0.018957 | -1.43 |
| w20 | 6 | -0.120307 | -8.002 |
| w21 | 14 | -0.131727 | -14.848 |
| w22 | 35 | 0.095669 | 75.558 |
| w23 | 18 | 0.016936 | -0.181 |
| w24 | 35 | 0.146788 | 63.96 |
| w25 | 45 | 0.081718 | 43.662 |
| w26 | 18 | -0.034464 | -13.402 |
| w27 | 36 | 0.020962 | 27.44 |
| w28 | 19 | -0.029015 | -3.341 |
| w29 | 46 | -0.081442 | -1.719 |
| w30 | 9 | 0.089853 | 5.292 |
| w31 | 17 | -0.021231 | -5.471 |
| w32 | 15 | 0.244397 | 35.845 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 25 | -0.131886 | -9.232 |
| w2 | 31 | -0.004968 | 0.409 |
| w3 | 32 | -0.12618 | -17.412 |
| w4 | 34 | 0.010678 | 55.526 |
| w5 | 40 | -0.019278 | 24.881 |
| w6 | 33 | 0.119404 | 58.256 |
| w7 | 9 | -0.156774 | -7.059 |
| w8 | 4 | -0.021087 | -0.553 |
| w9 | 3 | -0.070333 | -8.633 |
| w10 | 28 | -0.051879 | 5.457 |
| w11 | 33 | 0.085001 | 11.357 |
| w12 | 0 | None | 0.0 |
| w13 | 19 | -0.046008 | -6.474 |
| w14 | 29 | 0.056891 | 26.783 |
| w15 | 32 | -0.037518 | -9.908 |
| w16 | 56 | 0.007934 | 26.598 |
| w17 | 19 | 0.00081 | 10.732 |
| w18 | 32 | 0.010084 | -8.94 |
| w19 | 6 | 0.034803 | 1.698 |
| w20 | 7 | -0.199764 | -11.919 |
| w21 | 31 | -0.070345 | -7.121 |
| w22 | 40 | -0.127057 | -13.18 |
| w23 | 17 | -0.025132 | -8.567 |
| w24 | 33 | -0.157693 | -14.346 |
| w25 | 34 | 0.015821 | 9.881 |
| w26 | 2 | -0.081179 | -0.425 |
| w27 | 40 | 0.029311 | 32.998 |
| w28 | 22 | -0.05512 | -12.299 |
| w29 | 30 | -0.016071 | 2.441 |
| w30 | 12 | -0.048859 | -9.836 |
| w31 | 13 | -0.08787 | -9.172 |
| w32 | 9 | 0.111656 | 13.881 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 46 | 0.082714 | 57.761 |
| w7 | 11 | 0.164474 | 6.594 |
| w8 | 7 | 0.064329 | 1.706 |
| w9 | 13 | -0.086508 | -7.425 |
| w10 | 11 | 0.034645 | 3.51 |
| w11 | 20 | 0.143657 | 32.773 |
| w12 | 16 | -0.068641 | -9.649 |
| w13 | 17 | -0.009115 | -6.559 |
| w14 | 25 | 0.216574 | 57.014 |
| w15 | 31 | 0.231627 | 118.287 |
| w16 | 32 | 0.068529 | 56.779 |
| w17 | 19 | 0.018791 | 11.665 |
| w18 | 24 | -0.021541 | -6.892 |
| w19 | 14 | -0.14248 | -15.503 |
| w20 | 3 | 0.002609 | 0.071 |
| w21 | 28 | 0.010886 | 6.539 |
| w22 | 42 | -0.128248 | 9.67 |
| w23 | 27 | -0.060655 | 16.011 |
| w24 | 25 | 0.001305 | 22.797 |
| w25 | 18 | -0.194031 | -28.121 |
| w26 | 19 | 0.023106 | 3.016 |
| w27 | 24 | 0.293433 | 201.194 |
| w28 | 25 | -0.110523 | -13.028 |
| w29 | 29 | 0.117004 | 36.511 |
| w30 | 10 | 0.090121 | -0.351 |
| w31 | 8 | -0.039388 | -9.562 |
| w32 | 9 | 0.099622 | 7.726 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | -0.106193 | -8.688 |
| w8 | 9 | 0.022367 | -0.202 |
| w9 | 1 | 0.002724 | -3.823 |
| w10 | 13 | 0.073079 | 23.777 |
| w11 | 24 | -0.016739 | -3.605 |
| w12 | 8 | -0.060228 | -10.141 |
| w13 | 17 | -0.043419 | -9.101 |
| w14 | 28 | 0.059914 | 15.299 |
| w15 | 24 | -0.11079 | -33.037 |
| w16 | 52 | 0.04941 | 37.814 |
| w17 | 19 | -0.033275 | 2.197 |
| w18 | 22 | -0.033072 | -17.425 |
| w19 | 11 | 0.007185 | -3.323 |
| w20 | 5 | -0.128707 | -10.382 |
| w21 | 19 | -0.177748 | -25.336 |
| w22 | 40 | 0.017666 | 28.552 |
| w23 | 6 | 0.295202 | 72.774 |
| w24 | 16 | -0.04581 | -5.705 |
| w25 | 33 | 0.177151 | 95.022 |
| w26 | 8 | 0.00885 | -3.131 |
| w27 | 28 | 0.002134 | 7.215 |
| w28 | 18 | -0.071882 | -11.9 |
| w29 | 53 | -0.272777 | -29.989 |
| w30 | 34 | -0.149995 | -17.87 |
| w31 | 11 | -0.073569 | -7.851 |
| w32 | 8 | 0.220671 | 36.673 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 41 | 0.134102 | 123.751 |
| w2 | 24 | -0.054516 | -3.823 |
| w3 | 18 | 0.073928 | -1.584 |
| w4 | 35 | 0.199601 | 156.317 |
| w5 | 37 | 0.038203 | 59.279 |
| w6 | 34 | 0.047121 | 31.333 |
| w7 | 24 | 0.077031 | 16.992 |
| w8 | 6 | -0.00151 | -1.191 |
| w9 | 1 | -0.029319 | -2.945 |
| w10 | 28 | -0.008608 | -0.819 |
| w11 | 32 | 0.157919 | 47.182 |
| w12 | 10 | -0.02962 | -10.498 |
| w13 | 21 | 0.032471 | 14.361 |
| w14 | 39 | 0.15314 | 77.213 |
| w15 | 36 | -0.11603 | -14.374 |
| w16 | 56 | -0.056581 | 52.52 |
| w17 | 33 | -0.021947 | 16.704 |
| w18 | 43 | -0.09333 | -20.889 |
| w19 | 8 | 0.067751 | 2.771 |
| w20 | 12 | -0.029672 | -7.706 |
| w21 | 16 | -0.030418 | -2.852 |
| w22 | 40 | -0.049738 | 21.147 |
| w23 | 22 | -0.161927 | -20.318 |
| w24 | 32 | -0.06292 | 5.556 |
| w25 | 47 | 0.138147 | 57.169 |
| w26 | 16 | 0.069822 | 5.588 |
| w27 | 31 | -0.05709 | 3.179 |
| w28 | 5 | -0.112162 | -8.445 |
| w29 | 38 | 0.020339 | 58.186 |
| w30 | 13 | 0.076351 | 2.061 |
| w31 | 19 | -0.059286 | -13.903 |
| w32 | 13 | 0.134307 | 18.807 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 30 | 0.05704 | 27.13 |
| w11 | 20 | 0.011588 | -3.134 |
| w12 | 4 | -0.05882 | -4.882 |
| w13 | 24 | -0.0902 | -8.382 |
| w14 | 40 | 0.061784 | 41.169 |
| w15 | 28 | 0.000752 | 4.416 |
| w16 | 49 | 0.013326 | 75.15 |
| w17 | 34 | -0.036735 | 15.065 |
| w18 | 9 | -0.121221 | -6.415 |
| w19 | 5 | 0.040852 | 2.343 |
| w20 | 10 | -0.129679 | -20.231 |
| w21 | 10 | -0.106556 | -6.303 |
| w22 | 37 | -0.197205 | -15.155 |
| w23 | 4 | -0.008609 | -2.132 |
| w24 | 35 | 0.181368 | 161.676 |
| w25 | 28 | 0.056606 | -1.352 |
| w26 | 4 | -0.10585 | -7.67 |
| w27 | 26 | 0.252979 | 89.427 |
| w28 | 13 | -0.144078 | -8.18 |
| w29 | 25 | 0.012549 | 0.171 |
| w30 | 12 | 0.079762 | 2.43 |
| w31 | 0 | None | 0.0 |
| w32 | 16 | 0.082267 | 13.527 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 40 | -0.078429 | -5.935 |
| w13 | 14 | -0.043169 | -14.999 |
| w14 | 38 | 0.091215 | 72.009 |
| w15 | 21 | 0.048272 | 5.362 |
| w16 | 48 | 0.002999 | 47.262 |
| w17 | 20 | 0.011382 | 5.325 |
| w18 | 29 | -0.181698 | -11.829 |
| w19 | 20 | -0.126347 | -2.917 |
| w20 | 15 | -0.074301 | -10.172 |
| w21 | 26 | -0.107947 | -17.849 |
| w22 | 30 | -0.151832 | -2.886 |
| w23 | 0 | -0.047589 | 0.0 |
| w24 | 38 | -0.139691 | -12.996 |
| w25 | 22 | 0.064965 | 4.74 |
| w26 | 0 | None | 0.0 |
| w27 | 22 | 0.096606 | 23.508 |
| w28 | 8 | -0.183703 | -18.045 |
| w29 | 31 | -0.086306 | -19.252 |
| w30 | 5 | 0.016658 | -3.493 |
| w31 | 10 | 0.033127 | -5.439 |
| w32 | 15 | -0.023663 | -9.136 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 21 | -0.096977 | -13.591 |
| w16 | 47 | 0.014492 | 39.787 |
| w17 | 12 | -0.0846 | -11.677 |
| w18 | 25 | 0.097785 | 16.792 |
| w19 | 2 | -0.085086 | -2.545 |
| w20 | 6 | -0.034114 | -20.004 |
| w21 | 21 | -0.024258 | -19.475 |
| w22 | 20 | -0.219121 | -10.654 |
| w23 | 2 | -0.021251 | -0.913 |
| w24 | 31 | 0.043209 | 42.78 |
| w25 | 21 | 0.019279 | -2.222 |
| w26 | 2 | 0.032956 | 1.05 |
| w27 | 20 | 0.18713 | 94.791 |
| w28 | 10 | -0.002718 | -0.873 |
| w29 | 25 | -0.024858 | -10.147 |
| w30 | 2 | 0.083931 | 0.654 |
| w31 | 13 | 0.036653 | 0.163 |
| w32 | 15 | -0.155081 | -18.693 |

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
| w15 | 25 | -0.075245 | -13.561 |
| w16 | 44 | 0.008331 | 76.239 |
| w17 | 24 | -0.036069 | 4.818 |
| w18 | 33 | -0.17916 | -32.398 |
| w19 | 13 | -0.01154 | 6.614 |
| w20 | 19 | 0.027159 | 3.964 |
| w21 | 7 | -0.025151 | -9.432 |
| w22 | 38 | -0.106349 | 1.276 |
| w23 | 53 | -0.124375 | -12.714 |
| w24 | 58 | -0.171964 | 1.771 |
| w25 | 37 | 0.063926 | 15.893 |
| w26 | 42 | 0.164148 | 54.726 |
| w27 | 42 | 0.164098 | 192.235 |
| w28 | 21 | -0.106184 | -4.898 |
| w29 | 62 | -0.090776 | 18.252 |
| w30 | 10 | 0.038319 | 0.995 |
| w31 | 50 | -0.134044 | -6.671 |
| w32 | 34 | 0.041154 | 1.332 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 51 | 0.043316 | 36.498 |
| w17 | 20 | -0.120401 | -13.797 |
| w18 | 31 | -0.044159 | -8.379 |
| w19 | 10 | 0.047956 | -0.383 |
| w20 | 6 | 0.003947 | -1.154 |
| w21 | 9 | -0.116961 | -11.837 |
| w22 | 37 | -0.184333 | -8.387 |
| w23 | 8 | -0.138773 | -10.541 |
| w24 | 32 | 0.075419 | 43.96 |
| w25 | 31 | 0.115593 | 12.349 |
| w26 | 0 | -0.142897 | 0.0 |
| w27 | 24 | 0.163127 | 46.546 |
| w28 | 6 | -0.138954 | -5.846 |
| w29 | 17 | -0.076461 | -16.369 |
| w30 | 15 | 0.06885 | 3.134 |
| w31 | 1 | -0.085009 | -1.878 |
| w32 | 1 | -0.138608 | -12.983 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.039573 | -1.345 |
| w21 | 4 | -0.090304 | -6.349 |
| w22 | 35 | -0.125386 | -0.057 |
| w23 | 2 | -0.092481 | -2.13 |
| w24 | 33 | 0.243335 | 153.976 |
| w25 | 33 | 0.04603 | 0.108 |
| w26 | 1 | 0.039662 | 2.146 |
| w27 | 41 | -0.021283 | 9.008 |
| w28 | 10 | -0.05851 | -7.058 |
| w29 | 32 | -0.080992 | -18.19 |
| w30 | 16 | 0.112965 | 12.419 |
| w31 | 11 | -0.146542 | -8.237 |
| w32 | 9 | 0.092843 | 12.671 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 27 | -0.197723 | -11.284 |
| w23 | 1 | -0.01673 | -0.678 |
| w24 | 25 | 0.136739 | 133.928 |
| w25 | 38 | 0.051699 | 23.471 |
| w26 | 9 | -0.066295 | -6.382 |
| w27 | 35 | 0.055569 | 10.516 |
| w28 | 5 | -0.016532 | -3.028 |
| w29 | 29 | -0.04317 | -14.461 |
| w30 | 14 | -0.020272 | -6.347 |
| w31 | 16 | 0.017161 | 1.277 |
| w32 | 28 | -0.017489 | 6.393 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 28 | 0.02324 | 19.824 |
| w25 | 40 | -0.043679 | 3.793 |
| w26 | 4 | -0.129502 | -13.946 |
| w27 | 59 | 0.001503 | 41.852 |
| w28 | 12 | -0.026423 | -2.857 |
| w29 | 23 | -0.108564 | -18.059 |
| w30 | 10 | 0.072307 | 0.98 |
| w31 | 8 | -0.130014 | -5.785 |
| w32 | 10 | 0.115587 | 32.386 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 27 | 0.149365 | 68.024 |
| w6 | 33 | 0.075177 | 25.456 |
| w7 | 16 | -0.005621 | -0.961 |
| w8 | 5 | 0.065741 | 2.057 |
| w9 | 5 | -0.007008 | -5.397 |
| w10 | 18 | 0.174079 | 31.742 |
| w11 | 25 | 0.171511 | 28.838 |
| w12 | 0 | None | 0.0 |
| w13 | 19 | 0.148032 | 36.668 |
| w14 | 50 | -0.040456 | 11.275 |
| w15 | 22 | -0.136713 | -31.955 |
| w16 | 49 | 0.121058 | 85.825 |
| w17 | 18 | -0.081056 | -2.872 |
| w18 | 29 | -0.089614 | -27.038 |
| w19 | 17 | -0.038597 | -4.09 |
| w20 | 5 | -0.119563 | -10.526 |
| w21 | 6 | -0.150351 | -2.643 |
| w22 | 23 | -0.119127 | -5.973 |
| w23 | 4 | -0.117965 | -8.582 |
| w24 | 37 | -0.117265 | -11.143 |
| w25 | 17 | 0.053396 | 8.326 |
| w26 | 16 | 0.197267 | 38.012 |
| w27 | 32 | -0.000648 | 15.332 |
| w28 | 12 | -0.109882 | -10.135 |
| w29 | 25 | -0.020932 | -2.01 |
| w30 | 51 | 0.05781 | 124.663 |
| w31 | 6 | 0.054217 | 4.447 |
| w32 | 41 | 0.08624 | 53.85 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 43 | 0.094562 | 113.554 |
| w6 | 37 | -0.024304 | 37.0 |
| w7 | 17 | -0.040733 | -2.091 |
| w8 | 2 | -0.080492 | -1.579 |
| w9 | 7 | -0.203062 | -20.981 |
| w10 | 32 | 0.072124 | 16.151 |
| w11 | 39 | 0.036197 | 7.091 |
| w12 | 0 | 0.000503 | 0.0 |
| w13 | 20 | 0.003798 | 6.463 |
| w14 | 51 | -0.077815 | 6.713 |
| w15 | 53 | -0.127382 | -13.674 |
| w16 | 52 | -0.004543 | 47.169 |
| w17 | 26 | -0.096642 | -16.782 |
| w18 | 21 | -0.043987 | -14.995 |
| w19 | 21 | -0.07972 | -6.066 |
| w20 | 10 | -0.21001 | -17.481 |
| w21 | 27 | -0.250226 | -24.585 |
| w22 | 35 | -0.137929 | -16.128 |
| w23 | 17 | 0.001871 | -5.549 |
| w24 | 35 | -0.133371 | -9.951 |
| w25 | 5 | 0.00873 | -5.974 |
| w26 | 33 | -0.069569 | -4.243 |
| w27 | 37 | 0.002134 | 13.436 |
| w28 | 34 | -0.080954 | 9.075 |
| w29 | 20 | 0.09751 | 27.226 |
| w30 | 42 | -0.17728 | -7.835 |
| w31 | 22 | 0.118544 | 23.393 |
| w32 | 39 | -0.10443 | -4.21 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 15 | -0.215561 | -24.245 |
| w18 | 40 | 0.047179 | 26.379 |
| w19 | 15 | -0.041277 | -13.079 |
| w20 | 19 | -0.228376 | -25.267 |
| w21 | 7 | -0.04054 | -3.404 |
| w22 | 30 | 0.086917 | 35.757 |
| w23 | 3 | -0.143226 | -7.091 |
| w24 | 33 | -0.130554 | -10.53 |
| w25 | 14 | 0.12329 | 7.785 |
| w26 | 7 | -0.01189 | -7.8 |
| w27 | 21 | 0.150908 | 141.441 |
| w28 | 18 | -0.052297 | -1.109 |
| w29 | 35 | -0.012199 | -5.02 |
| w30 | 5 | -0.003543 | -0.536 |
| w31 | 7 | -0.049604 | -8.349 |
| w32 | 17 | 0.022281 | 8.653 |

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
| w17 | 28 | -0.194178 | -27.385 |
| w18 | 8 | -0.067138 | -10.758 |
| w19 | 9 | 0.091089 | 6.973 |
| w20 | 12 | -0.031194 | -2.796 |
| w21 | 15 | -0.149054 | -14.376 |
| w22 | 31 | 0.040209 | 47.25 |
| w23 | 19 | -0.049615 | -9.599 |
| w24 | 34 | -0.08364 | 6.611 |
| w25 | 23 | -0.112446 | -28.611 |
| w26 | 20 | 0.109348 | 33.42 |
| w27 | 46 | -0.04657 | 18.463 |
| w28 | 12 | -0.089901 | -5.406 |
| w29 | 48 | -0.131819 | 9.168 |
| w30 | 10 | 0.026973 | -2.339 |
| w31 | 2 | -0.042015 | -2.861 |
| w32 | 18 | 0.112445 | 21.041 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 11 | -0.013799 | 0.134 |
| w20 | 5 | -0.050152 | -10.258 |
| w21 | 35 | -0.080381 | -10.652 |
| w22 | 39 | 0.087628 | 108.687 |
| w23 | 27 | 0.014983 | 2.532 |
| w24 | 38 | 0.241684 | 224.424 |
| w25 | 27 | -0.066025 | -11.282 |
| w26 | 4 | -0.007619 | -10.732 |
| w27 | 31 | 0.005514 | -4.81 |
| w28 | 4 | 0.003515 | -2.298 |
| w29 | 42 | -0.062549 | -12.797 |
| w30 | 12 | 0.082285 | 1.324 |
| w31 | 11 | -0.035607 | -0.321 |
| w32 | 31 | 0.000369 | 16.568 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 36 | -0.07565 | 2.977 |
| w23 | 8 | -0.066182 | -8.686 |
| w24 | 27 | -0.051226 | 10.54 |
| w25 | 33 | -0.043417 | -16.656 |
| w26 | 10 | -0.028335 | 3.483 |
| w27 | 29 | -0.05651 | -9.353 |
| w28 | 15 | -0.133368 | -15.057 |
| w29 | 18 | 0.027101 | 9.318 |
| w30 | 14 | -0.051471 | -6.117 |
| w31 | 8 | -0.052686 | -1.777 |
| w32 | 22 | 0.057807 | 7.378 |

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
| w27 | 30 | 0.074353 | 21.283 |
| w28 | 16 | -0.132388 | -7.077 |
| w29 | 30 | -0.005256 | -5.729 |
| w30 | 11 | 0.072242 | 0.478 |
| w31 | 5 | -0.053312 | -2.241 |
| w32 | 35 | 0.07427 | 25.613 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | -0.08094 | -7.815 |
| w18 | 16 | -0.008418 | -13.916 |
| w19 | 3 | 0.149074 | 15.597 |
| w20 | 4 | -0.140728 | -12.858 |
| w21 | 12 | -0.157405 | -17.056 |
| w22 | 26 | -0.094414 | 8.488 |
| w23 | 5 | -0.126998 | -6.828 |
| w24 | 35 | -0.125842 | 0.138 |
| w25 | 39 | 0.040755 | 1.489 |
| w26 | 0 | None | 0.0 |
| w27 | 27 | 0.019878 | 5.035 |
| w28 | 10 | -0.081603 | -5.461 |
| w29 | 18 | -0.132708 | -22.006 |
| w30 | 5 | -0.165771 | -11.037 |
| w31 | 6 | -0.071045 | -5.068 |
| w32 | 10 | -0.10988 | -16.608 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.00138 | -2.087 |
| w18 | 32 | -0.153241 | -29.476 |
| w19 | 11 | 0.021741 | -1.772 |
| w20 | 5 | -0.059867 | -10.475 |
| w21 | 9 | -0.095507 | -25.527 |
| w22 | 37 | 0.04992 | 52.111 |
| w23 | 5 | -0.170398 | -16.091 |
| w24 | 32 | 0.059683 | 60.551 |
| w25 | 33 | 0.040221 | 23.916 |
| w26 | 0 | None | 0.0 |
| w27 | 31 | 0.064804 | 10.671 |
| w28 | 7 | -0.069719 | -9.707 |
| w29 | 23 | -0.131737 | -17.795 |
| w30 | 5 | 0.041743 | 0.385 |
| w31 | 0 | None | 0.0 |
| w32 | 12 | 0.024518 | -5.224 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 8 | -0.040536 | -7.164 |
| w29 | 22 | -0.104317 | -13.976 |
| w30 | 13 | -0.118694 | -13.949 |
| w31 | 10 | -0.089567 | -13.056 |
| w32 | 18 | -0.013264 | -9.83 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 29 | 0.053906 | 50.493 |
| w15 | 19 | 0.087193 | 41.908 |
| w16 | 22 | 0.048833 | 249.941 |
| w17 | 20 | 0.029996 | -3.071 |
| w18 | 17 | 0.008098 | -9.373 |
| w19 | 9 | -0.268606 | -23.262 |
| w20 | 7 | -0.073139 | -8.606 |
| w21 | 20 | 0.251893 | 65.015 |
| w22 | 19 | -0.127563 | -18.253 |
| w23 | 13 | 0.012751 | -0.111 |
| w24 | 26 | -0.030646 | 9.861 |
| w25 | 26 | 0.197909 | 60.577 |
| w26 | 6 | -0.094541 | -4.878 |
| w27 | 27 | 0.157718 | 72.056 |
| w28 | 7 | -0.081714 | -8.303 |
| w29 | 27 | -0.022179 | -0.416 |
| w30 | 17 | 0.156246 | 13.278 |
| w31 | 10 | 0.056548 | 9.626 |
| w32 | 15 | -0.030253 | -8.81 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 30 | 0.342262 | 113.855 |
| w26 | 18 | 0.018439 | 2.063 |
| w27 | 27 | 0.074653 | 25.356 |
| w28 | 6 | -0.02326 | -2.336 |
| w29 | 26 | -0.035473 | -8.307 |
| w30 | 0 | -0.067896 | 0.0 |
| w31 | 10 | -0.050554 | -4.005 |
| w32 | 13 | 0.208641 | 30.82 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

