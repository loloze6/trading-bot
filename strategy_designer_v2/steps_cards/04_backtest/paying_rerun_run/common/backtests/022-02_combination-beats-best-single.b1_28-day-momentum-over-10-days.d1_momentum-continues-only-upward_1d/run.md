# Backtest of 022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d

- Plan: `../../../../../03_test_plan/night3_learned_run/plans/022-02_combination-beats-best-single.b1_28-day-momentum-over-10-days.d1_momentum-continues-only-upward_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 28 | -0.030245 | 4.543 |
| w2 | 22 | 0.077594 | 53.138 |
| w3 | 38 | -0.002057 | 82.377 |
| w4 | 36 | -0.151227 | -36.172 |
| w5 | 24 | 0.056254 | 131.871 |
| w6 | 29 | 0.016746 | 85.176 |
| w7 | 14 | -0.111576 | -12.501 |
| w8 | 15 | -0.024593 | -10.238 |
| w9 | 12 | -0.097015 | -27.333 |
| w10 | 26 | 0.018523 | 36.684 |
| w11 | 33 | -0.033716 | 32.614 |
| w12 | 13 | -0.050692 | -10.29 |
| w13 | 28 | -0.005911 | 18.791 |
| w14 | 24 | 0.019129 | 31.584 |
| w15 | 22 | 0.133101 | 149.78 |
| w16 | 32 | -0.05652 | 21.037 |
| w17 | 14 | 0.09978 | 14.383 |
| w18 | 17 | 0.055569 | 3.37 |
| w19 | 21 | -0.108638 | -11.128 |
| w20 | 14 | 0.05753 | -6.269 |
| w21 | 14 | -0.141979 | -23.681 |
| w22 | 23 | -0.047628 | 43.154 |
| w23 | 10 | 0.036502 | 1.778 |
| w24 | 29 | 0.036645 | 70.138 |
| w25 | 13 | 0.11721 | 53.891 |
| w26 | 25 | -0.149862 | -25.293 |
| w27 | 34 | 0.034272 | 76.819 |
| w28 | 16 | -0.048339 | -3.506 |
| w29 | 33 | 0.007689 | 10.169 |
| w30 | 13 | 0.023395 | -7.19 |
| w31 | 23 | -0.054904 | -14.119 |
| w32 | 22 | 0.095414 | 19.024 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 15 | -0.05048 | 18.337 |
| w2 | 17 | 0.025159 | 11.598 |
| w3 | 25 | -0.16595 | -22.05 |
| w4 | 18 | 0.130227 | 179.093 |
| w5 | 31 | -0.050697 | 32.626 |
| w6 | 22 | 0.03741 | 78.119 |
| w7 | 14 | -0.077697 | -12.254 |
| w8 | 9 | -0.007742 | -12.753 |
| w9 | 8 | -0.137657 | -9.4 |
| w10 | 36 | -0.075389 | 22.444 |
| w11 | 22 | 0.084703 | 11.353 |
| w12 | 8 | -0.094191 | -14.883 |
| w13 | 28 | 0.027048 | 27.661 |
| w14 | 20 | 0.019569 | 27.757 |
| w15 | 30 | 0.040376 | 56.114 |
| w16 | 35 | -0.12264 | 9.431 |
| w17 | 20 | 0.02198 | 9.105 |
| w18 | 25 | 0.038135 | -10.357 |
| w19 | 13 | -0.075883 | -15.878 |
| w20 | 15 | 0.017572 | -2.746 |
| w21 | 23 | -0.081908 | 9.777 |
| w22 | 37 | -0.055793 | -3.335 |
| w23 | 20 | -0.159741 | -26.512 |
| w24 | 20 | -0.162677 | -10.893 |
| w25 | 20 | 0.055931 | 30.694 |
| w26 | 9 | -0.165294 | -9.33 |
| w27 | 36 | 0.015474 | 69.808 |
| w28 | 12 | -0.20732 | -16.409 |
| w29 | 25 | 0.046499 | 29.927 |
| w30 | 9 | -0.23969 | -25.997 |
| w31 | 12 | -0.038622 | -5.037 |
| w32 | 25 | -0.088224 | -17.39 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 25 | 0.160459 | 128.157 |
| w7 | 11 | -0.042143 | -9.536 |
| w8 | 3 | -0.029542 | -10.821 |
| w9 | 13 | -0.024343 | -12.227 |
| w10 | 21 | -0.201711 | -21.627 |
| w11 | 10 | 0.010764 | -1.441 |
| w12 | 15 | -0.04032 | -15.815 |
| w13 | 26 | -0.039142 | 3.181 |
| w14 | 20 | 0.117728 | 52.102 |
| w15 | 16 | 0.193075 | 168.331 |
| w16 | 24 | -0.034687 | 46.376 |
| w17 | 12 | 0.072217 | 21.314 |
| w18 | 18 | -0.116656 | -15.488 |
| w19 | 13 | -0.138326 | -11.541 |
| w20 | 13 | 0.049855 | -1.29 |
| w21 | 12 | 0.053668 | 23.951 |
| w22 | 20 | -0.075312 | 0.938 |
| w23 | 17 | -0.111247 | -20.072 |
| w24 | 16 | -0.031002 | 12.293 |
| w25 | 18 | 0.01641 | 10.924 |
| w26 | 11 | -0.032282 | -4.536 |
| w27 | 22 | 0.308736 | 255.131 |
| w28 | 8 | -0.256166 | -9.55 |
| w29 | 24 | 0.034436 | 43.97 |
| w30 | 4 | -0.012557 | -12.174 |
| w31 | 14 | -0.145172 | -23.747 |
| w32 | 14 | 0.055048 | 2.612 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | -0.014675 | -6.137 |
| w8 | 10 | 0.023191 | -9.307 |
| w9 | 8 | -0.113992 | -34.733 |
| w10 | 25 | 0.049327 | 54.205 |
| w11 | 15 | -0.106212 | -13.269 |
| w12 | 12 | -0.036996 | -13.37 |
| w13 | 23 | 0.061944 | 40.142 |
| w14 | 18 | 0.02834 | 12.068 |
| w15 | 18 | -0.10415 | 5.052 |
| w16 | 25 | -0.021079 | 50.002 |
| w17 | 18 | 0.043442 | 18.87 |
| w18 | 21 | -0.106607 | -31.16 |
| w19 | 13 | -0.07799 | -17.892 |
| w20 | 12 | 0.023975 | -6.212 |
| w21 | 10 | -0.193514 | -21.735 |
| w22 | 21 | -0.007377 | 7.324 |
| w23 | 7 | 0.164335 | 92.496 |
| w24 | 32 | -0.172116 | -8.704 |
| w25 | 27 | 0.056942 | 73.48 |
| w26 | 9 | -0.283893 | -21.785 |
| w27 | 22 | 0.018112 | 38.118 |
| w28 | 10 | -0.091752 | -13.081 |
| w29 | 45 | -0.127444 | 15.996 |
| w30 | 21 | -0.049968 | 8.398 |
| w31 | 15 | -0.039657 | -8.278 |
| w32 | 14 | -0.059971 | -33.623 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | 0.169566 | 198.495 |
| w2 | 26 | -0.012955 | 6.201 |
| w3 | 14 | 0.057052 | -0.67 |
| w4 | 37 | 0.026716 | 262.594 |
| w5 | 27 | 0.123623 | 106.682 |
| w6 | 17 | 0.103819 | 71.121 |
| w7 | 15 | 0.097549 | 13.254 |
| w8 | 6 | 0.086778 | -3.487 |
| w9 | 7 | -0.108788 | -8.713 |
| w10 | 32 | -0.171264 | -10.658 |
| w11 | 16 | 0.084799 | 19.82 |
| w12 | 10 | -0.214752 | -20.737 |
| w13 | 28 | 0.015828 | 49.173 |
| w14 | 25 | 3.1e-05 | 61.352 |
| w15 | 30 | 0.081727 | 46.443 |
| w16 | 31 | 0.027482 | 88.405 |
| w17 | 16 | 0.011426 | 25.122 |
| w18 | 20 | 0.030716 | -0.583 |
| w19 | 20 | -0.023234 | -6.114 |
| w20 | 17 | 0.113779 | 13.15 |
| w21 | 12 | -0.106698 | -12.799 |
| w22 | 25 | -0.041804 | 26.859 |
| w23 | 16 | -0.050032 | -11.387 |
| w24 | 29 | 0.031423 | 33.285 |
| w25 | 22 | 0.053506 | 26.742 |
| w26 | 14 | -0.032943 | -14.671 |
| w27 | 25 | 0.039477 | 42.418 |
| w28 | 0 | -0.027886 | 0.0 |
| w29 | 32 | -0.027269 | 77.053 |
| w30 | 10 | -0.009228 | -5.466 |
| w31 | 23 | -0.065295 | -19.625 |
| w32 | 20 | 0.043928 | 5.026 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 33 | 0.040079 | 53.655 |
| w11 | 13 | -0.006355 | -3.698 |
| w12 | 9 | -0.076766 | -16.038 |
| w13 | 15 | 0.069453 | 60.447 |
| w14 | 40 | -0.147907 | 18.83 |
| w15 | 27 | 0.012799 | 10.527 |
| w16 | 30 | 0.089969 | 98.557 |
| w17 | 17 | 0.01337 | 64.841 |
| w18 | 4 | -0.097038 | -12.083 |
| w19 | 16 | -0.050429 | -25.615 |
| w20 | 18 | -0.035359 | -11.365 |
| w21 | 3 | -0.137678 | -3.989 |
| w22 | 29 | -0.036558 | 14.25 |
| w23 | 14 | -0.04166 | -6.047 |
| w24 | 27 | 0.066882 | 152.795 |
| w25 | 15 | 0.055243 | 3.361 |
| w26 | 9 | -0.131792 | -20.874 |
| w27 | 25 | 0.210959 | 156.601 |
| w28 | 9 | -0.267501 | -15.963 |
| w29 | 23 | -0.03846 | 11.254 |
| w30 | 7 | 0.01785 | -8.464 |
| w31 | 7 | -0.176616 | -10.719 |
| w32 | 26 | -0.074224 | -21.619 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 29 | -0.148756 | 1.982 |
| w13 | 18 | -0.084425 | -23.751 |
| w14 | 32 | -0.078171 | 24.766 |
| w15 | 16 | -0.279205 | -24.423 |
| w16 | 27 | 0.043321 | 78.978 |
| w17 | 18 | 0.048581 | 21.976 |
| w18 | 22 | 0.013226 | 21.886 |
| w19 | 16 | -0.028242 | -14.409 |
| w20 | 17 | 0.08425 | 11.171 |
| w21 | 15 | -0.129595 | -18.515 |
| w22 | 22 | 0.046303 | 19.361 |
| w23 | 5 | 0.021804 | -0.96 |
| w24 | 23 | -0.077891 | 9.822 |
| w25 | 13 | 0.07164 | 13.543 |
| w26 | 1 | 0.035521 | 0.141 |
| w27 | 19 | 0.128527 | 51.29 |
| w28 | 8 | -0.161291 | -9.382 |
| w29 | 23 | -0.119474 | -15.821 |
| w30 | 4 | 0.007083 | -3.683 |
| w31 | 16 | -0.088974 | -15.339 |
| w32 | 24 | -0.063306 | -22.11 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 18 | -0.090742 | -14.898 |
| w16 | 30 | 0.030662 | 69.916 |
| w17 | 16 | 0.007769 | 3.243 |
| w18 | 13 | 0.082844 | 41.629 |
| w19 | 9 | -0.164391 | -16.994 |
| w20 | 10 | 0.035703 | -2.83 |
| w21 | 16 | -0.080926 | -32.382 |
| w22 | 23 | 0.004838 | -7.719 |
| w23 | 5 | -0.119212 | -5.838 |
| w24 | 34 | 0.010858 | 68.279 |
| w25 | 15 | 0.089793 | 11.892 |
| w26 | 10 | -0.153835 | -16.836 |
| w27 | 28 | 0.179908 | 141.935 |
| w28 | 6 | -0.034652 | -3.791 |
| w29 | 18 | 0.042503 | 21.592 |
| w30 | 0 | None | 0.0 |
| w31 | 28 | -0.046984 | -17.859 |
| w32 | 17 | -0.143122 | -25.472 |

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
| w15 | 24 | -0.057301 | -15.911 |
| w16 | 24 | -0.065396 | 96.059 |
| w17 | 10 | 0.050711 | 13.934 |
| w18 | 26 | -0.170016 | -19.013 |
| w19 | 17 | -0.117296 | -18.328 |
| w20 | 23 | -0.076764 | -19.155 |
| w21 | 17 | -0.054627 | -16.015 |
| w22 | 30 | -0.06616 | 7.273 |
| w23 | 29 | -0.095667 | -2.212 |
| w24 | 45 | -0.069799 | 32.165 |
| w25 | 23 | 0.123848 | 37.077 |
| w26 | 34 | -0.08186 | 12.747 |
| w27 | 39 | 0.056521 | 218.022 |
| w28 | 16 | -0.042503 | -6.852 |
| w29 | 47 | 0.001529 | 58.843 |
| w30 | 9 | -0.025015 | -10.446 |
| w31 | 37 | -0.04588 | 15.076 |
| w32 | 32 | -0.08183 | -0.444 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 20 | 0.129074 | 80.966 |
| w17 | 15 | -0.044722 | -7.252 |
| w18 | 25 | -0.034673 | 0.265 |
| w19 | 13 | -0.032354 | -15.655 |
| w20 | 11 | 0.027104 | -3.691 |
| w21 | 5 | -0.201293 | -14.424 |
| w22 | 19 | -0.012528 | 9.018 |
| w23 | 12 | 0.012475 | -6.394 |
| w24 | 24 | 0.042032 | 64.955 |
| w25 | 17 | 0.042814 | 2.629 |
| w26 | 11 | -0.089869 | -13.393 |
| w27 | 23 | 0.127547 | 62.33 |
| w28 | 3 | -0.079899 | -2.377 |
| w29 | 27 | -0.022067 | -1.715 |
| w30 | 11 | -0.001461 | -30.343 |
| w31 | 11 | -0.13108 | -17.301 |
| w32 | 10 | -0.116767 | -18.239 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 21 | 0.093567 | 0.974 |
| w21 | 6 | -0.148659 | -15.935 |
| w22 | 18 | -0.005804 | 8.193 |
| w23 | 7 | 0.034017 | -3.992 |
| w24 | 22 | 0.228981 | 255.113 |
| w25 | 24 | -0.012651 | -2.935 |
| w26 | 9 | -0.132906 | -21.33 |
| w27 | 29 | -0.047138 | 23.394 |
| w28 | 4 | -0.057151 | -1.464 |
| w29 | 22 | -0.091269 | 1.822 |
| w30 | 15 | 0.045556 | -1.776 |
| w31 | 19 | -0.100045 | -17.545 |
| w32 | 15 | -0.002514 | -8.971 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 16 | -0.007717 | 7.197 |
| w23 | 6 | 0.048089 | 0.227 |
| w24 | 26 | 0.101506 | 130.127 |
| w25 | 21 | 0.089065 | 37.693 |
| w26 | 20 | -0.069604 | -20.363 |
| w27 | 27 | -0.090293 | -5.467 |
| w28 | 1 | -0.18165 | -1.545 |
| w29 | 24 | -0.012497 | 7.839 |
| w30 | 11 | -0.062818 | -21.046 |
| w31 | 20 | -0.105527 | -17.689 |
| w32 | 18 | 0.05754 | 43.992 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 22 | -0.003268 | 23.071 |
| w25 | 25 | 0.030786 | 12.139 |
| w26 | 11 | -0.110187 | -10.992 |
| w27 | 31 | -0.07216 | 85.973 |
| w28 | 12 | 0.039452 | 3.792 |
| w29 | 17 | 0.020858 | 1.037 |
| w30 | 9 | -0.010184 | -18.223 |
| w31 | 16 | -0.088908 | -15.849 |
| w32 | 23 | -0.075964 | -24.475 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 18 | 0.161369 | 127.032 |
| w6 | 26 | -0.061222 | 6.018 |
| w7 | 14 | 0.014524 | -10.986 |
| w8 | 14 | -0.041977 | -25.913 |
| w9 | 8 | -0.100284 | -20.081 |
| w10 | 16 | -0.012423 | 19.404 |
| w11 | 25 | 0.062152 | -0.688 |
| w12 | 6 | -0.143954 | -7.103 |
| w13 | 16 | 0.094306 | 84.614 |
| w14 | 34 | -0.099975 | 22.667 |
| w15 | 14 | -0.121944 | -11.135 |
| w16 | 45 | -0.232859 | 25.265 |
| w17 | 14 | 0.035346 | 11.053 |
| w18 | 25 | -0.030665 | -11.479 |
| w19 | 14 | 0.020504 | 18.23 |
| w20 | 16 | 0.016951 | -11.504 |
| w21 | 8 | -0.041516 | -7.376 |
| w22 | 23 | -0.072769 | -11.457 |
| w23 | 9 | 0.025494 | -5.255 |
| w24 | 29 | -0.113986 | -14.437 |
| w25 | 10 | 0.053512 | 6.931 |
| w26 | 30 | 0.048254 | 19.918 |
| w27 | 31 | -0.01623 | 32.93 |
| w28 | 13 | -0.139987 | -21.21 |
| w29 | 24 | -0.01543 | -3.442 |
| w30 | 22 | 0.165507 | 308.17 |
| w31 | 18 | 0.061208 | 7.752 |
| w32 | 27 | 0.05789 | 54.91 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 35 | 0.078991 | 159.845 |
| w6 | 19 | 0.068205 | 109.091 |
| w7 | 15 | -0.126811 | -18.856 |
| w8 | 10 | -0.073921 | -14.469 |
| w9 | 11 | -0.050658 | -22.957 |
| w10 | 27 | -0.073608 | 12.563 |
| w11 | 26 | -0.073025 | -13.494 |
| w12 | 11 | -0.01527 | -3.313 |
| w13 | 27 | 0.002134 | 30.97 |
| w14 | 25 | 0.009978 | 45.238 |
| w15 | 30 | -0.029368 | 17.281 |
| w16 | 25 | -0.049323 | 44.882 |
| w17 | 25 | 0.005617 | -1.175 |
| w18 | 13 | -0.135381 | -15.053 |
| w19 | 30 | -0.025705 | -21.854 |
| w20 | 18 | -0.01105 | -21.858 |
| w21 | 21 | -0.10309 | -17.165 |
| w22 | 24 | -0.020638 | 3.281 |
| w23 | 10 | 0.032299 | 2.267 |
| w24 | 41 | -0.094357 | 8.846 |
| w25 | 14 | -0.231357 | -41.005 |
| w26 | 31 | 0.007599 | 18.272 |
| w27 | 37 | -0.01655 | -10.611 |
| w28 | 28 | -0.028644 | 22.24 |
| w29 | 11 | 0.133271 | 34.605 |
| w30 | 46 | -0.159943 | 19.738 |
| w31 | 19 | -0.051786 | -9.186 |
| w32 | 31 | 0.055748 | 33.621 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 20 | -0.095512 | -7.934 |
| w18 | 25 | -0.177608 | 17.714 |
| w19 | 15 | -0.105579 | -29.772 |
| w20 | 20 | 0.064878 | 4.147 |
| w21 | 10 | -0.271306 | -30.16 |
| w22 | 12 | 0.038337 | 16.788 |
| w23 | 10 | 0.01933 | -7.121 |
| w24 | 26 | -0.139672 | -8.105 |
| w25 | 14 | 0.13332 | 20.546 |
| w26 | 17 | -0.100325 | -19.295 |
| w27 | 20 | 0.15166 | 166.398 |
| w28 | 13 | 0.024066 | 8.526 |
| w29 | 19 | 0.081297 | 27.419 |
| w30 | 0 | -0.014225 | 0.0 |
| w31 | 16 | 0.001787 | -12.562 |
| w32 | 33 | 0.104811 | 47.407 |

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
| w17 | 24 | -0.097273 | -11.874 |
| w18 | 16 | -0.069654 | -12.306 |
| w19 | 17 | -0.071646 | -17.735 |
| w20 | 25 | 0.039754 | -6.597 |
| w21 | 13 | -0.153312 | -36.793 |
| w22 | 13 | 0.011105 | 11.022 |
| w23 | 11 | 0.010286 | -4.04 |
| w24 | 31 | -0.112644 | 19.666 |
| w25 | 19 | 0.084145 | 11.713 |
| w26 | 30 | -0.131681 | -4.698 |
| w27 | 28 | 0.005049 | 68.759 |
| w28 | 2 | -0.025822 | -1.324 |
| w29 | 26 | -0.053468 | 14.449 |
| w30 | 8 | -0.042174 | -11.341 |
| w31 | 5 | -0.19776 | -17.2 |
| w32 | 16 | -0.024085 | -5.378 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 14 | -0.139223 | -13.702 |
| w20 | 13 | 0.005284 | -8.116 |
| w21 | 14 | -0.01379 | -1.229 |
| w22 | 29 | 0.040388 | 165.512 |
| w23 | 17 | -0.076501 | -9.234 |
| w24 | 33 | 0.015921 | 199.766 |
| w25 | 14 | -0.092549 | -10.522 |
| w26 | 14 | -0.038152 | -17.194 |
| w27 | 33 | -0.032703 | 11.253 |
| w28 | 3 | -0.118836 | -4.311 |
| w29 | 32 | -0.039654 | 6.423 |
| w30 | 5 | -0.038077 | -10.453 |
| w31 | 9 | -0.045228 | -13.076 |
| w32 | 15 | 0.064728 | 28.408 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 21 | 0.061218 | 24.058 |
| w23 | 17 | -0.0784 | -18.751 |
| w24 | 20 | -0.012701 | 33.233 |
| w25 | 20 | -0.058626 | -8.229 |
| w26 | 13 | -0.03914 | -3.6 |
| w27 | 23 | -0.05582 | 10.417 |
| w28 | 7 | -0.098373 | -7.087 |
| w29 | 33 | -0.050531 | 9.364 |
| w30 | 6 | -0.047931 | -2.252 |
| w31 | 15 | -0.036624 | -14.284 |
| w32 | 16 | -0.017318 | -4.699 |

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
| w27 | 25 | -0.01638 | 45.224 |
| w28 | 7 | -0.058592 | -3.894 |
| w29 | 23 | -0.026883 | 6.684 |
| w30 | 7 | -0.061531 | -15.667 |
| w31 | 4 | -0.086855 | -0.396 |
| w32 | 22 | 0.023433 | 32.263 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 9 | 0.054719 | 7.105 |
| w18 | 9 | -0.077423 | -3.34 |
| w19 | 9 | -0.114287 | -19.359 |
| w20 | 13 | 0.042927 | -3.506 |
| w21 | 5 | -0.204703 | -19.83 |
| w22 | 19 | -0.022668 | 15.447 |
| w23 | 12 | -0.015265 | -6.896 |
| w24 | 24 | -0.010638 | 51.309 |
| w25 | 16 | 0.055437 | 0.225 |
| w26 | 8 | -0.211965 | -12.16 |
| w27 | 27 | 0.012794 | 36.608 |
| w28 | 2 | -0.141357 | -1.641 |
| w29 | 20 | -0.045957 | -3.668 |
| w30 | 14 | -0.202443 | -32.269 |
| w31 | 19 | -0.067058 | -19.861 |
| w32 | 17 | -0.057381 | -23.39 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | 0.048167 | 7.45 |
| w18 | 20 | -0.003147 | -5.645 |
| w19 | 9 | -0.07335 | -9.961 |
| w20 | 12 | 0.030459 | -5.907 |
| w21 | 6 | -0.151133 | -5.426 |
| w22 | 18 | 0.102015 | 121.83 |
| w23 | 11 | -0.056553 | -15.075 |
| w24 | 24 | 0.036114 | 56.845 |
| w25 | 14 | 0.18438 | 68.674 |
| w26 | 13 | -0.0708 | -8.702 |
| w27 | 27 | -0.073852 | 3.585 |
| w28 | 2 | -0.088822 | -2.058 |
| w29 | 27 | -0.009359 | -3.555 |
| w30 | 6 | -0.034061 | -12.198 |
| w31 | 11 | -0.129869 | -14.719 |
| w32 | 15 | -0.059276 | -31.63 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 11 | 0.044572 | -3.756 |
| w29 | 20 | 0.01781 | 2.549 |
| w30 | 10 | -0.015173 | -11.818 |
| w31 | 16 | 0.072272 | 12.821 |
| w32 | 9 | -0.011198 | 0.566 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 15 | 0.026056 | 4.742 |
| w15 | 19 | 0.065348 | 63.949 |
| w16 | 16 | -0.015411 | 165.567 |
| w17 | 16 | 0.064559 | 5.564 |
| w18 | 13 | -0.026689 | -10.223 |
| w19 | 15 | -0.054042 | -17.678 |
| w20 | 11 | -0.008709 | -13.768 |
| w21 | 18 | 0.034225 | 34.824 |
| w22 | 26 | -0.1204 | -10.991 |
| w23 | 18 | 0.046742 | -0.422 |
| w24 | 32 | 0.052833 | 43.347 |
| w25 | 16 | 0.203481 | 102.749 |
| w26 | 13 | -0.16177 | -21.559 |
| w27 | 24 | 0.185925 | 208.943 |
| w28 | 3 | -0.083348 | -2.609 |
| w29 | 30 | -0.02499 | 11.802 |
| w30 | 15 | -0.002027 | -12.799 |
| w31 | 18 | 0.008187 | -7.203 |
| w32 | 12 | 0.018012 | -5.643 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 12 | 0.289586 | 286.81 |
| w26 | 17 | -0.023072 | -1.187 |
| w27 | 30 | 0.03296 | 53.02 |
| w28 | 5 | -0.037984 | -2.774 |
| w29 | 20 | 0.024307 | 18.695 |
| w30 | 4 | -0.044115 | -16.335 |
| w31 | 19 | -0.079703 | -12.737 |
| w32 | 19 | 0.012608 | -2.648 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

