# Backtest of 001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d

- Plan: `../../../../../03_test_plan/validation_run/plans/001-01_rsi-high-extreme-reversal.a1_rsi-high-reversal-wider-sample.c1_high-rsi-trend-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.037399 | 0.599 |
| w2 | 25 | 0.165238 | 85.499 |
| w3 | 53 | -0.006474 | 90.059 |
| w4 | 33 | -0.010878 | 6.486 |
| w5 | 41 | 0.040576 | 97.735 |
| w6 | 45 | 0.094003 | 104.997 |
| w7 | 26 | -0.026956 | -5.006 |
| w8 | 19 | 0.07318 | 4.757 |
| w9 | 13 | -0.083052 | -11.531 |
| w10 | 34 | 0.068081 | 40.112 |
| w11 | 46 | 0.102783 | 51.228 |
| w12 | 16 | -0.017309 | -3.427 |
| w13 | 38 | 0.009452 | 14.622 |
| w14 | 34 | -0.01326 | 19.36 |
| w15 | 33 | 0.097462 | 141.339 |
| w16 | 45 | -0.007828 | 23.984 |
| w17 | 28 | 0.087696 | 13.153 |
| w18 | 33 | 0.056897 | 7.478 |
| w19 | 24 | -0.021691 | -6.495 |
| w20 | 17 | 0.010247 | -4.213 |
| w21 | 20 | -0.127602 | -17.434 |
| w22 | 37 | 0.023296 | 64.559 |
| w23 | 21 | 0.060937 | 5.895 |
| w24 | 35 | 0.020194 | 50.141 |
| w25 | 31 | 0.121934 | 56.536 |
| w26 | 28 | -0.071968 | -8.986 |
| w27 | 42 | 0.011244 | 55.214 |
| w28 | 19 | -0.008278 | -2.112 |
| w29 | 45 | 0.031847 | 12.082 |
| w30 | 17 | 2.3e-05 | -7.756 |
| w31 | 36 | -0.012984 | -8.528 |
| w32 | 26 | 0.157556 | 28.628 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | -0.102864 | -16.885 |
| w2 | 24 | 0.099967 | 26.953 |
| w3 | 31 | -0.160598 | -29.036 |
| w4 | 36 | 0.101528 | 69.616 |
| w5 | 62 | -0.000404 | 40.008 |
| w6 | 28 | 0.130875 | 111.035 |
| w7 | 27 | -0.089283 | -10.225 |
| w8 | 11 | 0.01369 | -2.681 |
| w9 | 18 | -0.165524 | -13.306 |
| w10 | 40 | -0.060183 | 19.887 |
| w11 | 33 | 0.04177 | 4.088 |
| w12 | 17 | -0.018559 | -4.323 |
| w13 | 37 | 0.018697 | 17.859 |
| w14 | 43 | -0.089556 | -1.281 |
| w15 | 44 | -0.01214 | 23.747 |
| w16 | 53 | -0.040711 | 11.821 |
| w17 | 27 | 0.056809 | 6.2 |
| w18 | 35 | 0.010213 | -2.057 |
| w19 | 21 | -0.013319 | -7.318 |
| w20 | 23 | -0.032212 | -8.805 |
| w21 | 38 | -0.073355 | -10.648 |
| w22 | 49 | -0.065049 | -4.073 |
| w23 | 31 | -0.129921 | -21.676 |
| w24 | 34 | -0.11055 | -12.524 |
| w25 | 34 | 0.002647 | 8.505 |
| w26 | 18 | -0.168175 | -10.762 |
| w27 | 49 | -0.019315 | 19.512 |
| w28 | 34 | -0.143394 | -17.401 |
| w29 | 45 | 0.011227 | 15.082 |
| w30 | 19 | -0.185847 | -27.074 |
| w31 | 22 | -0.04874 | -9.701 |
| w32 | 23 | 0.044715 | 1.22 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 37 | 0.199212 | 155.717 |
| w7 | 17 | 0.072318 | 6.056 |
| w8 | 8 | -0.019294 | -2.389 |
| w9 | 26 | 0.029082 | 3.106 |
| w10 | 18 | -0.137249 | -17.934 |
| w11 | 31 | 0.001957 | 1.883 |
| w12 | 27 | -0.084775 | -11.503 |
| w13 | 34 | 0.006281 | 7.859 |
| w14 | 37 | 0.05816 | 33.085 |
| w15 | 31 | 0.207637 | 141.211 |
| w16 | 39 | 0.028066 | 65.039 |
| w17 | 30 | 0.038581 | 14.957 |
| w18 | 31 | -0.111504 | -15.852 |
| w19 | 26 | -0.075328 | -12.557 |
| w20 | 16 | -0.019328 | -4.785 |
| w21 | 26 | -0.025393 | -2.489 |
| w22 | 33 | -0.088834 | -5.388 |
| w23 | 18 | -0.070507 | -6.414 |
| w24 | 30 | 0.012111 | 17.005 |
| w25 | 27 | -0.054463 | -8.312 |
| w26 | 25 | 0.026573 | 10.085 |
| w27 | 26 | 0.347312 | 298.236 |
| w28 | 27 | -0.120245 | -11.717 |
| w29 | 32 | 0.10043 | 36.874 |
| w30 | 15 | -0.060881 | -6.739 |
| w31 | 25 | -0.018858 | -6.94 |
| w32 | 15 | 0.112788 | 15.698 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 19 | 0.103836 | 17.71 |
| w8 | 15 | 0.021723 | -3.551 |
| w9 | 18 | 0.027386 | -2.895 |
| w10 | 22 | 0.092188 | 40.789 |
| w11 | 24 | -0.04375 | -7.375 |
| w12 | 24 | 0.019277 | -2.823 |
| w13 | 29 | 0.040202 | 34.123 |
| w14 | 42 | -0.123003 | -11.499 |
| w15 | 42 | -0.105541 | -17.555 |
| w16 | 46 | 0.054936 | 47.493 |
| w17 | 32 | 0.018525 | 4.941 |
| w18 | 28 | -0.071451 | -14.584 |
| w19 | 18 | 0.017308 | -5.301 |
| w20 | 17 | -0.029374 | -5.575 |
| w21 | 32 | -0.187709 | -20.174 |
| w22 | 36 | 0.011747 | 13.114 |
| w23 | 17 | 0.223466 | 67.764 |
| w24 | 35 | -0.154476 | -19.985 |
| w25 | 40 | 0.107047 | 69.143 |
| w26 | 18 | -0.091253 | -10.729 |
| w27 | 45 | -0.022951 | 2.375 |
| w28 | 16 | -0.072488 | -9.574 |
| w29 | 74 | -0.212649 | -13.122 |
| w30 | 51 | -0.21867 | -25.25 |
| w31 | 16 | -0.049364 | -8.699 |
| w32 | 14 | 0.030193 | 2.686 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.178307 | 202.218 |
| w2 | 29 | -0.007655 | 3.514 |
| w3 | 28 | 0.046729 | -2.695 |
| w4 | 48 | 0.008049 | 183.902 |
| w5 | 36 | 0.147593 | 118.149 |
| w6 | 36 | -0.010484 | 34.983 |
| w7 | 28 | 0.103232 | 22.622 |
| w8 | 14 | 0.029846 | -2.413 |
| w9 | 13 | -0.054661 | -4.641 |
| w10 | 31 | -0.01979 | 1.285 |
| w11 | 31 | 0.117952 | 31.436 |
| w12 | 21 | -0.038348 | -6.661 |
| w13 | 41 | 0.033394 | 42.802 |
| w14 | 51 | -0.023864 | 53.463 |
| w15 | 46 | -0.032792 | 16.173 |
| w16 | 52 | -0.049034 | 57.312 |
| w17 | 28 | 0.112938 | 53.903 |
| w18 | 42 | -0.05668 | -10.787 |
| w19 | 17 | 0.037887 | -0.592 |
| w20 | 17 | 0.03054 | -0.521 |
| w21 | 14 | -0.028415 | -6.652 |
| w22 | 45 | -0.044756 | 20.349 |
| w23 | 28 | -0.194937 | -22.364 |
| w24 | 35 | -0.016511 | 25.224 |
| w25 | 23 | 0.144114 | 62.95 |
| w26 | 15 | -0.00281 | -3.916 |
| w27 | 40 | -0.018878 | 12.101 |
| w28 | 5 | -0.055661 | -3.341 |
| w29 | 41 | -0.014285 | 57.149 |
| w30 | 16 | -0.082302 | -7.567 |
| w31 | 33 | -0.064304 | -15.251 |
| w32 | 30 | 0.095205 | 20.92 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 28 | 0.08633 | 54.088 |
| w11 | 30 | -0.109957 | -13.646 |
| w12 | 24 | -0.06314 | -7.612 |
| w13 | 36 | 0.065201 | 38.78 |
| w14 | 48 | -0.014666 | 39.146 |
| w15 | 44 | -0.025949 | 5.398 |
| w16 | 48 | 0.095433 | 96.111 |
| w17 | 24 | 0.06553 | 57.814 |
| w18 | 9 | -0.126305 | -11.814 |
| w19 | 13 | 0.050317 | 3.718 |
| w20 | 25 | -0.056122 | -12.168 |
| w21 | 12 | -0.158366 | -12.218 |
| w22 | 43 | -0.042738 | 11.403 |
| w23 | 13 | -0.240432 | -12.693 |
| w24 | 31 | 0.13714 | 142.679 |
| w25 | 23 | 0.107398 | 13.355 |
| w26 | 18 | -0.07056 | -8.216 |
| w27 | 30 | 0.234349 | 148.798 |
| w28 | 17 | -0.164402 | -13.759 |
| w29 | 32 | 0.012803 | 9.799 |
| w30 | 12 | -0.039771 | -7.27 |
| w31 | 11 | -0.169088 | -8.149 |
| w32 | 25 | 0.02952 | 0.005 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 51 | -0.140208 | -9.909 |
| w13 | 32 | -0.046736 | -14.005 |
| w14 | 45 | -0.025061 | 43.966 |
| w15 | 35 | -0.091328 | -11.377 |
| w16 | 53 | -0.023511 | 31.519 |
| w17 | 32 | 0.032969 | 16.705 |
| w18 | 45 | -0.162241 | -18.857 |
| w19 | 31 | -0.068305 | -13.902 |
| w20 | 36 | -0.053223 | -11.144 |
| w21 | 21 | -0.04826 | -11.407 |
| w22 | 40 | -0.005331 | 1.763 |
| w23 | 9 | -0.121431 | -6.597 |
| w24 | 38 | -0.049044 | 16.256 |
| w25 | 20 | 0.10744 | 15.365 |
| w26 | 7 | -0.183734 | -3.514 |
| w27 | 28 | 0.12594 | 47.7 |
| w28 | 16 | -0.09745 | -6.948 |
| w29 | 34 | -0.081807 | -18.104 |
| w30 | 7 | -0.015425 | -4.173 |
| w31 | 38 | -0.008872 | -5.742 |
| w32 | 34 | -0.084011 | -19.055 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 25 | -0.113834 | -18.261 |
| w16 | 54 | 0.017425 | 54.938 |
| w17 | 32 | -0.087825 | -15.974 |
| w18 | 38 | -0.028831 | 5.694 |
| w19 | 12 | 0.004037 | -6.46 |
| w20 | 19 | -0.072035 | -10.568 |
| w21 | 13 | 0.025417 | -7.768 |
| w22 | 36 | -0.0816 | -9.4 |
| w23 | 4 | -0.098578 | -3.476 |
| w24 | 41 | 0.052844 | 70.799 |
| w25 | 31 | 0.109933 | 17.826 |
| w26 | 15 | -0.035054 | -6.189 |
| w27 | 28 | 0.233177 | 140.977 |
| w28 | 16 | -0.035366 | -5.107 |
| w29 | 31 | 0.056864 | 16.113 |
| w30 | 6 | -0.16912 | -5.656 |
| w31 | 31 | 0.010845 | -1.888 |
| w32 | 26 | -0.039212 | -9.999 |

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
| w15 | 30 | -0.077399 | -15.808 |
| w16 | 54 | -0.016683 | 60.131 |
| w17 | 23 | 0.062803 | 14.11 |
| w18 | 34 | -0.111225 | -20.357 |
| w19 | 15 | -0.008888 | -4.868 |
| w20 | 46 | -0.119799 | -15.129 |
| w21 | 28 | -0.166386 | -18.383 |
| w22 | 50 | -0.080328 | -1.531 |
| w23 | 36 | -0.056139 | -1.808 |
| w24 | 46 | -0.08211 | 25.948 |
| w25 | 26 | 0.113428 | 33.044 |
| w26 | 44 | 0.062558 | 40.22 |
| w27 | 51 | 0.092303 | 186.78 |
| w28 | 42 | -0.242398 | -27.029 |
| w29 | 65 | -0.029961 | 39.269 |
| w30 | 15 | -0.133407 | -7.463 |
| w31 | 50 | -0.004088 | 17.212 |
| w32 | 37 | 0.079238 | 9.502 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 45 | 0.040877 | 44.238 |
| w17 | 30 | 0.01651 | 7.21 |
| w18 | 32 | -0.049628 | -10.613 |
| w19 | 20 | 0.021175 | -4.086 |
| w20 | 19 | 0.01955 | -2.524 |
| w21 | 11 | -0.119249 | -14.962 |
| w22 | 39 | -0.04865 | 5.183 |
| w23 | 20 | -0.121125 | -12.528 |
| w24 | 44 | 0.029344 | 32.11 |
| w25 | 20 | 0.133016 | 23.35 |
| w26 | 18 | -0.13908 | -11.395 |
| w27 | 30 | 0.153233 | 59.239 |
| w28 | 13 | -0.079038 | -5.979 |
| w29 | 26 | -0.017675 | -7.048 |
| w30 | 20 | -0.015372 | -10.107 |
| w31 | 18 | -0.125666 | -9.329 |
| w32 | 19 | -0.033888 | -7.192 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 19 | 0.043123 | -0.039 |
| w21 | 9 | -0.044871 | -6.844 |
| w22 | 40 | 0.026061 | 24.899 |
| w23 | 13 | -0.058547 | -5.507 |
| w24 | 36 | 0.214647 | 146.703 |
| w25 | 33 | 0.04786 | 5.003 |
| w26 | 20 | -0.075947 | -9.061 |
| w27 | 42 | 0.048837 | 35.01 |
| w28 | 15 | -0.042447 | -5.867 |
| w29 | 40 | -0.028555 | -3.06 |
| w30 | 13 | 0.078909 | 5.849 |
| w31 | 24 | -0.105785 | -12.032 |
| w32 | 13 | 0.057145 | 4.794 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 32 | -0.036765 | 5.973 |
| w23 | 12 | -0.109597 | -6.911 |
| w24 | 34 | 0.081961 | 101.401 |
| w25 | 38 | 0.099837 | 43.626 |
| w26 | 37 | -0.057426 | -9.516 |
| w27 | 35 | 0.041239 | 16.955 |
| w28 | 13 | -0.076718 | -5.751 |
| w29 | 32 | 0.003798 | -1.349 |
| w30 | 24 | -0.033589 | -8.229 |
| w31 | 42 | -0.079551 | -10.544 |
| w32 | 34 | 0.058185 | 38.702 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 46 | -0.057545 | 4.186 |
| w25 | 45 | -0.022051 | 1.931 |
| w26 | 23 | -0.081988 | -6.635 |
| w27 | 47 | -0.044844 | 57.673 |
| w28 | 14 | 0.09648 | 10.806 |
| w29 | 33 | -0.006036 | -0.872 |
| w30 | 15 | -0.038819 | -9.526 |
| w31 | 24 | -0.00992 | -7.033 |
| w32 | 20 | 0.072584 | 18.778 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 38 | 0.14534 | 94.18 |
| w6 | 42 | -0.02786 | 7.096 |
| w7 | 26 | -0.014553 | -0.822 |
| w8 | 18 | -0.058024 | -8.88 |
| w9 | 18 | -0.038871 | -10.436 |
| w10 | 32 | 0.031259 | 9.0 |
| w11 | 39 | 0.044524 | 3.522 |
| w12 | 9 | -0.149994 | -9.143 |
| w13 | 34 | 0.119336 | 61.48 |
| w14 | 55 | -0.085214 | 10.98 |
| w15 | 33 | -0.120672 | -18.891 |
| w16 | 45 | 0.039081 | 59.684 |
| w17 | 30 | 0.037094 | 4.217 |
| w18 | 29 | -0.040244 | -8.295 |
| w19 | 27 | -0.003886 | -3.275 |
| w20 | 16 | 0.040296 | 0.143 |
| w21 | 12 | -0.101346 | -8.149 |
| w22 | 39 | -0.144344 | -21.143 |
| w23 | 17 | -0.108015 | -8.219 |
| w24 | 54 | -0.131975 | -17.305 |
| w25 | 22 | 0.083963 | 9.618 |
| w26 | 39 | 0.065234 | 25.758 |
| w27 | 38 | -0.077545 | 2.957 |
| w28 | 20 | -0.096312 | -9.832 |
| w29 | 41 | -0.007229 | 0.916 |
| w30 | 46 | 0.127569 | 162.584 |
| w31 | 25 | -0.005625 | -3.523 |
| w32 | 41 | 0.079806 | 61.466 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 52 | 0.10896 | 150.877 |
| w6 | 23 | 0.131906 | 100.349 |
| w7 | 31 | -0.041968 | -6.476 |
| w8 | 15 | -0.083402 | -5.338 |
| w9 | 18 | -0.048561 | -12.088 |
| w10 | 45 | -0.039586 | 9.312 |
| w11 | 50 | -0.009225 | 0.828 |
| w12 | 14 | -0.074849 | -8.404 |
| w13 | 38 | 0.032153 | 31.688 |
| w14 | 50 | -0.120977 | 11.515 |
| w15 | 59 | -0.110776 | -3.313 |
| w16 | 42 | 0.014885 | 47.547 |
| w17 | 33 | 0.005506 | -1.568 |
| w18 | 34 | -0.184096 | -22.378 |
| w19 | 57 | -0.115993 | -19.933 |
| w20 | 29 | -0.010822 | -4.474 |
| w21 | 36 | -0.151557 | -24.385 |
| w22 | 39 | -0.035294 | -5.288 |
| w23 | 19 | 0.108647 | 11.504 |
| w24 | 53 | -0.124097 | -12.457 |
| w25 | 26 | -0.165487 | -31.942 |
| w26 | 35 | -0.022172 | 10.938 |
| w27 | 46 | -0.054226 | -10.0 |
| w28 | 49 | -0.024322 | 16.149 |
| w29 | 16 | 0.167445 | 46.649 |
| w30 | 64 | -0.178572 | -8.625 |
| w31 | 29 | 0.062698 | 14.271 |
| w32 | 37 | 0.042341 | 44.378 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 37 | -0.145911 | -23.057 |
| w18 | 53 | -0.138158 | -12.366 |
| w19 | 16 | -0.065069 | -13.731 |
| w20 | 27 | -0.071244 | -8.447 |
| w21 | 15 | -0.199954 | -20.033 |
| w22 | 28 | 0.075453 | 30.34 |
| w23 | 13 | -0.014262 | -5.069 |
| w24 | 40 | -0.143129 | -12.169 |
| w25 | 19 | 0.133105 | 20.775 |
| w26 | 19 | -0.039982 | -3.785 |
| w27 | 35 | 0.210002 | 127.56 |
| w28 | 29 | -0.026287 | -3.74 |
| w29 | 36 | 0.093478 | 25.598 |
| w30 | 7 | -0.063584 | -3.707 |
| w31 | 24 | -0.036196 | -8.9 |
| w32 | 41 | 0.025663 | 15.819 |

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
| w17 | 39 | -0.069325 | -15.126 |
| w18 | 30 | -0.127757 | -18.049 |
| w19 | 16 | 0.07046 | 9.366 |
| w20 | 28 | -0.039796 | -6.754 |
| w21 | 19 | -0.080578 | -12.748 |
| w22 | 33 | 0.017891 | 16.764 |
| w23 | 28 | -0.105764 | -14.381 |
| w24 | 55 | -0.087563 | 16.232 |
| w25 | 29 | -0.001413 | -3.344 |
| w26 | 38 | -0.040699 | 2.549 |
| w27 | 48 | -0.028181 | 25.321 |
| w28 | 15 | -0.061324 | -5.176 |
| w29 | 53 | -0.119368 | -2.293 |
| w30 | 13 | -0.197922 | -10.157 |
| w31 | 12 | -0.138549 | -12.758 |
| w32 | 37 | 0.054735 | 16.34 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 24 | -0.101042 | -13.901 |
| w20 | 20 | 0.009463 | -4.6 |
| w21 | 30 | -0.068244 | -15.667 |
| w22 | 52 | 0.022251 | 115.687 |
| w23 | 30 | 0.007047 | -0.067 |
| w24 | 47 | 0.116761 | 198.202 |
| w25 | 35 | -0.0521 | -10.611 |
| w26 | 24 | -0.06348 | -12.174 |
| w27 | 42 | -0.001007 | 3.822 |
| w28 | 9 | -0.040395 | -4.363 |
| w29 | 40 | -0.061995 | -6.088 |
| w30 | 8 | -0.049884 | -6.95 |
| w31 | 25 | -0.040568 | -8.852 |
| w32 | 37 | 0.037998 | 28.217 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 40 | 0.055883 | 21.879 |
| w23 | 26 | -0.142586 | -17.76 |
| w24 | 42 | -0.120459 | -2.226 |
| w25 | 45 | -0.065864 | -16.232 |
| w26 | 23 | -0.058115 | -10.325 |
| w27 | 38 | -0.04598 | -0.613 |
| w28 | 20 | -0.160239 | -11.932 |
| w29 | 32 | 0.02811 | 16.879 |
| w30 | 8 | -0.119277 | -6.023 |
| w31 | 26 | -0.068673 | -13.997 |
| w32 | 27 | 0.063052 | 11.683 |

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
| w27 | 45 | 0.07682 | 44.184 |
| w28 | 16 | -0.080413 | -5.934 |
| w29 | 28 | 0.011494 | 3.133 |
| w30 | 10 | 0.017888 | -3.489 |
| w31 | 15 | -0.126793 | -11.094 |
| w32 | 33 | -0.002285 | 30.051 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | 0.06669 | 5.701 |
| w18 | 9 | -0.027347 | -5.841 |
| w19 | 11 | 0.0211 | -1.899 |
| w20 | 12 | 0.093462 | 5.73 |
| w21 | 9 | -0.121428 | -14.188 |
| w22 | 37 | -0.063131 | 8.678 |
| w23 | 17 | -0.153302 | -13.843 |
| w24 | 43 | -0.022567 | 33.43 |
| w25 | 26 | 0.125851 | 23.407 |
| w26 | 16 | -0.10399 | -8.578 |
| w27 | 36 | 0.062057 | 21.166 |
| w28 | 10 | -0.078165 | -3.72 |
| w29 | 27 | -0.049978 | -13.562 |
| w30 | 17 | -0.022331 | -3.669 |
| w31 | 29 | -0.106961 | -15.625 |
| w32 | 17 | 0.057411 | 4.259 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | 0.064798 | 8.16 |
| w18 | 22 | -0.003943 | -6.817 |
| w19 | 17 | -0.039272 | -8.44 |
| w20 | 20 | 0.031516 | 0.254 |
| w21 | 10 | -0.188846 | -15.798 |
| w22 | 38 | 0.090804 | 94.32 |
| w23 | 21 | -0.097012 | -9.59 |
| w24 | 42 | 0.009786 | 44.272 |
| w25 | 28 | 0.148292 | 58.122 |
| w26 | 22 | -0.057431 | -7.857 |
| w27 | 38 | 0.04696 | 17.266 |
| w28 | 7 | 0.006876 | -0.848 |
| w29 | 31 | -0.014733 | -5.533 |
| w30 | 9 | -0.049809 | -8.257 |
| w31 | 15 | -0.152759 | -9.654 |
| w32 | 19 | 0.000112 | -8.052 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 15 | 0.063039 | 5.513 |
| w29 | 36 | 0.019932 | -0.9 |
| w30 | 23 | -0.076873 | -16.398 |
| w31 | 25 | 0.121498 | 21.99 |
| w32 | 31 | 0.041465 | 7.235 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 49 | 0.002662 | 40.2 |
| w15 | 31 | 0.078813 | 44.564 |
| w16 | 51 | -0.029574 | 263.776 |
| w17 | 22 | 0.05492 | 5.643 |
| w18 | 23 | -0.163688 | -18.348 |
| w19 | 21 | -0.114595 | -15.943 |
| w20 | 13 | 0.040713 | -1.065 |
| w21 | 22 | 0.16935 | 73.996 |
| w22 | 42 | -0.136409 | -14.088 |
| w23 | 26 | -0.037055 | -8.396 |
| w24 | 41 | 0.019189 | 24.409 |
| w25 | 35 | 0.167987 | 87.816 |
| w26 | 32 | -0.107133 | -9.502 |
| w27 | 36 | 0.201972 | 153.022 |
| w28 | 10 | -0.071557 | -5.956 |
| w29 | 32 | 0.054128 | 16.349 |
| w30 | 14 | 0.029938 | -3.381 |
| w31 | 20 | 0.003328 | 0.487 |
| w32 | 17 | 0.099444 | 13.463 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 29 | 0.307542 | 202.415 |
| w26 | 31 | 0.082323 | 15.057 |
| w27 | 50 | 0.070431 | 51.799 |
| w28 | 12 | 0.028946 | -0.379 |
| w29 | 27 | 0.004723 | 2.401 |
| w30 | 11 | -0.037083 | -6.105 |
| w31 | 28 | -0.014339 | -4.755 |
| w32 | 29 | 0.083783 | 13.238 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

