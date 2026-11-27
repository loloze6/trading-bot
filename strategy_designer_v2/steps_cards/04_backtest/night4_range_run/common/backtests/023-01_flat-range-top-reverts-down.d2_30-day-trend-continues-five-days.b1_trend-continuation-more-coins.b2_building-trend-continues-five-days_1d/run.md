# Backtest of 023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d

- Plan: `../../../../../03_test_plan/night4_range_run/plans/023-01_flat-range-top-reverts-down.d2_30-day-trend-continues-five-days.b1_trend-continuation-more-coins.b2_building-trend-continues-five-days_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 45 | -0.097261 | -7.398 |
| w2 | 37 | 0.069195 | 15.966 |
| w3 | 54 | 0.005568 | 66.896 |
| w4 | 56 | -0.196306 | -46.744 |
| w5 | 46 | 0.078783 | 146.535 |
| w6 | 60 | -0.006382 | 84.567 |
| w7 | 52 | -0.122274 | -18.34 |
| w8 | 46 | -0.050109 | -13.08 |
| w9 | 58 | -0.03422 | 33.505 |
| w10 | 47 | -0.008484 | 15.548 |
| w11 | 49 | -0.027584 | 30.293 |
| w12 | 51 | -0.083127 | -9.058 |
| w13 | 60 | 0.006356 | 18.721 |
| w14 | 41 | 0.029358 | 25.149 |
| w15 | 61 | 0.134609 | 135.279 |
| w16 | 44 | -0.13325 | 6.185 |
| w17 | 43 | 0.095526 | 55.141 |
| w18 | 40 | 0.04973 | 14.85 |
| w19 | 55 | -0.07744 | -11.675 |
| w20 | 41 | 0.007295 | 24.153 |
| w21 | 43 | -0.128875 | -23.866 |
| w22 | 50 | -0.024069 | 32.152 |
| w23 | 52 | 0.014736 | -2.321 |
| w24 | 49 | 0.06383 | 60.915 |
| w25 | 51 | 0.048943 | 19.551 |
| w26 | 73 | -0.131834 | -29.605 |
| w27 | 57 | -0.077368 | 40.386 |
| w28 | 47 | -0.007864 | -0.879 |
| w29 | 63 | -0.01991 | 10.12 |
| w30 | 54 | 0.007931 | 5.326 |
| w31 | 44 | 0.002183 | 2.421 |
| w32 | 52 | 0.158744 | 59.961 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 61 | -0.034507 | 3.499 |
| w2 | 44 | -0.013494 | 6.893 |
| w3 | 62 | -0.266574 | -63.587 |
| w4 | 54 | 0.120192 | 72.234 |
| w5 | 43 | -0.089364 | 21.554 |
| w6 | 47 | 0.025549 | 67.794 |
| w7 | 42 | -0.040491 | -10.696 |
| w8 | 47 | -0.063059 | 3.854 |
| w9 | 58 | -0.02437 | 29.432 |
| w10 | 48 | -0.162685 | -4.751 |
| w11 | 43 | 0.068752 | 19.797 |
| w12 | 59 | -0.070224 | -6.489 |
| w13 | 45 | 0.030072 | 23.872 |
| w14 | 45 | -0.019777 | -6.895 |
| w15 | 53 | 0.061103 | 50.533 |
| w16 | 63 | -0.115669 | 1.643 |
| w17 | 46 | 0.044855 | 20.607 |
| w18 | 38 | -0.009294 | -10.324 |
| w19 | 48 | -0.088247 | -11.295 |
| w20 | 48 | 0.039543 | 33.015 |
| w21 | 48 | -0.039864 | -1.589 |
| w22 | 58 | -0.082826 | -12.716 |
| w23 | 47 | -0.161395 | -54.144 |
| w24 | 42 | -0.171534 | -29.401 |
| w25 | 51 | 0.068833 | 39.854 |
| w26 | 57 | -0.206647 | -7.233 |
| w27 | 48 | -0.04085 | 8.065 |
| w28 | 51 | -0.072484 | -18.285 |
| w29 | 44 | 0.053734 | 31.807 |
| w30 | 63 | -0.266888 | -38.351 |
| w31 | 53 | 0.031961 | 33.469 |
| w32 | 57 | -0.004479 | -5.314 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 58 | 0.102854 | 93.847 |
| w7 | 25 | -0.069471 | -9.988 |
| w8 | 36 | -0.117595 | -12.179 |
| w9 | 55 | -0.047413 | -45.777 |
| w10 | 57 | -0.202477 | -27.401 |
| w11 | 40 | -0.036583 | -12.041 |
| w12 | 36 | 0.072568 | 23.855 |
| w13 | 52 | -0.038012 | -10.005 |
| w14 | 49 | 0.020164 | 21.6 |
| w15 | 38 | 0.149106 | 145.557 |
| w16 | 37 | -0.015297 | 38.735 |
| w17 | 29 | 0.078859 | 29.147 |
| w18 | 47 | -0.053811 | 0.84 |
| w19 | 61 | -0.067728 | -6.028 |
| w20 | 58 | 0.084817 | 45.663 |
| w21 | 40 | 0.023037 | -4.223 |
| w22 | 51 | -0.128994 | -18.151 |
| w23 | 39 | -0.156695 | -78.878 |
| w24 | 40 | -0.042696 | 3.658 |
| w25 | 59 | 0.014319 | 17.888 |
| w26 | 47 | -0.008831 | -0.583 |
| w27 | 45 | 0.214392 | 190.516 |
| w28 | 37 | -0.135209 | -19.557 |
| w29 | 51 | 0.082843 | 39.514 |
| w30 | 50 | -0.101792 | -17.604 |
| w31 | 43 | -0.081434 | -20.734 |
| w32 | 57 | 0.066743 | -16.648 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 35 | -0.042053 | -12.271 |
| w8 | 44 | -0.052597 | -6.304 |
| w9 | 52 | -0.04254 | -20.233 |
| w10 | 44 | 0.022726 | 32.331 |
| w11 | 40 | -0.033625 | -7.388 |
| w12 | 43 | -0.026976 | -14.877 |
| w13 | 48 | 0.056988 | 34.367 |
| w14 | 49 | -0.069694 | -22.025 |
| w15 | 46 | -0.096714 | -9.028 |
| w16 | 45 | -0.004977 | 46.302 |
| w17 | 42 | 0.094037 | 31.473 |
| w18 | 53 | -0.073099 | -6.462 |
| w19 | 59 | -0.060355 | -10.252 |
| w20 | 41 | 0.089865 | 44.736 |
| w21 | 49 | -0.130138 | -5.062 |
| w22 | 48 | 0.002715 | -4.326 |
| w23 | 37 | 0.111151 | -20.935 |
| w24 | 48 | -0.153335 | -16.407 |
| w25 | 52 | 0.021228 | 17.289 |
| w26 | 51 | -0.108421 | -16.899 |
| w27 | 61 | -0.058296 | -5.735 |
| w28 | 44 | -0.086245 | -12.015 |
| w29 | 50 | -0.080291 | 9.503 |
| w30 | 67 | -0.058782 | -8.632 |
| w31 | 56 | -0.09344 | -11.275 |
| w32 | 55 | 0.097883 | 63.593 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | 0.146671 | 149.77 |
| w2 | 55 | -0.091755 | -19.835 |
| w3 | 61 | 0.028165 | 20.592 |
| w4 | 45 | -0.184276 | 129.243 |
| w5 | 38 | 0.088948 | 78.655 |
| w6 | 45 | 0.001398 | 53.782 |
| w7 | 53 | -0.007607 | 4.249 |
| w8 | 46 | 0.043194 | 18.779 |
| w9 | 54 | -0.044157 | 19.774 |
| w10 | 56 | -0.170394 | -23.485 |
| w11 | 49 | 0.067759 | 33.521 |
| w12 | 50 | 0.00418 | -5.361 |
| w13 | 46 | -0.040069 | -4.094 |
| w14 | 45 | 0.024889 | 69.411 |
| w15 | 62 | 0.054231 | 40.184 |
| w16 | 51 | 0.083117 | 104.44 |
| w17 | 50 | 0.012623 | 10.554 |
| w18 | 60 | -0.06305 | -8.325 |
| w19 | 59 | -0.019604 | -2.722 |
| w20 | 39 | 0.143407 | 80.218 |
| w21 | 54 | -0.115495 | -25.127 |
| w22 | 59 | -0.065723 | 11.232 |
| w23 | 50 | -0.053676 | -3.163 |
| w24 | 51 | 0.040407 | 23.629 |
| w25 | 62 | 0.007146 | 1.015 |
| w26 | 45 | -0.039384 | -12.89 |
| w27 | 50 | 0.032907 | 52.678 |
| w28 | 43 | -0.058824 | 21.31 |
| w29 | 43 | 0.013749 | 58.691 |
| w30 | 53 | -0.030938 | -9.858 |
| w31 | 56 | 0.012693 | 12.137 |
| w32 | 45 | 0.125448 | 42.034 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 43 | 0.01518 | 38.758 |
| w11 | 51 | 0.024961 | 9.084 |
| w12 | 61 | -0.059159 | -20.68 |
| w13 | 51 | 0.052548 | 26.862 |
| w14 | 41 | 0.019665 | 39.307 |
| w15 | 53 | 0.043677 | 14.826 |
| w16 | 28 | 0.066035 | 98.878 |
| w17 | 55 | 0.039231 | 43.694 |
| w18 | 55 | -0.069989 | 0.933 |
| w19 | 54 | -0.066068 | -21.153 |
| w20 | 59 | -0.100843 | -11.152 |
| w21 | 60 | -0.194486 | 7.713 |
| w22 | 48 | -0.066194 | -2.913 |
| w23 | 39 | -0.050424 | 7.369 |
| w24 | 38 | 0.107309 | 119.907 |
| w25 | 38 | 0.060602 | 9.233 |
| w26 | 52 | -0.180301 | -21.424 |
| w27 | 43 | 0.108902 | 81.289 |
| w28 | 38 | -0.235737 | -60.099 |
| w29 | 59 | 0.03408 | 7.418 |
| w30 | 47 | 0.019468 | 10.001 |
| w31 | 55 | -0.121443 | -11.656 |
| w32 | 57 | 0.001316 | 21.164 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 47 | -0.147376 | -33.072 |
| w13 | 50 | 0.029713 | 10.829 |
| w14 | 47 | -0.107645 | -19.704 |
| w15 | 52 | -0.259098 | -36.248 |
| w16 | 31 | 0.053392 | 69.096 |
| w17 | 47 | -0.005422 | 42.693 |
| w18 | 57 | 0.021157 | 5.892 |
| w19 | 40 | 0.002197 | 16.486 |
| w20 | 57 | 0.132774 | 43.393 |
| w21 | 62 | -0.10867 | -25.497 |
| w22 | 54 | 0.104928 | 25.712 |
| w23 | 66 | -0.012632 | 39.772 |
| w24 | 55 | -0.059787 | -3.753 |
| w25 | 57 | 0.088788 | 21.687 |
| w26 | 47 | -0.097786 | 15.798 |
| w27 | 51 | 0.066149 | 23.114 |
| w28 | 48 | -0.154439 | -18.053 |
| w29 | 60 | -0.084308 | -32.996 |
| w30 | 41 | -0.046473 | 21.474 |
| w31 | 60 | -0.146962 | -37.661 |
| w32 | 72 | -0.086911 | -34.519 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 51 | -0.113898 | -18.907 |
| w16 | 41 | 0.037777 | 75.639 |
| w17 | 57 | -0.082617 | 4.767 |
| w18 | 39 | 0.061802 | 31.715 |
| w19 | 54 | -0.06368 | 15.207 |
| w20 | 50 | -0.018211 | 8.897 |
| w21 | 64 | -0.076593 | -34.874 |
| w22 | 58 | 0.002159 | -1.884 |
| w23 | 48 | -0.092977 | 11.281 |
| w24 | 50 | 0.02578 | 42.236 |
| w25 | 56 | 0.031381 | 6.181 |
| w26 | 62 | -0.139055 | -15.199 |
| w27 | 49 | 0.119334 | 84.995 |
| w28 | 38 | -0.020585 | 0.287 |
| w29 | 60 | 0.051579 | 11.934 |
| w30 | 44 | -0.079886 | 13.459 |
| w31 | 40 | 0.006045 | -18.047 |
| w32 | 62 | -0.130283 | -42.213 |

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
| w15 | 53 | -0.122681 | -23.931 |
| w16 | 50 | -0.061884 | 64.571 |
| w17 | 39 | 0.030508 | 17.778 |
| w18 | 55 | -0.046553 | -3.69 |
| w19 | 49 | -0.067539 | -25.941 |
| w20 | 46 | -0.159831 | -26.798 |
| w21 | 51 | -0.034493 | -19.335 |
| w22 | 62 | -0.120546 | -25.093 |
| w23 | 55 | -0.077027 | -10.665 |
| w24 | 54 | -0.042481 | 32.29 |
| w25 | 55 | 0.064026 | 18.045 |
| w26 | 59 | -0.083382 | -11.769 |
| w27 | 35 | 0.050908 | 171.254 |
| w28 | 56 | -0.09287 | -24.579 |
| w29 | 48 | 0.052228 | 59.574 |
| w30 | 50 | -0.016696 | -9.038 |
| w31 | 69 | -0.069357 | 5.795 |
| w32 | 59 | -0.078148 | -10.142 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 27 | 0.123364 | 68.101 |
| w17 | 49 | 0.014047 | 26.13 |
| w18 | 53 | 0.037429 | 11.656 |
| w19 | 53 | -0.05983 | -7.992 |
| w20 | 55 | 0.019859 | 15.799 |
| w21 | 47 | -0.133663 | -4.8 |
| w22 | 66 | -0.022037 | -1.528 |
| w23 | 55 | 0.019868 | 9.88 |
| w24 | 53 | 0.067614 | 39.354 |
| w25 | 56 | 0.03868 | 1.741 |
| w26 | 60 | -0.06802 | -0.966 |
| w27 | 44 | 0.086281 | 20.859 |
| w28 | 49 | -0.212651 | -6.146 |
| w29 | 55 | -0.016747 | -9.721 |
| w30 | 51 | -0.065832 | -17.652 |
| w31 | 45 | -0.122332 | -20.764 |
| w32 | 52 | -0.049429 | 0.176 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 50 | 0.117628 | 56.691 |
| w21 | 54 | -0.212025 | -17.143 |
| w22 | 35 | -0.052056 | -1.724 |
| w23 | 51 | 0.002301 | 28.321 |
| w24 | 40 | 0.191425 | 244.518 |
| w25 | 44 | 0.046098 | 0.827 |
| w26 | 63 | -0.172684 | -24.973 |
| w27 | 63 | 0.003171 | 31.934 |
| w28 | 47 | -0.012272 | 12.698 |
| w29 | 58 | 0.005611 | 2.266 |
| w30 | 40 | 0.008126 | 9.19 |
| w31 | 42 | -0.06605 | -1.387 |
| w32 | 48 | 0.021197 | 13.472 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 38 | -0.038684 | -4.392 |
| w23 | 55 | 0.003425 | 19.41 |
| w24 | 45 | 0.114472 | 126.995 |
| w25 | 39 | 0.125615 | 37.759 |
| w26 | 52 | -0.029927 | -9.405 |
| w27 | 53 | -0.079865 | -8.919 |
| w28 | 50 | -0.16315 | 0.813 |
| w29 | 61 | -0.011028 | -17.119 |
| w30 | 52 | -0.177007 | -48.938 |
| w31 | 51 | -0.072412 | -18.699 |
| w32 | 50 | 0.020669 | 28.777 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 55 | 0.041832 | 22.786 |
| w25 | 45 | 0.056189 | 2.924 |
| w26 | 51 | -0.065513 | -40.348 |
| w27 | 35 | -0.005837 | 90.062 |
| w28 | 44 | 0.068799 | 4.902 |
| w29 | 51 | -0.000385 | -1.957 |
| w30 | 51 | -0.020038 | -2.487 |
| w31 | 58 | -0.041736 | -11.463 |
| w32 | 51 | -0.059387 | -25.708 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 26 | 0.089731 | 58.277 |
| w6 | 55 | -0.035687 | 1.699 |
| w7 | 52 | -0.009205 | 3.833 |
| w8 | 50 | -0.04877 | -18.215 |
| w9 | 60 | -0.044724 | 2.834 |
| w10 | 41 | 0.005645 | 11.749 |
| w11 | 53 | 0.04231 | 15.089 |
| w12 | 47 | -0.113493 | -3.89 |
| w13 | 36 | 0.108214 | 74.01 |
| w14 | 54 | -0.11171 | 10.396 |
| w15 | 54 | -0.143916 | -32.131 |
| w16 | 56 | -0.169108 | -3.129 |
| w17 | 48 | -0.004285 | 7.848 |
| w18 | 46 | -0.00323 | -0.507 |
| w19 | 51 | -0.003442 | -2.33 |
| w20 | 56 | -0.02793 | -9.913 |
| w21 | 51 | -0.148328 | -7.1 |
| w22 | 52 | -0.081411 | -13.906 |
| w23 | 54 | -0.05966 | 0.686 |
| w24 | 51 | -0.188122 | -38.789 |
| w25 | 51 | 0.093758 | 39.075 |
| w26 | 41 | -0.011028 | -5.252 |
| w27 | 43 | -0.055674 | 12.963 |
| w28 | 42 | -0.134309 | -23.631 |
| w29 | 49 | -0.045486 | -25.292 |
| w30 | 29 | 0.137112 | 286.649 |
| w31 | 50 | 0.070348 | 17.331 |
| w32 | 55 | 0.022548 | 21.008 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 39 | 0.141771 | 181.645 |
| w6 | 38 | 0.023511 | 68.328 |
| w7 | 42 | -0.122056 | -26.378 |
| w8 | 71 | -0.064225 | -10.303 |
| w9 | 53 | -0.073928 | 7.837 |
| w10 | 58 | -0.118686 | -6.038 |
| w11 | 54 | -0.082341 | -13.311 |
| w12 | 52 | -0.022859 | 12.22 |
| w13 | 51 | -0.005669 | -2.857 |
| w14 | 45 | 0.046887 | 40.734 |
| w15 | 49 | -0.083556 | -7.795 |
| w16 | 48 | -0.044083 | 27.42 |
| w17 | 58 | -0.069384 | -23.971 |
| w18 | 63 | -0.120966 | -21.79 |
| w19 | 61 | -0.053982 | -24.163 |
| w20 | 40 | -0.113988 | -18.256 |
| w21 | 68 | -0.177616 | -51.659 |
| w22 | 59 | -0.012636 | 6.439 |
| w23 | 56 | 0.006015 | 2.392 |
| w24 | 61 | -0.095659 | -2.548 |
| w25 | 67 | -0.258705 | -47.147 |
| w26 | 57 | -0.02438 | -2.868 |
| w27 | 61 | -0.031421 | -33.451 |
| w28 | 59 | -0.032664 | 19.503 |
| w29 | 55 | 0.036302 | 10.751 |
| w30 | 68 | -0.10527 | 8.092 |
| w31 | 41 | -0.092491 | -22.079 |
| w32 | 56 | -0.009698 | 29.741 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 58 | -0.058084 | -22.734 |
| w18 | 49 | -0.107985 | -9.211 |
| w19 | 50 | -0.086866 | -13.11 |
| w20 | 56 | 0.060256 | 23.785 |
| w21 | 52 | -0.232629 | -28.813 |
| w22 | 57 | 0.014651 | 9.687 |
| w23 | 55 | -0.048701 | 6.731 |
| w24 | 54 | -0.119197 | -32.728 |
| w25 | 59 | 0.11378 | 37.654 |
| w26 | 51 | -0.10567 | -17.885 |
| w27 | 56 | 0.105583 | 124.756 |
| w28 | 42 | 0.072567 | 13.734 |
| w29 | 52 | 0.070259 | 20.162 |
| w30 | 37 | -0.093151 | -1.686 |
| w31 | 54 | -0.046464 | 3.678 |
| w32 | 56 | 0.008134 | -8.734 |

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
| w17 | 63 | -0.060194 | -28.712 |
| w18 | 54 | -0.089337 | -9.984 |
| w19 | 57 | -0.06155 | -18.46 |
| w20 | 43 | -0.027504 | -5.01 |
| w21 | 61 | -0.191045 | -34.557 |
| w22 | 56 | 0.007939 | 0.7 |
| w23 | 59 | -0.047291 | -13.22 |
| w24 | 44 | -0.148135 | 0.849 |
| w25 | 49 | 0.047483 | 19.452 |
| w26 | 61 | -0.148764 | -30.308 |
| w27 | 41 | -0.008939 | 40.478 |
| w28 | 43 | -0.008968 | 6.418 |
| w29 | 59 | -0.088989 | -20.017 |
| w30 | 53 | -0.116306 | -11.528 |
| w31 | 55 | -0.201217 | -16.578 |
| w32 | 64 | 0.035233 | 4.6 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 58 | -0.041989 | -2.409 |
| w20 | 46 | 0.011019 | 9.98 |
| w21 | 47 | -0.029965 | -5.134 |
| w22 | 43 | 0.015181 | 115.415 |
| w23 | 40 | -0.08208 | -15.692 |
| w24 | 49 | 0.048191 | 169.745 |
| w25 | 47 | 0.02086 | 2.1 |
| w26 | 56 | -0.19717 | -43.649 |
| w27 | 58 | -0.076491 | -20.45 |
| w28 | 39 | -0.139056 | 0.826 |
| w29 | 58 | -0.066832 | 4.268 |
| w30 | 36 | 0.004375 | 40.188 |
| w31 | 52 | -0.020444 | -7.933 |
| w32 | 46 | -0.021265 | 10.491 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 34 | 0.062659 | 31.356 |
| w23 | 62 | -0.168307 | -35.868 |
| w24 | 51 | -0.019259 | -18.374 |
| w25 | 65 | -0.009753 | -13.418 |
| w26 | 59 | 0.022897 | 18.48 |
| w27 | 47 | -0.099524 | -25.292 |
| w28 | 34 | 0.007662 | 15.111 |
| w29 | 61 | -0.074122 | -9.499 |
| w30 | 52 | -0.114587 | -14.918 |
| w31 | 42 | 0.048224 | 16.403 |
| w32 | 56 | 0.010062 | -13.918 |

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
| w27 | 60 | -0.031963 | 11.982 |
| w28 | 46 | -0.066467 | -14.412 |
| w29 | 72 | -0.021202 | -6.044 |
| w30 | 43 | -0.006257 | -6.718 |
| w31 | 53 | -0.056397 | -3.753 |
| w32 | 43 | -0.007926 | 27.773 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 37 | 0.035759 | 7.823 |
| w18 | 58 | -0.034293 | 17.877 |
| w19 | 48 | -0.041909 | -2.776 |
| w20 | 44 | 0.110679 | 28.151 |
| w21 | 45 | -0.173876 | -5.226 |
| w22 | 52 | -0.067969 | -9.318 |
| w23 | 55 | -0.017912 | 11.025 |
| w24 | 54 | -0.0262 | 7.494 |
| w25 | 47 | 0.031016 | -2.192 |
| w26 | 46 | -0.141181 | -12.266 |
| w27 | 55 | -0.057581 | -35.622 |
| w28 | 40 | -0.148563 | -1.753 |
| w29 | 61 | -0.06011 | -29.953 |
| w30 | 43 | -0.14767 | -48.774 |
| w31 | 45 | -0.104181 | -13.337 |
| w32 | 54 | -0.041013 | -4.959 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 46 | 0.046734 | 23.043 |
| w18 | 36 | 0.030895 | -2.16 |
| w19 | 68 | -0.096056 | -5.868 |
| w20 | 47 | 0.052387 | 10.052 |
| w21 | 51 | -0.108283 | -1.555 |
| w22 | 39 | 0.084354 | 103.398 |
| w23 | 63 | -0.105024 | -17.124 |
| w24 | 41 | 0.060026 | 40.008 |
| w25 | 47 | 0.155462 | 49.837 |
| w26 | 58 | -0.078067 | -6.806 |
| w27 | 55 | -0.066757 | -2.874 |
| w28 | 36 | -0.105221 | 10.767 |
| w29 | 60 | -0.001188 | -6.607 |
| w30 | 53 | -0.12405 | -8.866 |
| w31 | 48 | -0.146947 | -12.952 |
| w32 | 48 | -0.037398 | -14.658 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 62 | 0.036483 | -8.327 |
| w29 | 51 | 0.013985 | -2.117 |
| w30 | 51 | -0.09563 | -16.989 |
| w31 | 42 | 0.028099 | 0.906 |
| w32 | 46 | -0.07503 | -30.019 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 37 | -0.004391 | -30.587 |
| w15 | 39 | 0.086849 | 58.828 |
| w16 | 17 | -0.052387 | 167.406 |
| w17 | 28 | 0.067187 | 5.383 |
| w18 | 39 | -0.035813 | 1.496 |
| w19 | 60 | -0.084782 | -19.895 |
| w20 | 43 | 0.034707 | 20.882 |
| w21 | 49 | 0.030438 | 35.339 |
| w22 | 57 | -0.128343 | -28.345 |
| w23 | 55 | -0.032951 | -9.958 |
| w24 | 51 | 0.048795 | 27.508 |
| w25 | 38 | 0.191709 | 100.15 |
| w26 | 52 | -0.079522 | -15.615 |
| w27 | 44 | 0.072218 | 125.399 |
| w28 | 35 | 0.000598 | 14.296 |
| w29 | 53 | 0.01072 | 3.667 |
| w30 | 47 | -0.022307 | -4.557 |
| w31 | 48 | -0.025688 | -3.487 |
| w32 | 42 | 0.037044 | 16.85 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 34 | 0.245344 | 181.668 |
| w26 | 32 | -0.040378 | -9.154 |
| w27 | 53 | 0.003674 | -0.383 |
| w28 | 38 | 0.027082 | 18.225 |
| w29 | 43 | 0.050832 | 15.682 |
| w30 | 40 | -0.04538 | -4.937 |
| w31 | 47 | -0.073836 | -13.615 |
| w32 | 51 | 0.057729 | -22.476 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

