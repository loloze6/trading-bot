# Backtest of 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.069035 | -13.218 |
| w2 | 36 | 0.139442 | 64.497 |
| w3 | 53 | 0.012557 | 54.563 |
| w4 | 50 | -0.090751 | -0.699 |
| w5 | 42 | 0.003088 | 68.251 |
| w6 | 46 | 0.112124 | 91.485 |
| w7 | 28 | 0.029416 | 6.361 |
| w8 | 30 | 0.147377 | 21.438 |
| w9 | 36 | -0.012953 | -27.319 |
| w10 | 44 | 0.016999 | 15.798 |
| w11 | 39 | 0.098731 | 50.938 |
| w12 | 31 | -0.028058 | -21.611 |
| w13 | 46 | 0.02704 | 27.671 |
| w14 | 46 | -0.015666 | 8.744 |
| w15 | 51 | 0.04773 | 59.514 |
| w16 | 49 | 0.018559 | 33.584 |
| w17 | 35 | 0.006337 | -10.404 |
| w18 | 36 | 0.042462 | -17.805 |
| w19 | 33 | -0.104519 | -11.877 |
| w20 | 37 | -0.045408 | -28.722 |
| w21 | 41 | -0.082504 | -25.083 |
| w22 | 41 | 0.147023 | 89.295 |
| w23 | 36 | -0.132439 | -24.613 |
| w24 | 52 | 0.037482 | 51.785 |
| w25 | 39 | 0.076065 | 35.353 |
| w26 | 46 | 0.020584 | 14.058 |
| w27 | 51 | 0.060443 | 47.773 |
| w28 | 43 | -0.037148 | -21.621 |
| w29 | 39 | -0.041623 | 2.045 |
| w30 | 39 | 0.040995 | -8.117 |
| w31 | 33 | -0.027272 | -7.676 |
| w32 | 33 | 0.154605 | 35.19 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 48 | -0.132307 | -0.208 |
| w2 | 34 | -0.07379 | -11.421 |
| w3 | 51 | -0.085169 | -17.068 |
| w4 | 34 | -0.054288 | 10.387 |
| w5 | 34 | 0.000926 | 25.388 |
| w6 | 32 | 0.123176 | 68.581 |
| w7 | 29 | -0.024036 | -2.75 |
| w8 | 26 | 0.051701 | -11.306 |
| w9 | 31 | -0.007414 | -27.238 |
| w10 | 36 | -0.045172 | 11.051 |
| w11 | 36 | 0.029568 | -2.804 |
| w12 | 37 | -0.029974 | -25.175 |
| w13 | 37 | 0.028733 | 38.597 |
| w14 | 32 | 0.067307 | 26.696 |
| w15 | 37 | 0.016008 | 19.059 |
| w16 | 48 | 0.009082 | 21.492 |
| w17 | 32 | 0.081795 | 31.979 |
| w18 | 40 | 0.00857 | -6.245 |
| w19 | 32 | -0.022758 | -2.095 |
| w20 | 41 | -0.082116 | -31.504 |
| w21 | 37 | -0.066184 | -3.249 |
| w22 | 52 | -0.065957 | -2.44 |
| w23 | 25 | 0.046113 | 3.091 |
| w24 | 42 | -0.104675 | -7.272 |
| w25 | 46 | -0.002529 | 19.56 |
| w26 | 32 | 0.011936 | -15.93 |
| w27 | 44 | -0.011146 | 33.279 |
| w28 | 33 | 0.005149 | -8.779 |
| w29 | 36 | 0.036972 | 17.759 |
| w30 | 29 | -0.165437 | -31.638 |
| w31 | 47 | -0.111344 | -26.398 |
| w32 | 26 | 0.119652 | 21.971 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 39 | 0.109324 | 165.805 |
| w7 | 19 | 0.099008 | 8.587 |
| w8 | 23 | -0.033581 | -17.916 |
| w9 | 25 | 0.188695 | 46.75 |
| w10 | 40 | -0.067952 | -7.622 |
| w11 | 35 | 0.054688 | 3.677 |
| w12 | 40 | -0.073172 | -21.324 |
| w13 | 43 | -0.045893 | 9.668 |
| w14 | 27 | 0.264745 | 86.16 |
| w15 | 29 | 0.209546 | 143.135 |
| w16 | 37 | 0.160373 | 89.282 |
| w17 | 21 | 0.116221 | 43.048 |
| w18 | 33 | 0.015884 | -1.238 |
| w19 | 32 | 0.041622 | 9.986 |
| w20 | 14 | -0.013837 | -6.62 |
| w21 | 31 | 0.007623 | -0.434 |
| w22 | 43 | 0.028755 | 20.924 |
| w23 | 23 | -0.003683 | 26.731 |
| w24 | 37 | -0.006236 | 33.262 |
| w25 | 30 | -0.046323 | -10.794 |
| w26 | 38 | 0.070178 | 8.565 |
| w27 | 33 | 0.214529 | 201.965 |
| w28 | 38 | -0.100979 | -16.729 |
| w29 | 28 | 0.164963 | 56.025 |
| w30 | 32 | 0.001056 | -11.229 |
| w31 | 29 | 0.012048 | -5.38 |
| w32 | 28 | 0.094429 | 26.836 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 26 | 0.122342 | 25.197 |
| w8 | 33 | -0.044406 | -16.623 |
| w9 | 13 | 0.192865 | 27.966 |
| w10 | 25 | 0.025538 | 7.581 |
| w11 | 42 | -0.129659 | -19.8 |
| w12 | 30 | 0.003965 | -13.646 |
| w13 | 41 | 0.03094 | 39.52 |
| w14 | 39 | -0.008561 | 8.385 |
| w15 | 40 | -0.06261 | -28.313 |
| w16 | 36 | 0.033508 | 35.976 |
| w17 | 23 | 0.033374 | 20.627 |
| w18 | 36 | 0.037882 | -14.853 |
| w19 | 37 | 0.081386 | -15.75 |
| w20 | 25 | -0.043145 | -24.139 |
| w21 | 41 | -0.13824 | -21.365 |
| w22 | 39 | 0.020674 | 23.627 |
| w23 | 34 | 0.207898 | 82.111 |
| w24 | 38 | 0.049462 | 18.238 |
| w25 | 32 | 0.146342 | 88.395 |
| w26 | 36 | -0.044136 | -12.945 |
| w27 | 41 | -0.02091 | 7.705 |
| w28 | 38 | -0.060852 | -18.155 |
| w29 | 53 | -0.289622 | -32.519 |
| w30 | 51 | -0.1289 | -5.997 |
| w31 | 37 | -0.118429 | -21.725 |
| w32 | 20 | 0.215484 | 51.514 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | 0.140143 | 122.905 |
| w2 | 37 | 0.019638 | 8.921 |
| w3 | 28 | 0.028035 | -7.962 |
| w4 | 37 | 0.227279 | 207.945 |
| w5 | 45 | -0.0325 | 60.016 |
| w6 | 36 | 0.04914 | 41.894 |
| w7 | 25 | 0.155972 | 53.298 |
| w8 | 30 | 0.008362 | -10.54 |
| w9 | 22 | 0.022484 | -16.282 |
| w10 | 34 | -0.01508 | 1.817 |
| w11 | 40 | 0.054347 | 22.453 |
| w12 | 30 | -0.011291 | -13.943 |
| w13 | 52 | -0.018172 | 50.838 |
| w14 | 40 | 0.17134 | 79.63 |
| w15 | 36 | -0.063774 | 4.643 |
| w16 | 51 | -0.0268 | 57.674 |
| w17 | 34 | 0.059283 | 43.755 |
| w18 | 56 | -0.086519 | -17.857 |
| w19 | 33 | 0.025411 | -2.805 |
| w20 | 34 | 0.006098 | -25.684 |
| w21 | 45 | 0.028702 | -3.589 |
| w22 | 48 | 0.00491 | 33.076 |
| w23 | 36 | -0.156997 | -21.049 |
| w24 | 48 | -0.032695 | 22.778 |
| w25 | 49 | 0.140573 | 65.721 |
| w26 | 40 | 0.111658 | 1.794 |
| w27 | 47 | -0.058808 | 5.045 |
| w28 | 37 | -0.193369 | -51.917 |
| w29 | 39 | 0.04311 | 61.906 |
| w30 | 33 | -0.083582 | -22.52 |
| w31 | 38 | -0.081633 | -25.829 |
| w32 | 32 | 0.136435 | 42.694 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 36 | 0.000969 | 23.809 |
| w11 | 31 | -0.1056 | -28.792 |
| w12 | 36 | -0.077722 | -15.033 |
| w13 | 46 | 0.016945 | 49.389 |
| w14 | 39 | 0.070544 | 33.05 |
| w15 | 41 | -0.006325 | 11.35 |
| w16 | 42 | 0.011605 | 73.477 |
| w17 | 48 | 0.043258 | 65.581 |
| w18 | 21 | 0.005965 | -17.563 |
| w19 | 17 | 0.140517 | 22.592 |
| w20 | 37 | -0.053768 | -22.955 |
| w21 | 35 | -0.004028 | -16.298 |
| w22 | 42 | 0.028452 | 34.607 |
| w23 | 25 | -0.039576 | -5.16 |
| w24 | 38 | 0.210795 | 209.808 |
| w25 | 31 | 0.109292 | 15.644 |
| w26 | 29 | 0.057028 | -9.441 |
| w27 | 40 | 0.121499 | 73.601 |
| w28 | 25 | -0.118269 | -16.038 |
| w29 | 32 | 0.109104 | 42.469 |
| w30 | 30 | -0.12658 | -28.482 |
| w31 | 35 | -0.152 | -28.297 |
| w32 | 22 | 0.219181 | 45.366 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 52 | 0.036082 | 22.966 |
| w13 | 34 | -0.004465 | -13.501 |
| w14 | 46 | 0.075551 | 78.903 |
| w15 | 26 | 0.067458 | 13.235 |
| w16 | 41 | -0.034098 | 33.617 |
| w17 | 51 | 0.01262 | 12.807 |
| w18 | 38 | -0.126667 | -5.864 |
| w19 | 28 | -0.005433 | -10.249 |
| w20 | 35 | -0.042007 | -28.639 |
| w21 | 40 | -0.055997 | -21.879 |
| w22 | 36 | 0.025215 | 20.298 |
| w23 | 29 | -0.075339 | -33.229 |
| w24 | 49 | -0.088762 | -6.277 |
| w25 | 32 | 0.125162 | 14.071 |
| w26 | 40 | -0.113283 | -41.984 |
| w27 | 33 | 0.065305 | 19.851 |
| w28 | 33 | -0.133997 | -27.913 |
| w29 | 34 | -0.000163 | -11.053 |
| w30 | 24 | -0.082248 | -23.076 |
| w31 | 33 | 0.127379 | 10.17 |
| w32 | 27 | 0.106363 | 8.367 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 33 | 0.008878 | -5.581 |
| w16 | 41 | 0.012936 | 36.203 |
| w17 | 49 | -0.109889 | -16.426 |
| w18 | 27 | 0.092199 | 22.701 |
| w19 | 23 | 0.085054 | -2.699 |
| w20 | 33 | -0.14588 | -39.543 |
| w21 | 26 | -0.008699 | -11.723 |
| w22 | 45 | -0.085948 | -18.168 |
| w23 | 29 | 0.014584 | -27.704 |
| w24 | 40 | 0.01169 | 45.492 |
| w25 | 25 | 0.133945 | 28.566 |
| w26 | 27 | 0.069477 | -0.598 |
| w27 | 37 | 0.122889 | 81.467 |
| w28 | 36 | 0.007502 | -16.161 |
| w29 | 26 | 0.092456 | 22.285 |
| w30 | 25 | -0.044338 | -21.664 |
| w31 | 28 | 0.036946 | -11.168 |
| w32 | 30 | 0.020821 | -5.055 |

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
| w15 | 27 | -0.034271 | -15.382 |
| w16 | 40 | -0.036794 | 44.16 |
| w17 | 28 | 0.077579 | 22.326 |
| w18 | 35 | -0.150389 | -33.574 |
| w19 | 32 | 0.010627 | 6.123 |
| w20 | 39 | -0.002465 | -6.631 |
| w21 | 50 | -0.175709 | -30.193 |
| w22 | 50 | -0.126959 | -3.67 |
| w23 | 48 | -0.084914 | -15.688 |
| w24 | 52 | -0.093634 | 13.604 |
| w25 | 44 | 0.121415 | 27.668 |
| w26 | 56 | 0.131267 | 43.338 |
| w27 | 43 | 0.15713 | 112.08 |
| w28 | 38 | -0.143931 | -25.272 |
| w29 | 50 | -0.077326 | 12.037 |
| w30 | 34 | -0.052881 | -12.51 |
| w31 | 50 | -0.106651 | 6.679 |
| w32 | 56 | 0.066202 | 9.461 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 39 | 0.072463 | 37.948 |
| w17 | 35 | -0.051087 | -1.73 |
| w18 | 33 | -0.03095 | -7.002 |
| w19 | 33 | 0.009946 | -13.134 |
| w20 | 32 | 0.005784 | -16.9 |
| w21 | 33 | -0.118859 | -29.012 |
| w22 | 54 | -0.004311 | 15.212 |
| w23 | 24 | -0.116115 | -26.314 |
| w24 | 36 | 0.053622 | 55.966 |
| w25 | 40 | 0.101067 | 13.979 |
| w26 | 37 | -0.005272 | -14.881 |
| w27 | 39 | 0.088536 | 36.824 |
| w28 | 36 | -0.034025 | -21.219 |
| w29 | 27 | 0.046051 | -0.057 |
| w30 | 32 | -0.037438 | -17.768 |
| w31 | 20 | -0.115211 | -29.816 |
| w32 | 25 | 0.138577 | 9.06 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 25 | 0.003486 | -27.548 |
| w21 | 32 | -0.004967 | -25.289 |
| w22 | 46 | 0.033578 | 35.806 |
| w23 | 21 | -0.042681 | -25.389 |
| w24 | 36 | 0.186784 | 190.152 |
| w25 | 33 | 0.088139 | 10.955 |
| w26 | 25 | 0.061779 | 4.983 |
| w27 | 37 | -0.014424 | 10.904 |
| w28 | 27 | -0.120219 | -25.818 |
| w29 | 34 | -0.024154 | -4.343 |
| w30 | 36 | 0.025071 | -13.225 |
| w31 | 34 | -0.128424 | -28.666 |
| w32 | 37 | -0.044381 | -4.186 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 39 | 0.022704 | 18.525 |
| w23 | 31 | 0.037976 | -17.613 |
| w24 | 42 | 0.083635 | 124.798 |
| w25 | 33 | 0.121965 | 40.527 |
| w26 | 33 | 0.056092 | 7.779 |
| w27 | 38 | 0.150078 | 42.051 |
| w28 | 37 | -0.098535 | -30.645 |
| w29 | 32 | 0.002967 | -2.43 |
| w30 | 22 | -0.036466 | -8.803 |
| w31 | 40 | -0.045747 | -16.818 |
| w32 | 31 | 0.052393 | 28.71 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 36 | -0.035321 | 34.16 |
| w25 | 46 | -0.042169 | 12.015 |
| w26 | 22 | 0.083136 | 4.375 |
| w27 | 47 | 0.051324 | 57.381 |
| w28 | 25 | 0.002575 | -0.784 |
| w29 | 32 | 0.03982 | 10.083 |
| w30 | 27 | -0.018786 | -17.417 |
| w31 | 21 | 0.01043 | -9.753 |
| w32 | 34 | 0.171724 | 39.283 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 38 | 0.057561 | 82.86 |
| w6 | 39 | 0.014109 | 21.379 |
| w7 | 27 | 0.022624 | 0.59 |
| w8 | 25 | 0.07032 | 2.682 |
| w9 | 28 | 0.094768 | -9.983 |
| w10 | 33 | 0.111412 | 35.886 |
| w11 | 30 | 0.091807 | -0.235 |
| w12 | 30 | -0.075391 | -28.758 |
| w13 | 30 | 0.159064 | 90.55 |
| w14 | 43 | -0.019768 | 16.597 |
| w15 | 36 | -0.111807 | -40.962 |
| w16 | 40 | 0.141819 | 83.262 |
| w17 | 24 | 0.041564 | 13.027 |
| w18 | 35 | 0.013495 | -10.977 |
| w19 | 25 | 0.053063 | 18.43 |
| w20 | 28 | 0.011111 | -16.856 |
| w21 | 39 | -0.137875 | -37.128 |
| w22 | 41 | -0.078231 | -4.33 |
| w23 | 26 | -0.013113 | -14.234 |
| w24 | 49 | -0.143473 | -13.983 |
| w25 | 38 | 0.159577 | 24.998 |
| w26 | 32 | 0.16657 | 49.323 |
| w27 | 40 | 0.021182 | 35.92 |
| w28 | 36 | -0.059713 | -6.702 |
| w29 | 40 | 0.004133 | 7.219 |
| w30 | 47 | 0.109858 | 156.647 |
| w31 | 30 | -0.047274 | -10.667 |
| w32 | 43 | 0.119903 | 76.822 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 42 | 0.109917 | 136.267 |
| w6 | 36 | 0.037263 | 43.625 |
| w7 | 25 | -0.004358 | -2.789 |
| w8 | 13 | 0.02484 | -1.656 |
| w9 | 21 | 0.038907 | -11.522 |
| w10 | 47 | 0.02477 | 17.735 |
| w11 | 36 | 0.030927 | 0.529 |
| w12 | 38 | -0.084778 | -27.322 |
| w13 | 43 | 0.026715 | 49.433 |
| w14 | 54 | -0.071268 | 19.088 |
| w15 | 53 | -0.130779 | -11.489 |
| w16 | 47 | 0.050581 | 67.303 |
| w17 | 40 | -0.02203 | -0.113 |
| w18 | 40 | 0.014286 | -25.985 |
| w19 | 38 | -0.159806 | -17.412 |
| w20 | 46 | -0.059125 | -25.188 |
| w21 | 53 | -0.245218 | -30.48 |
| w22 | 45 | -0.098415 | -12.684 |
| w23 | 31 | 0.118608 | -2.782 |
| w24 | 51 | -0.085349 | -5.022 |
| w25 | 36 | 0.02286 | -30.653 |
| w26 | 46 | -0.039094 | 4.407 |
| w27 | 45 | -0.0371 | 11.293 |
| w28 | 46 | -0.006892 | 23.164 |
| w29 | 37 | 0.018095 | 11.552 |
| w30 | 50 | -0.159016 | -0.865 |
| w31 | 36 | 0.089895 | 20.19 |
| w32 | 53 | -0.06784 | 1.952 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 39 | -0.061338 | -11.129 |
| w18 | 36 | 0.020944 | 17.262 |
| w19 | 28 | 0.108581 | 2.043 |
| w20 | 33 | -0.066969 | -27.016 |
| w21 | 29 | -0.068061 | -29.465 |
| w22 | 51 | 0.091465 | 34.822 |
| w23 | 32 | -0.049786 | -16.874 |
| w24 | 44 | -0.003103 | 10.895 |
| w25 | 41 | 0.143382 | 16.001 |
| w26 | 34 | -0.003212 | -15.087 |
| w27 | 37 | 0.147849 | 93.249 |
| w28 | 34 | -0.076023 | -13.568 |
| w29 | 29 | 0.09549 | 28.809 |
| w30 | 25 | -0.060005 | -22.308 |
| w31 | 35 | -0.094116 | -26.631 |
| w32 | 31 | 0.155781 | 73.253 |

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
| w17 | 36 | -0.004236 | -6.4 |
| w18 | 37 | 0.003969 | -19.155 |
| w19 | 33 | 0.048437 | -4.48 |
| w20 | 33 | -0.022551 | -6.71 |
| w21 | 43 | -0.154797 | -28.232 |
| w22 | 49 | 0.060939 | 39.489 |
| w23 | 33 | 0.099312 | -0.107 |
| w24 | 37 | -0.029358 | 29.506 |
| w25 | 40 | -0.036575 | -21.765 |
| w26 | 27 | 0.140017 | 56.79 |
| w27 | 50 | -0.033613 | 25.094 |
| w28 | 33 | -0.080571 | -11.667 |
| w29 | 47 | -0.079063 | 26.6 |
| w30 | 29 | -0.051734 | -23.756 |
| w31 | 29 | -0.065826 | -9.84 |
| w32 | 34 | 0.101609 | 37.344 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 25 | 0.068625 | 19.54 |
| w20 | 30 | -0.057436 | -21.557 |
| w21 | 39 | -0.050664 | -5.977 |
| w22 | 41 | 0.032933 | 135.006 |
| w23 | 32 | 0.092087 | 15.196 |
| w24 | 47 | 0.181709 | 242.912 |
| w25 | 28 | -0.0295 | -14.604 |
| w26 | 31 | -0.014751 | -12.154 |
| w27 | 43 | 0.034268 | 0.189 |
| w28 | 33 | -0.10074 | -28.543 |
| w29 | 39 | -0.054806 | -11.612 |
| w30 | 29 | 0.016028 | -10.57 |
| w31 | 33 | -0.048155 | -12.733 |
| w32 | 41 | -0.017457 | 6.627 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 41 | 0.021274 | 13.148 |
| w23 | 25 | -0.009341 | -7.404 |
| w24 | 40 | -0.129434 | -8.052 |
| w25 | 47 | -0.12034 | -26.178 |
| w26 | 28 | 0.036362 | 2.307 |
| w27 | 38 | -0.05659 | -11.776 |
| w28 | 31 | -0.001947 | -13.666 |
| w29 | 22 | 0.052325 | 18.716 |
| w30 | 30 | -0.036146 | -14.526 |
| w31 | 27 | -0.063148 | -19.86 |
| w32 | 24 | 0.181418 | 49.388 |

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
| w27 | 35 | 0.075729 | 50.488 |
| w28 | 39 | -0.194141 | -26.432 |
| w29 | 37 | 0.050118 | 18.718 |
| w30 | 28 | -0.005141 | -16.149 |
| w31 | 32 | -0.123729 | -30.05 |
| w32 | 31 | 0.06712 | 38.053 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 22 | 0.041795 | 8.085 |
| w18 | 24 | -0.052511 | -26.959 |
| w19 | 27 | 0.056967 | -5.215 |
| w20 | 20 | 0.123904 | 13.208 |
| w21 | 28 | -0.094663 | -26.245 |
| w22 | 31 | 0.053106 | 56.676 |
| w23 | 35 | -0.008938 | -9.716 |
| w24 | 48 | -0.127849 | 4.043 |
| w25 | 34 | 0.08954 | 12.646 |
| w26 | 34 | 0.002882 | -14.56 |
| w27 | 38 | -0.042519 | -16.22 |
| w28 | 32 | -0.076369 | -29.695 |
| w29 | 35 | -0.045236 | -15.995 |
| w30 | 22 | 0.051403 | -4.374 |
| w31 | 40 | -0.136002 | -26.947 |
| w32 | 26 | 0.06718 | 6.125 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 30 | 0.021173 | -5.917 |
| w18 | 41 | -0.098197 | -25.675 |
| w19 | 30 | -0.037578 | -24.526 |
| w20 | 24 | 0.023368 | -8.513 |
| w21 | 36 | -0.013095 | -25.108 |
| w22 | 31 | 0.113113 | 90.582 |
| w23 | 20 | 0.026438 | -6.93 |
| w24 | 41 | 0.01865 | 54.68 |
| w25 | 36 | 0.054117 | 33.788 |
| w26 | 23 | 0.071177 | 8.209 |
| w27 | 43 | 0.112324 | 33.937 |
| w28 | 23 | -0.057005 | -18.352 |
| w29 | 32 | -0.00759 | -6.654 |
| w30 | 18 | -0.110608 | -29.356 |
| w31 | 31 | -0.083145 | -28.781 |
| w32 | 26 | 0.176227 | 10.217 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 33 | -0.00361 | -2.99 |
| w29 | 37 | -0.007554 | 2.916 |
| w30 | 30 | -0.02439 | -8.982 |
| w31 | 21 | 0.189337 | 35.806 |
| w32 | 33 | 0.032793 | 23.352 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 28 | 0.126785 | 52.162 |
| w15 | 28 | 0.052485 | 49.35 |
| w16 | 20 | 0.065239 | 264.285 |
| w17 | 26 | 0.044978 | 8.565 |
| w18 | 33 | -0.102459 | -26.275 |
| w19 | 29 | -0.003125 | -3.601 |
| w20 | 29 | 0.040017 | -1.474 |
| w21 | 27 | 0.248363 | 109.091 |
| w22 | 44 | -0.026052 | 5.551 |
| w23 | 28 | 0.011549 | -4.643 |
| w24 | 36 | -0.007676 | 14.912 |
| w25 | 32 | 0.155579 | 73.259 |
| w26 | 26 | 0.018363 | 9.147 |
| w27 | 28 | 0.155018 | 108.451 |
| w28 | 26 | -0.03875 | -22.165 |
| w29 | 29 | 0.061442 | 24.054 |
| w30 | 38 | 0.040267 | -8.88 |
| w31 | 43 | -0.075897 | -15.785 |
| w32 | 35 | 0.06818 | 6.082 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 16 | 0.322583 | 234.443 |
| w26 | 29 | 0.047231 | 7.423 |
| w27 | 26 | 0.106944 | 48.503 |
| w28 | 27 | -0.076766 | -22.786 |
| w29 | 30 | 0.049828 | 6.347 |
| w30 | 28 | -0.066361 | -17.178 |
| w31 | 36 | -0.035729 | 7.428 |
| w32 | 39 | 0.141154 | 25.136 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

