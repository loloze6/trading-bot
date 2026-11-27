# Backtest of 031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.d1_small-body-wide-uprun-day_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | 0.016872 | -7.053 |
| w2 | 3 | 0.057639 | 28.19 |
| w3 | 3 | 0.132555 | 15.642 |
| w4 | 8 | -0.105258 | -4.064 |
| w5 | 19 | 0.000434 | 24.84 |
| w6 | 11 | 0.074006 | 28.452 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.042587 | 3.662 |
| w11 | 13 | 0.136816 | 30.163 |
| w12 | 6 | 0.089177 | 1.718 |
| w13 | 6 | -0.039904 | 2.867 |
| w14 | 5 | 0.201253 | 25.905 |
| w15 | 10 | -0.010348 | 20.193 |
| w16 | 6 | -0.048021 | -4.805 |
| w17 | 2 | 0.121626 | 5.343 |
| w18 | 2 | -0.041478 | -1.546 |
| w19 | 1 | -0.048799 | -1.046 |
| w20 | 2 | -0.040765 | -6.419 |
| w21 | 1 | -0.07464 | -4.986 |
| w22 | 11 | 0.004326 | 19.505 |
| w23 | 2 | 0.019975 | 1.721 |
| w24 | 8 | 0.027744 | 2.398 |
| w25 | 13 | -0.020752 | 8.503 |
| w26 | 4 | 0.017765 | 0.53 |
| w27 | 5 | 0.005675 | 10.203 |
| w28 | 4 | 0.167917 | 1.538 |
| w29 | 7 | -0.017404 | 1.804 |
| w30 | 1 | 0.013709 | 3.885 |
| w31 | 2 | -0.057045 | 1.327 |
| w32 | 5 | -0.007286 | 3.315 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 12 | 0.067389 | 25.69 |
| w2 | 16 | -0.080388 | -24.049 |
| w3 | 10 | -0.080642 | -14.403 |
| w4 | 16 | 0.058568 | -3.739 |
| w5 | 12 | -0.000437 | 15.534 |
| w6 | 15 | 0.1234 | 45.973 |
| w7 | 4 | -0.12948 | -4.649 |
| w8 | 2 | -0.045695 | -6.929 |
| w9 | 1 | -0.014113 | -6.198 |
| w10 | 6 | -0.016394 | 0.129 |
| w11 | 6 | -0.021456 | 8.389 |
| w12 | 6 | 0.086397 | 2.945 |
| w13 | 11 | 0.021553 | 20.569 |
| w14 | 11 | 0.150279 | 11.786 |
| w15 | 12 | 0.236298 | 15.079 |
| w16 | 13 | -0.09379 | -2.012 |
| w17 | 8 | 0.242549 | 15.63 |
| w18 | 3 | 0.039325 | 0.891 |
| w19 | 1 | -0.118538 | -2.989 |
| w20 | 2 | 0.03736 | -0.872 |
| w21 | 7 | -0.087774 | -6.782 |
| w22 | 9 | -0.092699 | 0.055 |
| w23 | 5 | 0.06494 | -5.0 |
| w24 | 10 | 0.025207 | 3.37 |
| w25 | 17 | 0.066581 | 10.138 |
| w26 | 2 | -0.065999 | -4.583 |
| w27 | 9 | 0.119374 | 13.36 |
| w28 | 4 | 0.181918 | -3.577 |
| w29 | 10 | 0.11403 | 18.295 |
| w30 | 3 | -0.078005 | -9.92 |
| w31 | 0 | None | 0.0 |
| w32 | 4 | 0.10292 | 2.555 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 11 | -0.018267 | 14.91 |
| w7 | 9 | -0.022174 | 2.647 |
| w8 | 1 | -0.036486 | -4.68 |
| w9 | 10 | 0.025198 | -9.748 |
| w10 | 5 | 0.13332 | 2.34 |
| w11 | 9 | -0.127767 | 28.271 |
| w12 | 4 | -0.043692 | -7.553 |
| w13 | 14 | -0.135163 | -6.094 |
| w14 | 9 | 0.22788 | 15.138 |
| w15 | 11 | 0.128488 | 105.213 |
| w16 | 11 | -0.07003 | 4.325 |
| w17 | 8 | 0.109326 | 23.548 |
| w18 | 2 | 0.043433 | -0.079 |
| w19 | 1 | -0.004417 | -8.667 |
| w20 | 1 | -0.041414 | -3.28 |
| w21 | 4 | 0.276665 | 25.828 |
| w22 | 8 | -0.039509 | -1.891 |
| w23 | 4 | -0.00431 | 2.521 |
| w24 | 11 | -0.034855 | -10.303 |
| w25 | 4 | 0.004624 | 9.562 |
| w26 | 4 | -0.058048 | -4.495 |
| w27 | 12 | -0.002923 | 89.255 |
| w28 | 4 | 0.068365 | 3.075 |
| w29 | 7 | 0.005298 | 8.065 |
| w30 | 2 | 0.060165 | 2.545 |
| w31 | 6 | -0.145451 | -17.5 |
| w32 | 7 | -0.005922 | -19.648 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 6 | 0.064544 | 0.538 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | 0.271651 | 9.953 |
| w10 | 6 | 0.077928 | 2.582 |
| w11 | 9 | -0.029698 | -0.194 |
| w12 | 4 | 0.074477 | 6.988 |
| w13 | 7 | -0.047878 | 6.244 |
| w14 | 6 | 0.238405 | 14.277 |
| w15 | 6 | 0.25114 | 7.848 |
| w16 | 10 | -0.143674 | 2.424 |
| w17 | 7 | -0.022904 | 10.874 |
| w18 | 2 | -0.229717 | -14.229 |
| w19 | 3 | -0.005916 | -1.652 |
| w20 | 1 | -0.060774 | -5.127 |
| w21 | 0 | None | 0.0 |
| w22 | 12 | -0.154295 | -12.875 |
| w23 | 3 | 0.354534 | 33.741 |
| w24 | 10 | -0.140679 | -8.25 |
| w25 | 10 | -0.08803 | 5.921 |
| w26 | 3 | -0.00957 | -1.569 |
| w27 | 14 | 0.091191 | 16.031 |
| w28 | 3 | 0.294453 | 17.143 |
| w29 | 7 | -0.016105 | 5.72 |
| w30 | 3 | -0.088555 | -4.598 |
| w31 | 1 | 0.000875 | -0.964 |
| w32 | 6 | -0.011868 | -3.386 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 20 | 0.198556 | 58.284 |
| w2 | 4 | -0.021774 | -9.788 |
| w3 | 8 | -0.003215 | -1.785 |
| w4 | 11 | 0.051102 | 88.414 |
| w5 | 15 | -0.092387 | 12.809 |
| w6 | 4 | -0.051104 | -7.699 |
| w7 | 6 | -0.042147 | 1.332 |
| w8 | 4 | -0.036758 | -2.6 |
| w9 | 2 | -0.231428 | -18.876 |
| w10 | 6 | -0.000104 | 2.696 |
| w11 | 9 | -0.076071 | 23.494 |
| w12 | 5 | 0.001953 | -1.594 |
| w13 | 15 | 0.003123 | 8.554 |
| w14 | 6 | 0.148748 | 22.826 |
| w15 | 12 | 0.138615 | 12.093 |
| w16 | 10 | -0.031207 | -5.076 |
| w17 | 7 | 0.056871 | 4.35 |
| w18 | 6 | -0.024835 | 0.148 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | 0.078161 | -0.461 |
| w22 | 8 | -0.000607 | 21.418 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.029526 | 4.425 |
| w25 | 10 | 0.072736 | 24.692 |
| w26 | 1 | -0.0351 | 1.004 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.22568 | -14.544 |
| w29 | 7 | 0.204467 | 7.327 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.022509 | 1.754 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 9 | 0.049446 | 13.807 |
| w11 | 11 | -0.095646 | 12.902 |
| w12 | 11 | 0.124033 | 1.581 |
| w13 | 6 | 0.032916 | -5.125 |
| w14 | 8 | 0.168705 | 14.44 |
| w15 | 5 | -0.054749 | -4.316 |
| w16 | 17 | -0.047391 | 31.102 |
| w17 | 8 | 0.028727 | 13.171 |
| w18 | 2 | -0.043044 | -2.386 |
| w19 | 2 | 0.034105 | 3.539 |
| w20 | 2 | -0.139975 | -8.212 |
| w21 | 1 | 0.084254 | 4.0 |
| w22 | 12 | -0.014367 | 5.423 |
| w23 | 2 | -0.03939 | -6.444 |
| w24 | 12 | 0.158595 | 72.925 |
| w25 | 7 | 0.177088 | 7.354 |
| w26 | 1 | -0.071823 | -0.952 |
| w27 | 6 | -0.196407 | -7.295 |
| w28 | 3 | 0.021318 | -4.102 |
| w29 | 10 | 0.063863 | -0.624 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.089848 | -6.204 |
| w32 | 7 | -0.023828 | -11.841 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 5 | -0.046185 | 15.031 |
| w13 | 4 | -0.004673 | -4.069 |
| w14 | 18 | -0.119612 | 9.471 |
| w15 | 3 | -0.121332 | 0.806 |
| w16 | 9 | -0.011739 | 15.729 |
| w17 | 12 | 0.068416 | 7.858 |
| w18 | 5 | -0.111704 | 1.755 |
| w19 | 4 | -0.097334 | -3.772 |
| w20 | 4 | -0.02933 | -10.591 |
| w21 | 0 | None | 0.0 |
| w22 | 7 | 0.059176 | -5.436 |
| w23 | 1 | -0.019402 | -3.107 |
| w24 | 13 | -0.010654 | 37.125 |
| w25 | 7 | 0.231878 | 22.404 |
| w26 | 0 | None | 0.0 |
| w27 | 5 | -0.03856 | 0.189 |
| w28 | 2 | -0.066766 | 0.016 |
| w29 | 6 | 0.085599 | 2.649 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.114918 | -4.694 |
| w32 | 6 | 0.003874 | -14.664 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | -0.045221 | -3.977 |
| w16 | 9 | -0.052376 | 12.321 |
| w17 | 6 | 0.02156 | -6.753 |
| w18 | 10 | 0.163016 | 36.923 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.054247 | -6.087 |
| w21 | 10 | -0.040257 | -0.709 |
| w22 | 7 | -0.019098 | 0.589 |
| w23 | 2 | 0.007151 | -0.686 |
| w24 | 13 | 0.038614 | 43.958 |
| w25 | 9 | -0.008986 | 1.367 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.014757 | 56.139 |
| w28 | 2 | 0.023084 | -3.993 |
| w29 | 6 | 0.003651 | 26.65 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | 0.208469 | 6.321 |
| w32 | 10 | -0.024148 | -22.076 |

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
| w15 | 13 | -0.14713 | -7.904 |
| w16 | 20 | -0.045719 | 0.405 |
| w17 | 6 | 0.028464 | 4.778 |
| w18 | 5 | -0.002722 | -8.695 |
| w19 | 3 | 0.137563 | 13.021 |
| w20 | 5 | -0.141424 | -4.852 |
| w21 | 5 | -0.049335 | -15.827 |
| w22 | 5 | -0.122447 | -5.458 |
| w23 | 8 | -0.022582 | -8.862 |
| w24 | 3 | 0.226266 | 15.12 |
| w25 | 15 | -0.021152 | -7.084 |
| w26 | 5 | 0.160388 | 20.466 |
| w27 | 7 | 0.00948 | 31.69 |
| w28 | 2 | -0.195755 | -0.947 |
| w29 | 10 | -0.008827 | 13.592 |
| w30 | 0 | None | 0.0 |
| w31 | 13 | -0.209344 | -4.194 |
| w32 | 5 | 0.147689 | 2.601 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 14 | 0.150238 | 3.943 |
| w17 | 6 | -0.057844 | -6.411 |
| w18 | 4 | 0.040119 | -0.35 |
| w19 | 2 | 0.011861 | -2.285 |
| w20 | 1 | -0.080986 | -4.521 |
| w21 | 1 | -0.29 | -15.743 |
| w22 | 9 | 0.027893 | 19.289 |
| w23 | 6 | -0.100724 | -17.03 |
| w24 | 13 | -0.015052 | -1.744 |
| w25 | 12 | 0.144963 | 13.024 |
| w26 | 2 | 0.02694 | 1.433 |
| w27 | 7 | -0.133352 | 12.526 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | 0.049348 | 6.008 |
| w30 | 4 | 0.001136 | -7.905 |
| w31 | 3 | -0.087683 | -4.611 |
| w32 | 5 | -0.067175 | -17.328 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.005773 | -0.572 |
| w21 | 1 | 0.007707 | -3.804 |
| w22 | 12 | 0.064967 | 7.912 |
| w23 | 3 | -0.024648 | -8.426 |
| w24 | 16 | 0.175822 | 81.731 |
| w25 | 7 | -0.008024 | 5.018 |
| w26 | 1 | -0.023376 | -1.465 |
| w27 | 9 | 0.062757 | 3.28 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.04152 | -3.837 |
| w30 | 2 | -0.03218 | -9.119 |
| w31 | 3 | -0.079815 | -0.25 |
| w32 | 5 | 0.004185 | -9.022 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.006272 | 21.025 |
| w23 | 4 | -0.027533 | -10.001 |
| w24 | 10 | 0.201936 | 63.514 |
| w25 | 7 | 0.207994 | 55.837 |
| w26 | 1 | -0.06968 | -2.715 |
| w27 | 7 | 0.16157 | 12.294 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.061295 | -1.295 |
| w30 | 7 | 0.000897 | -10.267 |
| w31 | 2 | 0.056758 | 2.957 |
| w32 | 7 | -0.016288 | -7.442 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 15 | 0.027573 | 16.008 |
| w25 | 10 | 0.025599 | 5.546 |
| w26 | 7 | 0.081066 | -4.882 |
| w27 | 12 | -0.007354 | 18.697 |
| w28 | 4 | 0.002958 | -0.159 |
| w29 | 3 | -0.070111 | -0.064 |
| w30 | 2 | 0.03386 | 2.433 |
| w31 | 1 | -0.071953 | -3.588 |
| w32 | 7 | 0.127714 | 3.54 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 14 | -0.010182 | 5.35 |
| w6 | 10 | -0.1286 | -1.334 |
| w7 | 7 | -0.059927 | 0.994 |
| w8 | 2 | -0.184148 | -9.768 |
| w9 | 4 | -0.115365 | -16.429 |
| w10 | 7 | -0.043848 | -2.666 |
| w11 | 9 | 0.053413 | 24.488 |
| w12 | 5 | 0.022089 | -8.037 |
| w13 | 7 | 0.005 | 21.941 |
| w14 | 4 | -0.085905 | 4.797 |
| w15 | 5 | 0.025299 | 0.295 |
| w16 | 15 | 0.139708 | 58.847 |
| w17 | 8 | 0.003415 | 2.36 |
| w18 | 9 | 0.099844 | 6.295 |
| w19 | 1 | -0.182547 | -3.427 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.069827 | 0.052 |
| w23 | 4 | 0.019565 | -4.871 |
| w24 | 13 | -0.050348 | 1.349 |
| w25 | 10 | 0.153246 | 17.611 |
| w26 | 5 | 0.136373 | -1.02 |
| w27 | 10 | -0.057889 | 2.075 |
| w28 | 4 | -0.054296 | -6.476 |
| w29 | 9 | -0.046478 | -6.896 |
| w30 | 15 | 0.203306 | 81.438 |
| w31 | 1 | -0.05177 | -2.723 |
| w32 | 7 | 0.109413 | 33.593 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 12 | 0.153345 | 42.907 |
| w6 | 18 | 0.191681 | 25.067 |
| w7 | 2 | 0.086839 | 6.251 |
| w8 | 2 | -0.013562 | 2.299 |
| w9 | 1 | -0.030324 | -3.774 |
| w10 | 4 | -0.166979 | 5.761 |
| w11 | 10 | 0.016681 | 10.949 |
| w12 | 2 | -0.064936 | -2.021 |
| w13 | 8 | 0.01602 | 5.601 |
| w14 | 9 | 0.069584 | 13.294 |
| w15 | 5 | -0.106665 | -9.062 |
| w16 | 20 | 0.226129 | 40.624 |
| w17 | 9 | 0.04972 | -4.34 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.000523 | -0.12 |
| w20 | 2 | 0.024915 | 0.525 |
| w21 | 7 | 0.02353 | 3.177 |
| w22 | 9 | -0.079246 | 7.814 |
| w23 | 0 | None | 0.0 |
| w24 | 12 | 0.033848 | 2.777 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.102444 | -2.228 |
| w27 | 2 | 0.022176 | 2.008 |
| w28 | 4 | 0.099194 | 2.743 |
| w29 | 6 | -0.264579 | -13.483 |
| w30 | 7 | -0.067495 | -12.056 |
| w31 | 7 | -0.060363 | 3.85 |
| w32 | 12 | -0.122422 | -4.527 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 3 | 0.01507 | 1.28 |
| w18 | 8 | 0.056252 | 12.427 |
| w19 | 2 | -0.082579 | -8.313 |
| w20 | 4 | -0.063081 | -5.137 |
| w21 | 5 | -0.117074 | -19.067 |
| w22 | 8 | 0.077501 | 4.961 |
| w23 | 5 | -0.056669 | -5.584 |
| w24 | 12 | 0.118641 | 12.999 |
| w25 | 7 | 0.171607 | 29.088 |
| w26 | 8 | 0.014439 | -2.724 |
| w27 | 12 | 0.236762 | 63.019 |
| w28 | 1 | -0.180009 | -9.277 |
| w29 | 7 | -0.026478 | 1.687 |
| w30 | 1 | -0.013055 | 1.414 |
| w31 | 4 | -0.086484 | -7.645 |
| w32 | 13 | 0.179694 | 23.577 |

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
| w17 | 5 | 0.155961 | -3.399 |
| w18 | 7 | -0.008032 | -0.014 |
| w19 | 5 | -0.072657 | 1.067 |
| w20 | 5 | -0.022297 | 1.144 |
| w21 | 1 | -0.331496 | -17.968 |
| w22 | 6 | 0.081863 | 9.481 |
| w23 | 3 | 0.049895 | 5.265 |
| w24 | 15 | -0.00341 | 21.068 |
| w25 | 7 | 0.07475 | 14.745 |
| w26 | 8 | 0.060396 | 7.267 |
| w27 | 9 | 0.044044 | 12.9 |
| w28 | 3 | 0.220545 | 3.498 |
| w29 | 6 | -0.108255 | -0.809 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.080364 | -1.108 |
| w32 | 4 | 0.37485 | 8.218 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 7 | -0.186925 | -10.013 |
| w20 | 9 | -0.139674 | -16.042 |
| w21 | 14 | 0.054801 | 5.555 |
| w22 | 22 | -0.016105 | 35.951 |
| w23 | 4 | 0.154176 | 0.888 |
| w24 | 23 | 0.235976 | 116.105 |
| w25 | 3 | 0.028067 | -4.553 |
| w26 | 10 | -0.008572 | -7.462 |
| w27 | 6 | 0.035342 | 6.034 |
| w28 | 4 | -0.012542 | -1.052 |
| w29 | 6 | -0.000403 | -10.841 |
| w30 | 2 | 0.043805 | 0.551 |
| w31 | 6 | -0.110193 | -11.481 |
| w32 | 9 | 0.079047 | 12.955 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 12 | -0.041679 | -7.158 |
| w23 | 4 | -0.05481 | -14.742 |
| w24 | 12 | 0.005354 | -0.516 |
| w25 | 9 | 0.112294 | -2.086 |
| w26 | 6 | 0.11094 | 4.908 |
| w27 | 8 | 0.065851 | -0.665 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | 0.034459 | -6.984 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | 0.122548 | -3.247 |
| w32 | 4 | -0.092957 | -8.758 |

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
| w27 | 7 | 0.03971 | 16.385 |
| w28 | 6 | 0.012742 | -3.927 |
| w29 | 10 | 0.057021 | 3.918 |
| w30 | 1 | -0.068714 | -5.81 |
| w31 | 2 | -0.123479 | -13.219 |
| w32 | 12 | 0.364687 | 57.885 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | 0.022561 | 1.347 |
| w18 | 4 | -0.053777 | -9.437 |
| w19 | 7 | 0.039968 | -4.191 |
| w20 | 5 | -0.110325 | -6.886 |
| w21 | 4 | -0.044076 | -24.722 |
| w22 | 7 | -0.013582 | -2.512 |
| w23 | 9 | -0.043715 | -4.029 |
| w24 | 14 | -0.051125 | 9.628 |
| w25 | 11 | 0.061078 | 6.295 |
| w26 | 2 | -0.082815 | -3.751 |
| w27 | 9 | -0.008797 | -10.561 |
| w28 | 1 | -0.037989 | -5.972 |
| w29 | 4 | 0.015034 | -9.727 |
| w30 | 4 | -0.135444 | -13.024 |
| w31 | 4 | 0.044801 | -2.296 |
| w32 | 7 | 0.175946 | -6.749 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.119154 | 8.063 |
| w18 | 6 | -0.270994 | -20.349 |
| w19 | 5 | 0.138341 | 2.631 |
| w20 | 5 | 0.031327 | -5.091 |
| w21 | 7 | 0.04351 | -12.099 |
| w22 | 12 | -0.016523 | 14.464 |
| w23 | 6 | 0.114457 | 2.199 |
| w24 | 12 | 0.146992 | 52.001 |
| w25 | 10 | 0.11061 | 13.934 |
| w26 | 0 | None | 0.0 |
| w27 | 9 | -0.007837 | 1.355 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | 0.163151 | 0.615 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.132315 | -4.631 |
| w32 | 12 | 0.010902 | -16.061 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 7 | 0.01549 | 0.899 |
| w29 | 8 | 0.043829 | -0.671 |
| w30 | 1 | -0.173249 | -10.448 |
| w31 | 6 | -0.17664 | -15.144 |
| w32 | 9 | 0.145684 | 6.23 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 1 | -0.107803 | -5.966 |
| w15 | 12 | 0.181663 | 66.105 |
| w16 | 7 | -0.069633 | -1.329 |
| w17 | 13 | 0.045642 | 7.223 |
| w18 | 5 | -0.025789 | 2.301 |
| w19 | 8 | 0.178148 | -5.458 |
| w20 | 5 | 0.139754 | 8.394 |
| w21 | 8 | 0.218715 | 50.724 |
| w22 | 12 | 0.209225 | 5.23 |
| w23 | 7 | 0.094435 | 2.739 |
| w24 | 11 | 0.074906 | 9.271 |
| w25 | 11 | 0.294286 | 29.615 |
| w26 | 5 | 0.034711 | -5.848 |
| w27 | 6 | -0.10335 | -14.704 |
| w28 | 1 | -0.16345 | -3.678 |
| w29 | 11 | 0.057797 | 23.675 |
| w30 | 3 | -0.065781 | -5.174 |
| w31 | 7 | -0.012123 | -1.634 |
| w32 | 2 | 0.060743 | -8.733 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 13 | -0.018529 | 30.937 |
| w26 | 7 | 0.006112 | 3.162 |
| w27 | 11 | 0.293819 | 42.869 |
| w28 | 1 | -0.008312 | -6.761 |
| w29 | 6 | 0.109659 | 13.33 |
| w30 | 1 | -0.043335 | -5.489 |
| w31 | 3 | 0.109343 | 0.583 |
| w32 | 4 | -0.0093 | -11.014 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

