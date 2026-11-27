# Backtest of 025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d

- Plan: `../../../../../03_test_plan/night4_fallingbounce_run/plans/025-03_bounce-falling-versus-rising-regime.d2_sharp-rises-follow-monthly-trend_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.015981 | 8.33 |
| w2 | 5 | 0.125963 | 16.432 |
| w3 | 16 | 0.05634 | 36.662 |
| w4 | 7 | -0.177462 | -36.676 |
| w5 | 4 | 0.065133 | 13.308 |
| w6 | 8 | 0.169454 | 22.045 |
| w7 | 2 | 0.005138 | 0.063 |
| w8 | 5 | -0.030039 | -0.77 |
| w9 | 5 | 0.008681 | 3.261 |
| w10 | 8 | 0.019268 | 13.688 |
| w11 | 10 | -0.122456 | 0.379 |
| w12 | 2 | 0.082504 | -0.255 |
| w13 | 4 | -0.013292 | 0.467 |
| w14 | 5 | -0.131477 | -0.803 |
| w15 | 10 | -0.073956 | 0.549 |
| w16 | 6 | 0.113 | 4.865 |
| w17 | 4 | 0.005253 | -12.265 |
| w18 | 3 | -0.040249 | 1.791 |
| w19 | 2 | 0.082653 | -3.525 |
| w20 | 7 | 0.208075 | 32.919 |
| w21 | 9 | 0.051065 | -15.033 |
| w22 | 12 | 0.180409 | 51.219 |
| w23 | 8 | -0.004214 | 1.724 |
| w24 | 7 | -0.129611 | 8.298 |
| w25 | 11 | 0.025247 | 27.435 |
| w26 | 6 | -0.098393 | -0.22 |
| w27 | 3 | -0.006221 | 41.461 |
| w28 | 5 | 0.146406 | 6.285 |
| w29 | 6 | 0.003454 | 0.612 |
| w30 | 3 | 0.012494 | 11.043 |
| w31 | 7 | 0.08319 | 1.627 |
| w32 | 5 | 0.213458 | 18.946 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.027498 | 20.413 |
| w2 | 4 | 0.101152 | -14.323 |
| w3 | 1 | -0.113239 | -0.875 |
| w4 | 6 | -0.14199 | -13.39 |
| w5 | 9 | 0.024477 | 26.653 |
| w6 | 12 | 0.156638 | 79.245 |
| w7 | 2 | 0.160711 | 4.692 |
| w8 | 2 | 0.115499 | 4.497 |
| w9 | 4 | -0.02187 | 0.076 |
| w10 | 7 | 0.148188 | 11.636 |
| w11 | 10 | -0.095938 | 2.048 |
| w12 | 2 | 0.058729 | 0.237 |
| w13 | 9 | 0.023073 | 8.322 |
| w14 | 7 | 0.038884 | 31.035 |
| w15 | 6 | 0.039127 | 44.554 |
| w16 | 7 | -0.094341 | 12.233 |
| w17 | 10 | -0.012367 | -1.505 |
| w18 | 5 | 0.068496 | -6.818 |
| w19 | 0 | 0.036411 | 0.0 |
| w20 | 5 | 0.183125 | 17.617 |
| w21 | 6 | 0.072112 | -20.447 |
| w22 | 4 | -0.124596 | -5.634 |
| w23 | 2 | -0.023549 | -2.696 |
| w24 | 5 | -0.206351 | -17.611 |
| w25 | 4 | 0.018176 | -23.474 |
| w26 | 3 | 0.007338 | -1.969 |
| w27 | 8 | 0.008504 | 49.782 |
| w28 | 4 | 0.018858 | 3.581 |
| w29 | 11 | -0.013047 | -1.595 |
| w30 | 5 | 0.012779 | 16.446 |
| w31 | 1 | 0.053034 | 2.33 |
| w32 | 8 | -0.11287 | -9.306 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 12 | 0.151693 | 55.277 |
| w7 | 4 | 0.062294 | -0.531 |
| w8 | 3 | 0.07387 | 4.752 |
| w9 | 10 | 0.078309 | -13.904 |
| w10 | 6 | -0.07297 | -0.281 |
| w11 | 4 | 0.248451 | -4.706 |
| w12 | 5 | -0.08701 | -8.363 |
| w13 | 6 | 0.136992 | -6.866 |
| w14 | 6 | 0.132448 | 23.316 |
| w15 | 6 | 0.265559 | 186.823 |
| w16 | 8 | 0.098021 | 41.471 |
| w17 | 10 | 0.041299 | 21.372 |
| w18 | 1 | -0.002564 | 0.958 |
| w19 | 2 | 0.108292 | -0.138 |
| w20 | 0 | None | 0.0 |
| w21 | 10 | 0.04995 | -7.169 |
| w22 | 7 | -0.202404 | -5.363 |
| w23 | 3 | -0.113192 | 0.971 |
| w24 | 5 | 0.0847 | -3.529 |
| w25 | 7 | -0.130993 | -8.41 |
| w26 | 6 | 0.153068 | 0.663 |
| w27 | 9 | 0.197683 | 125.562 |
| w28 | 2 | 0.044025 | -0.091 |
| w29 | 11 | 0.037873 | 20.824 |
| w30 | 0 | None | 0.0 |
| w31 | 8 | -0.020866 | -3.07 |
| w32 | 9 | 0.012022 | -7.078 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 9 | -0.081288 | -8.507 |
| w8 | 4 | 0.058285 | 5.098 |
| w9 | 12 | -0.325694 | -38.732 |
| w10 | 8 | 0.129612 | 16.618 |
| w11 | 7 | -0.007077 | -1.358 |
| w12 | 6 | -0.056798 | -12.269 |
| w13 | 7 | -0.045889 | 18.956 |
| w14 | 5 | 0.102195 | 36.227 |
| w15 | 6 | -0.052157 | -12.027 |
| w16 | 9 | -0.061062 | -10.954 |
| w17 | 8 | 0.060694 | -2.133 |
| w18 | 1 | -0.151013 | -4.521 |
| w19 | 6 | -0.119911 | -10.86 |
| w20 | 2 | 0.075851 | 13.582 |
| w21 | 3 | -0.021399 | -6.599 |
| w22 | 7 | 0.027992 | -9.044 |
| w23 | 6 | 0.218751 | 43.101 |
| w24 | 10 | -0.050914 | -3.448 |
| w25 | 5 | -0.046777 | 1.101 |
| w26 | 6 | 0.096671 | -3.564 |
| w27 | 6 | -0.06082 | 32.23 |
| w28 | 4 | 0.07334 | -3.423 |
| w29 | 10 | -0.188093 | -10.46 |
| w30 | 12 | -0.001628 | 2.702 |
| w31 | 3 | -0.053137 | -2.186 |
| w32 | 5 | -0.044216 | -7.703 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 10 | -0.115214 | 32.538 |
| w2 | 6 | -0.06549 | -11.028 |
| w3 | 6 | 0.027066 | -4.425 |
| w4 | 13 | 0.097317 | 93.012 |
| w5 | 10 | 0.001369 | 17.837 |
| w6 | 8 | 0.318222 | 43.139 |
| w7 | 6 | 0.026044 | 4.645 |
| w8 | 3 | 0.108428 | 9.026 |
| w9 | 10 | -0.072254 | -13.063 |
| w10 | 7 | 0.004885 | 7.923 |
| w11 | 7 | 0.245548 | 30.319 |
| w12 | 5 | 0.083086 | 4.35 |
| w13 | 8 | 0.102772 | 20.218 |
| w14 | 9 | -0.020669 | 18.103 |
| w15 | 6 | 0.035408 | -1.128 |
| w16 | 4 | -0.05154 | 5.951 |
| w17 | 13 | -0.06148 | 8.337 |
| w18 | 6 | -0.002542 | 8.607 |
| w19 | 7 | 0.010127 | -10.389 |
| w20 | 4 | -0.038057 | 0.532 |
| w21 | 6 | 0.040584 | -17.31 |
| w22 | 9 | 0.031201 | 22.5 |
| w23 | 4 | -0.136477 | -6.902 |
| w24 | 9 | -0.114002 | -21.22 |
| w25 | 6 | 0.046763 | 19.07 |
| w26 | 4 | 0.118724 | 1.078 |
| w27 | 7 | 0.006701 | 23.763 |
| w28 | 4 | 0.344805 | 11.293 |
| w29 | 6 | 0.128973 | 27.015 |
| w30 | 2 | -0.06507 | 2.636 |
| w31 | 9 | -0.030978 | 3.041 |
| w32 | 8 | 0.037134 | 5.766 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | 0.09862 | 17.221 |
| w11 | 2 | -0.08282 | 3.22 |
| w12 | 5 | 0.074764 | 0.567 |
| w13 | 9 | 0.03227 | 11.97 |
| w14 | 9 | 0.017262 | 15.876 |
| w15 | 11 | 0.101219 | 8.132 |
| w16 | 9 | -0.004901 | 44.679 |
| w17 | 9 | 0.063188 | 32.257 |
| w18 | 4 | 0.063512 | 16.734 |
| w19 | 7 | -0.085549 | -6.857 |
| w20 | 5 | 0.110915 | 13.951 |
| w21 | 2 | -0.00893 | -0.562 |
| w22 | 11 | -0.008197 | -2.279 |
| w23 | 2 | -0.163123 | -5.353 |
| w24 | 7 | -0.007258 | 67.72 |
| w25 | 2 | 0.076969 | 2.047 |
| w26 | 0 | -0.028537 | 0.0 |
| w27 | 7 | 0.305122 | 67.845 |
| w28 | 5 | -0.082553 | -1.53 |
| w29 | 12 | -0.005676 | 23.931 |
| w30 | 2 | -0.095564 | 1.466 |
| w31 | 6 | 0.026129 | 2.434 |
| w32 | 14 | -0.049345 | -17.913 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 6 | -0.103714 | 2.984 |
| w13 | 10 | 0.027602 | -13.725 |
| w14 | 9 | 0.139231 | 17.61 |
| w15 | 7 | -0.095677 | -15.87 |
| w16 | 7 | 0.060797 | 12.028 |
| w17 | 9 | 0.047069 | 19.792 |
| w18 | 7 | 0.120551 | 15.313 |
| w19 | 7 | -0.071617 | -2.345 |
| w20 | 7 | 0.13935 | 16.886 |
| w21 | 3 | 0.021736 | -17.514 |
| w22 | 10 | 0.010103 | 6.071 |
| w23 | 3 | -0.039616 | 5.607 |
| w24 | 5 | -0.071913 | -1.815 |
| w25 | 6 | -0.025499 | 4.507 |
| w26 | 3 | -0.066807 | 6.43 |
| w27 | 4 | 0.038624 | 28.755 |
| w28 | 3 | 0.303868 | 1.969 |
| w29 | 5 | 0.177176 | 8.148 |
| w30 | 2 | 0.054975 | 2.083 |
| w31 | 7 | -0.057122 | -2.154 |
| w32 | 5 | 0.024234 | -6.775 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 3 | 0.131017 | 0.393 |
| w16 | 8 | 0.1213 | 15.023 |
| w17 | 4 | 0.079546 | -2.517 |
| w18 | 5 | 0.207241 | 4.436 |
| w19 | 4 | -0.031655 | 7.817 |
| w20 | 0 | None | 0.0 |
| w21 | 8 | 0.075749 | -32.234 |
| w22 | 11 | -0.018088 | -11.449 |
| w23 | 1 | -0.174006 | -0.836 |
| w24 | 12 | -0.023311 | 15.46 |
| w25 | 8 | 0.277207 | 23.46 |
| w26 | 1 | 0.043773 | 0.277 |
| w27 | 7 | 0.132241 | 100.746 |
| w28 | 3 | 0.256881 | 5.659 |
| w29 | 6 | 0.09563 | 18.444 |
| w30 | 4 | -0.094431 | 9.771 |
| w31 | 7 | 0.031126 | 2.602 |
| w32 | 10 | 0.042479 | -2.666 |

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
| w15 | 7 | -0.160715 | -5.757 |
| w16 | 13 | -0.032928 | 43.687 |
| w17 | 2 | 0.015041 | 5.575 |
| w18 | 3 | -0.073619 | -2.455 |
| w19 | 2 | 0.052763 | 3.121 |
| w20 | 6 | -0.128442 | -3.293 |
| w21 | 3 | -0.033708 | -7.804 |
| w22 | 5 | -0.051874 | 4.663 |
| w23 | 10 | 0.084301 | -7.907 |
| w24 | 9 | -0.060716 | -9.953 |
| w25 | 6 | -0.09805 | -3.71 |
| w26 | 9 | -0.070665 | 21.876 |
| w27 | 8 | -0.145007 | 1.461 |
| w28 | 5 | -0.044917 | -2.471 |
| w29 | 6 | -0.128105 | -9.944 |
| w30 | 0 | -0.010474 | 0.0 |
| w31 | 12 | -0.164077 | -4.182 |
| w32 | 7 | 0.044566 | -8.426 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 2 | 0.092163 | 20.141 |
| w17 | 12 | 0.013961 | 4.836 |
| w18 | 4 | 0.046233 | 1.75 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | 0.138033 | 26.688 |
| w21 | 4 | 0.007261 | -9.614 |
| w22 | 5 | -0.048292 | -1.324 |
| w23 | 2 | -0.05533 | -7.645 |
| w24 | 9 | -0.139617 | 1.923 |
| w25 | 4 | 0.150597 | 28.197 |
| w26 | 7 | 0.098974 | -0.026 |
| w27 | 5 | 0.147279 | 6.136 |
| w28 | 3 | 0.303397 | 4.533 |
| w29 | 7 | 0.049154 | 9.523 |
| w30 | 5 | -0.065894 | 7.956 |
| w31 | 8 | -0.027691 | -1.043 |
| w32 | 6 | -0.120292 | -6.076 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 3 | 0.132326 | 28.57 |
| w21 | 3 | 0.008582 | -1.482 |
| w22 | 8 | -0.039362 | -14.152 |
| w23 | 3 | 0.164683 | 8.383 |
| w24 | 9 | 0.104217 | 92.33 |
| w25 | 3 | 0.107592 | 6.061 |
| w26 | 6 | 0.001293 | -7.432 |
| w27 | 4 | -0.132368 | -1.444 |
| w28 | 3 | 0.243902 | 9.302 |
| w29 | 6 | 0.007788 | 5.724 |
| w30 | 5 | -0.048307 | -1.369 |
| w31 | 3 | 0.017421 | 0.862 |
| w32 | 8 | 0.065825 | -2.502 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 13 | -0.101109 | 4.325 |
| w23 | 3 | 0.074687 | 1.587 |
| w24 | 6 | 0.008478 | 53.222 |
| w25 | 4 | -0.111053 | 42.405 |
| w26 | 3 | -0.00289 | 0.724 |
| w27 | 3 | -0.032367 | -11.824 |
| w28 | 0 | -0.086462 | 0.0 |
| w29 | 4 | -0.030664 | 2.405 |
| w30 | 6 | -0.05099 | -5.525 |
| w31 | 7 | -0.013941 | -7.559 |
| w32 | 8 | -0.064545 | 12.569 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 11 | 0.003027 | 17.375 |
| w25 | 8 | 0.055371 | 6.57 |
| w26 | 7 | -0.040448 | -9.091 |
| w27 | 15 | 0.056439 | 29.502 |
| w28 | 7 | 0.296352 | 12.638 |
| w29 | 5 | 0.027143 | -0.202 |
| w30 | 4 | -0.083801 | 1.472 |
| w31 | 7 | 0.011908 | 7.781 |
| w32 | 6 | 0.295937 | 13.329 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 8 | 0.35785 | 46.456 |
| w6 | 6 | -0.022516 | 30.532 |
| w7 | 6 | 0.109328 | -6.007 |
| w8 | 4 | 0.141057 | 1.59 |
| w9 | 4 | 0.048854 | 0.778 |
| w10 | 4 | 0.121273 | 7.681 |
| w11 | 6 | 0.025222 | 15.807 |
| w12 | 2 | 0.070873 | 0.411 |
| w13 | 8 | 0.063427 | 34.733 |
| w14 | 10 | -0.112472 | 16.155 |
| w15 | 6 | 0.055512 | -5.307 |
| w16 | 6 | -0.14548 | 14.333 |
| w17 | 6 | 0.019886 | -2.622 |
| w18 | 4 | -0.172379 | 1.999 |
| w19 | 6 | 0.001957 | 0.822 |
| w20 | 2 | 0.059367 | -0.75 |
| w21 | 3 | -0.082525 | 6.195 |
| w22 | 5 | -0.071852 | -13.608 |
| w23 | 5 | -0.016738 | 16.972 |
| w24 | 4 | -0.097995 | -8.228 |
| w25 | 5 | -0.165149 | -0.552 |
| w26 | 13 | 0.180163 | -1.288 |
| w27 | 7 | -0.022152 | 3.889 |
| w28 | 2 | 0.185603 | -0.179 |
| w29 | 8 | -0.120238 | -0.266 |
| w30 | 10 | 0.07232 | 112.291 |
| w31 | 6 | 0.030168 | 12.764 |
| w32 | 9 | 0.078125 | 2.365 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 10 | 0.02509 | 92.444 |
| w6 | 12 | -0.185516 | -11.773 |
| w7 | 8 | -0.047532 | -0.463 |
| w8 | 2 | -0.064369 | -3.103 |
| w9 | 6 | 0.074976 | -6.227 |
| w10 | 5 | 0.209835 | 32.9 |
| w11 | 5 | -0.183523 | -0.892 |
| w12 | 4 | 0.033337 | 4.624 |
| w13 | 5 | -0.060349 | 5.855 |
| w14 | 6 | -0.235615 | 3.539 |
| w15 | 5 | -0.066657 | -2.465 |
| w16 | 7 | -0.162505 | -10.276 |
| w17 | 5 | 0.065053 | 3.778 |
| w18 | 5 | -0.0062 | -5.363 |
| w19 | 12 | -0.093962 | -15.728 |
| w20 | 4 | 0.019972 | 2.531 |
| w21 | 3 | 0.023982 | -32.059 |
| w22 | 4 | -0.057634 | 2.669 |
| w23 | 2 | 0.046498 | 2.839 |
| w24 | 4 | -0.099242 | -0.449 |
| w25 | 4 | 0.055137 | 4.778 |
| w26 | 3 | 0.077059 | 23.013 |
| w27 | 9 | -0.194071 | 3.436 |
| w28 | 3 | 0.142516 | 10.097 |
| w29 | 5 | -0.269727 | -6.385 |
| w30 | 8 | -0.150601 | -8.795 |
| w31 | 3 | 0.228329 | 10.515 |
| w32 | 6 | -0.082099 | 0.136 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 2 | -0.047364 | -5.442 |
| w18 | 10 | 0.142363 | 27.343 |
| w19 | 5 | -0.000935 | -0.557 |
| w20 | 7 | 0.023109 | 10.884 |
| w21 | 6 | -0.086364 | -14.841 |
| w22 | 6 | -0.043923 | 8.602 |
| w23 | 2 | 0.004627 | 19.604 |
| w24 | 8 | 0.033576 | 0.479 |
| w25 | 5 | -0.05823 | 28.964 |
| w26 | 2 | 0.067891 | -4.643 |
| w27 | 8 | 0.057335 | 130.673 |
| w28 | 2 | 0.131057 | 3.827 |
| w29 | 5 | 0.080416 | 0.363 |
| w30 | 4 | -0.134931 | 5.445 |
| w31 | 5 | 0.007241 | 4.63 |
| w32 | 11 | 0.162881 | 8.392 |

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
| w17 | 6 | -0.105747 | -16.939 |
| w18 | 2 | -0.204373 | -0.245 |
| w19 | 6 | -0.031157 | 3.733 |
| w20 | 5 | 0.134691 | 11.347 |
| w21 | 5 | -0.060173 | -29.009 |
| w22 | 4 | -0.10873 | -3.813 |
| w23 | 2 | -0.020693 | 4.029 |
| w24 | 18 | 0.000916 | -3.238 |
| w25 | 7 | 0.032133 | 22.843 |
| w26 | 7 | -0.142337 | -17.076 |
| w27 | 13 | -0.101977 | 5.599 |
| w28 | 3 | 0.32363 | 7.945 |
| w29 | 10 | 0.111295 | 2.359 |
| w30 | 2 | -0.09535 | 0.29 |
| w31 | 7 | 0.013455 | 4.862 |
| w32 | 9 | 0.002005 | -2.89 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 0 | -0.050228 | 0.0 |
| w20 | 4 | 0.148566 | 10.821 |
| w21 | 4 | -0.015776 | 11.67 |
| w22 | 17 | -0.013197 | 33.42 |
| w23 | 4 | 0.091104 | -6.702 |
| w24 | 13 | -0.032622 | 80.808 |
| w25 | 4 | -0.104621 | -18.113 |
| w26 | 4 | -0.112225 | -24.577 |
| w27 | 4 | -0.061349 | -1.11 |
| w28 | 2 | 0.021651 | -0.046 |
| w29 | 6 | 0.008399 | 6.991 |
| w30 | 4 | -0.002697 | 4.062 |
| w31 | 5 | -0.120956 | -4.711 |
| w32 | 11 | -0.066188 | 10.359 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | -0.045796 | 23.882 |
| w23 | 8 | -0.01085 | -31.977 |
| w24 | 13 | -0.019466 | 0.207 |
| w25 | 8 | -0.193142 | -12.08 |
| w26 | 2 | 0.066393 | 6.966 |
| w27 | 7 | -0.094733 | -8.326 |
| w28 | 4 | -0.111257 | 2.146 |
| w29 | 7 | 0.085128 | 27.694 |
| w30 | 2 | 0.040696 | 2.26 |
| w31 | 6 | -0.163039 | -21.629 |
| w32 | 4 | -0.001806 | -11.895 |

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
| w27 | 6 | 0.103768 | 14.98 |
| w28 | 4 | 0.246749 | 12.624 |
| w29 | 8 | -0.185068 | 1.338 |
| w30 | 4 | -0.041657 | 14.531 |
| w31 | 6 | -0.119603 | -2.742 |
| w32 | 7 | 0.206192 | 47.496 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 5 | 0.038187 | -1.68 |
| w18 | 4 | 0.163062 | -2.87 |
| w19 | 3 | -0.016539 | -2.29 |
| w20 | 3 | 0.054122 | -1.49 |
| w21 | 6 | 0.099941 | 1.834 |
| w22 | 7 | 0.01604 | -12.367 |
| w23 | 2 | -0.076236 | 2.927 |
| w24 | 6 | -0.213411 | -16.474 |
| w25 | 5 | 0.103733 | 15.749 |
| w26 | 6 | 0.161691 | -4.158 |
| w27 | 6 | -0.0599 | 5.196 |
| w28 | 3 | 0.27838 | 5.05 |
| w29 | 4 | 0.033309 | 8.517 |
| w30 | 5 | -0.2238 | -17.072 |
| w31 | 5 | -0.001748 | 3.397 |
| w32 | 7 | -0.239815 | -13.833 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 6 | 0.077417 | -4.325 |
| w18 | 4 | 0.089039 | 3.081 |
| w19 | 3 | -0.017189 | 6.668 |
| w20 | 5 | -0.047823 | 0.667 |
| w21 | 4 | -0.139477 | 5.98 |
| w22 | 11 | -0.013981 | 18.857 |
| w23 | 2 | -0.39483 | -0.294 |
| w24 | 11 | -0.265974 | 35.735 |
| w25 | 7 | 0.093543 | 58.422 |
| w26 | 7 | 0.086859 | 5.714 |
| w27 | 5 | -0.177319 | -0.066 |
| w28 | 0 | 0.07246 | 0.0 |
| w29 | 4 | 0.015012 | 6.459 |
| w30 | 1 | 0.077925 | 2.274 |
| w31 | 5 | -0.066395 | -4.635 |
| w32 | 7 | -0.070079 | -7.385 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 3 | -0.062753 | -2.755 |
| w29 | 7 | 0.037715 | 3.304 |
| w30 | 4 | 0.017279 | -7.516 |
| w31 | 7 | 0.101424 | -0.275 |
| w32 | 12 | -0.10376 | 5.482 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 7 | 0.059186 | -9.48 |
| w15 | 9 | -0.047905 | 22.348 |
| w16 | 9 | 0.166619 | 134.749 |
| w17 | 7 | -0.053894 | -3.113 |
| w18 | 3 | -0.056094 | 4.073 |
| w19 | 6 | -0.395445 | -19.698 |
| w20 | 4 | -0.046984 | -11.689 |
| w21 | 4 | 0.401188 | 93.303 |
| w22 | 9 | -0.101695 | -15.282 |
| w23 | 7 | -0.140214 | -1.214 |
| w24 | 6 | -0.273416 | -12.789 |
| w25 | 6 | 0.027824 | 100.29 |
| w26 | 3 | -0.175933 | 0.12 |
| w27 | 9 | 0.236098 | 57.829 |
| w28 | 1 | 0.265724 | 6.987 |
| w29 | 5 | -0.059451 | -4.976 |
| w30 | 2 | 0.022603 | 3.04 |
| w31 | 9 | 0.001612 | 4.811 |
| w32 | 7 | 0.235105 | 11.705 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 3 | 0.376011 | 153.241 |
| w26 | 6 | 0.157805 | 11.846 |
| w27 | 6 | 0.128614 | -1.27 |
| w28 | 5 | 0.145325 | 7.766 |
| w29 | 5 | 0.149124 | 19.915 |
| w30 | 6 | -0.046855 | 5.751 |
| w31 | 7 | 0.0455 | 3.484 |
| w32 | 9 | 0.033156 | -8.86 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

