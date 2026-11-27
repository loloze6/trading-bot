# Backtest of 031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-02.b1.b1.b1.g3_heavy-volume-extends-up-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.039982 | -16.391 |
| w2 | 21 | 0.080693 | 36.986 |
| w3 | 42 | 0.053831 | 33.281 |
| w4 | 24 | -0.335289 | -42.32 |
| w5 | 38 | 0.012633 | 36.273 |
| w6 | 26 | 0.078533 | 23.481 |
| w7 | 10 | -0.044624 | -2.296 |
| w8 | 11 | 0.219638 | 28.655 |
| w9 | 16 | 0.160066 | 1.644 |
| w10 | 17 | 0.015974 | 11.255 |
| w11 | 30 | 0.096799 | 57.056 |
| w12 | 15 | 0.099337 | 4.477 |
| w13 | 33 | -0.004793 | 9.507 |
| w14 | 21 | 0.044902 | 17.506 |
| w15 | 48 | 0.006002 | 55.097 |
| w16 | 23 | -0.107063 | -2.996 |
| w17 | 13 | 0.074677 | 4.294 |
| w18 | 25 | -0.053654 | 3.107 |
| w19 | 24 | -0.022469 | -6.509 |
| w20 | 14 | 0.043657 | -7.915 |
| w21 | 18 | -0.014654 | -6.991 |
| w22 | 33 | 0.141084 | 59.204 |
| w23 | 22 | -0.063658 | -16.9 |
| w24 | 31 | 0.005257 | 36.478 |
| w25 | 31 | -0.019497 | 11.787 |
| w26 | 24 | -0.067211 | -10.772 |
| w27 | 36 | 0.086901 | 22.593 |
| w28 | 20 | -0.122544 | -27.245 |
| w29 | 29 | -0.005964 | 13.892 |
| w30 | 17 | 0.055016 | 3.199 |
| w31 | 21 | -0.041427 | -4.335 |
| w32 | 23 | 0.206133 | 38.528 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 18 | 0.139701 | 7.458 |
| w2 | 25 | -0.065423 | -8.321 |
| w3 | 23 | 0.02699 | 1.534 |
| w4 | 34 | -0.09925 | -16.26 |
| w5 | 22 | 0.115525 | 29.151 |
| w6 | 24 | 0.159279 | 88.456 |
| w7 | 11 | -0.098331 | -8.082 |
| w8 | 12 | 0.023687 | -9.455 |
| w9 | 23 | 0.041813 | -10.621 |
| w10 | 22 | -0.048146 | 22.288 |
| w11 | 21 | -0.071829 | -7.744 |
| w12 | 12 | 0.046594 | -1.744 |
| w13 | 31 | -0.015106 | 0.682 |
| w14 | 23 | -0.016762 | 17.151 |
| w15 | 44 | 0.062195 | 36.225 |
| w16 | 30 | 0.006771 | 8.685 |
| w17 | 25 | 0.113764 | 14.321 |
| w18 | 15 | 0.027188 | 3.503 |
| w19 | 9 | 0.015108 | -10.513 |
| w20 | 13 | -0.137723 | -19.218 |
| w21 | 26 | 0.141587 | 11.193 |
| w22 | 23 | -0.028517 | 13.06 |
| w23 | 19 | 0.031935 | 1.626 |
| w24 | 36 | -0.008076 | -5.135 |
| w25 | 25 | -0.043413 | 9.108 |
| w26 | 14 | -0.078706 | -11.836 |
| w27 | 27 | 0.066492 | 22.104 |
| w28 | 18 | -0.025114 | -14.712 |
| w29 | 31 | 0.113973 | 23.095 |
| w30 | 19 | -0.101335 | -13.206 |
| w31 | 16 | -0.04394 | -4.004 |
| w32 | 27 | 0.125993 | 18.734 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 31 | 0.084306 | 55.004 |
| w7 | 18 | -0.04249 | -5.155 |
| w8 | 18 | 0.019312 | -7.628 |
| w9 | 20 | 0.237621 | 48.092 |
| w10 | 18 | -0.090608 | -6.905 |
| w11 | 14 | 0.042226 | 13.312 |
| w12 | 18 | -0.011931 | -5.259 |
| w13 | 32 | -0.032395 | 1.988 |
| w14 | 27 | 0.137005 | 52.724 |
| w15 | 20 | 0.219736 | 155.257 |
| w16 | 16 | -0.069591 | 13.192 |
| w17 | 20 | 0.104744 | 29.46 |
| w18 | 16 | -0.114536 | -8.252 |
| w19 | 16 | 0.116131 | -4.324 |
| w20 | 10 | -0.047559 | -2.971 |
| w21 | 16 | -0.006872 | 1.223 |
| w22 | 25 | 0.078683 | 21.225 |
| w23 | 24 | -0.102357 | -15.778 |
| w24 | 36 | -0.065455 | -1.755 |
| w25 | 19 | -0.113413 | -22.25 |
| w26 | 20 | 0.031884 | 4.973 |
| w27 | 27 | 0.138867 | 97.995 |
| w28 | 17 | -0.001286 | -6.433 |
| w29 | 27 | 0.218149 | 37.984 |
| w30 | 15 | -0.082408 | -17.946 |
| w31 | 22 | -0.029528 | -0.511 |
| w32 | 22 | 0.263184 | 22.194 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 15 | 0.035367 | 34.369 |
| w8 | 12 | 0.0314 | -1.512 |
| w9 | 15 | 0.304122 | 49.662 |
| w10 | 26 | 0.006481 | 5.507 |
| w11 | 15 | -0.117328 | -11.254 |
| w12 | 19 | 0.007465 | -6.401 |
| w13 | 18 | -0.073147 | 5.316 |
| w14 | 23 | 0.025951 | 15.217 |
| w15 | 30 | -0.065042 | -19.671 |
| w16 | 27 | -0.130848 | 15.749 |
| w17 | 18 | -0.033092 | -3.806 |
| w18 | 22 | -0.114921 | -20.391 |
| w19 | 16 | 0.080587 | 9.43 |
| w20 | 12 | -0.008101 | -3.849 |
| w21 | 17 | -0.061912 | -27.62 |
| w22 | 20 | -0.039407 | 11.146 |
| w23 | 22 | 0.185888 | 33.509 |
| w24 | 29 | -0.074348 | 2.366 |
| w25 | 27 | 0.033224 | 27.101 |
| w26 | 25 | 0.105207 | 4.468 |
| w27 | 26 | -0.018877 | 3.581 |
| w28 | 20 | 0.026796 | 8.467 |
| w29 | 31 | -0.096926 | 6.853 |
| w30 | 28 | -0.053222 | -14.049 |
| w31 | 16 | -0.022017 | -9.556 |
| w32 | 19 | 0.179377 | 26.469 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 31 | 0.151863 | 90.722 |
| w2 | 20 | -0.09176 | -11.396 |
| w3 | 16 | 0.026902 | -1.737 |
| w4 | 28 | 0.097736 | 172.935 |
| w5 | 24 | -0.080063 | 51.329 |
| w6 | 24 | 0.050542 | 23.593 |
| w7 | 18 | -0.005296 | 6.991 |
| w8 | 9 | -0.053328 | -12.71 |
| w9 | 22 | 0.112667 | 1.603 |
| w10 | 15 | -0.052221 | -5.066 |
| w11 | 13 | 0.075887 | 29.078 |
| w12 | 12 | 0.107894 | 10.323 |
| w13 | 41 | -0.027051 | 25.996 |
| w14 | 26 | 0.126503 | 35.438 |
| w15 | 32 | 0.026721 | 36.602 |
| w16 | 33 | 0.088386 | 64.908 |
| w17 | 29 | 0.104596 | 16.741 |
| w18 | 22 | -0.04155 | -11.937 |
| w19 | 20 | 0.092231 | 0.499 |
| w20 | 16 | 0.05592 | 11.552 |
| w21 | 15 | 0.117485 | 11.695 |
| w22 | 31 | 0.190828 | 58.958 |
| w23 | 20 | -0.173774 | -25.456 |
| w24 | 38 | -0.131542 | 7.423 |
| w25 | 20 | 0.117795 | 26.955 |
| w26 | 15 | 0.009835 | -8.618 |
| w27 | 26 | 0.068777 | 29.371 |
| w28 | 14 | -0.189207 | -26.671 |
| w29 | 35 | 0.150177 | 49.447 |
| w30 | 12 | -0.119293 | -14.672 |
| w31 | 20 | -0.111272 | -20.22 |
| w32 | 21 | 0.179859 | 17.528 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 33 | -0.00586 | 16.365 |
| w11 | 14 | -0.025765 | 9.459 |
| w12 | 18 | 0.087323 | 1.151 |
| w13 | 36 | 0.002192 | 22.745 |
| w14 | 23 | 0.175677 | 43.109 |
| w15 | 32 | 0.060515 | 20.988 |
| w16 | 37 | 0.123578 | 53.386 |
| w17 | 24 | 0.088432 | 46.351 |
| w18 | 16 | -0.244276 | -34.128 |
| w19 | 20 | 0.040528 | -4.106 |
| w20 | 18 | -0.08162 | -34.548 |
| w21 | 17 | 0.018807 | -5.973 |
| w22 | 37 | 0.093555 | 9.666 |
| w23 | 17 | -0.137184 | -16.934 |
| w24 | 30 | 0.085758 | 120.287 |
| w25 | 25 | 0.046802 | -0.96 |
| w26 | 15 | 0.085669 | -6.948 |
| w27 | 22 | 0.153578 | 68.196 |
| w28 | 20 | -0.065329 | -9.749 |
| w29 | 32 | 0.227425 | 39.332 |
| w30 | 14 | -0.128644 | -19.993 |
| w31 | 17 | -0.102973 | -11.068 |
| w32 | 31 | 0.182605 | 21.333 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 27 | -0.079309 | 14.743 |
| w13 | 23 | 0.048808 | -13.318 |
| w14 | 26 | 0.101437 | 76.55 |
| w15 | 20 | 0.015338 | 11.504 |
| w16 | 39 | 0.027288 | 38.977 |
| w17 | 33 | 0.116923 | 20.37 |
| w18 | 28 | -0.107761 | -19.51 |
| w19 | 15 | -0.135758 | -6.379 |
| w20 | 18 | -0.079154 | -10.756 |
| w21 | 21 | -0.055355 | 2.616 |
| w22 | 29 | 0.036122 | 14.741 |
| w23 | 17 | -0.100271 | -20.072 |
| w24 | 40 | -0.022377 | 4.331 |
| w25 | 28 | 0.062374 | 11.575 |
| w26 | 19 | -0.073575 | -21.747 |
| w27 | 18 | 0.100524 | 27.685 |
| w28 | 18 | -0.236346 | -19.577 |
| w29 | 27 | 0.15635 | 3.422 |
| w30 | 6 | 0.026357 | 3.194 |
| w31 | 25 | 0.058447 | 20.26 |
| w32 | 32 | 0.016479 | -10.822 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 19 | -0.132641 | -13.393 |
| w16 | 37 | 0.03917 | 46.249 |
| w17 | 27 | 0.032663 | 6.352 |
| w18 | 30 | 0.12367 | 45.768 |
| w19 | 16 | 0.014162 | 5.232 |
| w20 | 14 | -0.212643 | -21.124 |
| w21 | 17 | 0.099522 | 9.606 |
| w22 | 30 | -0.130799 | -19.485 |
| w23 | 15 | -0.09363 | -14.494 |
| w24 | 38 | 0.030848 | 58.896 |
| w25 | 30 | 0.075811 | 22.538 |
| w26 | 12 | 0.013341 | 8.585 |
| w27 | 39 | 0.017282 | 29.127 |
| w28 | 16 | -0.174645 | -24.033 |
| w29 | 27 | 0.020369 | 6.563 |
| w30 | 12 | -0.040564 | -5.533 |
| w31 | 12 | 0.164531 | 13.861 |
| w32 | 22 | 0.16115 | 15.47 |

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
| w15 | 25 | -0.086703 | -7.251 |
| w16 | 34 | 0.038939 | 40.889 |
| w17 | 18 | 0.050681 | 17.292 |
| w18 | 22 | -0.104526 | -13.892 |
| w19 | 16 | 0.001791 | -14.017 |
| w20 | 17 | 0.069723 | 7.432 |
| w21 | 20 | -0.158495 | -10.86 |
| w22 | 29 | -0.121386 | -11.549 |
| w23 | 24 | 0.016834 | -13.21 |
| w24 | 40 | 0.190685 | 39.495 |
| w25 | 34 | 0.02065 | -1.136 |
| w26 | 43 | 0.247218 | 69.285 |
| w27 | 25 | 0.112901 | 83.793 |
| w28 | 28 | 0.034724 | -4.275 |
| w29 | 36 | -0.061379 | 10.282 |
| w30 | 20 | -0.013662 | -5.404 |
| w31 | 28 | -0.038902 | 16.005 |
| w32 | 25 | 0.138587 | -4.636 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 30 | 0.0701 | 20.331 |
| w17 | 36 | 0.043109 | 24.55 |
| w18 | 21 | -0.012873 | -5.346 |
| w19 | 21 | -0.001794 | -17.674 |
| w20 | 9 | -0.001678 | -3.444 |
| w21 | 20 | -0.203818 | -19.958 |
| w22 | 30 | -0.092756 | 12.322 |
| w23 | 19 | 0.014127 | -10.079 |
| w24 | 35 | 0.080587 | 25.029 |
| w25 | 17 | -0.001722 | -6.496 |
| w26 | 12 | -0.012418 | -7.295 |
| w27 | 19 | 0.075719 | 33.126 |
| w28 | 12 | -0.25622 | -15.013 |
| w29 | 25 | 0.133277 | 7.997 |
| w30 | 9 | 0.015922 | -3.63 |
| w31 | 15 | -0.075759 | -15.541 |
| w32 | 16 | 0.315095 | 27.797 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 15 | 0.034351 | 16.019 |
| w21 | 26 | -0.14914 | -26.693 |
| w22 | 24 | -0.032481 | 30.3 |
| w23 | 14 | 0.076825 | -6.17 |
| w24 | 38 | 0.163656 | 160.733 |
| w25 | 22 | 0.121922 | 9.771 |
| w26 | 14 | 0.006145 | -12.693 |
| w27 | 31 | 0.093739 | 26.527 |
| w28 | 21 | -0.136796 | -17.576 |
| w29 | 27 | 0.038273 | 2.914 |
| w30 | 18 | -0.014988 | -7.669 |
| w31 | 21 | 0.017024 | 1.15 |
| w32 | 27 | 0.122094 | 5.856 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 35 | -0.051315 | 14.681 |
| w23 | 24 | -0.118214 | -28.398 |
| w24 | 32 | 0.18727 | 114.522 |
| w25 | 27 | -0.089088 | 49.663 |
| w26 | 19 | -0.0194 | -5.832 |
| w27 | 27 | 0.127155 | 38.465 |
| w28 | 14 | 0.002553 | -3.494 |
| w29 | 23 | 0.064231 | -3.054 |
| w30 | 14 | -0.006888 | -7.227 |
| w31 | 16 | -0.044191 | -7.266 |
| w32 | 18 | 0.132848 | 67.203 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 29 | 0.00998 | 28.447 |
| w25 | 23 | 0.044755 | 9.078 |
| w26 | 20 | 0.054807 | -0.029 |
| w27 | 36 | 0.016739 | 73.569 |
| w28 | 19 | 0.112883 | 7.254 |
| w29 | 20 | -0.067761 | -6.666 |
| w30 | 18 | 0.0027 | -5.351 |
| w31 | 22 | -0.038598 | -8.692 |
| w32 | 25 | 0.126862 | 36.746 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 32 | -0.049873 | 82.595 |
| w6 | 27 | 0.025289 | 14.481 |
| w7 | 14 | -0.031421 | -4.088 |
| w8 | 20 | 0.053581 | 2.913 |
| w9 | 22 | -0.017244 | -16.504 |
| w10 | 20 | 0.011918 | 1.74 |
| w11 | 19 | 0.052399 | 16.475 |
| w12 | 18 | -0.011611 | -3.196 |
| w13 | 29 | 0.056943 | 32.499 |
| w14 | 34 | -0.077811 | -4.808 |
| w15 | 27 | -0.057042 | -6.469 |
| w16 | 39 | 0.030423 | 39.927 |
| w17 | 18 | 0.108548 | 13.579 |
| w18 | 21 | 0.089337 | 26.072 |
| w19 | 17 | 0.164884 | 18.522 |
| w20 | 14 | -0.019321 | -6.112 |
| w21 | 11 | -0.046434 | -21.295 |
| w22 | 36 | -0.074228 | 14.264 |
| w23 | 10 | -0.010956 | -8.568 |
| w24 | 35 | 0.03719 | -16.872 |
| w25 | 22 | 0.004563 | 10.452 |
| w26 | 30 | 0.072297 | 16.532 |
| w27 | 30 | -0.015007 | 17.34 |
| w28 | 21 | 0.003466 | 1.057 |
| w29 | 31 | 0.026308 | 11.552 |
| w30 | 34 | 0.290959 | 132.724 |
| w31 | 16 | 0.062245 | 2.685 |
| w32 | 25 | 0.140192 | 37.798 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 29 | 0.024106 | 90.543 |
| w6 | 19 | 0.008981 | 24.274 |
| w7 | 18 | -0.134622 | -8.172 |
| w8 | 19 | 0.038637 | -6.573 |
| w9 | 21 | 0.035968 | -1.768 |
| w10 | 21 | -0.034021 | 9.558 |
| w11 | 29 | 0.058082 | 19.936 |
| w12 | 17 | -0.073264 | -12.996 |
| w13 | 26 | 0.060371 | 19.021 |
| w14 | 34 | -0.154102 | -8.647 |
| w15 | 39 | -0.143396 | -10.006 |
| w16 | 35 | -0.001981 | 51.694 |
| w17 | 29 | 0.102134 | 19.849 |
| w18 | 27 | -0.047253 | -19.765 |
| w19 | 29 | -0.116711 | -16.458 |
| w20 | 18 | -0.151317 | -26.325 |
| w21 | 20 | -0.028172 | -7.433 |
| w22 | 22 | 0.014565 | -9.69 |
| w23 | 22 | 0.114516 | -1.816 |
| w24 | 34 | -0.061992 | 5.476 |
| w25 | 13 | -0.004586 | -56.571 |
| w26 | 35 | 0.055103 | 29.421 |
| w27 | 16 | 0.143243 | 24.029 |
| w28 | 26 | 0.02752 | 7.236 |
| w29 | 19 | -0.136272 | -5.082 |
| w30 | 44 | -0.109116 | -5.29 |
| w31 | 24 | 0.032206 | 7.412 |
| w32 | 37 | -0.089781 | -20.28 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 28 | -0.124864 | -20.441 |
| w18 | 29 | -0.019301 | 17.454 |
| w19 | 17 | 0.062358 | -10.175 |
| w20 | 11 | -0.092289 | -20.687 |
| w21 | 14 | -0.087578 | -27.436 |
| w22 | 40 | -0.052692 | -5.994 |
| w23 | 17 | -0.054074 | -11.798 |
| w24 | 23 | 0.084002 | 30.397 |
| w25 | 25 | 0.127837 | 33.488 |
| w26 | 22 | -0.007807 | -7.462 |
| w27 | 35 | 0.023015 | 33.476 |
| w28 | 21 | -0.074051 | -12.949 |
| w29 | 20 | 0.219371 | 23.515 |
| w30 | 17 | 0.037528 | -2.835 |
| w31 | 24 | -0.003937 | -21.89 |
| w32 | 20 | 0.150359 | 38.035 |

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
| w17 | 21 | -0.003522 | -1.228 |
| w18 | 24 | 0.105094 | 1.944 |
| w19 | 23 | 0.028027 | -6.555 |
| w20 | 25 | 0.149391 | 13.461 |
| w21 | 20 | -0.164648 | -37.554 |
| w22 | 29 | 0.087422 | 18.102 |
| w23 | 16 | -0.14138 | -5.599 |
| w24 | 36 | 0.061968 | 33.63 |
| w25 | 26 | 0.214568 | 36.771 |
| w26 | 18 | -0.00635 | 12.701 |
| w27 | 32 | -0.10479 | -4.102 |
| w28 | 15 | 0.027919 | -1.576 |
| w29 | 38 | -0.012943 | -5.202 |
| w30 | 7 | -0.077203 | -4.322 |
| w31 | 16 | 0.029104 | 1.579 |
| w32 | 21 | 0.243229 | 36.329 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 19 | -0.109664 | -19.174 |
| w20 | 16 | -0.072057 | -12.49 |
| w21 | 26 | -0.0067 | -5.792 |
| w22 | 41 | -0.101239 | 53.527 |
| w23 | 28 | 0.053635 | -6.69 |
| w24 | 43 | 0.105741 | 112.637 |
| w25 | 24 | -0.097532 | -13.09 |
| w26 | 15 | 0.042549 | -4.898 |
| w27 | 27 | 0.084361 | 36.272 |
| w28 | 16 | -0.092083 | -24.023 |
| w29 | 29 | 0.015907 | -9.23 |
| w30 | 9 | -0.092375 | -8.406 |
| w31 | 27 | 0.039718 | 3.867 |
| w32 | 23 | 0.044942 | 30.652 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 33 | -0.126728 | -1.765 |
| w23 | 23 | 0.04508 | -2.979 |
| w24 | 37 | -0.041808 | 0.756 |
| w25 | 27 | -0.122567 | -22.426 |
| w26 | 17 | 0.13466 | 17.317 |
| w27 | 21 | -0.071453 | -9.142 |
| w28 | 23 | 0.005768 | 2.568 |
| w29 | 21 | 0.160421 | 6.072 |
| w30 | 14 | -0.117021 | -14.773 |
| w31 | 27 | -0.050523 | -14.094 |
| w32 | 27 | 0.055471 | 21.238 |

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
| w27 | 26 | 0.066843 | 16.209 |
| w28 | 22 | -0.154565 | -21.798 |
| w29 | 27 | 0.088062 | -14.711 |
| w30 | 8 | 0.006185 | -7.482 |
| w31 | 18 | -0.09327 | -21.388 |
| w32 | 25 | 0.221641 | 81.453 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 20 | 0.011686 | -7.611 |
| w18 | 15 | 0.033122 | 2.997 |
| w19 | 15 | 0.057604 | -8.852 |
| w20 | 10 | 0.059947 | 14.949 |
| w21 | 15 | -0.01999 | -11.918 |
| w22 | 28 | 0.089895 | 16.732 |
| w23 | 16 | -0.117278 | -38.346 |
| w24 | 33 | -0.062538 | 15.077 |
| w25 | 20 | 0.170577 | 32.075 |
| w26 | 19 | 0.031302 | -1.644 |
| w27 | 36 | 0.020178 | 18.903 |
| w28 | 15 | 0.032695 | -14.624 |
| w29 | 22 | 0.026854 | -16.263 |
| w30 | 16 | 0.165368 | 6.237 |
| w31 | 14 | -0.122002 | -20.711 |
| w32 | 13 | -0.059061 | 0.694 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 25 | 0.036424 | 16.416 |
| w18 | 22 | -0.123642 | -32.876 |
| w19 | 15 | 0.086639 | -9.318 |
| w20 | 16 | 0.035127 | 0.908 |
| w21 | 19 | -0.008755 | -11.719 |
| w22 | 29 | 0.019191 | 50.74 |
| w23 | 22 | 0.153084 | -7.083 |
| w24 | 23 | -0.055685 | 9.469 |
| w25 | 23 | 0.129718 | 17.282 |
| w26 | 24 | -0.035033 | -14.007 |
| w27 | 27 | 0.100927 | 34.48 |
| w28 | 9 | -0.215749 | -16.743 |
| w29 | 24 | 0.086275 | 2.885 |
| w30 | 8 | -0.023832 | -1.284 |
| w31 | 16 | -0.169522 | -17.682 |
| w32 | 22 | 0.186827 | 30.796 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 22 | 0.069488 | -3.426 |
| w29 | 25 | -0.058114 | -21.739 |
| w30 | 20 | 0.055099 | 9.115 |
| w31 | 31 | 0.009911 | 19.852 |
| w32 | 25 | 0.021396 | -6.82 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 18 | 0.252008 | 84.346 |
| w15 | 23 | 0.14237 | 47.182 |
| w16 | 20 | 0.03448 | 151.904 |
| w17 | 18 | -0.050759 | -1.899 |
| w18 | 12 | -0.102693 | -16.166 |
| w19 | 24 | -0.009462 | -8.043 |
| w20 | 14 | -0.038373 | -5.879 |
| w21 | 13 | 0.259348 | 111.182 |
| w22 | 37 | 0.057498 | 13.617 |
| w23 | 17 | 0.02606 | -4.815 |
| w24 | 26 | -0.002511 | -0.597 |
| w25 | 23 | 0.170345 | 46.75 |
| w26 | 21 | 0.014501 | -12.478 |
| w27 | 31 | 0.23666 | 93.9 |
| w28 | 19 | -0.100106 | -15.4 |
| w29 | 29 | 0.099395 | 26.599 |
| w30 | 11 | -0.033252 | -5.354 |
| w31 | 20 | -0.005741 | 0.177 |
| w32 | 25 | 0.234214 | 13.99 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 30 | 0.230874 | 108.847 |
| w26 | 16 | -0.035172 | -3.345 |
| w27 | 30 | 0.213164 | 66.391 |
| w28 | 16 | -0.265818 | -25.286 |
| w29 | 30 | 0.10432 | -3.64 |
| w30 | 12 | -0.012504 | -5.721 |
| w31 | 20 | 0.034915 | 12.104 |
| w32 | 30 | 0.17849 | 13.931 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

