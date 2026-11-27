# Backtest of 031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d

- Plan: `../../../../../03_test_plan/night6_yearlow_run/plans/031-01.g1.g1.d1_midweek-gain-lifts-saturday_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 11 | 0.018588 | 1.671 |
| w2 | 8 | 0.214764 | 24.792 |
| w3 | 10 | -0.071046 | -2.032 |
| w4 | 8 | -0.024063 | -0.739 |
| w5 | 12 | -0.007897 | 3.034 |
| w6 | 10 | -0.102412 | -5.666 |
| w7 | 9 | 0.118173 | 9.541 |
| w8 | 8 | 0.060631 | 2.822 |
| w9 | 6 | 0.119013 | 6.093 |
| w10 | 7 | 0.025716 | 4.14 |
| w11 | 8 | 0.181818 | 25.039 |
| w12 | 6 | -0.027446 | -3.095 |
| w13 | 11 | -0.017435 | -3.37 |
| w14 | 7 | 0.06696 | 9.546 |
| w15 | 10 | -0.005533 | 3.497 |
| w16 | 11 | 0.054086 | 9.527 |
| w17 | 7 | -0.024939 | -2.839 |
| w18 | 9 | 0.04907 | 4.06 |
| w19 | 7 | 0.032823 | 1.144 |
| w20 | 9 | 0.054986 | 1.626 |
| w21 | 10 | -0.001779 | -1.813 |
| w22 | 10 | 0.000494 | 6.775 |
| w23 | 7 | -0.098264 | -7.569 |
| w24 | 11 | -0.047265 | -0.163 |
| w25 | 5 | -0.017824 | -0.439 |
| w26 | 6 | 0.027364 | 2.361 |
| w27 | 12 | -0.07157 | -2.757 |
| w28 | 11 | -0.009233 | -1.98 |
| w29 | 10 | 0.032408 | 2.333 |
| w30 | 7 | 0.012475 | -1.969 |
| w31 | 8 | 0.020113 | 0.135 |
| w32 | 8 | 0.038543 | 2.588 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.083133 | 3.471 |
| w2 | 7 | -0.080739 | -8.147 |
| w3 | 11 | 0.012278 | 2.077 |
| w4 | 8 | 0.017573 | 0.857 |
| w5 | 12 | 0.039328 | 4.865 |
| w6 | 9 | 0.000923 | 4.481 |
| w7 | 6 | -0.029332 | -3.988 |
| w8 | 6 | 0.12947 | 6.37 |
| w9 | 6 | 0.096051 | 6.217 |
| w10 | 9 | 0.105314 | 9.786 |
| w11 | 6 | -0.015856 | -1.995 |
| w12 | 4 | -0.071046 | -5.278 |
| w13 | 11 | -0.012693 | -2.809 |
| w14 | 7 | 0.351703 | 35.759 |
| w15 | 10 | 0.087946 | 8.725 |
| w16 | 11 | 0.029472 | 3.448 |
| w17 | 8 | 0.002483 | 0.156 |
| w18 | 12 | 0.047559 | 3.527 |
| w19 | 7 | 0.128039 | 8.547 |
| w20 | 5 | 0.113592 | 8.172 |
| w21 | 9 | 0.056971 | 6.545 |
| w22 | 6 | -0.054411 | -4.582 |
| w23 | 9 | -0.051416 | -7.365 |
| w24 | 5 | -0.044449 | -3.428 |
| w25 | 5 | 0.102078 | 12.334 |
| w26 | 7 | 0.101994 | 7.761 |
| w27 | 11 | 0.055461 | 13.729 |
| w28 | 9 | -0.101549 | -9.492 |
| w29 | 9 | 0.143987 | 16.959 |
| w30 | 7 | -0.018658 | -3.716 |
| w31 | 7 | -0.02099 | -5.162 |
| w32 | 5 | 0.069746 | 3.886 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 10 | -0.066039 | -1.153 |
| w7 | 5 | 0.010346 | -2.815 |
| w8 | 6 | -0.048491 | -6.308 |
| w9 | 7 | 0.068372 | 6.797 |
| w10 | 6 | -0.01027 | -2.476 |
| w11 | 4 | -0.036424 | -2.488 |
| w12 | 4 | -0.047803 | -3.698 |
| w13 | 9 | -0.024031 | -4.97 |
| w14 | 6 | 0.32632 | 35.563 |
| w15 | 8 | 0.184626 | 50.138 |
| w16 | 9 | 0.11863 | 19.717 |
| w17 | 7 | 0.095725 | 9.743 |
| w18 | 11 | 0.087643 | 8.158 |
| w19 | 4 | 0.021023 | 0.405 |
| w20 | 4 | 0.153223 | 10.095 |
| w21 | 10 | -0.088555 | -8.255 |
| w22 | 8 | -0.033651 | -1.681 |
| w23 | 7 | -0.076621 | -11.749 |
| w24 | 11 | -0.04648 | -3.029 |
| w25 | 5 | 0.08555 | 7.447 |
| w26 | 5 | 0.196284 | 21.962 |
| w27 | 7 | 0.238495 | 36.674 |
| w28 | 10 | -0.000231 | -0.252 |
| w29 | 7 | 0.038847 | 3.501 |
| w30 | 5 | -0.035125 | -3.9 |
| w31 | 8 | -0.009903 | -4.767 |
| w32 | 5 | 0.040442 | 2.766 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | -0.013122 | -1.668 |
| w8 | 6 | 0.274126 | 14.182 |
| w9 | 5 | 0.024179 | -0.937 |
| w10 | 7 | 0.070997 | 6.928 |
| w11 | 4 | 0.017034 | 0.829 |
| w12 | 3 | 0.008379 | -2.069 |
| w13 | 9 | -0.032961 | -5.065 |
| w14 | 8 | 0.264067 | 21.939 |
| w15 | 8 | 0.004933 | -0.736 |
| w16 | 9 | 0.146181 | 12.867 |
| w17 | 7 | 0.038052 | 2.557 |
| w18 | 11 | 0.089795 | 4.251 |
| w19 | 7 | 0.100267 | 5.676 |
| w20 | 5 | 0.030628 | 0.098 |
| w21 | 9 | 0.007904 | -1.236 |
| w22 | 6 | 0.039245 | 2.258 |
| w23 | 8 | -0.00199 | -9.028 |
| w24 | 6 | 0.001728 | -0.525 |
| w25 | 7 | 0.323129 | 57.506 |
| w26 | 6 | 0.021554 | -1.481 |
| w27 | 8 | 0.099684 | 10.018 |
| w28 | 11 | 0.013065 | -3.435 |
| w29 | 8 | -0.087182 | -9.825 |
| w30 | 6 | -0.085314 | -10.736 |
| w31 | 6 | -0.018599 | -6.695 |
| w32 | 5 | -0.009266 | -4.158 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 8 | 0.041221 | 8.937 |
| w2 | 11 | -0.200133 | -20.105 |
| w3 | 6 | -0.069922 | -5.174 |
| w4 | 12 | -0.191679 | -12.27 |
| w5 | 10 | 0.048724 | 8.546 |
| w6 | 9 | -0.043968 | 0.543 |
| w7 | 7 | 0.047071 | 4.204 |
| w8 | 7 | 0.071013 | 1.435 |
| w9 | 6 | 0.139948 | 12.371 |
| w10 | 5 | 0.016253 | 1.496 |
| w11 | 5 | -0.068074 | -4.624 |
| w12 | 3 | -0.048054 | -4.727 |
| w13 | 9 | 0.032383 | 3.365 |
| w14 | 8 | 0.3204 | 36.966 |
| w15 | 8 | -0.025185 | -1.589 |
| w16 | 10 | -0.12104 | -9.347 |
| w17 | 9 | 0.101754 | 12.694 |
| w18 | 13 | 0.065144 | 7.065 |
| w19 | 7 | 0.048509 | 2.512 |
| w20 | 6 | 0.097591 | 6.852 |
| w21 | 8 | 0.011783 | 0.808 |
| w22 | 10 | 0.021271 | 7.571 |
| w23 | 6 | -0.174316 | -11.398 |
| w24 | 11 | -0.057424 | -3.875 |
| w25 | 6 | 0.01694 | 2.845 |
| w26 | 5 | 0.032461 | 1.54 |
| w27 | 6 | 0.136126 | 13.321 |
| w28 | 8 | 0.006587 | -4.174 |
| w29 | 11 | 0.080536 | 13.55 |
| w30 | 6 | 0.010101 | -0.751 |
| w31 | 8 | 0.054382 | 3.346 |
| w32 | 7 | -0.029589 | -2.178 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | 0.147288 | 16.165 |
| w11 | 3 | -0.082101 | -5.133 |
| w12 | 3 | -0.007896 | -2.004 |
| w13 | 10 | -0.022104 | -5.125 |
| w14 | 11 | 0.296769 | 32.379 |
| w15 | 6 | -0.059269 | -5.032 |
| w16 | 9 | 0.064265 | 10.455 |
| w17 | 10 | 0.012578 | 7.311 |
| w18 | 7 | -0.008864 | -6.525 |
| w19 | 6 | 0.131126 | 8.344 |
| w20 | 9 | 0.014737 | 0.251 |
| w21 | 6 | 0.098314 | 4.977 |
| w22 | 9 | -0.043802 | -2.911 |
| w23 | 7 | -0.04066 | -5.198 |
| w24 | 12 | 0.046044 | 10.806 |
| w25 | 4 | 0.085224 | 6.012 |
| w26 | 6 | 0.057351 | 3.304 |
| w27 | 7 | 0.055189 | 12.472 |
| w28 | 8 | -0.038656 | -6.086 |
| w29 | 8 | 0.067822 | 6.073 |
| w30 | 6 | -0.007645 | -4.069 |
| w31 | 7 | -0.045233 | -6.221 |
| w32 | 6 | 0.097155 | 5.861 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 7 | 0.005974 | 1.924 |
| w13 | 11 | -0.042825 | -10.867 |
| w14 | 11 | 0.127247 | 19.615 |
| w15 | 4 | 0.004264 | -0.528 |
| w16 | 7 | -0.053248 | -2.284 |
| w17 | 10 | 0.108357 | 15.806 |
| w18 | 10 | -0.016932 | -1.034 |
| w19 | 7 | 0.070637 | 2.321 |
| w20 | 7 | -0.030646 | -6.505 |
| w21 | 8 | -0.010934 | -3.404 |
| w22 | 10 | -0.058378 | -5.675 |
| w23 | 3 | -0.030394 | -4.58 |
| w24 | 9 | 0.143616 | 15.153 |
| w25 | 8 | 0.048663 | 1.105 |
| w26 | 7 | 0.017098 | -4.045 |
| w27 | 6 | -0.002033 | 0.742 |
| w28 | 12 | -0.017484 | -5.448 |
| w29 | 8 | 0.120247 | 9.268 |
| w30 | 8 | -0.02208 | -7.212 |
| w31 | 6 | 0.030978 | -1.152 |
| w32 | 5 | -0.052945 | -8.392 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 8 | 0.03015 | 0.544 |
| w16 | 8 | 0.030464 | 6.279 |
| w17 | 8 | -0.009556 | -1.77 |
| w18 | 11 | -0.032359 | -3.923 |
| w19 | 5 | 0.073142 | 1.38 |
| w20 | 6 | 0.113538 | 7.407 |
| w21 | 6 | -0.028061 | -3.925 |
| w22 | 7 | 0.011558 | -0.792 |
| w23 | 4 | -0.010973 | -3.505 |
| w24 | 9 | 0.0287 | 5.179 |
| w25 | 8 | -0.063318 | -9.089 |
| w26 | 5 | 0.074557 | 3.296 |
| w27 | 6 | -0.018195 | 0.55 |
| w28 | 10 | -0.010616 | -3.289 |
| w29 | 6 | 0.059933 | 4.37 |
| w30 | 6 | 0.042305 | -0.93 |
| w31 | 6 | -0.065722 | -7.378 |
| w32 | 6 | -0.10505 | -9.07 |

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
| w15 | 8 | -0.133214 | -5.636 |
| w16 | 8 | 0.025689 | 7.465 |
| w17 | 10 | 0.046621 | 6.302 |
| w18 | 11 | 0.016356 | 0.456 |
| w19 | 10 | 0.095656 | 7.861 |
| w20 | 9 | 0.016088 | 0.442 |
| w21 | 8 | 0.056206 | 1.141 |
| w22 | 5 | 0.06024 | 4.848 |
| w23 | 9 | -0.000296 | -0.4 |
| w24 | 14 | 0.04103 | 6.415 |
| w25 | 8 | 0.108486 | 9.368 |
| w26 | 9 | 0.038392 | 6.351 |
| w27 | 10 | -0.016549 | 7.363 |
| w28 | 10 | 0.011474 | 2.813 |
| w29 | 14 | -0.008704 | -0.536 |
| w30 | 7 | 0.01366 | -2.396 |
| w31 | 11 | 0.221785 | 18.01 |
| w32 | 10 | 0.047724 | 0.9 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 11 | 0.249126 | 23.601 |
| w17 | 10 | -0.033817 | -4.364 |
| w18 | 9 | -0.000747 | -1.662 |
| w19 | 5 | 0.089188 | 4.195 |
| w20 | 5 | 0.066762 | 2.645 |
| w21 | 6 | 0.021525 | -1.301 |
| w22 | 8 | 0.077886 | 11.244 |
| w23 | 6 | -0.062724 | -6.121 |
| w24 | 9 | 0.131734 | 17.914 |
| w25 | 8 | -0.017676 | -6.404 |
| w26 | 6 | -0.032117 | -6.518 |
| w27 | 6 | 0.0106 | 4.915 |
| w28 | 10 | -0.087934 | -10.124 |
| w29 | 8 | 0.17731 | 18.273 |
| w30 | 6 | 0.027223 | -1.604 |
| w31 | 7 | -0.019827 | -4.142 |
| w32 | 6 | 0.011469 | -3.478 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.102818 | 6.344 |
| w21 | 6 | -0.011278 | -2.967 |
| w22 | 9 | -0.011596 | 0.842 |
| w23 | 4 | -0.062441 | -5.18 |
| w24 | 11 | 0.00374 | 5.437 |
| w25 | 6 | -0.02855 | -3.156 |
| w26 | 5 | 0.024669 | 0.158 |
| w27 | 7 | -0.04804 | -1.563 |
| w28 | 8 | 0.063876 | 2.96 |
| w29 | 8 | 0.152955 | 14.609 |
| w30 | 6 | 0.00374 | -2.015 |
| w31 | 8 | 0.048831 | 0.978 |
| w32 | 6 | -0.030747 | -3.571 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.132761 | 15.46 |
| w23 | 4 | 0.027826 | 0.326 |
| w24 | 11 | 0.092462 | 12.925 |
| w25 | 7 | 0.023013 | 2.022 |
| w26 | 7 | 0.033201 | 1.293 |
| w27 | 7 | 0.081258 | 8.631 |
| w28 | 9 | -0.024771 | -6.938 |
| w29 | 8 | 0.162252 | 16.854 |
| w30 | 6 | 0.067461 | 3.701 |
| w31 | 7 | 0.107855 | 7.152 |
| w32 | 7 | 0.052508 | 4.547 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 10 | 0.115892 | 16.847 |
| w25 | 8 | 0.030784 | 3.995 |
| w26 | 4 | 0.097908 | 8.25 |
| w27 | 10 | 0.034716 | 8.792 |
| w28 | 9 | -0.03497 | -4.43 |
| w29 | 9 | 0.077029 | 5.646 |
| w30 | 6 | 0.056243 | 2.844 |
| w31 | 7 | -0.004229 | -3.468 |
| w32 | 7 | 0.028186 | 1.157 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 9 | 0.051029 | 10.736 |
| w6 | 9 | -0.017207 | 0.833 |
| w7 | 6 | 0.000459 | -2.892 |
| w8 | 6 | 0.084158 | 5.201 |
| w9 | 7 | 0.023613 | -2.808 |
| w10 | 8 | 0.048552 | 5.574 |
| w11 | 5 | -0.043558 | -5.773 |
| w12 | 5 | -0.020447 | -4.686 |
| w13 | 10 | -0.09783 | -10.535 |
| w14 | 7 | 0.08718 | 8.83 |
| w15 | 6 | -0.073763 | -8.629 |
| w16 | 10 | 0.221803 | 30.972 |
| w17 | 10 | 0.013171 | 0.468 |
| w18 | 11 | 0.075012 | 10.577 |
| w19 | 9 | 0.085922 | 7.875 |
| w20 | 9 | 0.077283 | 3.752 |
| w21 | 4 | -0.013885 | -1.945 |
| w22 | 9 | 0.027804 | 2.042 |
| w23 | 4 | -0.048699 | -3.16 |
| w24 | 9 | 0.106369 | 10.221 |
| w25 | 7 | 0.117837 | 8.58 |
| w26 | 9 | -0.023411 | -3.826 |
| w27 | 8 | 0.006738 | 0.56 |
| w28 | 9 | -0.051929 | -6.375 |
| w29 | 9 | 0.082305 | 9.239 |
| w30 | 8 | 0.140093 | 15.981 |
| w31 | 5 | 0.025228 | 1.001 |
| w32 | 7 | 0.075131 | 9.944 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | 0.046827 | 14.582 |
| w6 | 11 | 0.073732 | 13.19 |
| w7 | 6 | 0.035926 | 1.125 |
| w8 | 6 | 0.040119 | 0.37 |
| w9 | 6 | 0.046187 | 1.33 |
| w10 | 9 | -0.013949 | 0.092 |
| w11 | 6 | 0.071994 | 6.197 |
| w12 | 5 | -0.023919 | -4.783 |
| w13 | 9 | -0.021697 | -4.681 |
| w14 | 10 | 0.186369 | 27.26 |
| w15 | 10 | 0.122304 | 11.354 |
| w16 | 9 | 0.097291 | 14.76 |
| w17 | 7 | 0.007772 | 1.624 |
| w18 | 10 | 0.017722 | -1.48 |
| w19 | 8 | 0.094555 | 4.488 |
| w20 | 8 | -0.044219 | -4.773 |
| w21 | 11 | 0.022293 | -0.126 |
| w22 | 6 | 0.032625 | 2.385 |
| w23 | 6 | -0.04153 | -4.989 |
| w24 | 8 | -0.019425 | -3.669 |
| w25 | 6 | 0.077922 | 7.456 |
| w26 | 10 | 0.040076 | 2.053 |
| w27 | 11 | 0.010529 | -0.855 |
| w28 | 10 | -0.108018 | -5.441 |
| w29 | 5 | 0.067202 | 4.847 |
| w30 | 9 | 0.053871 | 7.182 |
| w31 | 9 | -0.026703 | -2.995 |
| w32 | 9 | -0.073774 | -5.808 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | -0.065498 | -8.896 |
| w18 | 9 | 0.045346 | 8.138 |
| w19 | 7 | 0.091748 | 4.097 |
| w20 | 8 | -0.021594 | -3.886 |
| w21 | 5 | 0.011993 | -1.536 |
| w22 | 10 | -0.010435 | -0.272 |
| w23 | 5 | -0.044867 | -7.85 |
| w24 | 8 | -0.036642 | -3.531 |
| w25 | 6 | 0.015135 | -1.676 |
| w26 | 8 | -0.050591 | -6.911 |
| w27 | 8 | -0.073163 | -4.365 |
| w28 | 13 | -0.058835 | -6.604 |
| w29 | 8 | -0.01864 | -3.35 |
| w30 | 9 | 0.031472 | -0.029 |
| w31 | 5 | 0.011221 | -3.625 |
| w32 | 8 | -0.006198 | -0.948 |

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
| w17 | 7 | -0.066941 | -6.86 |
| w18 | 10 | 0.026427 | 0.329 |
| w19 | 7 | 0.003748 | -1.065 |
| w20 | 8 | 0.086089 | 6.62 |
| w21 | 7 | 0.008831 | -1.079 |
| w22 | 11 | -0.039572 | -2.12 |
| w23 | 7 | -0.06453 | -7.437 |
| w24 | 10 | -0.029504 | 2.84 |
| w25 | 6 | 0.042853 | 2.206 |
| w26 | 9 | -0.113612 | -10.339 |
| w27 | 6 | 0.04076 | 7.073 |
| w28 | 8 | -0.005652 | -1.951 |
| w29 | 11 | 0.109192 | 12.597 |
| w30 | 6 | 0.032293 | -0.782 |
| w31 | 5 | -0.092889 | -11.274 |
| w32 | 6 | 0.02346 | 2.353 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 5 | 0.0368 | 0.465 |
| w20 | 9 | 0.00933 | -4.952 |
| w21 | 6 | -0.008029 | -0.708 |
| w22 | 10 | 0.008829 | 8.471 |
| w23 | 6 | 0.091875 | 4.622 |
| w24 | 12 | -0.044358 | 3.982 |
| w25 | 6 | -0.067657 | -8.559 |
| w26 | 6 | 0.027569 | -0.007 |
| w27 | 7 | 0.032062 | 2.738 |
| w28 | 8 | 0.015837 | -2.942 |
| w29 | 9 | 0.106923 | 12.282 |
| w30 | 5 | -0.024485 | -6.554 |
| w31 | 6 | 0.050916 | 0.506 |
| w32 | 7 | -0.073784 | -9.174 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.049725 | -3.725 |
| w23 | 6 | -0.079694 | -5.491 |
| w24 | 11 | -0.095897 | -6.717 |
| w25 | 7 | -0.078633 | -8.314 |
| w26 | 5 | -0.036751 | -4.745 |
| w27 | 7 | -0.023826 | -1.223 |
| w28 | 7 | -0.101202 | -10.407 |
| w29 | 8 | 0.209767 | 24.154 |
| w30 | 4 | 0.005629 | -1.4 |
| w31 | 8 | -0.075066 | -12.391 |
| w32 | 9 | -0.015188 | -3.383 |

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
| w27 | 8 | -0.04084 | -0.889 |
| w28 | 10 | -0.083865 | -10.788 |
| w29 | 8 | 0.125165 | 10.902 |
| w30 | 6 | -0.009261 | -5.271 |
| w31 | 7 | -0.015983 | -6.409 |
| w32 | 8 | -0.15817 | -18.309 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.084386 | 6.31 |
| w18 | 7 | 0.25009 | 29.185 |
| w19 | 4 | 0.126645 | 6.917 |
| w20 | 4 | 0.282778 | 32.123 |
| w21 | 6 | 0.033002 | 0.256 |
| w22 | 7 | 0.008329 | 4.589 |
| w23 | 7 | -0.028712 | -6.201 |
| w24 | 9 | 0.128725 | 16.564 |
| w25 | 5 | 0.068729 | 4.893 |
| w26 | 6 | 0.043216 | 0.369 |
| w27 | 7 | 0.097949 | 10.923 |
| w28 | 9 | -0.045147 | -6.622 |
| w29 | 9 | 0.076362 | 4.273 |
| w30 | 5 | -0.066237 | -6.866 |
| w31 | 7 | -0.041103 | -6.205 |
| w32 | 6 | -0.146157 | -17.643 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | -0.034223 | -5.579 |
| w18 | 9 | 0.116962 | 9.743 |
| w19 | 8 | 0.085221 | 3.599 |
| w20 | 5 | 0.08511 | 4.959 |
| w21 | 6 | 0.029279 | 0.272 |
| w22 | 11 | 0.075582 | 17.184 |
| w23 | 5 | -0.020155 | -3.355 |
| w24 | 8 | -0.05539 | -2.552 |
| w25 | 6 | 0.285659 | 32.729 |
| w26 | 6 | 0.048532 | 1.832 |
| w27 | 7 | 0.004802 | 1.528 |
| w28 | 8 | -0.052594 | -7.822 |
| w29 | 8 | 0.129207 | 11.461 |
| w30 | 5 | 0.032705 | -1.839 |
| w31 | 7 | -0.061889 | -8.08 |
| w32 | 3 | -0.138582 | -11.545 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 8 | -0.017276 | -4.036 |
| w29 | 8 | 0.11072 | 7.463 |
| w30 | 8 | 0.017169 | -0.675 |
| w31 | 6 | 0.078593 | 7.774 |
| w32 | 6 | -0.000351 | -4.389 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 7 | 0.102139 | 7.124 |
| w15 | 7 | -0.041606 | -7.763 |
| w16 | 8 | -0.061571 | 3.477 |
| w17 | 6 | -0.020425 | 0.066 |
| w18 | 8 | 0.004169 | -1.72 |
| w19 | 5 | 0.071865 | 6.661 |
| w20 | 8 | 0.013994 | -0.693 |
| w21 | 7 | 0.316077 | 44.362 |
| w22 | 7 | 0.106697 | 9.144 |
| w23 | 8 | -0.05641 | -11.894 |
| w24 | 10 | -0.080767 | -7.11 |
| w25 | 6 | -0.034398 | -3.466 |
| w26 | 4 | 0.001995 | -0.502 |
| w27 | 7 | 0.13281 | 21.99 |
| w28 | 8 | -0.013158 | -4.597 |
| w29 | 8 | 0.195457 | 22.246 |
| w30 | 5 | 0.030777 | 0.265 |
| w31 | 7 | -0.035974 | -6.148 |
| w32 | 8 | -0.040502 | -6.716 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | -0.02031 | 1.237 |
| w26 | 8 | 0.020543 | 0.698 |
| w27 | 6 | 0.007931 | 3.986 |
| w28 | 9 | -0.077218 | -11.612 |
| w29 | 7 | 0.099882 | 8.521 |
| w30 | 5 | 0.024964 | -1.874 |
| w31 | 7 | -0.030132 | -5.071 |
| w32 | 4 | -0.040518 | -4.55 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

