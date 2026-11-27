# Backtest of 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-uptrend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.024845 | 2.416 |
| w2 | 25 | 0.165238 | 85.499 |
| w3 | 42 | 0.05155 | 90.081 |
| w4 | 33 | -0.010878 | 6.486 |
| w5 | 41 | 0.040576 | 97.735 |
| w6 | 45 | 0.094003 | 104.997 |
| w7 | 4 | -0.04105 | -0.9 |
| w8 | 9 | 0.00759 | -1.503 |
| w9 | 6 | -0.060348 | -8.855 |
| w10 | 30 | 0.035291 | 27.245 |
| w11 | 46 | 0.102783 | 51.228 |
| w12 | 1 | -0.062532 | -0.431 |
| w13 | 22 | -0.039233 | 0.456 |
| w14 | 33 | -0.034543 | 17.883 |
| w15 | 28 | 0.110033 | 118.028 |
| w16 | 45 | -0.007828 | 23.984 |
| w17 | 24 | 0.054122 | 6.161 |
| w18 | 33 | 0.057226 | 7.478 |
| w19 | 12 | 0.020072 | -0.026 |
| w20 | 4 | -0.014998 | -2.025 |
| w21 | 13 | -0.130958 | -16.988 |
| w22 | 35 | 0.017652 | 59.882 |
| w23 | 17 | 0.058349 | 5.923 |
| w24 | 23 | 0.066763 | 58.329 |
| w25 | 29 | 0.117508 | 54.924 |
| w26 | 11 | -0.033312 | -4.612 |
| w27 | 31 | 0.030241 | 50.777 |
| w28 | 14 | -0.062002 | -7.686 |
| w29 | 45 | 0.031847 | 12.082 |
| w30 | 7 | -0.003124 | -5.446 |
| w31 | 21 | -0.004002 | -6.635 |
| w32 | 16 | 0.177485 | 35.823 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | -0.064571 | -9.323 |
| w2 | 21 | 0.121848 | 34.059 |
| w3 | 22 | -0.138728 | -25.082 |
| w4 | 29 | 0.12261 | 78.256 |
| w5 | 61 | 0.004161 | 41.016 |
| w6 | 24 | 0.152118 | 119.217 |
| w7 | 6 | -0.121244 | -1.667 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.065942 | -3.904 |
| w10 | 35 | -0.039385 | 21.577 |
| w11 | 33 | 0.04177 | 4.088 |
| w12 | 0 | None | 0.0 |
| w13 | 23 | -0.018253 | 2.121 |
| w14 | 33 | -0.037456 | 3.819 |
| w15 | 35 | -0.017644 | 16.124 |
| w16 | 53 | -0.040711 | 11.821 |
| w17 | 17 | 0.005236 | -5.976 |
| w18 | 29 | 0.001744 | -3.228 |
| w19 | 10 | -0.005508 | -4.46 |
| w20 | 9 | -0.041513 | -5.494 |
| w21 | 35 | -0.089605 | -14.59 |
| w22 | 42 | -0.061074 | -5.061 |
| w23 | 23 | -0.113934 | -18.866 |
| w24 | 27 | -0.122075 | -15.021 |
| w25 | 26 | 0.001534 | 9.44 |
| w26 | 3 | -0.071932 | -3.288 |
| w27 | 37 | 0.012762 | 23.893 |
| w28 | 29 | -0.120025 | -14.551 |
| w29 | 35 | -0.006365 | 8.201 |
| w30 | 10 | -0.273719 | -28.79 |
| w31 | 10 | -0.027933 | -5.061 |
| w32 | 14 | 0.071662 | 8.175 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 33 | 0.193405 | 143.698 |
| w7 | 5 | 0.033289 | -0.052 |
| w8 | 4 | -0.085685 | -1.555 |
| w9 | 16 | -0.10171 | -9.788 |
| w10 | 6 | -0.024675 | -4.086 |
| w11 | 30 | -0.00187 | 1.045 |
| w12 | 18 | -0.080691 | -8.716 |
| w13 | 16 | 0.03188 | 9.939 |
| w14 | 26 | 0.10463 | 39.798 |
| w15 | 21 | 0.216595 | 149.818 |
| w16 | 28 | 0.057511 | 63.676 |
| w17 | 21 | 0.013788 | 8.359 |
| w18 | 19 | -0.066021 | -8.428 |
| w19 | 18 | -0.102626 | -12.997 |
| w20 | 4 | -0.010851 | -1.974 |
| w21 | 23 | -0.039896 | -6.407 |
| w22 | 30 | -0.09706 | -8.008 |
| w23 | 16 | -0.097564 | -18.431 |
| w24 | 19 | 0.025247 | 17.775 |
| w25 | 17 | -0.165566 | -19.29 |
| w26 | 16 | 0.027789 | 9.15 |
| w27 | 21 | 0.3379 | 267.202 |
| w28 | 22 | -0.107733 | -10.705 |
| w29 | 25 | 0.074619 | 25.087 |
| w30 | 6 | 0.026621 | 0.333 |
| w31 | 5 | -0.028952 | -3.224 |
| w32 | 10 | 0.035064 | 0.295 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 14 | -0.074824 | -7.922 |
| w8 | 8 | 0.058674 | 1.34 |
| w9 | 5 | 0.002949 | -4.4 |
| w10 | 17 | 0.145327 | 54.925 |
| w11 | 21 | -0.020322 | -3.82 |
| w12 | 9 | -0.046641 | -7.337 |
| w13 | 13 | -0.026431 | 2.555 |
| w14 | 31 | -0.027618 | -3.1 |
| w15 | 28 | -0.112153 | -18.388 |
| w16 | 46 | 0.056286 | 46.816 |
| w17 | 23 | -0.013413 | -3.641 |
| w18 | 15 | -0.152613 | -19.604 |
| w19 | 9 | -0.02728 | -7.985 |
| w20 | 4 | -0.028443 | -1.107 |
| w21 | 8 | -0.190981 | -15.537 |
| w22 | 33 | 0.03014 | 15.794 |
| w23 | 15 | 0.22919 | 71.607 |
| w24 | 23 | -0.183017 | -24.474 |
| w25 | 39 | 0.104313 | 67.357 |
| w26 | 4 | -0.013869 | -1.649 |
| w27 | 32 | 0.006715 | 7.342 |
| w28 | 11 | -0.000865 | -1.439 |
| w29 | 71 | -0.283166 | -21.465 |
| w30 | 36 | -0.192867 | -23.755 |
| w31 | 11 | -0.035521 | -6.269 |
| w32 | 9 | 0.027435 | 3.995 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.18055 | 198.084 |
| w2 | 18 | -0.024164 | 0.018 |
| w3 | 28 | 0.088488 | 1.676 |
| w4 | 41 | 0.020591 | 160.296 |
| w5 | 29 | 0.173612 | 112.688 |
| w6 | 33 | -0.006744 | 35.543 |
| w7 | 16 | 0.078923 | 17.981 |
| w8 | 7 | -0.122684 | -5.264 |
| w9 | 4 | -0.026699 | -2.413 |
| w10 | 26 | 0.010336 | 4.914 |
| w11 | 31 | 0.118733 | 31.436 |
| w12 | 13 | -0.065816 | -6.003 |
| w13 | 18 | 0.054339 | 38.233 |
| w14 | 47 | 0.002769 | 54.855 |
| w15 | 35 | -0.027057 | 15.042 |
| w16 | 52 | -0.049034 | 57.312 |
| w17 | 21 | 0.082385 | 36.516 |
| w18 | 42 | -0.056619 | -10.787 |
| w19 | 7 | 0.060199 | 5.034 |
| w20 | 6 | -0.002672 | -1.845 |
| w21 | 9 | -0.072542 | -10.855 |
| w22 | 41 | -0.046764 | 18.805 |
| w23 | 23 | -0.170186 | -18.229 |
| w24 | 28 | -0.029663 | 19.797 |
| w25 | 23 | 0.144366 | 62.95 |
| w26 | 9 | 0.009272 | -0.815 |
| w27 | 30 | 0.006054 | 14.829 |
| w28 | 3 | -0.104661 | -3.356 |
| w29 | 39 | -0.026552 | 51.324 |
| w30 | 12 | -0.042559 | -4.768 |
| w31 | 20 | -0.047762 | -12.271 |
| w32 | 17 | 0.119245 | 22.966 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 20 | 0.107832 | 57.558 |
| w11 | 29 | -0.108326 | -13.11 |
| w12 | 2 | -0.048443 | -0.594 |
| w13 | 23 | -0.011005 | 13.641 |
| w14 | 49 | -0.004864 | 39.688 |
| w15 | 30 | 0.006665 | 8.715 |
| w16 | 47 | 0.09342 | 94.472 |
| w17 | 21 | 0.029722 | 30.126 |
| w18 | 3 | -0.063476 | -4.767 |
| w19 | 4 | 0.021493 | -1.564 |
| w20 | 9 | -0.043537 | -6.945 |
| w21 | 5 | -0.094682 | -6.184 |
| w22 | 28 | -0.130667 | -9.605 |
| w23 | 2 | -0.019243 | -0.875 |
| w24 | 24 | 0.13512 | 128.407 |
| w25 | 14 | 0.078482 | 7.414 |
| w26 | 3 | -0.099716 | -5.461 |
| w27 | 16 | 0.259816 | 148.403 |
| w28 | 10 | -0.192009 | -13.787 |
| w29 | 28 | -0.049053 | -4.442 |
| w30 | 13 | -0.034505 | -6.754 |
| w31 | 0 | None | 0.0 |
| w32 | 16 | 0.017631 | -0.548 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 39 | -0.096795 | -7.0 |
| w13 | 21 | -0.035298 | -12.576 |
| w14 | 38 | 0.002024 | 47.715 |
| w15 | 26 | -0.060682 | -8.494 |
| w16 | 52 | -0.005524 | 36.855 |
| w17 | 19 | 0.037104 | 15.416 |
| w18 | 34 | -0.128667 | -12.587 |
| w19 | 20 | -0.081368 | -12.97 |
| w20 | 24 | -0.028332 | -6.741 |
| w21 | 21 | -0.04826 | -11.407 |
| w22 | 27 | -0.046631 | -4.718 |
| w23 | 0 | None | 0.0 |
| w24 | 28 | -0.02785 | 18.822 |
| w25 | 12 | 0.090704 | 11.718 |
| w26 | 0 | None | 0.0 |
| w27 | 17 | 0.155042 | 56.66 |
| w28 | 6 | -0.153683 | -6.244 |
| w29 | 26 | -0.116679 | -21.353 |
| w30 | 3 | -0.001275 | -2.123 |
| w31 | 14 | -0.107852 | -12.198 |
| w32 | 24 | -0.052659 | -13.24 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 18 | -0.127352 | -19.294 |
| w16 | 52 | 0.018452 | 53.239 |
| w17 | 16 | -0.084237 | -12.976 |
| w18 | 27 | 0.017787 | 15.722 |
| w19 | 2 | -0.118433 | -6.624 |
| w20 | 6 | -0.013904 | -3.054 |
| w21 | 11 | 0.001718 | -10.33 |
| w22 | 14 | -0.138742 | -12.277 |
| w23 | 3 | -0.056838 | -2.604 |
| w24 | 26 | 0.101206 | 89.125 |
| w25 | 14 | 0.00297 | -2.204 |
| w26 | 3 | -0.008337 | -1.729 |
| w27 | 16 | 0.237498 | 138.355 |
| w28 | 9 | -0.059536 | -3.488 |
| w29 | 26 | -0.075679 | -10.906 |
| w30 | 0 | None | 0.0 |
| w31 | 16 | 0.001988 | -2.151 |
| w32 | 18 | -0.106348 | -16.773 |

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
| w15 | 26 | -0.062563 | -10.717 |
| w16 | 53 | -0.011815 | 62.732 |
| w17 | 16 | 0.019264 | 3.65 |
| w18 | 33 | -0.176348 | -26.858 |
| w19 | 10 | 0.00296 | -2.185 |
| w20 | 28 | -0.09293 | -11.107 |
| w21 | 9 | -0.00056 | -1.894 |
| w22 | 36 | -0.066882 | -0.84 |
| w23 | 36 | -0.066714 | -3.228 |
| w24 | 44 | -0.092849 | 20.523 |
| w25 | 19 | 0.102801 | 30.11 |
| w26 | 36 | 0.073454 | 38.902 |
| w27 | 50 | 0.097927 | 193.66 |
| w28 | 24 | -0.13475 | -15.332 |
| w29 | 65 | -0.029961 | 39.269 |
| w30 | 9 | -0.116196 | -3.848 |
| w31 | 39 | -0.056076 | 4.97 |
| w32 | 25 | 0.110005 | 16.631 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 45 | 0.040877 | 44.238 |
| w17 | 20 | -0.057012 | -9.23 |
| w18 | 31 | -0.042803 | -9.23 |
| w19 | 13 | 0.026272 | -2.668 |
| w20 | 8 | -0.032945 | -5.313 |
| w21 | 3 | -0.092994 | -4.8 |
| w22 | 32 | -0.100006 | -7.809 |
| w23 | 5 | -0.124825 | -7.343 |
| w24 | 36 | 0.038518 | 32.351 |
| w25 | 15 | 0.125328 | 19.53 |
| w26 | 0 | None | 0.0 |
| w27 | 19 | 0.180488 | 72.582 |
| w28 | 2 | -0.17393 | -1.342 |
| w29 | 13 | -0.026363 | -5.482 |
| w30 | 16 | -0.029601 | -11.288 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.13781 | -10.773 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.024118 | -1.466 |
| w21 | 2 | -0.166242 | -6.545 |
| w22 | 26 | -0.024917 | 6.343 |
| w23 | 0 | None | 0.0 |
| w24 | 29 | 0.22133 | 148.001 |
| w25 | 28 | 0.036685 | 3.639 |
| w26 | 3 | 0.01885 | 0.286 |
| w27 | 31 | 0.056353 | 32.241 |
| w28 | 4 | -0.056705 | -3.403 |
| w29 | 37 | -0.083715 | -12.347 |
| w30 | 13 | 0.078909 | 5.849 |
| w31 | 7 | -0.117569 | -6.609 |
| w32 | 10 | 0.088391 | 11.18 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 24 | -0.107338 | -6.728 |
| w23 | 0 | None | 0.0 |
| w24 | 32 | 0.060803 | 75.405 |
| w25 | 34 | 0.082192 | 33.552 |
| w26 | 21 | -0.073346 | -8.683 |
| w27 | 28 | -0.003904 | 6.799 |
| w28 | 1 | -0.107404 | -0.971 |
| w29 | 26 | -0.045553 | -10.043 |
| w30 | 18 | -0.086562 | -16.019 |
| w31 | 18 | -0.015339 | -2.92 |
| w32 | 28 | 0.035217 | 27.841 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 34 | -0.028364 | 6.674 |
| w25 | 45 | -0.022051 | 1.931 |
| w26 | 6 | -0.13825 | -7.814 |
| w27 | 47 | -0.044844 | 57.673 |
| w28 | 11 | -0.030805 | -3.286 |
| w29 | 27 | -0.087858 | -13.357 |
| w30 | 6 | 0.045822 | 0.902 |
| w31 | 6 | -0.121459 | -8.412 |
| w32 | 15 | 0.072704 | 19.288 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 26 | 0.164137 | 88.83 |
| w6 | 35 | -0.004808 | 11.746 |
| w7 | 12 | -0.036284 | -1.133 |
| w8 | 7 | -0.048587 | -2.944 |
| w9 | 7 | -0.019676 | -7.192 |
| w10 | 23 | 0.074835 | 15.488 |
| w11 | 39 | 0.044524 | 3.522 |
| w12 | 0 | None | 0.0 |
| w13 | 13 | 0.109992 | 45.998 |
| w14 | 53 | -0.068477 | 12.618 |
| w15 | 23 | -0.09164 | -13.526 |
| w16 | 45 | 0.039081 | 59.684 |
| w17 | 24 | -0.01677 | -7.24 |
| w18 | 26 | -0.13946 | -23.812 |
| w19 | 15 | -0.024477 | -3.501 |
| w20 | 7 | -0.058378 | -6.187 |
| w21 | 2 | -0.025948 | -0.312 |
| w22 | 27 | -0.128861 | -17.434 |
| w23 | 2 | -0.15882 | -3.525 |
| w24 | 39 | -0.09726 | -12.002 |
| w25 | 13 | 0.039189 | 2.166 |
| w26 | 26 | 0.089279 | 24.416 |
| w27 | 28 | -0.058729 | 1.578 |
| w28 | 8 | -0.100608 | -5.118 |
| w29 | 36 | 0.008671 | 3.054 |
| w30 | 46 | 0.127385 | 162.584 |
| w31 | 16 | 0.040943 | 3.137 |
| w32 | 29 | 0.071495 | 54.651 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 46 | 0.123488 | 144.299 |
| w6 | 24 | 0.067262 | 58.388 |
| w7 | 11 | -0.031723 | -5.127 |
| w8 | 0 | None | 0.0 |
| w9 | 4 | -0.188778 | -17.234 |
| w10 | 37 | -0.037495 | 6.739 |
| w11 | 48 | -0.004676 | 1.525 |
| w12 | 0 | None | 0.0 |
| w13 | 22 | -0.003046 | 12.507 |
| w14 | 47 | -0.095827 | 13.256 |
| w15 | 59 | -0.110776 | -3.313 |
| w16 | 42 | 0.014885 | 47.547 |
| w17 | 21 | -0.04423 | -11.702 |
| w18 | 17 | -0.157958 | -16.41 |
| w19 | 32 | -0.028405 | -5.462 |
| w20 | 6 | -0.057826 | -4.61 |
| w21 | 17 | -0.204326 | -29.059 |
| w22 | 21 | -0.006679 | -0.352 |
| w23 | 14 | -0.011712 | -4.112 |
| w24 | 36 | -0.086568 | -9.606 |
| w25 | 1 | -0.040605 | -0.674 |
| w26 | 24 | -0.047375 | -1.862 |
| w27 | 34 | -0.018638 | -2.5 |
| w28 | 40 | -0.012316 | 14.07 |
| w29 | 9 | 0.175501 | 49.124 |
| w30 | 52 | -0.173769 | -12.133 |
| w31 | 23 | 0.079806 | 17.49 |
| w32 | 26 | 0.071878 | 48.233 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | -0.215146 | -28.417 |
| w18 | 53 | -0.138158 | -12.366 |
| w19 | 8 | -0.102448 | -11.556 |
| w20 | 16 | -0.136998 | -12.789 |
| w21 | 3 | -0.047911 | -0.924 |
| w22 | 22 | 0.13077 | 40.375 |
| w23 | 3 | -0.075589 | -3.542 |
| w24 | 34 | -0.126605 | -11.151 |
| w25 | 9 | 0.066716 | 5.191 |
| w26 | 7 | -0.047163 | -4.451 |
| w27 | 30 | 0.188143 | 100.862 |
| w28 | 18 | 0.016339 | 1.83 |
| w29 | 32 | 0.047753 | 14.442 |
| w30 | 1 | -0.027973 | -0.382 |
| w31 | 5 | -0.053119 | -5.24 |
| w32 | 24 | 0.04311 | 16.311 |

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
| w17 | 23 | -0.093725 | -19.992 |
| w18 | 10 | -0.160351 | -12.375 |
| w19 | 11 | 0.081133 | 11.753 |
| w20 | 15 | -0.057943 | -7.322 |
| w21 | 9 | -0.151471 | -17.301 |
| w22 | 22 | 0.072589 | 24.984 |
| w23 | 18 | -0.066337 | -6.729 |
| w24 | 46 | -0.066435 | 14.477 |
| w25 | 22 | -0.104062 | -19.776 |
| w26 | 27 | -0.020705 | 2.368 |
| w27 | 48 | -0.028181 | 25.321 |
| w28 | 11 | -0.12243 | -5.198 |
| w29 | 47 | -0.133477 | -6.892 |
| w30 | 3 | -0.147821 | -5.562 |
| w31 | 2 | -0.044065 | -2.35 |
| w32 | 18 | 0.051807 | 11.164 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 17 | -0.019234 | -4.903 |
| w20 | 10 | -0.031148 | -7.756 |
| w21 | 26 | -0.088987 | -18.454 |
| w22 | 45 | 0.045753 | 109.229 |
| w23 | 24 | -0.033113 | -4.708 |
| w24 | 31 | 0.158088 | 211.382 |
| w25 | 27 | -0.050187 | -10.227 |
| w26 | 9 | -0.029133 | -6.128 |
| w27 | 32 | -0.032576 | -1.73 |
| w28 | 2 | -0.067301 | -1.435 |
| w29 | 36 | -0.056033 | -6.054 |
| w30 | 4 | 0.043772 | -0.559 |
| w31 | 7 | -0.028664 | -5.967 |
| w32 | 32 | 0.036181 | 27.048 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 34 | 0.001485 | 10.97 |
| w23 | 6 | -0.059919 | -6.089 |
| w24 | 36 | -0.088877 | 5.243 |
| w25 | 41 | -0.06307 | -15.679 |
| w26 | 10 | -0.120976 | -7.492 |
| w27 | 28 | -0.026072 | 1.707 |
| w28 | 14 | -0.163485 | -10.737 |
| w29 | 23 | 0.004766 | 9.69 |
| w30 | 8 | -0.115564 | -6.023 |
| w31 | 11 | -0.048376 | -6.949 |
| w32 | 20 | -0.053186 | -6.221 |

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
| w27 | 33 | 0.088022 | 41.399 |
| w28 | 8 | -0.07663 | -4.746 |
| w29 | 21 | -0.027723 | -4.246 |
| w30 | 8 | 0.029844 | -1.626 |
| w31 | 5 | -0.054238 | -2.894 |
| w32 | 28 | 0.018389 | 33.199 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 15 | -0.045095 | -8.093 |
| w18 | 8 | -0.01362 | -4.339 |
| w19 | 9 | 0.030178 | -0.782 |
| w20 | 10 | -0.093621 | -11.948 |
| w21 | 3 | -0.124779 | -11.644 |
| w22 | 33 | -0.122791 | -8.381 |
| w23 | 5 | -0.108518 | -5.554 |
| w24 | 36 | -0.043765 | 21.557 |
| w25 | 25 | 0.116419 | 20.82 |
| w26 | 0 | None | 0.0 |
| w27 | 23 | 0.091682 | 27.695 |
| w28 | 5 | -0.121514 | -2.428 |
| w29 | 11 | -0.149062 | -20.026 |
| w30 | 5 | -0.178079 | -9.102 |
| w31 | 8 | -0.044207 | -5.664 |
| w32 | 9 | -0.108085 | -17.025 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 12 | 0.056912 | 6.633 |
| w18 | 21 | -0.093011 | -16.815 |
| w19 | 11 | -0.005161 | -3.527 |
| w20 | 9 | -0.036865 | -6.06 |
| w21 | 4 | -0.207865 | -14.374 |
| w22 | 34 | 0.06401 | 72.899 |
| w23 | 4 | -0.165553 | -8.238 |
| w24 | 37 | 0.021824 | 46.151 |
| w25 | 26 | 0.151501 | 58.948 |
| w26 | 0 | None | 0.0 |
| w27 | 28 | 0.035059 | 12.177 |
| w28 | 2 | -0.148773 | -2.015 |
| w29 | 22 | -0.111463 | -15.176 |
| w30 | 3 | 0.042486 | 0.738 |
| w31 | 0 | None | 0.0 |
| w32 | 12 | -0.007045 | -8.007 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 7 | -0.056979 | -6.849 |
| w29 | 27 | -0.043137 | -8.704 |
| w30 | 14 | -0.110531 | -14.059 |
| w31 | 14 | -0.017912 | -1.963 |
| w32 | 21 | -0.005753 | -3.311 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 49 | -0.00599 | 38.358 |
| w15 | 23 | 0.087443 | 45.927 |
| w16 | 49 | -0.030899 | 231.604 |
| w17 | 19 | 0.000268 | -4.817 |
| w18 | 11 | -0.148109 | -11.255 |
| w19 | 7 | -0.122913 | -13.908 |
| w20 | 4 | 0.048895 | 0.893 |
| w21 | 17 | 0.140607 | 53.872 |
| w22 | 15 | -0.117248 | -11.621 |
| w23 | 15 | -0.026451 | -4.879 |
| w24 | 38 | -0.005049 | 13.47 |
| w25 | 24 | 0.163327 | 66.206 |
| w26 | 7 | -0.06805 | -2.58 |
| w27 | 24 | 0.190248 | 134.027 |
| w28 | 5 | -0.107944 | -4.855 |
| w29 | 26 | -0.019403 | -1.857 |
| w30 | 13 | 0.035564 | -2.711 |
| w31 | 5 | 0.098822 | 11.462 |
| w32 | 15 | -0.045333 | -13.927 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 22 | 0.285845 | 112.054 |
| w26 | 19 | 0.045878 | 8.91 |
| w27 | 41 | 0.031822 | 35.602 |
| w28 | 6 | -0.010762 | -2.295 |
| w29 | 19 | 0.004846 | -0.531 |
| w30 | 0 | None | 0.0 |
| w31 | 16 | -0.028595 | -4.883 |
| w32 | 18 | 0.105656 | 20.187 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

