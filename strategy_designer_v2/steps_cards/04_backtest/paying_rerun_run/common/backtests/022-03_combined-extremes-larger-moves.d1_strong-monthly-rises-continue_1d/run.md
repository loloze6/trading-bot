# Backtest of 022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-03_combined-extremes-larger-moves.d1_strong-monthly-rises-continue_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.030245 | 4.342 |
| w2 | 22 | 0.077594 | 54.08 |
| w3 | 41 | -0.002057 | 79.72 |
| w4 | 37 | -0.151227 | -23.506 |
| w5 | 28 | 0.056254 | 128.755 |
| w6 | 35 | 0.016746 | 94.625 |
| w7 | 18 | -0.111576 | -11.539 |
| w8 | 17 | -0.024593 | -6.92 |
| w9 | 13 | -0.097015 | -14.068 |
| w10 | 29 | 0.018523 | 34.503 |
| w11 | 42 | -0.033716 | 24.508 |
| w12 | 16 | -0.050692 | -10.524 |
| w13 | 34 | -0.005911 | 19.367 |
| w14 | 29 | 0.019129 | 30.64 |
| w15 | 24 | 0.133101 | 147.799 |
| w16 | 31 | -0.05652 | 18.125 |
| w17 | 19 | 0.09978 | 16.364 |
| w18 | 19 | 0.055569 | 7.883 |
| w19 | 28 | -0.108638 | -18.937 |
| w20 | 17 | 0.05753 | -2.981 |
| w21 | 23 | -0.141979 | -27.016 |
| w22 | 25 | -0.047628 | 47.803 |
| w23 | 11 | 0.036502 | 2.137 |
| w24 | 37 | 0.036645 | 62.708 |
| w25 | 13 | 0.11721 | 53.917 |
| w26 | 23 | -0.149862 | -21.077 |
| w27 | 41 | 0.034272 | 63.924 |
| w28 | 15 | -0.048339 | -5.966 |
| w29 | 37 | 0.007689 | 3.726 |
| w30 | 13 | 0.023395 | -3.36 |
| w31 | 28 | -0.054904 | -12.837 |
| w32 | 27 | 0.095414 | 15.816 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.05048 | 11.388 |
| w2 | 17 | 0.025159 | 11.762 |
| w3 | 40 | -0.16595 | -29.154 |
| w4 | 31 | 0.130227 | 114.361 |
| w5 | 42 | -0.050697 | 28.867 |
| w6 | 26 | 0.03741 | 75.3 |
| w7 | 17 | -0.077697 | -7.776 |
| w8 | 10 | -0.007742 | -6.238 |
| w9 | 10 | -0.137657 | -8.966 |
| w10 | 37 | -0.075389 | 20.238 |
| w11 | 25 | 0.084703 | 11.902 |
| w12 | 12 | -0.094191 | -12.442 |
| w13 | 30 | 0.027048 | 26.167 |
| w14 | 21 | 0.019569 | 25.105 |
| w15 | 32 | 0.040376 | 52.68 |
| w16 | 43 | -0.12264 | 7.435 |
| w17 | 22 | 0.02198 | 7.685 |
| w18 | 29 | 0.038135 | 3.815 |
| w19 | 22 | -0.075883 | -15.135 |
| w20 | 16 | 0.017572 | -2.06 |
| w21 | 28 | -0.081908 | -8.387 |
| w22 | 41 | -0.055793 | -2.63 |
| w23 | 25 | -0.159741 | -31.185 |
| w24 | 32 | -0.162677 | -16.83 |
| w25 | 32 | 0.055931 | 30.132 |
| w26 | 11 | -0.165294 | -9.362 |
| w27 | 51 | 0.015474 | 48.659 |
| w28 | 22 | -0.20732 | -14.526 |
| w29 | 30 | 0.046499 | 27.324 |
| w30 | 13 | -0.23969 | -24.131 |
| w31 | 15 | -0.038622 | -5.852 |
| w32 | 31 | -0.088224 | -17.019 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 34 | 0.160459 | 121.634 |
| w7 | 14 | -0.042143 | -8.764 |
| w8 | 6 | -0.029542 | -6.046 |
| w9 | 14 | -0.024343 | -9.905 |
| w10 | 37 | -0.201711 | -18.542 |
| w11 | 12 | 0.010764 | 1.874 |
| w12 | 26 | -0.04032 | -11.875 |
| w13 | 35 | -0.039142 | 1.247 |
| w14 | 30 | 0.117728 | 48.517 |
| w15 | 17 | 0.193075 | 150.032 |
| w16 | 27 | -0.034687 | 52.236 |
| w17 | 16 | 0.072217 | 22.375 |
| w18 | 20 | -0.116656 | -11.201 |
| w19 | 31 | -0.138326 | -19.553 |
| w20 | 15 | 0.049855 | 1.374 |
| w21 | 14 | 0.053668 | 26.53 |
| w22 | 21 | -0.075312 | 2.019 |
| w23 | 19 | -0.111247 | -18.109 |
| w24 | 22 | -0.031002 | 6.416 |
| w25 | 24 | 0.01641 | 4.158 |
| w26 | 13 | -0.032282 | -4.241 |
| w27 | 22 | 0.308736 | 232.075 |
| w28 | 8 | -0.256166 | -9.953 |
| w29 | 34 | 0.034436 | 35.309 |
| w30 | 6 | -0.012557 | -2.17 |
| w31 | 24 | -0.145172 | -20.639 |
| w32 | 16 | 0.055048 | 5.74 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | -0.014675 | -4.74 |
| w8 | 11 | 0.023191 | -5.72 |
| w9 | 11 | -0.113992 | -22.332 |
| w10 | 34 | 0.049327 | 41.023 |
| w11 | 18 | -0.106212 | -7.903 |
| w12 | 13 | -0.036996 | -7.371 |
| w13 | 25 | 0.061944 | 40.807 |
| w14 | 17 | 0.02834 | 12.016 |
| w15 | 41 | -0.10415 | -9.769 |
| w16 | 33 | -0.021079 | 58.342 |
| w17 | 19 | 0.043442 | 21.379 |
| w18 | 22 | -0.106607 | -19.012 |
| w19 | 24 | -0.07799 | -16.079 |
| w20 | 16 | 0.023975 | -7.09 |
| w21 | 14 | -0.193514 | -19.144 |
| w22 | 25 | -0.007377 | 9.964 |
| w23 | 7 | 0.164335 | 71.385 |
| w24 | 41 | -0.172116 | -6.549 |
| w25 | 33 | 0.056942 | 66.013 |
| w26 | 10 | -0.283893 | -22.273 |
| w27 | 35 | 0.018112 | 14.585 |
| w28 | 12 | -0.091752 | -14.76 |
| w29 | 55 | -0.127444 | 2.405 |
| w30 | 41 | -0.049968 | 1.127 |
| w31 | 14 | -0.039657 | -6.512 |
| w32 | 17 | -0.059971 | -17.321 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 27 | 0.169566 | 230.658 |
| w2 | 28 | -0.012955 | 7.537 |
| w3 | 19 | 0.057052 | -1.927 |
| w4 | 35 | 0.026716 | 265.05 |
| w5 | 30 | 0.123623 | 97.549 |
| w6 | 21 | 0.103819 | 82.66 |
| w7 | 18 | 0.097549 | 19.028 |
| w8 | 7 | 0.086778 | 1.186 |
| w9 | 8 | -0.108788 | -6.16 |
| w10 | 36 | -0.171264 | -12.893 |
| w11 | 18 | 0.084799 | 27.279 |
| w12 | 20 | -0.214752 | -16.903 |
| w13 | 33 | 0.015828 | 47.026 |
| w14 | 40 | 3.1e-05 | 56.307 |
| w15 | 37 | 0.081727 | 45.74 |
| w16 | 34 | 0.027482 | 84.537 |
| w17 | 22 | 0.011426 | 20.854 |
| w18 | 24 | 0.030716 | 5.275 |
| w19 | 22 | -0.023234 | -7.946 |
| w20 | 20 | 0.113779 | 10.549 |
| w21 | 22 | -0.106698 | -15.979 |
| w22 | 33 | -0.041804 | 29.17 |
| w23 | 16 | -0.050032 | -12.492 |
| w24 | 36 | 0.031423 | 35.246 |
| w25 | 22 | 0.053506 | 26.625 |
| w26 | 14 | -0.032943 | -15.049 |
| w27 | 33 | 0.039477 | 17.52 |
| w28 | 0 | -0.027886 | 0.0 |
| w29 | 35 | -0.027269 | 72.496 |
| w30 | 10 | -0.009228 | -4.499 |
| w31 | 35 | -0.065295 | -15.181 |
| w32 | 26 | 0.043928 | 7.335 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 38 | 0.040079 | 47.91 |
| w11 | 19 | -0.006355 | -3.412 |
| w12 | 18 | -0.076766 | -10.601 |
| w13 | 23 | 0.069453 | 54.939 |
| w14 | 46 | -0.147907 | 12.538 |
| w15 | 31 | 0.012799 | 19.494 |
| w16 | 31 | 0.089969 | 98.269 |
| w17 | 25 | 0.01337 | 49.918 |
| w18 | 7 | -0.097038 | -13.348 |
| w19 | 19 | -0.050429 | -24.86 |
| w20 | 21 | -0.035359 | -12.675 |
| w21 | 5 | -0.137678 | -4.681 |
| w22 | 31 | -0.036558 | 16.485 |
| w23 | 12 | -0.04166 | -4.377 |
| w24 | 29 | 0.066882 | 149.317 |
| w25 | 16 | 0.055243 | -1.975 |
| w26 | 17 | -0.131792 | -20.031 |
| w27 | 32 | 0.210959 | 127.61 |
| w28 | 9 | -0.267501 | -16.355 |
| w29 | 32 | -0.03846 | 9.641 |
| w30 | 11 | 0.01785 | -2.086 |
| w31 | 10 | -0.176616 | -8.979 |
| w32 | 36 | -0.074224 | -15.209 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 42 | -0.148756 | -1.686 |
| w13 | 31 | -0.084425 | -23.386 |
| w14 | 40 | -0.078171 | 22.644 |
| w15 | 32 | -0.279205 | -25.972 |
| w16 | 30 | 0.043321 | 74.396 |
| w17 | 20 | 0.048581 | 16.686 |
| w18 | 24 | 0.013226 | 9.99 |
| w19 | 20 | -0.028242 | -16.565 |
| w20 | 32 | 0.08425 | 6.56 |
| w21 | 28 | -0.129595 | -21.352 |
| w22 | 21 | 0.046303 | 16.999 |
| w23 | 9 | 0.021804 | 0.508 |
| w24 | 33 | -0.077891 | 12.894 |
| w25 | 18 | 0.07164 | 7.505 |
| w26 | 4 | 0.035521 | -0.379 |
| w27 | 25 | 0.128527 | 43.371 |
| w28 | 12 | -0.161291 | -12.622 |
| w29 | 31 | -0.119474 | -18.708 |
| w30 | 7 | 0.007083 | -4.271 |
| w31 | 17 | -0.088974 | -13.295 |
| w32 | 31 | -0.063306 | -18.506 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 22 | -0.090742 | -13.297 |
| w16 | 32 | 0.030662 | 66.87 |
| w17 | 17 | 0.007769 | 1.113 |
| w18 | 14 | 0.082844 | 37.578 |
| w19 | 20 | -0.164391 | -16.564 |
| w20 | 11 | 0.035703 | 1.222 |
| w21 | 20 | -0.080926 | -31.637 |
| w22 | 25 | 0.004838 | -4.324 |
| w23 | 5 | -0.119212 | -1.266 |
| w24 | 41 | 0.010858 | 66.266 |
| w25 | 16 | 0.089793 | 7.256 |
| w26 | 11 | -0.153835 | -10.493 |
| w27 | 34 | 0.179908 | 127.969 |
| w28 | 8 | -0.034652 | -2.702 |
| w29 | 22 | 0.042503 | 15.83 |
| w30 | 0 | None | 0.0 |
| w31 | 32 | -0.046984 | -15.121 |
| w32 | 21 | -0.143122 | -20.392 |

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
| w15 | 29 | -0.057301 | -16.549 |
| w16 | 36 | -0.065396 | 67.487 |
| w17 | 11 | 0.050711 | 13.986 |
| w18 | 39 | -0.170016 | -25.045 |
| w19 | 21 | -0.117296 | -23.17 |
| w20 | 36 | -0.076764 | -22.591 |
| w21 | 27 | -0.054627 | -13.307 |
| w22 | 38 | -0.06616 | -2.095 |
| w23 | 40 | -0.095667 | -5.524 |
| w24 | 47 | -0.069799 | 29.943 |
| w25 | 25 | 0.123848 | 34.576 |
| w26 | 42 | -0.08186 | 11.206 |
| w27 | 42 | 0.056521 | 204.386 |
| w28 | 25 | -0.042503 | -3.066 |
| w29 | 57 | 0.001529 | 50.692 |
| w30 | 11 | -0.025015 | -5.648 |
| w31 | 55 | -0.04588 | 12.659 |
| w32 | 39 | -0.08183 | -0.099 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 27 | 0.129074 | 68.94 |
| w17 | 17 | -0.044722 | -10.14 |
| w18 | 30 | -0.034673 | -9.058 |
| w19 | 16 | -0.032354 | -11.829 |
| w20 | 15 | 0.027104 | -4.196 |
| w21 | 6 | -0.201293 | -17.356 |
| w22 | 29 | -0.012528 | 9.716 |
| w23 | 15 | 0.012475 | -4.738 |
| w24 | 29 | 0.042032 | 55.357 |
| w25 | 18 | 0.042814 | -3.275 |
| w26 | 15 | -0.089869 | -10.124 |
| w27 | 25 | 0.127547 | 46.702 |
| w28 | 3 | -0.079899 | -2.398 |
| w29 | 32 | -0.022067 | -1.951 |
| w30 | 20 | -0.001461 | -16.472 |
| w31 | 21 | -0.13108 | -14.706 |
| w32 | 14 | -0.116767 | -13.903 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 23 | 0.093567 | 4.015 |
| w21 | 9 | -0.148659 | -16.024 |
| w22 | 27 | -0.005804 | 12.267 |
| w23 | 7 | 0.034017 | -2.56 |
| w24 | 27 | 0.228981 | 249.206 |
| w25 | 26 | -0.012651 | -8.247 |
| w26 | 11 | -0.132906 | -15.179 |
| w27 | 43 | -0.047138 | 16.697 |
| w28 | 4 | -0.057151 | -2.727 |
| w29 | 35 | -0.091269 | -8.819 |
| w30 | 19 | 0.045556 | 0.208 |
| w31 | 26 | -0.100045 | -14.123 |
| w32 | 21 | -0.002514 | -2.955 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 18 | -0.007717 | 9.037 |
| w23 | 11 | 0.048089 | -0.399 |
| w24 | 28 | 0.101506 | 136.459 |
| w25 | 24 | 0.089065 | 37.251 |
| w26 | 24 | -0.069604 | -14.554 |
| w27 | 37 | -0.090293 | -9.249 |
| w28 | 1 | -0.18165 | -0.926 |
| w29 | 34 | -0.012497 | 3.342 |
| w30 | 23 | -0.062818 | -17.535 |
| w31 | 29 | -0.105527 | -14.28 |
| w32 | 29 | 0.05754 | 43.635 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 30 | -0.003268 | 16.802 |
| w25 | 36 | 0.030786 | 7.124 |
| w26 | 15 | -0.110187 | -11.183 |
| w27 | 36 | -0.07216 | 71.26 |
| w28 | 10 | 0.039452 | 5.31 |
| w29 | 17 | 0.020858 | 1.56 |
| w30 | 10 | -0.010184 | -5.916 |
| w31 | 24 | -0.088908 | -13.169 |
| w32 | 33 | -0.075964 | -10.618 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 25 | 0.161369 | 118.179 |
| w6 | 34 | -0.061222 | 12.95 |
| w7 | 19 | 0.014524 | -4.049 |
| w8 | 25 | -0.041977 | -10.275 |
| w9 | 8 | -0.100284 | -18.222 |
| w10 | 28 | -0.012423 | 12.18 |
| w11 | 30 | 0.062152 | 6.972 |
| w12 | 9 | -0.143954 | -7.738 |
| w13 | 21 | 0.094306 | 70.358 |
| w14 | 45 | -0.099975 | 11.433 |
| w15 | 26 | -0.121944 | -14.21 |
| w16 | 50 | -0.232859 | 15.519 |
| w17 | 17 | 0.035346 | 11.301 |
| w18 | 29 | -0.030665 | -5.819 |
| w19 | 26 | 0.020504 | -0.024 |
| w20 | 22 | 0.016951 | -7.415 |
| w21 | 10 | -0.041516 | -4.969 |
| w22 | 37 | -0.072769 | -7.685 |
| w23 | 20 | 0.025494 | -2.798 |
| w24 | 42 | -0.113986 | -12.71 |
| w25 | 9 | 0.053512 | 7.711 |
| w26 | 33 | 0.048254 | 23.317 |
| w27 | 43 | -0.01623 | 28.73 |
| w28 | 12 | -0.139987 | -19.066 |
| w29 | 28 | -0.01543 | -3.169 |
| w30 | 23 | 0.165507 | 314.998 |
| w31 | 19 | 0.061208 | 9.362 |
| w32 | 35 | 0.05789 | 51.702 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 39 | 0.078991 | 147.615 |
| w6 | 22 | 0.068205 | 107.236 |
| w7 | 22 | -0.126811 | -17.086 |
| w8 | 13 | -0.073921 | -9.955 |
| w9 | 22 | -0.050658 | -19.853 |
| w10 | 42 | -0.073608 | 8.404 |
| w11 | 38 | -0.073025 | -5.556 |
| w12 | 10 | -0.01527 | -7.032 |
| w13 | 30 | 0.002134 | 29.574 |
| w14 | 32 | 0.009978 | 38.525 |
| w15 | 35 | -0.029368 | 14.134 |
| w16 | 33 | -0.049323 | 43.535 |
| w17 | 31 | 0.005617 | -2.378 |
| w18 | 19 | -0.135381 | -15.843 |
| w19 | 32 | -0.025705 | -15.879 |
| w20 | 24 | -0.01105 | -10.977 |
| w21 | 28 | -0.10309 | -31.71 |
| w22 | 34 | -0.020638 | -1.172 |
| w23 | 10 | 0.032299 | 2.267 |
| w24 | 52 | -0.094357 | -2.945 |
| w25 | 16 | -0.231357 | -40.331 |
| w26 | 37 | 0.007599 | 12.331 |
| w27 | 39 | -0.01655 | -6.315 |
| w28 | 41 | -0.028644 | 11.893 |
| w29 | 15 | 0.133271 | 34.281 |
| w30 | 63 | -0.159943 | 10.591 |
| w31 | 28 | -0.051786 | -5.914 |
| w32 | 37 | 0.055748 | 46.834 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 22 | -0.095512 | -15.321 |
| w18 | 36 | -0.177608 | 1.537 |
| w19 | 24 | -0.105579 | -21.365 |
| w20 | 26 | 0.064878 | 5.676 |
| w21 | 12 | -0.271306 | -28.991 |
| w22 | 17 | 0.038337 | 19.937 |
| w23 | 12 | 0.01933 | -7.431 |
| w24 | 31 | -0.139672 | -10.782 |
| w25 | 17 | 0.13332 | 25.442 |
| w26 | 22 | -0.100325 | -15.341 |
| w27 | 24 | 0.15166 | 132.942 |
| w28 | 24 | 0.024066 | 4.041 |
| w29 | 22 | 0.081297 | 23.174 |
| w30 | 0 | -0.014225 | 0.0 |
| w31 | 20 | 0.001787 | -6.065 |
| w32 | 40 | 0.104811 | 43.522 |

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
| w17 | 37 | -0.097273 | -19.296 |
| w18 | 25 | -0.069654 | -14.679 |
| w19 | 19 | -0.071646 | -10.565 |
| w20 | 28 | 0.039754 | -2.703 |
| w21 | 22 | -0.153312 | -34.473 |
| w22 | 17 | 0.011105 | 15.215 |
| w23 | 14 | 0.010286 | -5.368 |
| w24 | 40 | -0.112644 | 11.175 |
| w25 | 22 | 0.084145 | 8.95 |
| w26 | 37 | -0.131681 | -11.867 |
| w27 | 45 | 0.005049 | 54.756 |
| w28 | 3 | -0.025822 | -0.796 |
| w29 | 34 | -0.053468 | 12.622 |
| w30 | 13 | -0.042174 | -11.731 |
| w31 | 9 | -0.19776 | -14.811 |
| w32 | 23 | -0.024085 | -1.11 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 20 | -0.139223 | -14.922 |
| w20 | 22 | 0.005284 | -5.819 |
| w21 | 17 | -0.01379 | -4.513 |
| w22 | 32 | 0.040388 | 141.492 |
| w23 | 22 | -0.076501 | -7.746 |
| w24 | 40 | 0.015921 | 166.639 |
| w25 | 18 | -0.092549 | -13.573 |
| w26 | 19 | -0.038152 | -12.376 |
| w27 | 42 | -0.032703 | 6.57 |
| w28 | 3 | -0.118836 | -3.161 |
| w29 | 40 | -0.039654 | 1.015 |
| w30 | 5 | -0.038077 | -5.117 |
| w31 | 11 | -0.045228 | -9.875 |
| w32 | 19 | 0.064728 | 33.032 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 25 | 0.061218 | 24.387 |
| w23 | 20 | -0.0784 | -12.277 |
| w24 | 29 | -0.012701 | 27.804 |
| w25 | 27 | -0.058626 | -9.849 |
| w26 | 12 | -0.03914 | -2.445 |
| w27 | 29 | -0.05582 | -5.552 |
| w28 | 9 | -0.098373 | -7.354 |
| w29 | 38 | -0.050531 | 11.76 |
| w30 | 5 | -0.047931 | -3.94 |
| w31 | 25 | -0.036624 | -10.839 |
| w32 | 21 | -0.017318 | -5.548 |

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
| w27 | 34 | -0.01638 | 27.615 |
| w28 | 7 | -0.058592 | -3.971 |
| w29 | 31 | -0.026883 | 3.096 |
| w30 | 9 | -0.061531 | -12.769 |
| w31 | 10 | -0.086855 | -5.68 |
| w32 | 29 | 0.023433 | 37.791 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.054719 | 7.105 |
| w18 | 11 | -0.077423 | 0.923 |
| w19 | 16 | -0.114287 | -19.952 |
| w20 | 15 | 0.042927 | -4.089 |
| w21 | 5 | -0.204703 | -16.887 |
| w22 | 24 | -0.022668 | 22.126 |
| w23 | 12 | -0.015265 | -6.148 |
| w24 | 35 | -0.010638 | 36.749 |
| w25 | 23 | 0.055437 | 1.399 |
| w26 | 9 | -0.211965 | -9.315 |
| w27 | 40 | 0.012794 | 4.226 |
| w28 | 2 | -0.141357 | -1.069 |
| w29 | 24 | -0.045957 | -4.286 |
| w30 | 18 | -0.202443 | -22.43 |
| w31 | 22 | -0.067058 | -15.661 |
| w32 | 19 | -0.057381 | -12.855 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 13 | 0.048167 | 7.431 |
| w18 | 22 | -0.003147 | -10.323 |
| w19 | 10 | -0.07335 | -10.774 |
| w20 | 17 | 0.030459 | -5.645 |
| w21 | 7 | -0.151133 | -3.74 |
| w22 | 19 | 0.102015 | 122.428 |
| w23 | 15 | -0.056553 | -13.363 |
| w24 | 27 | 0.036114 | 57.141 |
| w25 | 14 | 0.18438 | 67.351 |
| w26 | 18 | -0.0708 | -5.979 |
| w27 | 39 | -0.073852 | -2.952 |
| w28 | 2 | -0.088822 | -2.058 |
| w29 | 28 | -0.009359 | -7.16 |
| w30 | 7 | -0.034061 | -7.494 |
| w31 | 13 | -0.129869 | -12.566 |
| w32 | 21 | -0.059276 | -13.037 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 10 | 0.044572 | -0.575 |
| w29 | 23 | 0.01781 | -0.477 |
| w30 | 13 | -0.015173 | -12.523 |
| w31 | 17 | 0.072272 | 14.221 |
| w32 | 9 | -0.011198 | -0.42 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 25 | 0.026056 | 16.092 |
| w15 | 30 | 0.065348 | 71.782 |
| w16 | 16 | -0.015411 | 200.265 |
| w17 | 16 | 0.064559 | 5.564 |
| w18 | 17 | -0.026689 | -6.32 |
| w19 | 20 | -0.054042 | -16.83 |
| w20 | 15 | -0.008709 | -14.829 |
| w21 | 18 | 0.034225 | 37.2 |
| w22 | 31 | -0.1204 | -9.477 |
| w23 | 20 | 0.046742 | 0.244 |
| w24 | 34 | 0.052833 | 43.136 |
| w25 | 18 | 0.203481 | 100.065 |
| w26 | 15 | -0.16177 | -20.638 |
| w27 | 32 | 0.185925 | 193.853 |
| w28 | 3 | -0.083348 | -2.609 |
| w29 | 30 | -0.02499 | 7.8 |
| w30 | 18 | -0.002027 | -3.297 |
| w31 | 25 | 0.008187 | -3.386 |
| w32 | 12 | 0.018012 | -5.624 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 16 | 0.289586 | 193.761 |
| w26 | 19 | -0.023072 | -4.893 |
| w27 | 34 | 0.03296 | 45.89 |
| w28 | 12 | -0.037984 | -1.884 |
| w29 | 21 | 0.024307 | 8.292 |
| w30 | 4 | -0.044115 | -6.929 |
| w31 | 25 | -0.079703 | -13.519 |
| w32 | 25 | 0.012608 | 2.004 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

