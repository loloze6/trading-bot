# Backtest of 013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d

- Plan: `../../../../../03_test_plan/volume_run/plans/013-01_nearness-to-high-predicts-gains.d2_nearness-with-rising-month.d2_nearness-without-the-short-side.e1_heavy-volume-rising-follow-through_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.02746 | 1.297 |
| w2 | 43 | 0.064207 | 29.863 |
| w3 | 80 | 0.050002 | 86.415 |
| w4 | 57 | -0.216577 | -36.515 |
| w5 | 72 | 0.063653 | 81.26 |
| w6 | 71 | 0.018848 | 61.995 |
| w7 | 22 | -0.10848 | -12.906 |
| w8 | 31 | -0.019414 | -6.929 |
| w9 | 21 | -0.147379 | -30.313 |
| w10 | 58 | 0.057721 | 33.355 |
| w11 | 62 | 0.069117 | 57.644 |
| w12 | 21 | 0.048482 | 1.106 |
| w13 | 54 | -0.011955 | 5.396 |
| w14 | 64 | 0.00276 | 16.903 |
| w15 | 65 | 0.050247 | 78.626 |
| w16 | 77 | -0.014667 | 27.608 |
| w17 | 32 | 0.116462 | 14.351 |
| w18 | 38 | -0.0529 | -10.897 |
| w19 | 40 | -0.029525 | -9.63 |
| w20 | 25 | 0.075663 | -1.572 |
| w21 | 29 | -0.044624 | -10.704 |
| w22 | 68 | 0.098573 | 75.585 |
| w23 | 24 | 0.103223 | 10.445 |
| w24 | 75 | 0.045065 | 45.629 |
| w25 | 51 | -0.021728 | 10.517 |
| w26 | 41 | -0.166657 | -29.326 |
| w27 | 67 | 0.039009 | 55.106 |
| w28 | 32 | -0.123199 | -17.707 |
| w29 | 62 | 0.024406 | 4.743 |
| w30 | 19 | -0.062485 | -15.175 |
| w31 | 46 | -0.00863 | -8.788 |
| w32 | 42 | 0.092789 | 12.856 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 24 | 0.085624 | 25.476 |
| w2 | 39 | -0.17367 | -26.678 |
| w3 | 52 | -0.120566 | -25.246 |
| w4 | 47 | -0.019979 | 16.918 |
| w5 | 74 | 0.130535 | 57.736 |
| w6 | 65 | 0.093998 | 55.281 |
| w7 | 27 | -0.119422 | -17.397 |
| w8 | 18 | -0.00833 | -8.492 |
| w9 | 18 | -0.063714 | -11.392 |
| w10 | 68 | -0.11592 | 1.382 |
| w11 | 41 | -0.027755 | -6.817 |
| w12 | 18 | -0.050414 | -11.14 |
| w13 | 53 | 0.013395 | 13.211 |
| w14 | 55 | -0.025489 | 12.749 |
| w15 | 44 | 0.098992 | 52.157 |
| w16 | 57 | -0.167242 | -5.89 |
| w17 | 38 | 0.080629 | 16.913 |
| w18 | 35 | 0.082849 | 12.528 |
| w19 | 33 | -0.064453 | -11.579 |
| w20 | 24 | -0.013585 | -14.243 |
| w21 | 46 | 0.023281 | 3.676 |
| w22 | 53 | -0.042892 | -1.215 |
| w23 | 29 | -0.063624 | -11.721 |
| w24 | 60 | -0.009597 | 3.672 |
| w25 | 47 | 0.023535 | 12.513 |
| w26 | 20 | -0.149777 | -17.763 |
| w27 | 59 | 0.02111 | 36.711 |
| w28 | 28 | -0.097895 | -15.255 |
| w29 | 42 | 0.133431 | 41.098 |
| w30 | 13 | -0.252009 | -33.036 |
| w31 | 31 | -0.057924 | -15.872 |
| w32 | 38 | 0.049057 | 0.082 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 53 | 0.115655 | 102.557 |
| w7 | 33 | 0.00852 | -5.392 |
| w8 | 12 | -0.041991 | -4.433 |
| w9 | 29 | 0.161707 | 23.183 |
| w10 | 42 | -0.141059 | -18.519 |
| w11 | 30 | -0.121233 | -15.615 |
| w12 | 22 | -0.060597 | -12.447 |
| w13 | 44 | 0.025942 | 11.485 |
| w14 | 53 | 0.137567 | 41.263 |
| w15 | 38 | 0.196618 | 136.271 |
| w16 | 51 | -0.001575 | 36.213 |
| w17 | 32 | 0.062542 | 15.932 |
| w18 | 36 | -0.121963 | -21.439 |
| w19 | 39 | 0.08161 | 1.815 |
| w20 | 24 | 0.070529 | 2.694 |
| w21 | 28 | 0.079605 | 23.063 |
| w22 | 43 | -0.100333 | -9.51 |
| w23 | 44 | -0.08851 | -15.627 |
| w24 | 47 | -0.110366 | -9.346 |
| w25 | 27 | -0.069051 | -15.679 |
| w26 | 38 | 0.030371 | 4.396 |
| w27 | 30 | 0.152114 | 145.002 |
| w28 | 29 | -0.01648 | -4.334 |
| w29 | 51 | 0.110938 | 44.118 |
| w30 | 12 | -0.109243 | -14.978 |
| w31 | 31 | -0.084612 | -21.664 |
| w32 | 27 | 0.065286 | 5.447 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 12 | -0.090125 | -7.876 |
| w8 | 17 | -0.036594 | -7.791 |
| w9 | 12 | -0.087774 | -25.333 |
| w10 | 47 | 0.053479 | 25.392 |
| w11 | 37 | -0.116496 | -17.994 |
| w12 | 21 | 0.000841 | -4.866 |
| w13 | 41 | -0.062316 | 0.37 |
| w14 | 51 | -0.084685 | -3.61 |
| w15 | 50 | 0.011733 | 5.481 |
| w16 | 64 | -0.077673 | 21.909 |
| w17 | 41 | 0.047981 | 8.337 |
| w18 | 30 | -0.003142 | -9.376 |
| w19 | 29 | 0.12966 | 8.535 |
| w20 | 23 | 0.092397 | 3.367 |
| w21 | 20 | -0.208408 | -27.95 |
| w22 | 39 | 0.012054 | 4.022 |
| w23 | 12 | 0.333051 | 59.368 |
| w24 | 60 | -0.031625 | 0.018 |
| w25 | 53 | 0.092937 | 48.189 |
| w26 | 30 | -0.030119 | -13.216 |
| w27 | 52 | -0.054209 | -5.286 |
| w28 | 25 | -0.188283 | -26.448 |
| w29 | 65 | -0.05382 | 0.87 |
| w30 | 47 | 0.026167 | 1.768 |
| w31 | 22 | -0.061814 | -10.986 |
| w32 | 29 | -0.051173 | -19.884 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 56 | 0.153573 | 92.081 |
| w2 | 38 | -0.048646 | -5.217 |
| w3 | 23 | 0.038796 | -6.003 |
| w4 | 56 | 0.1368 | 186.936 |
| w5 | 59 | 0.085703 | 65.048 |
| w6 | 58 | 0.014617 | 40.048 |
| w7 | 34 | -0.030074 | -1.684 |
| w8 | 20 | -0.06192 | -9.238 |
| w9 | 15 | -0.087486 | -12.837 |
| w10 | 54 | 0.015976 | 6.393 |
| w11 | 30 | 0.067002 | 15.171 |
| w12 | 31 | -0.048114 | -13.625 |
| w13 | 53 | 0.012083 | 24.717 |
| w14 | 82 | 0.139155 | 86.246 |
| w15 | 53 | 0.042343 | 31.423 |
| w16 | 79 | 0.08535 | 101.224 |
| w17 | 50 | 0.10193 | 36.3 |
| w18 | 52 | 0.007156 | -0.613 |
| w19 | 36 | 0.138286 | 14.872 |
| w20 | 28 | 0.091395 | 6.225 |
| w21 | 27 | -0.062881 | -12.47 |
| w22 | 69 | 0.104283 | 51.706 |
| w23 | 34 | -0.121506 | -17.982 |
| w24 | 59 | -0.117735 | -5.225 |
| w25 | 45 | 0.075991 | 27.907 |
| w26 | 21 | 0.025936 | -2.153 |
| w27 | 54 | -0.143183 | -11.783 |
| w28 | 1 | -0.047881 | -2.003 |
| w29 | 58 | 0.173959 | 113.929 |
| w30 | 24 | -0.109346 | -14.418 |
| w31 | 54 | -0.098963 | -26.098 |
| w32 | 50 | 0.131469 | 29.553 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 50 | -0.04764 | 9.273 |
| w11 | 30 | -0.079025 | -14.633 |
| w12 | 22 | -0.015677 | -7.289 |
| w13 | 46 | 0.053877 | 21.005 |
| w14 | 72 | 0.193904 | 76.276 |
| w15 | 43 | 0.062952 | 25.219 |
| w16 | 70 | 0.096662 | 88.108 |
| w17 | 35 | 0.203589 | 100.23 |
| w18 | 12 | -0.082474 | -13.249 |
| w19 | 29 | 0.067798 | 4.918 |
| w20 | 29 | -0.083892 | -17.394 |
| w21 | 4 | -0.065811 | -4.719 |
| w22 | 54 | 0.146102 | 51.15 |
| w23 | 22 | -0.079821 | -9.167 |
| w24 | 58 | 0.148261 | 101.6 |
| w25 | 42 | 0.024132 | -5.222 |
| w26 | 22 | -0.135232 | -22.266 |
| w27 | 53 | 0.081725 | 60.117 |
| w28 | 25 | -0.169548 | -18.314 |
| w29 | 58 | 0.108927 | 26.752 |
| w30 | 12 | 0.016037 | -6.071 |
| w31 | 16 | -0.212018 | -19.883 |
| w32 | 41 | 0.14166 | 15.197 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 59 | -0.185064 | -25.028 |
| w13 | 46 | 0.029844 | -5.676 |
| w14 | 64 | -0.01496 | 24.37 |
| w15 | 39 | -0.139003 | -21.592 |
| w16 | 64 | -0.042114 | 16.502 |
| w17 | 36 | 0.040058 | 20.335 |
| w18 | 34 | -0.00581 | 0.627 |
| w19 | 26 | -0.071825 | -15.897 |
| w20 | 35 | 0.058669 | 3.632 |
| w21 | 37 | 0.009321 | -6.236 |
| w22 | 44 | 0.129617 | 25.321 |
| w23 | 10 | 0.038101 | -1.671 |
| w24 | 51 | 0.042788 | 21.896 |
| w25 | 34 | 0.082564 | 9.486 |
| w26 | 11 | -0.068104 | -9.536 |
| w27 | 39 | 0.073312 | 21.162 |
| w28 | 11 | 0.005033 | -4.632 |
| w29 | 50 | -0.057993 | -17.268 |
| w30 | 10 | -0.093555 | -13.953 |
| w31 | 28 | 0.006856 | -3.767 |
| w32 | 32 | 0.047397 | -2.488 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 33 | -0.047115 | -10.371 |
| w16 | 72 | 0.002697 | 32.358 |
| w17 | 29 | 0.048816 | 11.225 |
| w18 | 36 | 0.070059 | 20.234 |
| w19 | 19 | -0.004689 | -9.988 |
| w20 | 25 | 0.036972 | -3.897 |
| w21 | 20 | 0.052188 | -0.018 |
| w22 | 35 | -0.059904 | -11.783 |
| w23 | 7 | -0.140517 | -14.031 |
| w24 | 59 | 0.05616 | 43.988 |
| w25 | 33 | 0.101895 | 17.994 |
| w26 | 14 | -0.200144 | -22.572 |
| w27 | 44 | 0.031688 | 44.676 |
| w28 | 19 | 0.049552 | 1.903 |
| w29 | 37 | 0.021448 | 6.858 |
| w30 | 4 | -0.176425 | -10.3 |
| w31 | 28 | -0.0435 | -15.782 |
| w32 | 30 | 0.050834 | -0.742 |

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
| w15 | 24 | -0.112111 | -29.774 |
| w16 | 68 | 0.006001 | 53.783 |
| w17 | 23 | 0.036844 | 8.131 |
| w18 | 46 | -0.023547 | -11.22 |
| w19 | 28 | 0.085694 | 9.267 |
| w20 | 36 | -0.113111 | -24.487 |
| w21 | 33 | -0.039358 | -14.252 |
| w22 | 62 | -0.06435 | -2.777 |
| w23 | 58 | 0.003964 | 0.509 |
| w24 | 83 | 0.173944 | 66.272 |
| w25 | 53 | 0.010881 | 3.689 |
| w26 | 61 | 0.115317 | 31.769 |
| w27 | 67 | 0.146911 | 226.851 |
| w28 | 36 | -0.023211 | -8.591 |
| w29 | 74 | -0.041924 | 18.696 |
| w30 | 21 | -0.146774 | -18.834 |
| w31 | 64 | 0.085954 | 19.497 |
| w32 | 66 | 0.03985 | -2.905 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 64 | 0.013316 | 23.841 |
| w17 | 33 | 0.014724 | 5.971 |
| w18 | 47 | -0.049726 | -11.515 |
| w19 | 31 | -0.092044 | -23.197 |
| w20 | 22 | -0.051474 | -14.197 |
| w21 | 8 | -0.09365 | -15.008 |
| w22 | 45 | -0.073882 | -5.804 |
| w23 | 15 | -0.004094 | -5.851 |
| w24 | 44 | 0.106849 | 39.399 |
| w25 | 40 | 0.062299 | 1.885 |
| w26 | 23 | -0.103685 | -20.449 |
| w27 | 41 | 0.075977 | 28.705 |
| w28 | 4 | -0.203163 | -10.078 |
| w29 | 39 | 0.028853 | -0.319 |
| w30 | 23 | 0.023478 | -5.425 |
| w31 | 28 | -0.119897 | -18.651 |
| w32 | 15 | 0.096021 | 5.377 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 28 | 0.080033 | 3.58 |
| w21 | 11 | -0.129079 | -23.18 |
| w22 | 48 | -0.04695 | 1.551 |
| w23 | 13 | 0.107578 | 5.15 |
| w24 | 41 | 0.322115 | 179.741 |
| w25 | 46 | 0.076975 | 12.411 |
| w26 | 20 | -0.136269 | -21.697 |
| w27 | 64 | 0.127967 | 58.162 |
| w28 | 18 | 0.01216 | -2.025 |
| w29 | 50 | -0.001198 | -0.985 |
| w30 | 22 | 0.078584 | 5.623 |
| w31 | 29 | -0.089708 | -18.404 |
| w32 | 21 | 0.06174 | 4.93 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 41 | 0.022771 | 16.042 |
| w23 | 15 | 0.026914 | -2.288 |
| w24 | 43 | 0.209448 | 145.888 |
| w25 | 53 | -0.023417 | 13.761 |
| w26 | 38 | -0.022398 | -5.302 |
| w27 | 44 | 0.015634 | 9.996 |
| w28 | 4 | -0.107677 | -10.128 |
| w29 | 43 | 0.063393 | 8.288 |
| w30 | 25 | -0.130935 | -22.206 |
| w31 | 44 | -0.099602 | -18.414 |
| w32 | 34 | 0.048331 | 50.328 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 35 | 0.046746 | 20.684 |
| w25 | 55 | -0.041105 | 0.016 |
| w26 | 23 | -0.118038 | -16.482 |
| w27 | 74 | 0.137628 | 82.009 |
| w28 | 23 | 0.088756 | 11.642 |
| w29 | 45 | -0.040956 | -3.379 |
| w30 | 17 | 0.015717 | -4.81 |
| w31 | 31 | -0.097257 | -21.262 |
| w32 | 33 | -0.034484 | -10.766 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 55 | 0.039884 | 49.709 |
| w6 | 53 | 0.089072 | 31.561 |
| w7 | 24 | -0.081346 | -11.376 |
| w8 | 30 | -0.025307 | -10.743 |
| w9 | 13 | -0.115987 | -23.006 |
| w10 | 43 | -0.01561 | -2.122 |
| w11 | 36 | 0.023255 | 0.616 |
| w12 | 8 | 0.018192 | -0.88 |
| w13 | 38 | 0.082641 | 50.13 |
| w14 | 68 | -0.013854 | 17.522 |
| w15 | 42 | -0.000465 | -5.897 |
| w16 | 61 | 0.045198 | 44.064 |
| w17 | 32 | 0.153709 | 34.322 |
| w18 | 37 | 0.14534 | 42.711 |
| w19 | 33 | 0.120809 | 17.524 |
| w20 | 19 | -0.037479 | -10.342 |
| w21 | 9 | -0.05994 | -7.572 |
| w22 | 36 | 0.022706 | 0.31 |
| w23 | 23 | -0.058543 | -9.446 |
| w24 | 66 | -0.066259 | -9.77 |
| w25 | 21 | -0.082285 | -12.324 |
| w26 | 46 | 0.024278 | 8.767 |
| w27 | 57 | 0.068599 | 42.562 |
| w28 | 24 | 0.041991 | 1.511 |
| w29 | 51 | 0.00523 | -0.544 |
| w30 | 52 | 0.26793 | 190.974 |
| w31 | 32 | 0.031461 | 2.768 |
| w32 | 58 | 0.058469 | 49.026 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 61 | 0.116764 | 131.549 |
| w6 | 45 | 0.044186 | 32.743 |
| w7 | 31 | -0.153504 | -21.322 |
| w8 | 24 | -0.003109 | -6.591 |
| w9 | 28 | -0.050299 | -19.012 |
| w10 | 53 | -0.033411 | 4.083 |
| w11 | 55 | -0.03221 | -6.134 |
| w12 | 15 | -0.084634 | -10.856 |
| w13 | 52 | -0.004562 | 10.212 |
| w14 | 72 | -0.105571 | -0.343 |
| w15 | 66 | -0.122349 | -9.519 |
| w16 | 54 | 0.03465 | 48.96 |
| w17 | 34 | 0.026467 | 9.034 |
| w18 | 32 | -0.13601 | -21.528 |
| w19 | 48 | -0.103513 | -20.012 |
| w20 | 32 | -0.182239 | -34.941 |
| w21 | 34 | -0.061198 | -9.988 |
| w22 | 43 | 0.075309 | 11.256 |
| w23 | 20 | 0.08905 | 6.312 |
| w24 | 80 | -0.042954 | -0.901 |
| w25 | 21 | -0.067395 | -13.667 |
| w26 | 46 | 0.039473 | 12.843 |
| w27 | 38 | 0.013155 | 4.808 |
| w28 | 56 | -0.072147 | 2.462 |
| w29 | 39 | -0.07418 | -12.473 |
| w30 | 71 | -0.089281 | 5.78 |
| w31 | 40 | -0.047084 | -12.043 |
| w32 | 52 | -0.018895 | 8.585 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 31 | -0.086402 | -17.272 |
| w18 | 68 | 0.004789 | 16.794 |
| w19 | 27 | -0.018019 | -12.638 |
| w20 | 30 | 0.07266 | 5.636 |
| w21 | 14 | -0.187575 | -28.043 |
| w22 | 44 | -0.037827 | 4.827 |
| w23 | 12 | -0.126501 | -12.109 |
| w24 | 54 | -0.025748 | 0.507 |
| w25 | 27 | 0.18004 | 30.145 |
| w26 | 29 | -0.107034 | -22.16 |
| w27 | 40 | 0.229055 | 89.866 |
| w28 | 27 | 0.047104 | 3.725 |
| w29 | 37 | 0.198723 | 46.912 |
| w30 | 4 | -0.117605 | -8.011 |
| w31 | 23 | -0.1503 | -21.769 |
| w32 | 37 | 0.0857 | 34.448 |

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
| w17 | 53 | 0.011983 | -2.631 |
| w18 | 26 | -0.178718 | -27.589 |
| w19 | 38 | 0.060045 | 3.563 |
| w20 | 28 | -0.03052 | -8.09 |
| w21 | 19 | -0.041675 | -13.107 |
| w22 | 37 | 0.029918 | 16.014 |
| w23 | 15 | -0.180313 | -16.76 |
| w24 | 59 | 0.054278 | 55.483 |
| w25 | 31 | 0.111579 | 20.908 |
| w26 | 44 | -0.047989 | 2.485 |
| w27 | 74 | -0.027607 | 21.679 |
| w28 | 10 | -0.054686 | -6.166 |
| w29 | 59 | -0.101292 | -1.882 |
| w30 | 16 | -0.136881 | -17.942 |
| w31 | 11 | -0.090988 | -8.102 |
| w32 | 37 | 0.043092 | 12.259 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 28 | -0.111727 | -19.455 |
| w20 | 20 | 0.017734 | -1.673 |
| w21 | 30 | 0.008331 | -1.564 |
| w22 | 55 | -0.070324 | 40.668 |
| w23 | 35 | -0.001905 | -2.189 |
| w24 | 64 | 0.130348 | 167.415 |
| w25 | 42 | -0.04017 | -11.661 |
| w26 | 18 | -0.00979 | -6.071 |
| w27 | 60 | 0.066066 | 16.619 |
| w28 | 7 | 0.004982 | -1.659 |
| w29 | 56 | -0.001918 | 4.012 |
| w30 | 11 | -0.034827 | -8.185 |
| w31 | 26 | -0.135917 | -23.77 |
| w32 | 49 | -0.075086 | -0.655 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 57 | -0.081383 | -4.122 |
| w23 | 25 | -0.068495 | -11.783 |
| w24 | 35 | -0.106951 | -8.609 |
| w25 | 36 | -0.043515 | -19.234 |
| w26 | 16 | 0.12146 | 13.693 |
| w27 | 43 | -0.130238 | -16.153 |
| w28 | 16 | -0.178742 | -18.794 |
| w29 | 43 | 0.107184 | 34.471 |
| w30 | 10 | -0.149536 | -12.505 |
| w31 | 33 | 0.022982 | -7.829 |
| w32 | 30 | 0.017502 | 2.003 |

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
| w27 | 54 | 0.02904 | 20.189 |
| w28 | 20 | -0.030069 | -5.743 |
| w29 | 40 | 0.107808 | 16.455 |
| w30 | 17 | 0.017241 | -6.216 |
| w31 | 29 | -0.060492 | -14.211 |
| w32 | 43 | 0.054993 | 38.961 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 19 | 0.045316 | 0.628 |
| w18 | 16 | 0.08263 | 11.835 |
| w19 | 21 | 0.133329 | 11.012 |
| w20 | 15 | 0.152863 | 23.541 |
| w21 | 5 | -0.066487 | -8.906 |
| w22 | 44 | 0.142417 | 42.288 |
| w23 | 14 | -0.054957 | -7.196 |
| w24 | 53 | 0.004462 | 40.604 |
| w25 | 34 | 0.149924 | 29.131 |
| w26 | 20 | -0.13566 | -18.196 |
| w27 | 52 | 0.02466 | 14.854 |
| w28 | 6 | -0.164405 | -8.497 |
| w29 | 36 | -0.051188 | -17.33 |
| w30 | 19 | -0.15178 | -21.669 |
| w31 | 25 | -0.090122 | -19.831 |
| w32 | 24 | -0.130011 | -24.362 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 24 | 0.117112 | 17.677 |
| w18 | 28 | -0.073571 | -18.511 |
| w19 | 16 | 0.095594 | 3.835 |
| w20 | 23 | 0.03131 | -5.204 |
| w21 | 6 | -0.02632 | -2.489 |
| w22 | 36 | 0.088541 | 78.475 |
| w23 | 19 | -0.080004 | -13.259 |
| w24 | 42 | 0.028054 | 25.315 |
| w25 | 42 | 0.115854 | 37.413 |
| w26 | 21 | 0.019657 | -2.057 |
| w27 | 50 | -0.021268 | 1.12 |
| w28 | 5 | -0.201422 | -13.847 |
| w29 | 43 | 0.043705 | 2.967 |
| w30 | 8 | -0.092041 | -10.139 |
| w31 | 18 | -0.285839 | -30.294 |
| w32 | 23 | 0.041826 | -4.8 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 17 | 0.057352 | 3.661 |
| w29 | 44 | -0.016196 | -7.335 |
| w30 | 27 | -0.086051 | -19.81 |
| w31 | 38 | 0.000648 | -0.99 |
| w32 | 31 | -0.031589 | -5.622 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 44 | 0.146305 | 70.022 |
| w15 | 31 | 0.162055 | 70.87 |
| w16 | 39 | 0.022895 | 219.018 |
| w17 | 26 | 0.014743 | 4.748 |
| w18 | 24 | 0.04012 | -0.028 |
| w19 | 24 | -0.025045 | -10.014 |
| w20 | 20 | 0.046356 | -1.493 |
| w21 | 26 | 0.223943 | 101.743 |
| w22 | 41 | -0.069947 | -7.463 |
| w23 | 21 | 0.004284 | -6.069 |
| w24 | 40 | 0.107882 | 36.468 |
| w25 | 33 | 0.162523 | 83.492 |
| w26 | 22 | -0.075836 | -14.064 |
| w27 | 57 | 0.151497 | 100.097 |
| w28 | 13 | -0.12532 | -17.833 |
| w29 | 44 | 0.051846 | 19.566 |
| w30 | 25 | -0.063807 | -19.095 |
| w31 | 29 | -0.044235 | -7.562 |
| w32 | 30 | 0.16496 | 22.151 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 27 | 0.335525 | 137.732 |
| w26 | 34 | 0.07173 | 11.47 |
| w27 | 47 | 0.126239 | 57.591 |
| w28 | 20 | -0.074176 | -13.609 |
| w29 | 43 | 0.118559 | 21.94 |
| w30 | 8 | -0.091458 | -13.571 |
| w31 | 33 | 0.127998 | 16.321 |
| w32 | 40 | 0.076033 | 5.522 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

