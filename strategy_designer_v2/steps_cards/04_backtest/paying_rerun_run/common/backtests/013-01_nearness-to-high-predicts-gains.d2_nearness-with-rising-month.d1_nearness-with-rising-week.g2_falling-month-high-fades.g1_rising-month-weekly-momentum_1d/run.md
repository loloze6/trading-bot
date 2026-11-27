# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d

- Plan: `../../../../../03_test_plan/hold_paying_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d1_nearness-with-rising-week.g2_falling-month-high-fades.g1_rising-month-weekly-momentum_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 23 | -0.065183 | 3.337 |
| w2 | 18 | 0.184543 | 80.281 |
| w3 | 45 | -0.007289 | 77.37 |
| w4 | 29 | -0.058002 | -26.342 |
| w5 | 35 | -0.038705 | 76.08 |
| w6 | 36 | 0.121712 | 78.368 |
| w7 | 12 | -0.120079 | -12.424 |
| w8 | 9 | 0.11068 | 5.171 |
| w9 | 8 | -0.160969 | -10.35 |
| w10 | 32 | 0.062184 | 32.595 |
| w11 | 29 | 0.12438 | 63.81 |
| w12 | 10 | 0.057498 | 3.938 |
| w13 | 33 | 0.021594 | 16.172 |
| w14 | 33 | 0.02809 | 22.428 |
| w15 | 41 | 0.037886 | 69.504 |
| w16 | 31 | -0.00394 | 43.398 |
| w17 | 20 | 0.039577 | 5.316 |
| w18 | 27 | -0.063429 | -14.889 |
| w19 | 12 | -0.029074 | -11.894 |
| w20 | 11 | -0.004015 | -9.562 |
| w21 | 13 | -0.046372 | -17.773 |
| w22 | 35 | 0.126221 | 86.798 |
| w23 | 10 | 0.057596 | 1.511 |
| w24 | 30 | 0.028536 | 53.891 |
| w25 | 32 | 0.020521 | 21.221 |
| w26 | 17 | 0.023449 | 2.144 |
| w27 | 42 | -0.039167 | 30.88 |
| w28 | 14 | -0.023719 | 2.638 |
| w29 | 33 | -0.013451 | 4.342 |
| w30 | 13 | 0.065238 | -0.782 |
| w31 | 29 | -0.020195 | -16.423 |
| w32 | 23 | 0.13981 | 15.268 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.051663 | 16.483 |
| w2 | 17 | 0.025096 | -0.718 |
| w3 | 26 | -0.104811 | -13.648 |
| w4 | 35 | 0.109089 | 165.34 |
| w5 | 23 | -0.016932 | 31.857 |
| w6 | 30 | 0.16633 | 148.666 |
| w7 | 5 | -0.101719 | -16.935 |
| w8 | 5 | 0.005505 | -7.908 |
| w9 | 7 | -0.048826 | -9.619 |
| w10 | 27 | -0.099262 | 12.06 |
| w11 | 19 | 0.027385 | 7.47 |
| w12 | 10 | -0.035792 | -23.963 |
| w13 | 28 | 0.05223 | 25.156 |
| w14 | 30 | 0.02229 | 14.149 |
| w15 | 31 | -0.043125 | 2.805 |
| w16 | 33 | -0.04032 | 27.774 |
| w17 | 15 | 0.066988 | 32.42 |
| w18 | 18 | -0.042759 | -2.666 |
| w19 | 11 | -0.075766 | -30.244 |
| w20 | 13 | -0.033398 | -5.152 |
| w21 | 20 | 0.035322 | 6.089 |
| w22 | 31 | -0.135923 | -10.078 |
| w23 | 11 | -0.096976 | -2.727 |
| w24 | 28 | -0.107118 | -10.17 |
| w25 | 27 | -0.00269 | 2.948 |
| w26 | 6 | -0.072989 | -4.164 |
| w27 | 36 | -0.025376 | 49.917 |
| w28 | 12 | -0.101334 | -17.13 |
| w29 | 22 | 0.033932 | 20.324 |
| w30 | 10 | -0.123858 | -22.699 |
| w31 | 16 | -0.047505 | -7.527 |
| w32 | 22 | 0.017514 | -12.263 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 26 | 0.157066 | 89.193 |
| w7 | 11 | 0.104563 | 14.965 |
| w8 | 4 | 0.037062 | -3.635 |
| w9 | 11 | 0.170996 | 20.709 |
| w10 | 18 | -0.129031 | -12.834 |
| w11 | 15 | -0.027362 | -5.921 |
| w12 | 17 | -0.007518 | -26.293 |
| w13 | 21 | 0.020259 | 7.223 |
| w14 | 22 | 0.154424 | 48.077 |
| w15 | 22 | 0.222186 | 126.977 |
| w16 | 25 | 0.077832 | 68.265 |
| w17 | 15 | 0.060469 | 27.731 |
| w18 | 11 | -0.137946 | -13.909 |
| w19 | 13 | -0.0999 | -4.715 |
| w20 | 11 | 0.011745 | -6.814 |
| w21 | 16 | 0.074244 | 11.513 |
| w22 | 14 | -0.050997 | 5.338 |
| w23 | 14 | -0.025203 | -0.501 |
| w24 | 22 | 0.080801 | 35.354 |
| w25 | 19 | -0.073017 | -11.864 |
| w26 | 15 | 0.058462 | 9.97 |
| w27 | 21 | 0.361122 | 252.148 |
| w28 | 11 | -0.024777 | -4.923 |
| w29 | 16 | 0.092493 | 40.246 |
| w30 | 7 | -0.11787 | -22.062 |
| w31 | 13 | -0.008937 | -17.669 |
| w32 | 14 | 0.004036 | -8.521 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 4 | 0.076102 | 7.159 |
| w8 | 9 | -0.01066 | -5.846 |
| w9 | 2 | -0.016009 | -11.702 |
| w10 | 23 | 0.072975 | 35.558 |
| w11 | 22 | -0.109633 | -1.933 |
| w12 | 11 | 0.057035 | -30.819 |
| w13 | 18 | 0.043004 | 40.008 |
| w14 | 22 | 0.049133 | 12.092 |
| w15 | 26 | -0.135053 | -33.106 |
| w16 | 32 | 0.107174 | 73.265 |
| w17 | 21 | 0.029182 | 35.165 |
| w18 | 15 | -0.101131 | -22.491 |
| w19 | 16 | 0.034567 | -19.169 |
| w20 | 8 | -0.037741 | -2.639 |
| w21 | 12 | -0.087437 | -18.859 |
| w22 | 32 | 0.004784 | -1.562 |
| w23 | 5 | 0.319037 | 83.94 |
| w24 | 19 | -0.133254 | -11.953 |
| w25 | 24 | 0.114156 | 25.463 |
| w26 | 15 | -0.131985 | -37.039 |
| w27 | 33 | -0.031801 | 4.469 |
| w28 | 7 | -0.157148 | -14.839 |
| w29 | 32 | -0.256754 | -14.69 |
| w30 | 30 | -0.122225 | -17.555 |
| w31 | 7 | -0.035396 | -6.582 |
| w32 | 12 | -0.109972 | -33.436 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.119598 | 137.077 |
| w2 | 24 | -0.104325 | -16.139 |
| w3 | 15 | -0.014857 | -9.573 |
| w4 | 31 | 0.072568 | 150.577 |
| w5 | 39 | 0.159257 | 84.388 |
| w6 | 23 | 0.070821 | 57.304 |
| w7 | 18 | 0.076174 | 22.598 |
| w8 | 7 | 0.02593 | -5.314 |
| w9 | 3 | -0.07485 | -5.712 |
| w10 | 29 | 0.000821 | 0.836 |
| w11 | 19 | 0.105605 | 47.701 |
| w12 | 16 | -0.032565 | -6.287 |
| w13 | 18 | 0.016494 | 38.826 |
| w14 | 30 | 0.086263 | 48.381 |
| w15 | 38 | -0.140396 | -25.687 |
| w16 | 39 | 0.020532 | 100.675 |
| w17 | 26 | 0.110519 | 32.761 |
| w18 | 20 | -0.165444 | -7.552 |
| w19 | 15 | -0.018152 | -3.2 |
| w20 | 14 | 0.053299 | 4.302 |
| w21 | 11 | 0.051521 | -4.71 |
| w22 | 42 | -0.006766 | 20.494 |
| w23 | 15 | -0.150504 | -26.987 |
| w24 | 27 | -0.061114 | 32.734 |
| w25 | 32 | 0.075552 | 42.35 |
| w26 | 7 | 0.104345 | 3.564 |
| w27 | 20 | -0.020738 | 8.961 |
| w28 | 2 | -0.047881 | -2.094 |
| w29 | 28 | 0.074603 | 63.739 |
| w30 | 9 | -0.001688 | -5.818 |
| w31 | 24 | -0.012037 | -18.333 |
| w32 | 25 | 0.062368 | 17.294 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 28 | 0.09884 | 57.456 |
| w11 | 14 | -0.110117 | -5.651 |
| w12 | 11 | -0.085384 | -29.234 |
| w13 | 29 | 0.07888 | 55.721 |
| w14 | 26 | 0.087321 | 66.274 |
| w15 | 28 | 0.032651 | 11.445 |
| w16 | 31 | 0.07132 | 88.979 |
| w17 | 25 | -0.001026 | 51.107 |
| w18 | 5 | -0.130372 | -22.654 |
| w19 | 12 | 0.113136 | -8.406 |
| w20 | 13 | -0.066164 | -16.133 |
| w21 | 0 | -0.020724 | 0.0 |
| w22 | 29 | -0.06079 | 1.394 |
| w23 | 5 | -0.116553 | -10.203 |
| w24 | 25 | 0.16537 | 165.919 |
| w25 | 15 | 0.091003 | -4.887 |
| w26 | 9 | -0.050963 | -8.194 |
| w27 | 28 | 0.232795 | 118.802 |
| w28 | 6 | -0.224885 | -18.805 |
| w29 | 22 | 0.015779 | 13.687 |
| w30 | 14 | -0.01239 | -11.541 |
| w31 | 8 | -0.168642 | -20.879 |
| w32 | 27 | -0.03593 | -15.09 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 34 | -0.09628 | 1.571 |
| w13 | 19 | -0.038022 | -20.047 |
| w14 | 28 | -0.011799 | 63.814 |
| w15 | 17 | -0.126061 | -9.666 |
| w16 | 27 | 0.002755 | 84.458 |
| w17 | 27 | -0.050333 | 16.704 |
| w18 | 15 | -0.133797 | 1.274 |
| w19 | 10 | -0.05835 | -16.472 |
| w20 | 18 | -0.088088 | -1.881 |
| w21 | 11 | 0.003052 | 8.363 |
| w22 | 22 | -0.003179 | -0.753 |
| w23 | 5 | -0.080811 | -7.493 |
| w24 | 27 | -0.068583 | 38.253 |
| w25 | 19 | 0.114883 | 9.385 |
| w26 | 3 | -0.06643 | -1.583 |
| w27 | 25 | 0.085365 | 25.794 |
| w28 | 8 | -0.156544 | -13.938 |
| w29 | 22 | -0.092842 | -18.185 |
| w30 | 3 | -0.077296 | -6.183 |
| w31 | 16 | 0.075204 | 1.674 |
| w32 | 20 | -0.13149 | -38.155 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 12 | -0.090323 | -11.188 |
| w16 | 33 | 0.040522 | 50.442 |
| w17 | 18 | -0.074717 | -1.311 |
| w18 | 21 | 0.06975 | 26.869 |
| w19 | 7 | 0.079693 | -4.908 |
| w20 | 12 | -0.010308 | -11.013 |
| w21 | 10 | 0.007746 | -14.724 |
| w22 | 22 | -0.097378 | -17.317 |
| w23 | 6 | -0.100336 | -12.747 |
| w24 | 22 | 0.026433 | 84.787 |
| w25 | 21 | 0.084796 | -3.267 |
| w26 | 12 | 0.01223 | -9.562 |
| w27 | 21 | 0.320958 | 198.908 |
| w28 | 11 | 0.04122 | 1.746 |
| w29 | 14 | 0.078019 | 12.006 |
| w30 | 2 | -0.164279 | -22.647 |
| w31 | 15 | 0.016817 | -10.554 |
| w32 | 18 | -0.053651 | -30.074 |

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
| w15 | 21 | -0.042262 | -2.281 |
| w16 | 32 | 0.015392 | 71.013 |
| w17 | 13 | 0.034517 | 13.783 |
| w18 | 20 | -0.205567 | -26.046 |
| w19 | 17 | -0.025212 | -2.508 |
| w20 | 14 | -0.110511 | -16.3 |
| w21 | 16 | -0.08704 | -6.519 |
| w22 | 24 | -0.011511 | 31.079 |
| w23 | 33 | -0.101898 | -16.583 |
| w24 | 43 | -0.188166 | 14.983 |
| w25 | 29 | 0.085493 | 30.356 |
| w26 | 36 | 0.08458 | 20.934 |
| w27 | 33 | 0.09793 | 87.376 |
| w28 | 22 | -0.126505 | -19.831 |
| w29 | 50 | -0.1155 | 18.899 |
| w30 | 13 | -0.004479 | -9.006 |
| w31 | 39 | -0.022754 | 24.463 |
| w32 | 37 | 0.014605 | 2.235 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 34 | 0.033589 | 32.965 |
| w17 | 20 | -0.001713 | -9.754 |
| w18 | 18 | -0.095166 | -15.855 |
| w19 | 15 | 0.005858 | -25.772 |
| w20 | 10 | -0.008666 | -10.951 |
| w21 | 8 | -0.084471 | -8.963 |
| w22 | 23 | -0.117084 | -13.122 |
| w23 | 11 | -0.130627 | -11.996 |
| w24 | 26 | 0.041801 | 49.048 |
| w25 | 26 | 0.131728 | 3.651 |
| w26 | 10 | 0.018549 | -9.657 |
| w27 | 22 | 0.18817 | 43.848 |
| w28 | 3 | -0.087971 | -6.483 |
| w29 | 15 | -0.008476 | -6.911 |
| w30 | 17 | -0.030919 | -25.832 |
| w31 | 10 | -0.039858 | -13.885 |
| w32 | 8 | 0.007349 | -0.478 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 13 | 0.033971 | 0.342 |
| w21 | 5 | 0.008965 | -1.938 |
| w22 | 26 | -0.026775 | -5.449 |
| w23 | 4 | 0.051577 | -3.892 |
| w24 | 31 | 0.232543 | 182.204 |
| w25 | 24 | 0.046773 | 8.504 |
| w26 | 10 | 0.025013 | -4.073 |
| w27 | 32 | 0.061815 | 39.419 |
| w28 | 13 | -0.068128 | -13.675 |
| w29 | 23 | -0.035281 | -2.98 |
| w30 | 11 | 0.092562 | 3.365 |
| w31 | 16 | -0.048421 | -14.438 |
| w32 | 14 | 0.085537 | 6.76 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 25 | 0.024986 | 6.971 |
| w23 | 3 | 0.055745 | -0.025 |
| w24 | 22 | 0.111712 | 122.296 |
| w25 | 20 | 0.016068 | 15.622 |
| w26 | 8 | -0.011963 | 2.257 |
| w27 | 21 | -0.061928 | 32.903 |
| w28 | 4 | -0.156183 | -15.361 |
| w29 | 18 | 0.005613 | -4.677 |
| w30 | 11 | -0.118885 | -16.609 |
| w31 | 28 | -0.067498 | -14.312 |
| w32 | 18 | -0.006215 | 12.426 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 23 | -0.019624 | 27.158 |
| w25 | 19 | -0.033929 | 7.834 |
| w26 | 6 | -0.020048 | -12.725 |
| w27 | 32 | 0.036252 | 87.446 |
| w28 | 9 | 0.124209 | 17.085 |
| w29 | 18 | 0.014719 | -2.253 |
| w30 | 9 | -0.02679 | -15.719 |
| w31 | 15 | 0.047969 | -5.508 |
| w32 | 12 | 0.010109 | -5.546 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 30 | 0.153992 | 80.104 |
| w6 | 20 | -0.026109 | 7.112 |
| w7 | 10 | -0.001688 | 17.327 |
| w8 | 11 | -0.075028 | -12.172 |
| w9 | 10 | -0.038092 | -20.601 |
| w10 | 22 | 0.052504 | 17.881 |
| w11 | 13 | 0.01887 | -0.851 |
| w12 | 4 | -0.056249 | -3.077 |
| w13 | 23 | 0.146152 | 76.528 |
| w14 | 32 | -0.000789 | 41.826 |
| w15 | 21 | -0.077178 | -9.37 |
| w16 | 29 | 0.119579 | 79.258 |
| w17 | 19 | -0.02983 | 10.895 |
| w18 | 21 | -0.083694 | -25.338 |
| w19 | 14 | -0.04345 | 6.67 |
| w20 | 10 | 0.021726 | -1.624 |
| w21 | 1 | -0.085986 | -5.022 |
| w22 | 18 | -0.238077 | -14.657 |
| w23 | 8 | -0.134647 | -18.463 |
| w24 | 31 | -0.092563 | -16.964 |
| w25 | 16 | 0.095602 | -4.173 |
| w26 | 15 | 0.117654 | 34.713 |
| w27 | 27 | -0.063763 | 19.661 |
| w28 | 13 | -0.065148 | -3.139 |
| w29 | 17 | -0.024042 | -2.52 |
| w30 | 32 | 0.165946 | 198.783 |
| w31 | 9 | 0.072046 | 8.692 |
| w32 | 25 | 0.057195 | 26.1 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 36 | 0.096611 | 98.393 |
| w6 | 24 | 0.136939 | 88.277 |
| w7 | 13 | -0.019959 | -8.94 |
| w8 | 4 | -0.10965 | -5.047 |
| w9 | 8 | -0.145126 | -15.729 |
| w10 | 25 | -0.027514 | 1.571 |
| w11 | 28 | -0.049024 | -5.38 |
| w12 | 5 | 0.026856 | 0.463 |
| w13 | 25 | -0.026369 | 7.843 |
| w14 | 32 | -0.05032 | 28.621 |
| w15 | 33 | -0.123473 | 1.296 |
| w16 | 33 | 0.016661 | 64.152 |
| w17 | 28 | -0.037985 | -12.692 |
| w18 | 16 | -0.280615 | -26.232 |
| w19 | 20 | -0.235877 | -37.01 |
| w20 | 14 | -0.03545 | -0.343 |
| w21 | 15 | -0.112961 | -21.334 |
| w22 | 26 | -0.072033 | -2.417 |
| w23 | 11 | 0.119389 | -2.148 |
| w24 | 41 | -0.023921 | 5.176 |
| w25 | 6 | -0.076915 | -32.527 |
| w26 | 26 | -0.01943 | 4.241 |
| w27 | 35 | -0.055178 | -31.833 |
| w28 | 34 | -0.082638 | 19.47 |
| w29 | 15 | 0.049357 | 8.473 |
| w30 | 35 | -0.149378 | 32.748 |
| w31 | 13 | 0.075213 | 18.215 |
| w32 | 35 | 0.015049 | 34.575 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 19 | -0.122926 | 2.359 |
| w18 | 29 | -0.083115 | 13.695 |
| w19 | 20 | -0.056508 | -30.359 |
| w20 | 11 | -0.102868 | -11.596 |
| w21 | 6 | -0.227496 | -29.517 |
| w22 | 23 | 0.161126 | 30.056 |
| w23 | 5 | -0.152526 | -8.163 |
| w24 | 24 | -0.023509 | 10.296 |
| w25 | 20 | 0.162098 | 15.123 |
| w26 | 16 | -0.018566 | -10.119 |
| w27 | 27 | 0.248556 | 132.893 |
| w28 | 11 | -0.082571 | -8.508 |
| w29 | 14 | 0.046438 | 12.397 |
| w30 | 5 | -0.127275 | -35.967 |
| w31 | 16 | -0.078609 | -13.878 |
| w32 | 21 | -0.026027 | -3.405 |

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
| w17 | 21 | -0.108337 | -15.021 |
| w18 | 11 | -0.213261 | -28.525 |
| w19 | 14 | 0.064632 | -0.781 |
| w20 | 12 | 0.026771 | 0.31 |
| w21 | 7 | -0.058775 | -29.868 |
| w22 | 20 | 0.098306 | 19.261 |
| w23 | 7 | -0.100517 | -5.323 |
| w24 | 31 | -0.080501 | 22.625 |
| w25 | 19 | 0.005154 | -16.679 |
| w26 | 22 | 0.053677 | 19.477 |
| w27 | 32 | -0.030933 | 23.073 |
| w28 | 6 | -0.018907 | -8.504 |
| w29 | 30 | -0.096366 | -4.132 |
| w30 | 5 | -0.097824 | -2.724 |
| w31 | 4 | -0.064478 | -10.876 |
| w32 | 14 | -0.010467 | 1.516 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 9 | -0.142938 | -16.943 |
| w20 | 13 | 0.04991 | 2.186 |
| w21 | 17 | -0.058065 | -2.982 |
| w22 | 33 | 0.028931 | 113.925 |
| w23 | 14 | 0.031156 | -14.001 |
| w24 | 38 | 0.21243 | 273.362 |
| w25 | 15 | -0.123782 | -28.398 |
| w26 | 7 | -0.030262 | -15.23 |
| w27 | 22 | -0.003986 | 17.62 |
| w28 | 3 | -0.10983 | -8.491 |
| w29 | 26 | -0.021384 | -8.86 |
| w30 | 7 | -0.081438 | -20.687 |
| w31 | 16 | -0.12462 | 0.648 |
| w32 | 22 | -0.032177 | 2.838 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 22 | 0.01513 | 19.674 |
| w23 | 9 | -0.111211 | -24.321 |
| w24 | 27 | -0.204557 | 14.043 |
| w25 | 26 | -0.002577 | -20.841 |
| w26 | 11 | 0.056076 | 9.132 |
| w27 | 23 | -0.082467 | -4.217 |
| w28 | 10 | -0.166088 | -19.733 |
| w29 | 15 | 0.118506 | 34.968 |
| w30 | 6 | -0.142564 | -25.388 |
| w31 | 14 | -0.069775 | -3.325 |
| w32 | 20 | 0.072636 | 1.873 |

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
| w27 | 27 | 0.054642 | 20.448 |
| w28 | 13 | -0.067804 | -7.303 |
| w29 | 18 | 0.001835 | -5.602 |
| w30 | 5 | 0.009497 | -6.208 |
| w31 | 11 | -0.097689 | -13.777 |
| w32 | 19 | 0.071991 | 18.828 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.076437 | 13.322 |
| w18 | 7 | -0.027764 | -6.994 |
| w19 | 10 | 0.118443 | 4.647 |
| w20 | 12 | 0.159155 | 11.978 |
| w21 | 4 | -0.055069 | -20.823 |
| w22 | 17 | -0.047554 | 7.512 |
| w23 | 4 | -0.173952 | -7.005 |
| w24 | 29 | -0.000504 | 78.797 |
| w25 | 21 | 0.06699 | -8.329 |
| w26 | 12 | -0.036096 | -18.425 |
| w27 | 23 | 0.09157 | 37.63 |
| w28 | 4 | -0.121134 | -4.337 |
| w29 | 21 | -0.052966 | -14.342 |
| w30 | 12 | -0.189243 | -34.618 |
| w31 | 12 | -0.144153 | -8.327 |
| w32 | 11 | -0.061465 | -21.526 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 17 | 0.002856 | 14.27 |
| w18 | 20 | -0.094136 | -21.025 |
| w19 | 6 | -0.026251 | -8.498 |
| w20 | 10 | -0.012608 | -13.562 |
| w21 | 3 | -0.080675 | -10.779 |
| w22 | 29 | 0.090528 | 55.918 |
| w23 | 6 | -0.226257 | -28.805 |
| w24 | 23 | -0.013891 | 49.077 |
| w25 | 19 | 0.087486 | 56.289 |
| w26 | 8 | 0.039785 | -0.487 |
| w27 | 28 | 0.000857 | 39.915 |
| w28 | 2 | -0.080228 | -8.952 |
| w29 | 16 | -0.008009 | -5.974 |
| w30 | 5 | -0.130461 | -19.634 |
| w31 | 7 | -0.183229 | -8.562 |
| w32 | 10 | 0.014097 | -12.932 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 13 | 0.036343 | -17.377 |
| w29 | 18 | 0.037466 | -8.153 |
| w30 | 13 | -0.01474 | 13.261 |
| w31 | 14 | 0.038437 | 0.937 |
| w32 | 13 | 0.027843 | 5.792 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 20 | 0.09228 | 23.976 |
| w15 | 23 | 0.120165 | 70.953 |
| w16 | 22 | 0.057266 | 339.841 |
| w17 | 15 | 0.079836 | 9.583 |
| w18 | 12 | -0.173107 | -7.641 |
| w19 | 17 | -0.194495 | -33.991 |
| w20 | 12 | -0.07307 | -13.911 |
| w21 | 11 | 0.273757 | 108.784 |
| w22 | 23 | -0.185608 | -14.947 |
| w23 | 12 | -0.054186 | -2.606 |
| w24 | 20 | 0.063065 | 35.911 |
| w25 | 23 | 0.206366 | 97.348 |
| w26 | 7 | 0.015218 | -1.579 |
| w27 | 31 | 0.091324 | 110.659 |
| w28 | 3 | -0.125245 | -14.579 |
| w29 | 18 | 0.024939 | 9.794 |
| w30 | 10 | 0.06229 | -3.456 |
| w31 | 14 | 0.005321 | -2.89 |
| w32 | 11 | 0.125648 | 15.04 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 11 | 0.358672 | 214.171 |
| w26 | 14 | 0.033307 | 19.093 |
| w27 | 21 | 0.06748 | 52.854 |
| w28 | 12 | -0.001074 | -15.197 |
| w29 | 15 | 0.016028 | -2.04 |
| w30 | 4 | -0.130126 | -21.381 |
| w31 | 9 | 0.069695 | 18.994 |
| w32 | 22 | 0.063495 | 6.304 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

