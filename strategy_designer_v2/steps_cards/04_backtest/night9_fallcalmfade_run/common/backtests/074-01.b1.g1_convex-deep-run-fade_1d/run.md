# Backtest of 074-01.b1.g1_convex-deep-run-fade_1d

- Plan: `../../../../../03_test_plan/night9_fallcalmfade_run/plans/074-01.b1.g1_convex-deep-run-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, LTC, XRP, BCH, ETH, ADA, ATOM, ALGO, TRX, DOT, AVAX, NEAR, SUI, ZEC, XMR, CRV, AAVE, INJ, LDO, ONDO, FIL, GRT, TAO, DOGE, PEPE as BTCUSD, LTCUSD, XRPUSD, BCHUSD, ETHUSD, ADAUSD, ATOMUSD, ALGOUSD, TRXUSD, DOTUSD, AVAXUSD, NEARUSD, SUIUSD, ZECUSD, XMRUSD, CRVUSD, AAVEUSD, INJUSD, LDOUSD, ONDOUSD, FILUSD, GRTUSD, TAOUSD, DOGEUSD, PEPEUSD; 1d bars; windows research_2016 (the common record: every portfolio coin, each window after the coin's first 90 days)
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.05092 | 0.0 |
| w2 | 1 | 0.044582 | 0.155 |
| w3 | 0 | -0.194109 | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 8 | 0.164006 | 12.231 |
| w8 | 5 | 0.144029 | 11.668 |
| w9 | 8 | 0.307227 | 42.007 |
| w10 | 1 | 0.036785 | 0.268 |
| w11 | 0 | None | 0.0 |
| w12 | 10 | -0.032213 | -2.152 |
| w13 | 1 | 0.143748 | 5.295 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.14413 | 7.245 |
| w18 | 4 | -0.033709 | -2.207 |
| w19 | 7 | 0.037163 | 2.864 |
| w20 | 10 | 0.191788 | 16.26 |
| w21 | 9 | 0.046442 | 2.674 |
| w22 | 0 | 0.006562 | 0.0 |
| w23 | 0 | -0.099794 | 0.0 |
| w24 | 2 | -0.012233 | -2.109 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.040623 | 1.978 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | -0.067661 | -3.776 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.005544 | 0.026 |
| w31 | 6 | 0.040162 | 5.596 |
| w32 | 4 | -0.0146 | -1.003 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | -0.040217 | 0.0 |
| w2 | 5 | -0.02405 | -1.278 |
| w3 | 0 | None | 0.0 |
| w4 | 3 | -0.017423 | -3.282 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.028963 | -0.311 |
| w7 | 8 | 0.067591 | 4.084 |
| w8 | 13 | 0.221468 | 27.699 |
| w9 | 10 | 0.165043 | 19.653 |
| w10 | 1 | 0.12214 | 0.934 |
| w11 | 3 | -0.015385 | -1.378 |
| w12 | 11 | -0.001295 | -0.105 |
| w13 | 3 | 0.131025 | 4.215 |
| w14 | 2 | -0.099845 | -0.678 |
| w15 | 2 | 0.006502 | -0.926 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.055349 | -2.738 |
| w18 | 2 | 0.013116 | 0.577 |
| w19 | 9 | 0.08444 | 7.661 |
| w20 | 5 | 0.037611 | 5.303 |
| w21 | 1 | 0.081434 | 0.303 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.0324 | -1.8 |
| w24 | 7 | -0.012477 | -2.099 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | 0.113882 | 10.258 |
| w27 | 1 | -0.023316 | -1.14 |
| w28 | 4 | 0.041479 | 2.849 |
| w29 | 1 | 0.062399 | 0.613 |
| w30 | 9 | -0.031131 | -1.711 |
| w31 | 11 | 0.03116 | 4.084 |
| w32 | 5 | 0.043114 | 3.029 |

- XRPUSD: 27 of 27 windows run. w1 to w5 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w6 | 0 | -0.017101 | 0.0 |
| w7 | 6 | -0.061392 | -5.771 |
| w8 | 8 | 0.004659 | 3.497 |
| w9 | 9 | 0.079194 | 6.984 |
| w10 | 6 | 0.073756 | 2.981 |
| w11 | 6 | -0.038785 | -3.215 |
| w12 | 6 | 0.117484 | 8.89 |
| w13 | 3 | 0.147645 | 5.273 |
| w14 | 1 | -0.002793 | -0.157 |
| w15 | 3 | -0.004235 | -1.231 |
| w16 | 1 | -0.044261 | -1.322 |
| w17 | 3 | -0.039573 | -1.572 |
| w18 | 7 | 0.00951 | 1.034 |
| w19 | 6 | 0.066035 | 5.351 |
| w20 | 5 | -0.181659 | 13.573 |
| w21 | 3 | 0.043641 | 2.098 |
| w22 | 0 | 0.031967 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 6 | 0.009209 | -0.587 |
| w25 | 5 | 0.053028 | 4.936 |
| w26 | 6 | 0.13782 | 11.942 |
| w27 | 1 | 0.112435 | 2.371 |
| w28 | 2 | 0.069181 | 2.635 |
| w29 | 1 | 0.010489 | 0.009 |
| w30 | 14 | -0.051526 | -4.112 |
| w31 | 6 | 0.065824 | 5.938 |
| w32 | 7 | -0.001343 | -1.242 |

- BCHUSD: 26 of 26 windows run. w1 to w6 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 7 | 0.061522 | 1.838 |
| w8 | 8 | 0.107384 | 9.38 |
| w9 | 8 | -0.002452 | 0.447 |
| w10 | 3 | 0.051761 | 1.339 |
| w11 | 7 | 0.101158 | 2.468 |
| w12 | 7 | -0.042934 | -5.083 |
| w13 | 3 | 0.056873 | 0.929 |
| w14 | 2 | -0.027247 | -1.854 |
| w15 | 2 | 0.000708 | -0.477 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | -0.020638 | -1.461 |
| w18 | 6 | -0.055403 | -3.928 |
| w19 | 7 | 0.147635 | 11.486 |
| w20 | 11 | 0.202057 | 18.572 |
| w21 | 5 | -0.011602 | -0.773 |
| w22 | 1 | 0.069088 | 2.523 |
| w23 | 1 | 0.068119 | 4.914 |
| w24 | 1 | 0.058082 | 1.384 |
| w25 | 0 | None | 0.0 |
| w26 | 10 | 0.14195 | 14.355 |
| w27 | 1 | -0.085647 | -3.857 |
| w28 | 7 | -0.086518 | -8.452 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.024327 | -0.003 |
| w31 | 8 | -0.067975 | -7.111 |
| w32 | 9 | 0.112432 | 12.533 |

- ETHUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | -0.115033 | -4.472 |
| w3 | 6 | 0.027623 | 5.102 |
| w4 | 0 | -0.003206 | 0.0 |
| w5 | 0 | 0.041802 | 0.0 |
| w6 | 0 | 0.044887 | 0.0 |
| w7 | 5 | 0.055545 | 3.601 |
| w8 | 8 | 0.226472 | 26.121 |
| w9 | 8 | 0.176631 | 27.795 |
| w10 | 2 | 0.10585 | 1.072 |
| w11 | 5 | 0.045256 | 2.219 |
| w12 | 8 | 0.051834 | 4.126 |
| w13 | 1 | -0.016761 | -0.417 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.066955 | -1.792 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.023666 | -0.435 |
| w18 | 1 | 0.020562 | 0.86 |
| w19 | 5 | 0.037533 | 2.909 |
| w20 | 8 | 0.075317 | 5.654 |
| w21 | 5 | 0.01144 | 0.571 |
| w22 | 0 | 0.00824 | 0.0 |
| w23 | 2 | -0.086153 | -2.536 |
| w24 | 4 | -0.000722 | -2.784 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.055655 | 5.154 |
| w27 | 2 | -0.029781 | -0.88 |
| w28 | 9 | 0.233057 | 21.881 |
| w29 | 0 | 0.02179 | 0.0 |
| w30 | 8 | 0.008919 | 1.85 |
| w31 | 5 | 0.054751 | 5.088 |
| w32 | 2 | 0.001438 | 0.034 |

- ADAUSD: 23 of 23 windows run. w1 to w9 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 1 | 0.076788 | 1.313 |
| w11 | 6 | -0.084892 | -4.668 |
| w12 | 6 | 0.048079 | 3.03 |
| w13 | 2 | 0.127709 | 4.06 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.11149 | 6.142 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.059326 | 2.142 |
| w18 | 9 | 0.113461 | 15.842 |
| w19 | 9 | 0.046837 | 2.942 |
| w20 | 7 | 0.036416 | 4.774 |
| w21 | 6 | 0.005917 | 1.014 |
| w22 | 0 | -0.001789 | 0.0 |
| w23 | 4 | 0.145299 | 11.742 |
| w24 | 5 | 0.0363 | -2.496 |
| w25 | 2 | 0.036217 | 1.504 |
| w26 | 11 | 0.102471 | 10.345 |
| w27 | 1 | -0.040718 | -3.194 |
| w28 | 10 | 0.033027 | 1.208 |
| w29 | 4 | -0.024287 | -2.082 |
| w30 | 9 | -0.059512 | -2.027 |
| w31 | 9 | -0.019993 | -1.166 |
| w32 | 5 | -0.03292 | -3.545 |

- ATOMUSD: 21 of 21 windows run. w1 to w11 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 3 | 0.025335 | -0.522 |
| w13 | 4 | 0.032178 | 2.962 |
| w14 | 1 | -0.068566 | -5.681 |
| w15 | 5 | -0.018888 | -1.186 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.029531 | 0.26 |
| w18 | 7 | 0.06782 | 4.25 |
| w19 | 4 | 0.070773 | 5.129 |
| w20 | 8 | 0.175326 | 17.168 |
| w21 | 3 | 0.02056 | 0.871 |
| w22 | 1 | 0.066272 | 1.987 |
| w23 | 7 | -0.062832 | -4.824 |
| w24 | 5 | -0.028012 | -8.947 |
| w25 | 4 | -0.034382 | -4.475 |
| w26 | 13 | -0.029316 | -2.619 |
| w27 | 2 | -0.100786 | -11.08 |
| w28 | 8 | -0.006283 | -1.837 |
| w29 | 1 | -0.001234 | -0.227 |
| w30 | 12 | -0.061304 | -4.283 |
| w31 | 7 | -0.086435 | -7.629 |
| w32 | 7 | 0.058003 | 2.829 |

- ALGOUSD: 18 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w15 | 9 | 0.032011 | 0.888 |
| w16 | 0 | 0.056292 | 0.0 |
| w17 | 6 | -0.064478 | -4.731 |
| w18 | 4 | -0.071286 | -5.036 |
| w19 | 12 | 0.15994 | 13.792 |
| w20 | 10 | 0.016693 | 0.077 |
| w21 | 5 | 0.103071 | 5.557 |
| w22 | 4 | -0.148051 | -12.646 |
| w23 | 9 | 0.120021 | 15.392 |
| w24 | 4 | -0.001169 | -6.376 |
| w25 | 1 | 0.035222 | 1.899 |
| w26 | 11 | 0.130904 | 12.88 |
| w27 | 3 | 0.071905 | 2.936 |
| w28 | 8 | -0.051693 | -5.454 |
| w29 | 5 | 0.003917 | -1.203 |
| w30 | 15 | 0.002411 | 0.802 |
| w31 | 12 | -0.033292 | -6.235 |
| w32 | 7 | -0.028 | -3.873 |

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
| w15 | 3 | -0.033977 | -4.04 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | -0.199254 | -7.076 |
| w18 | 3 | 0.045801 | 1.259 |
| w19 | 6 | 0.158232 | 10.142 |
| w20 | 3 | -0.09859 | -5.677 |
| w21 | 5 | 0.144855 | 9.639 |
| w22 | 0 | 0.072275 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 1 | 0.045741 | 1.066 |
| w26 | 1 | -0.07441 | -0.711 |
| w27 | 0 | None | 0.0 |
| w28 | 4 | -0.019579 | -2.386 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | -0.020973 | -2.082 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.017096 | 0.0 |

- DOTUSD: 17 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w16 | 1 | -0.120467 | -9.606 |
| w17 | 7 | 0.117711 | 7.649 |
| w18 | 3 | -0.066812 | -2.865 |
| w19 | 7 | 0.132265 | 8.851 |
| w20 | 9 | -0.046395 | -2.937 |
| w21 | 10 | -0.138724 | -16.691 |
| w22 | 1 | 0.026663 | 0.601 |
| w23 | 6 | -0.011541 | -1.807 |
| w24 | 6 | 0.011551 | -7.44 |
| w25 | 3 | 0.015057 | -0.231 |
| w26 | 12 | -0.121418 | -13.055 |
| w27 | 2 | -0.026706 | -3.35 |
| w28 | 8 | 0.095499 | 7.909 |
| w29 | 3 | -0.06042 | -5.046 |
| w30 | 10 | -0.058997 | -5.374 |
| w31 | 11 | -0.015678 | -1.124 |
| w32 | 14 | 0.115629 | 10.412 |

- AVAXUSD: 13 of 13 windows run. w1 to w19 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | 0.016863 | 4.579 |
| w21 | 8 | 0.076602 | 3.873 |
| w22 | 1 | 0.048328 | 1.933 |
| w23 | 7 | 0.081948 | 7.505 |
| w24 | 6 | 0.002175 | -7.554 |
| w25 | 4 | 0.052616 | 2.327 |
| w26 | 14 | 0.03633 | 2.182 |
| w27 | 1 | -0.062317 | -0.722 |
| w28 | 8 | 0.038114 | 3.307 |
| w29 | 1 | -0.018277 | -0.866 |
| w30 | 9 | -0.096855 | -6.761 |
| w31 | 9 | -0.006432 | 0.137 |
| w32 | 6 | 0.017672 | 1.269 |

- NEARUSD: 11 of 11 windows run. w1 to w21 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.004054 | -1.008 |
| w23 | 10 | -0.039078 | -2.541 |
| w24 | 7 | 0.028876 | -5.721 |
| w25 | 1 | -0.034355 | -3.091 |
| w26 | 5 | 0.076837 | 6.323 |
| w27 | 3 | 0.09608 | 3.428 |
| w28 | 10 | -0.039401 | -3.522 |
| w29 | 2 | -0.063265 | -2.822 |
| w30 | 11 | -0.107581 | -12.334 |
| w31 | 10 | 0.012866 | 1.013 |
| w32 | 4 | 0.066758 | 3.233 |

- SUIUSD: 9 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w24 | 5 | 0.05321 | 2.44 |
| w25 | 2 | 0.022976 | 0.695 |
| w26 | 10 | -0.002469 | -0.434 |
| w27 | 0 | None | 0.0 |
| w28 | 9 | 0.009846 | -0.261 |
| w29 | 3 | -0.005572 | -0.403 |
| w30 | 11 | -0.0935 | -6.262 |
| w31 | 8 | 0.022581 | 2.541 |
| w32 | 7 | -0.089593 | -8.848 |

- ZECUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | 0.025671 | 0.0 |
| w6 | 1 | -0.038463 | -0.394 |
| w7 | 6 | 0.044444 | 3.278 |
| w8 | 12 | 0.032319 | 3.228 |
| w9 | 12 | 0.104995 | 13.795 |
| w10 | 5 | -0.04245 | -3.085 |
| w11 | 5 | 0.103047 | 4.973 |
| w12 | 11 | 0.031009 | 3.933 |
| w13 | 4 | 0.106121 | 3.314 |
| w14 | 0 | -0.015115 | 0.0 |
| w15 | 6 | -0.044413 | -2.866 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.012996 | -0.187 |
| w18 | 1 | -0.028359 | -0.518 |
| w19 | 7 | 0.037942 | 4.814 |
| w20 | 9 | 0.298837 | 23.563 |
| w21 | 11 | 0.090251 | 10.833 |
| w22 | 3 | -0.002352 | -1.17 |
| w23 | 8 | 0.026939 | 4.849 |
| w24 | 4 | -0.014134 | -1.82 |
| w25 | 5 | -0.170859 | -10.64 |
| w26 | 7 | 0.05594 | 2.484 |
| w27 | 1 | -0.028523 | -2.497 |
| w28 | 7 | 0.051687 | 4.287 |
| w29 | 4 | -0.052826 | -4.798 |
| w30 | 0 | None | 0.0 |
| w31 | 7 | -0.15575 | -12.925 |
| w32 | 1 | 0.001364 | -0.141 |

- XMRUSD: 28 of 28 windows run. w1 to w4 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w5 | 0 | 0.054115 | 0.0 |
| w6 | 3 | 0.028856 | 0.411 |
| w7 | 7 | 0.177507 | 11.873 |
| w8 | 12 | 0.2152 | 16.998 |
| w9 | 9 | 0.102962 | 9.804 |
| w10 | 2 | 0.042047 | 0.161 |
| w11 | 3 | 0.022136 | 0.622 |
| w12 | 11 | 0.052378 | 5.317 |
| w13 | 2 | 0.061702 | 2.153 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | -0.050616 | -1.932 |
| w18 | 3 | 0.023545 | 1.199 |
| w19 | 5 | 0.157484 | 11.864 |
| w20 | 5 | 0.012056 | -1.421 |
| w21 | 3 | 0.06848 | 2.197 |
| w22 | 2 | -0.266649 | -10.856 |
| w23 | 4 | -0.124788 | -6.467 |
| w24 | 1 | -0.027263 | -0.976 |
| w25 | 6 | 0.012065 | 3.085 |
| w26 | 2 | 0.075504 | 1.577 |
| w27 | 2 | -0.006202 | -1.523 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.239851 | -20.217 |
| w30 | 0 | -0.003815 | 0.0 |
| w31 | 6 | -0.023641 | -1.833 |
| w32 | 0 | 0.014812 | 0.0 |

- CRVUSD: 16 of 17 windows run. w1 to w15 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 8 | -0.020316 | -5.699 |
| w18 | 0 | None | 0.0 |
| w19 | 7 | -0.016276 | 0.177 |
| w20 | 8 | -0.152743 | -14.392 |
| w21 | 11 | 0.084978 | 7.406 |
| w22 | 2 | 0.038576 | 1.182 |
| w23 | 7 | 0.222261 | 24.273 |
| w24 | 4 | -0.040529 | -6.977 |
| w25 | 3 | 0.033512 | 0.596 |
| w26 | 11 | 0.178247 | 24.251 |
| w27 | 2 | 0.003993 | -1.414 |
| w28 | 6 | -0.043795 | -4.751 |
| w29 | 2 | 0.003682 | -0.348 |
| w30 | 12 | -0.091969 | -8.291 |
| w31 | 9 | -0.043198 | -2.774 |
| w32 | 2 | -0.084441 | -4.146 |

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
| w17 | 4 | -0.103273 | -2.979 |
| w18 | 10 | -0.037425 | -5.849 |
| w19 | 6 | 0.12341 | 9.456 |
| w20 | 6 | -0.09386 | -5.988 |
| w21 | 10 | 0.101568 | 7.201 |
| w22 | 3 | 0.036526 | 1.303 |
| w23 | 6 | -0.008545 | -0.996 |
| w24 | 3 | 0.019981 | -1.395 |
| w25 | 1 | 0.002418 | 0.148 |
| w26 | 4 | 0.061051 | 1.933 |
| w27 | 0 | None | 0.0 |
| w28 | 9 | 0.028936 | 3.732 |
| w29 | 0 | -0.00461 | 0.0 |
| w30 | 8 | -0.05759 | -4.857 |
| w31 | 11 | -0.063219 | -5.266 |
| w32 | 5 | 0.090717 | 5.794 |

- INJUSD: 14 of 14 windows run. w1 to w18 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w19 | 6 | 0.013103 | 1.509 |
| w20 | 9 | 0.129378 | 18.033 |
| w21 | 3 | 0.041279 | 1.414 |
| w22 | 0 | -0.029146 | 0.0 |
| w23 | 2 | 0.036855 | 1.895 |
| w24 | 4 | 0.069439 | 1.142 |
| w25 | 2 | 0.022815 | 0.425 |
| w26 | 8 | 0.119724 | 10.7 |
| w27 | 3 | 0.108635 | 3.719 |
| w28 | 10 | -0.049151 | -5.524 |
| w29 | 1 | 0.024212 | 0.296 |
| w30 | 11 | 0.041937 | 5.677 |
| w31 | 12 | -0.061702 | -6.11 |
| w32 | 3 | -0.152569 | -17.306 |

- LDOUSD: 11 of 12 windows run. w1 to w20 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.054191 | 1.867 |
| w23 | 9 | 0.082494 | 3.859 |
| w24 | 4 | -0.025644 | -7.398 |
| w25 | 1 | 0.055879 | 2.217 |
| w26 | 7 | 0.061583 | 4.508 |
| w27 | 3 | 0.087765 | 2.37 |
| w28 | 8 | 0.057597 | 4.355 |
| w29 | 4 | -0.195988 | -13.156 |
| w30 | 11 | -0.106411 | -5.805 |
| w31 | 10 | 0.045395 | 4.832 |
| w32 | 4 | 0.043134 | 1.1 |

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
| w27 | 2 | 0.065812 | 1.906 |
| w28 | 8 | 0.03523 | 2.663 |
| w29 | 3 | -0.08647 | -3.896 |
| w30 | 13 | 0.022926 | 6.085 |
| w31 | 10 | 0.02074 | 2.359 |
| w32 | 3 | -0.333426 | -19.237 |

- FILUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 4 | -0.11491 | -5.781 |
| w18 | 10 | -0.015574 | -2.113 |
| w19 | 7 | 0.051071 | 4.759 |
| w20 | 9 | 0.095977 | 8.981 |
| w21 | 6 | 0.025006 | 1.824 |
| w22 | 1 | 0.032756 | 0.407 |
| w23 | 6 | 0.003525 | 1.644 |
| w24 | 5 | 0.02594 | -2.862 |
| w25 | 1 | 0.021511 | 0.1 |
| w26 | 9 | 0.112476 | 10.511 |
| w27 | 2 | 0.034858 | 2.836 |
| w28 | 8 | -0.085616 | -5.732 |
| w29 | 2 | -0.045265 | -2.362 |
| w30 | 11 | -0.131912 | -21.42 |
| w31 | 9 | -0.023366 | -2.315 |
| w32 | 10 | -0.092564 | -11.407 |

- GRTUSD: 16 of 16 windows run. w1 to w16 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w17 | 11 | 0.092312 | 6.667 |
| w18 | 3 | -0.0311 | -0.362 |
| w19 | 6 | 0.08718 | 5.427 |
| w20 | 11 | 0.169297 | 21.425 |
| w21 | 7 | 0.12177 | 11.537 |
| w22 | 2 | 0.012933 | -0.096 |
| w23 | 6 | 0.040552 | 1.05 |
| w24 | 6 | -0.04345 | -13.196 |
| w25 | 0 | None | 0.0 |
| w26 | 13 | 0.129051 | 13.112 |
| w27 | 2 | -0.052141 | -1.117 |
| w28 | 9 | -0.022049 | -1.566 |
| w29 | 2 | -0.025728 | -1.291 |
| w30 | 13 | -0.008905 | -0.132 |
| w31 | 11 | 0.009141 | 0.114 |
| w32 | 9 | 0.048527 | 5.284 |

- TAOUSD: 5 of 5 windows run. w1 to w27 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w28 | 11 | 0.086134 | 8.195 |
| w29 | 1 | -0.056361 | -0.163 |
| w30 | 4 | 0.021879 | 3.346 |
| w31 | 6 | -0.043909 | -5.375 |
| w32 | 10 | 0.068674 | 5.115 |

- DOGEUSD: 19 of 19 windows run. w1 to w13 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.053136 | 3.707 |
| w16 | 1 | 0.016188 | 0.168 |
| w17 | 5 | -0.132362 | -6.505 |
| w18 | 6 | 0.027168 | 1.888 |
| w19 | 10 | 0.049599 | 3.895 |
| w20 | 5 | -0.189568 | -11.397 |
| w21 | 5 | 0.053518 | 3.294 |
| w22 | 2 | -0.162826 | -9.281 |
| w23 | 5 | 0.119925 | 9.365 |
| w24 | 6 | 0.042341 | 1.282 |
| w25 | 1 | -0.024315 | -2.833 |
| w26 | 13 | -0.124315 | -11.011 |
| w27 | 2 | -0.021757 | -1.067 |
| w28 | 11 | 0.030156 | 3.885 |
| w29 | 2 | -0.017949 | -0.998 |
| w30 | 12 | -0.049021 | -1.906 |
| w31 | 7 | 0.021509 | 2.437 |
| w32 | 7 | -0.138476 | -11.779 |

- PEPEUSD: 8 of 9 windows run. w1 to w23 not used: they start before the coin's 91st day (common/data_use.md).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.023987 | -0.643 |
| w26 | 3 | 0.072364 | 3.189 |
| w27 | 2 | -0.047327 | -1.365 |
| w28 | 11 | 0.016288 | 0.557 |
| w29 | 1 | -0.038376 | -2.467 |
| w30 | 12 | -0.054034 | -3.849 |
| w31 | 7 | -0.026786 | -3.78 |
| w32 | 4 | -0.007435 | -2.024 |

- w24 not run: the dates were not fetched (run the data tool).

```
  File "/home/user/trading-bot/trading-bot/data/coverage.py", line 88, in check
    raise DataNotFetched(f"{file_name}: {days} not fetched (no coverage in {path_for(data_dir)}): a backtest reads "
                         f"local data only; fetch these days first with the data tool, {DATA_TOOL}")
data.coverage.DataNotFetched: kraken_PEPEUSD_1d.csv: <date> to <date> not fetched (no coverage in /home/user/trading-bot/trading-bot/local_data/coverage.yaml): a backtest reads local data only; fetch these days first with the data tool, trading-bot/tools/extend_kraken_daily.py (daily) or trading-bot/tools/ingest_kraken_archive.py (archive)
```

