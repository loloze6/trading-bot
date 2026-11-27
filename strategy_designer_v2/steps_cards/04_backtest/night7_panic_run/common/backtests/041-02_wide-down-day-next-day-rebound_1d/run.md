# Backtest of 041-02_wide-down-day-next-day-rebound_1d

- Plan: `../../../../../03_test_plan/night7_panic_run/plans/041-02_wide-down-day-next-day-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 51 | 0.062071 | 6.557 |
| w2 | 47 | -0.020767 | 1.762 |
| w3 | 41 | -0.065954 | 15.077 |
| w4 | 34 | -0.085113 | -18.142 |
| w5 | 42 | 0.122784 | 48.555 |
| w6 | 42 | -0.151124 | -4.839 |
| w7 | 51 | 0.03451 | 0.809 |
| w8 | 57 | 0.043871 | -0.922 |
| w9 | 56 | 0.052768 | -24.993 |
| w10 | 45 | 0.088152 | 15.073 |
| w11 | 48 | -0.013032 | 11.719 |
| w12 | 60 | 0.033381 | -9.224 |
| w13 | 52 | 0.140843 | 23.137 |
| w14 | 51 | 0.153225 | 36.652 |
| w15 | 43 | -0.065996 | 8.253 |
| w16 | 50 | -0.011225 | 11.798 |
| w17 | 54 | 0.217199 | 28.62 |
| w18 | 53 | -0.011868 | -6.119 |
| w19 | 54 | -0.051712 | -16.338 |
| w20 | 56 | 0.083613 | -13.262 |
| w21 | 55 | -0.003326 | -16.32 |
| w22 | 52 | -0.040247 | 11.679 |
| w23 | 58 | 0.025195 | -9.298 |
| w24 | 52 | 0.103853 | 29.662 |
| w25 | 46 | 0.052142 | 13.254 |
| w26 | 56 | 0.065095 | 2.005 |
| w27 | 49 | 0.035609 | 22.8 |
| w28 | 48 | 0.072892 | 4.885 |
| w29 | 54 | 0.010169 | 0.882 |
| w30 | 54 | -0.042718 | -20.691 |
| w31 | 50 | -0.024114 | -25.841 |
| w32 | 50 | -0.172578 | -26.849 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | 0.295401 | 62.856 |
| w2 | 47 | -0.131986 | -19.37 |
| w3 | 55 | 0.040466 | 13.249 |
| w4 | 41 | -0.101977 | -9.942 |
| w5 | 53 | 0.036941 | 31.049 |
| w6 | 47 | 0.13575 | 47.257 |
| w7 | 56 | 0.087363 | 8.895 |
| w8 | 58 | 0.122354 | -8.608 |
| w9 | 54 | 0.161627 | 1.747 |
| w10 | 49 | 0.037081 | 15.867 |
| w11 | 56 | -0.018513 | -8.312 |
| w12 | 53 | 0.046284 | -13.744 |
| w13 | 55 | 0.082662 | 12.458 |
| w14 | 56 | 0.219133 | 56.312 |
| w15 | 47 | 0.05087 | 18.688 |
| w16 | 45 | -0.173185 | -11.637 |
| w17 | 51 | 0.277729 | 52.245 |
| w18 | 51 | -0.011052 | -7.386 |
| w19 | 54 | 0.059982 | -7.991 |
| w20 | 53 | 0.137983 | 2.411 |
| w21 | 48 | -0.018792 | -6.718 |
| w22 | 49 | 0.050187 | 9.104 |
| w23 | 52 | -0.061558 | -14.67 |
| w24 | 50 | 0.053798 | 5.434 |
| w25 | 44 | 0.033355 | 4.654 |
| w26 | 52 | 0.015568 | -17.144 |
| w27 | 50 | 0.014574 | 15.072 |
| w28 | 53 | -0.058449 | -11.767 |
| w29 | 52 | 0.188323 | 32.719 |
| w30 | 47 | 0.071787 | 0.219 |
| w31 | 51 | -0.012239 | -24.851 |
| w32 | 56 | -0.067663 | -27.068 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 46 | -0.095337 | 11.483 |
| w7 | 61 | 0.041568 | -0.463 |
| w8 | 52 | 0.094654 | -13.28 |
| w9 | 52 | 0.032986 | 3.408 |
| w10 | 54 | 0.200218 | 20.229 |
| w11 | 56 | -0.065748 | -11.054 |
| w12 | 52 | -0.04975 | -21.033 |
| w13 | 50 | 0.051768 | 0.339 |
| w14 | 56 | 0.1951 | 47.559 |
| w15 | 52 | 0.032736 | 18.789 |
| w16 | 48 | 0.046638 | 31.573 |
| w17 | 48 | 0.248785 | 34.209 |
| w18 | 53 | 0.080788 | -1.298 |
| w19 | 52 | 0.014075 | -14.592 |
| w20 | 26 | 0.126963 | 1.452 |
| w21 | 51 | 0.200195 | 42.609 |
| w22 | 51 | 0.274876 | 73.581 |
| w23 | 48 | 0.026738 | 37.169 |
| w24 | 50 | 0.123857 | 25.176 |
| w25 | 52 | 0.115666 | 16.169 |
| w26 | 53 | 0.006095 | -0.353 |
| w27 | 45 | -0.098151 | 13.829 |
| w28 | 47 | 0.053148 | 5.746 |
| w29 | 53 | 0.018647 | 6.842 |
| w30 | 52 | 0.011239 | -14.353 |
| w31 | 58 | -0.102776 | -32.969 |
| w32 | 51 | -0.113235 | -20.984 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 52 | 0.04565 | 0.86 |
| w8 | 52 | 0.153898 | -2.465 |
| w9 | 56 | -0.203512 | -53.515 |
| w10 | 50 | 0.072769 | 21.59 |
| w11 | 49 | 0.094603 | 4.945 |
| w12 | 53 | -0.049222 | -26.579 |
| w13 | 53 | 0.0453 | 11.559 |
| w14 | 55 | 0.272326 | 37.374 |
| w15 | 49 | 0.016096 | -4.923 |
| w16 | 43 | 0.008328 | 16.787 |
| w17 | 46 | 0.301392 | 59.073 |
| w18 | 57 | 0.013594 | -14.764 |
| w19 | 56 | 0.01555 | -20.115 |
| w20 | 54 | 0.145667 | -2.184 |
| w21 | 48 | 0.16427 | 4.468 |
| w22 | 47 | -0.015084 | -7.112 |
| w23 | 56 | 0.160464 | 62.636 |
| w24 | 46 | 0.083385 | 10.286 |
| w25 | 51 | 0.012504 | 9.609 |
| w26 | 53 | 0.015049 | -15.008 |
| w27 | 52 | 0.031827 | 8.327 |
| w28 | 47 | 0.128161 | 10.136 |
| w29 | 51 | 0.215976 | 36.094 |
| w30 | 53 | 0.042033 | -3.223 |
| w31 | 54 | 0.155958 | 0.962 |
| w32 | 60 | -0.138736 | -56.621 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.111504 | 11.389 |
| w2 | 44 | 0.011928 | -0.647 |
| w3 | 56 | 0.086319 | -10.315 |
| w4 | 38 | -0.055121 | 14.194 |
| w5 | 44 | 0.007579 | 22.11 |
| w6 | 50 | 0.009174 | 19.275 |
| w7 | 49 | -0.052239 | -1.213 |
| w8 | 55 | 0.107883 | -5.916 |
| w9 | 51 | 0.066058 | -15.022 |
| w10 | 56 | 0.171786 | 25.671 |
| w11 | 53 | 0.009726 | 4.538 |
| w12 | 49 | 0.010447 | -16.2 |
| w13 | 50 | 0.051106 | 9.628 |
| w14 | 54 | 0.105128 | 36.442 |
| w15 | 44 | 0.021581 | 9.239 |
| w16 | 45 | 0.009266 | 20.444 |
| w17 | 46 | 0.217438 | 45.705 |
| w18 | 56 | 0.148711 | 18.417 |
| w19 | 51 | -0.08969 | -23.265 |
| w20 | 49 | 0.062085 | -9.326 |
| w21 | 54 | 0.102462 | 0.979 |
| w22 | 48 | 0.014941 | 12.515 |
| w23 | 57 | 0.059552 | -4.902 |
| w24 | 47 | 0.054645 | 14.745 |
| w25 | 49 | 0.08325 | 19.408 |
| w26 | 51 | 0.040753 | -7.632 |
| w27 | 51 | 0.007377 | 10.819 |
| w28 | 56 | 0.149814 | 6.048 |
| w29 | 43 | -0.051023 | 11.675 |
| w30 | 54 | -0.093006 | -23.977 |
| w31 | 52 | -0.02662 | -20.644 |
| w32 | 48 | -0.158874 | -26.934 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 52 | 0.164822 | 30.075 |
| w11 | 51 | 0.017817 | -7.924 |
| w12 | 50 | -0.024053 | -17.652 |
| w13 | 49 | 0.030849 | 3.305 |
| w14 | 54 | 0.254691 | 62.634 |
| w15 | 47 | 0.027864 | 6.267 |
| w16 | 45 | -0.010111 | 23.02 |
| w17 | 46 | 0.252537 | 63.705 |
| w18 | 52 | 0.130912 | -7.15 |
| w19 | 60 | 0.06654 | -5.167 |
| w20 | 48 | 0.127146 | 8.803 |
| w21 | 55 | 0.054447 | -14.915 |
| w22 | 50 | 0.079258 | 16.836 |
| w23 | 50 | 0.066479 | -5.138 |
| w24 | 49 | -0.078174 | 7.815 |
| w25 | 49 | 0.071154 | -1.586 |
| w26 | 60 | 0.031032 | -11.585 |
| w27 | 48 | -0.101252 | -1.017 |
| w28 | 52 | 0.010801 | -5.65 |
| w29 | 52 | -0.005209 | -0.661 |
| w30 | 64 | -0.011862 | -25.433 |
| w31 | 54 | 0.056452 | -6.71 |
| w32 | 53 | -0.273469 | -49.604 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 48 | 0.04332 | 13.38 |
| w13 | 48 | -0.075918 | -28.854 |
| w14 | 49 | 0.117959 | 42.479 |
| w15 | 47 | 0.130526 | 10.63 |
| w16 | 58 | -0.018266 | 14.247 |
| w17 | 48 | 0.169872 | 30.405 |
| w18 | 47 | 0.073335 | 10.674 |
| w19 | 53 | 0.155313 | -1.57 |
| w20 | 52 | 0.036875 | -5.141 |
| w21 | 52 | -0.000504 | -10.99 |
| w22 | 48 | 0.147675 | 17.699 |
| w23 | 50 | 0.081372 | -20.849 |
| w24 | 50 | 0.079771 | 14.138 |
| w25 | 51 | 0.121614 | 5.006 |
| w26 | 58 | -0.009748 | -31.491 |
| w27 | 54 | -0.040372 | -3.444 |
| w28 | 58 | 0.025973 | -8.723 |
| w29 | 54 | -0.073879 | -18.404 |
| w30 | 55 | 0.036665 | -25.5 |
| w31 | 55 | -0.027158 | -14.787 |
| w32 | 52 | 0.168432 | 10.9 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 55 | 0.157783 | 15.051 |
| w16 | 46 | -0.108376 | 0.16 |
| w17 | 49 | 0.321316 | 60.41 |
| w18 | 51 | 0.216661 | 52.346 |
| w19 | 48 | 0.08797 | -17.257 |
| w20 | 56 | 0.118617 | -0.519 |
| w21 | 48 | 0.074791 | -4.062 |
| w22 | 48 | 0.027842 | -2.704 |
| w23 | 54 | -0.01883 | -29.106 |
| w24 | 42 | 0.075164 | 31.105 |
| w25 | 47 | 0.058985 | -1.569 |
| w26 | 50 | 0.050692 | -11.474 |
| w27 | 49 | -0.031055 | 11.889 |
| w28 | 49 | 0.055323 | -4.247 |
| w29 | 51 | -0.051171 | -9.814 |
| w30 | 59 | -0.000254 | -23.676 |
| w31 | 49 | -0.087987 | -18.875 |
| w32 | 59 | -0.089573 | -24.463 |

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
| w15 | 50 | 0.053223 | 5.659 |
| w16 | 51 | -0.08362 | 10.959 |
| w17 | 46 | 0.233726 | 33.21 |
| w18 | 49 | 0.169115 | 15.132 |
| w19 | 49 | -0.028602 | -15.195 |
| w20 | 49 | 0.23782 | 42.354 |
| w21 | 52 | 0.124208 | -2.255 |
| w22 | 45 | 0.161778 | 27.945 |
| w23 | 47 | -0.012626 | 0.841 |
| w24 | 48 | 0.075148 | 17.18 |
| w25 | 47 | -0.081361 | -20.079 |
| w26 | 47 | -0.054033 | -6.285 |
| w27 | 38 | -0.058786 | -2.58 |
| w28 | 52 | 0.02352 | 5.186 |
| w29 | 49 | 0.045278 | 17.358 |
| w30 | 55 | 0.072453 | -10.154 |
| w31 | 52 | -0.008908 | -0.267 |
| w32 | 46 | -0.21915 | -26.881 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 51 | -0.112686 | -2.258 |
| w17 | 41 | 0.251244 | 62.166 |
| w18 | 51 | 0.031297 | -4.156 |
| w19 | 49 | -0.005595 | -20.384 |
| w20 | 50 | 0.182695 | 10.687 |
| w21 | 55 | 0.146304 | -6.43 |
| w22 | 50 | 0.164737 | 25.134 |
| w23 | 52 | -0.001014 | -25.856 |
| w24 | 46 | -0.055294 | -3.516 |
| w25 | 44 | 0.117541 | 2.537 |
| w26 | 49 | -0.164591 | -35.326 |
| w27 | 55 | -0.075016 | -11.311 |
| w28 | 52 | -0.011057 | -14.969 |
| w29 | 52 | -0.008275 | -10.464 |
| w30 | 54 | 0.010356 | -19.365 |
| w31 | 57 | 0.040855 | -11.263 |
| w32 | 57 | -0.036527 | -29.021 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 50 | 0.052569 | -8.689 |
| w21 | 54 | 0.13369 | 0.768 |
| w22 | 50 | 0.044579 | 14.319 |
| w23 | 55 | 0.0745 | -13.774 |
| w24 | 41 | -0.00546 | 26.843 |
| w25 | 50 | 0.232949 | 31.852 |
| w26 | 58 | -0.064479 | -21.428 |
| w27 | 52 | -0.028415 | 3.873 |
| w28 | 51 | 0.038981 | -5.891 |
| w29 | 47 | -0.113845 | -16.165 |
| w30 | 54 | -0.057545 | -19.466 |
| w31 | 53 | 0.064997 | -7.679 |
| w32 | 57 | -0.023177 | -23.862 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 52 | 0.015015 | 6.459 |
| w23 | 53 | 0.039303 | -14.081 |
| w24 | 39 | 0.103801 | 34.064 |
| w25 | 46 | 0.157711 | 41.18 |
| w26 | 55 | -0.026908 | -14.023 |
| w27 | 52 | 0.010726 | 5.028 |
| w28 | 49 | 0.019191 | -12.737 |
| w29 | 49 | 0.006155 | -2.526 |
| w30 | 51 | -0.005143 | -8.154 |
| w31 | 52 | -0.007335 | -10.201 |
| w32 | 55 | -0.030044 | 14.959 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 51 | 0.284152 | 77.001 |
| w25 | 48 | 0.011859 | 2.694 |
| w26 | 53 | 0.000367 | -7.298 |
| w27 | 48 | 0.178929 | 50.989 |
| w28 | 52 | 0.044383 | 5.0 |
| w29 | 54 | 0.037998 | 2.738 |
| w30 | 56 | 0.049686 | -12.746 |
| w31 | 55 | -0.108036 | -23.76 |
| w32 | 52 | 0.023773 | 6.283 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 49 | -0.013862 | 14.458 |
| w6 | 46 | 0.088458 | 26.8 |
| w7 | 53 | 0.111097 | 4.331 |
| w8 | 56 | 0.109053 | -0.299 |
| w9 | 57 | 0.09557 | -13.475 |
| w10 | 51 | 0.113697 | 12.255 |
| w11 | 56 | 0.106458 | 9.665 |
| w12 | 53 | 0.004983 | -17.446 |
| w13 | 46 | -0.052382 | -0.709 |
| w14 | 52 | 0.067125 | 21.953 |
| w15 | 54 | 0.054536 | 0.836 |
| w16 | 42 | -0.105835 | 0.364 |
| w17 | 43 | 0.331464 | 65.432 |
| w18 | 53 | -0.023535 | -5.456 |
| w19 | 50 | -0.093368 | -17.475 |
| w20 | 51 | 0.113075 | -0.162 |
| w21 | 52 | 0.054511 | -8.338 |
| w22 | 50 | 0.083198 | 6.871 |
| w23 | 50 | -0.028593 | -16.229 |
| w24 | 46 | 0.171967 | 32.022 |
| w25 | 51 | 0.059332 | -5.489 |
| w26 | 60 | -0.025018 | 4.488 |
| w27 | 54 | -0.110723 | -7.159 |
| w28 | 50 | -0.030512 | -12.042 |
| w29 | 52 | -0.092725 | -12.292 |
| w30 | 38 | -0.075387 | 18.915 |
| w31 | 56 | -0.140968 | -20.96 |
| w32 | 45 | 0.018343 | 18.688 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 46 | 0.047308 | 36.31 |
| w6 | 53 | 0.216218 | 67.395 |
| w7 | 52 | 0.144315 | 16.724 |
| w8 | 55 | 0.199198 | 11.663 |
| w9 | 54 | 0.188916 | 0.897 |
| w10 | 47 | 0.125995 | 18.21 |
| w11 | 52 | -0.032758 | -5.711 |
| w12 | 57 | 0.067267 | -10.366 |
| w13 | 52 | 0.052684 | 4.675 |
| w14 | 48 | 0.284779 | 61.297 |
| w15 | 45 | 0.139196 | 26.991 |
| w16 | 42 | 0.074603 | 38.123 |
| w17 | 42 | 0.268134 | 51.304 |
| w18 | 46 | -0.022209 | -12.518 |
| w19 | 57 | 0.052694 | -0.277 |
| w20 | 46 | 0.043601 | -4.526 |
| w21 | 49 | 0.148179 | 7.267 |
| w22 | 49 | 0.15177 | 17.582 |
| w23 | 47 | -0.012242 | -23.498 |
| w24 | 52 | 0.10167 | 7.414 |
| w25 | 49 | 0.160359 | 3.98 |
| w26 | 46 | 0.354029 | 65.337 |
| w27 | 43 | 0.056904 | 5.588 |
| w28 | 44 | 0.075331 | 17.053 |
| w29 | 49 | -0.081379 | -22.935 |
| w30 | 43 | -0.005208 | 8.526 |
| w31 | 50 | 0.128266 | 17.827 |
| w32 | 46 | 0.131437 | 38.898 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 51 | 0.150637 | 20.497 |
| w18 | 47 | 0.104876 | 28.571 |
| w19 | 55 | 0.046147 | -10.454 |
| w20 | 55 | -0.013918 | -11.957 |
| w21 | 53 | 0.202305 | 6.926 |
| w22 | 46 | 0.159998 | 27.318 |
| w23 | 63 | 0.169295 | -1.666 |
| w24 | 48 | 0.202339 | 36.594 |
| w25 | 53 | 0.199567 | 21.952 |
| w26 | 56 | 0.180683 | 15.766 |
| w27 | 49 | 0.017966 | 27.676 |
| w28 | 49 | 0.093842 | 9.423 |
| w29 | 53 | -0.086934 | -13.494 |
| w30 | 59 | -0.071617 | -23.747 |
| w31 | 53 | 0.04142 | -14.32 |
| w32 | 53 | -0.07943 | -11.34 |

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
| w17 | 49 | 0.246562 | 46.624 |
| w18 | 52 | 0.000934 | -15.37 |
| w19 | 56 | 0.075019 | 1.756 |
| w20 | 58 | 0.075536 | 3.069 |
| w21 | 48 | 0.167757 | 10.701 |
| w22 | 48 | 0.164915 | 30.166 |
| w23 | 51 | -0.045466 | -11.882 |
| w24 | 49 | 0.045489 | 20.389 |
| w25 | 54 | 0.091078 | 9.751 |
| w26 | 47 | -0.105205 | -10.093 |
| w27 | 47 | -0.023816 | 13.567 |
| w28 | 47 | 0.116276 | 5.735 |
| w29 | 52 | -0.027537 | 4.423 |
| w30 | 48 | -0.009963 | -19.084 |
| w31 | 55 | -0.001762 | -16.09 |
| w32 | 48 | -0.092735 | -6.841 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 50 | -0.061395 | -31.612 |
| w20 | 52 | 0.054879 | -3.09 |
| w21 | 54 | 0.137591 | 11.733 |
| w22 | 40 | -0.130339 | 5.158 |
| w23 | 57 | 0.024788 | -7.179 |
| w24 | 44 | 0.111427 | 36.874 |
| w25 | 52 | 0.072431 | -3.562 |
| w26 | 53 | 0.029579 | -4.82 |
| w27 | 56 | -0.034593 | -6.828 |
| w28 | 50 | 0.024151 | -12.781 |
| w29 | 53 | -0.072799 | -10.099 |
| w30 | 59 | 0.043508 | -19.94 |
| w31 | 50 | 0.022691 | -8.942 |
| w32 | 52 | 0.006585 | 6.6 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 48 | 0.240505 | 43.329 |
| w23 | 52 | 0.157011 | 9.517 |
| w24 | 48 | 0.224792 | 41.601 |
| w25 | 51 | -0.033755 | -18.823 |
| w26 | 48 | 0.016231 | -11.745 |
| w27 | 48 | -0.073129 | -4.487 |
| w28 | 57 | 0.09681 | -0.252 |
| w29 | 47 | -0.158701 | -18.293 |
| w30 | 54 | 0.076095 | -6.522 |
| w31 | 52 | 0.025123 | -13.87 |
| w32 | 46 | -0.095436 | -12.789 |

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
| w27 | 46 | 0.025585 | 14.77 |
| w28 | 51 | 0.285278 | 31.419 |
| w29 | 49 | -0.016574 | -3.862 |
| w30 | 58 | 0.009347 | -24.491 |
| w31 | 59 | -0.006477 | -14.377 |
| w32 | 50 | 0.016755 | 7.949 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 54 | 0.200522 | 24.956 |
| w18 | 63 | -0.002001 | -22.544 |
| w19 | 56 | -0.040108 | -26.992 |
| w20 | 54 | -0.007636 | -16.064 |
| w21 | 50 | 0.05723 | -15.092 |
| w22 | 55 | 0.128179 | 30.415 |
| w23 | 60 | -0.019823 | -27.032 |
| w24 | 44 | 0.025199 | 9.788 |
| w25 | 48 | 0.021401 | -3.794 |
| w26 | 54 | 0.093795 | -9.987 |
| w27 | 49 | -0.046204 | -4.797 |
| w28 | 54 | -0.0391 | -18.732 |
| w29 | 57 | -0.029116 | -17.396 |
| w30 | 48 | -0.090504 | -28.489 |
| w31 | 48 | 0.01093 | -14.153 |
| w32 | 60 | 0.146298 | 9.89 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 55 | 0.260756 | 32.679 |
| w18 | 54 | 0.155132 | 15.206 |
| w19 | 57 | 0.096759 | -4.372 |
| w20 | 48 | 0.085952 | -2.949 |
| w21 | 50 | 0.103046 | -6.045 |
| w22 | 43 | 0.056007 | 21.754 |
| w23 | 50 | -0.017472 | -18.267 |
| w24 | 43 | 0.010713 | 11.906 |
| w25 | 49 | 0.11753 | 19.781 |
| w26 | 57 | 0.044243 | -11.638 |
| w27 | 52 | -0.068988 | -6.95 |
| w28 | 54 | 0.048732 | -12.078 |
| w29 | 50 | -0.049909 | -13.822 |
| w30 | 56 | 0.038681 | -22.612 |
| w31 | 53 | 0.097923 | -6.9 |
| w32 | 65 | 0.070245 | -15.956 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 51 | 0.028125 | -3.822 |
| w29 | 55 | 0.066075 | 2.685 |
| w30 | 57 | 0.122097 | 18.722 |
| w31 | 54 | -0.080828 | -12.667 |
| w32 | 58 | 0.10193 | 16.24 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 52 | 0.01252 | 18.424 |
| w15 | 43 | 0.006731 | 10.594 |
| w16 | 46 | 0.019259 | 84.739 |
| w17 | 51 | 0.059319 | 6.631 |
| w18 | 50 | 0.150988 | 11.733 |
| w19 | 51 | 0.068083 | 4.883 |
| w20 | 51 | 0.098426 | -3.264 |
| w21 | 63 | 0.00154 | 4.672 |
| w22 | 53 | 0.128651 | 24.002 |
| w23 | 55 | 0.121801 | 8.126 |
| w24 | 51 | 0.044437 | 15.804 |
| w25 | 48 | -0.042612 | 1.03 |
| w26 | 56 | 0.015552 | -9.515 |
| w27 | 44 | -0.132495 | 3.133 |
| w28 | 57 | 0.040783 | -7.092 |
| w29 | 49 | -0.118018 | -13.492 |
| w30 | 57 | 0.042359 | -8.942 |
| w31 | 55 | -0.073866 | -15.715 |
| w32 | 50 | -0.108244 | -29.226 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 72 | 0.041783 | 23.064 |
| w26 | 53 | 0.006621 | 1.42 |
| w27 | 48 | -0.087878 | -0.257 |
| w28 | 53 | 0.078286 | -4.979 |
| w29 | 55 | -0.099281 | -14.225 |
| w30 | 52 | 0.006618 | -21.685 |
| w31 | 55 | 0.074327 | 3.887 |
| w32 | 79 | -0.131653 | -34.225 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

