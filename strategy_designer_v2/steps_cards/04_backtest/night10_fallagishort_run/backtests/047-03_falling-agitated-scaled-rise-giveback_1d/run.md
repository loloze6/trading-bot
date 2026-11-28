# Backtest of 047-03_falling-agitated-scaled-rise-giveback_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/047-03_falling-agitated-scaled-rise-giveback_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 14 | 0.11172 | 6.161 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | 0.000421 | -0.779 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.047119 | -3.108 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 34 | 0.032339 | 4.662 |
| w21 | 7 | -0.077516 | -5.208 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.099632 | 7.021 |
| w24 | 8 | -0.098288 | -7.514 |
| w25 | 0 | None | 0.0 |
| w26 | 20 | -0.009807 | -4.817 |
| w27 | 0 | None | 0.0 |
| w28 | 13 | 0.053619 | 1.871 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | 0.114784 | 6.42 |
| w31 | 5 | 0.006793 | -0.006 |
| w32 | 13 | -0.003757 | 0.624 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 26 | -0.024017 | -5.035 |
| w27 | 1 | 0.053125 | 0.608 |
| w28 | 33 | 0.165971 | 25.0 |
| w29 | 1 | 0.040983 | 0.575 |
| w30 | 10 | -0.021417 | -0.574 |
| w31 | 8 | 0.017323 | 0.99 |
| w32 | 7 | 0.050251 | 3.616 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 4 | -0.012313 | -0.445 |
| w12 | 1 | 0.08913 | 0.491 |
| w13 | 23 | 0.056536 | 0.953 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 14 | 0.012725 | 0.016 |
| w18 | 0 | None | 0.0 |
| w19 | 10 | -0.015374 | -2.056 |
| w20 | 22 | -0.112841 | -11.608 |
| w21 | 2 | 0.001283 | -0.21 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 7 | -0.101638 | -7.643 |
| w25 | 17 | -0.024087 | -5.478 |
| w26 | 3 | 0.028056 | -0.054 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 6 | -0.219773 | -19.889 |
| w30 | 6 | -0.025351 | -2.957 |
| w31 | 12 | -0.051426 | -3.45 |
| w32 | 8 | 0.093006 | 1.761 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 8 | 0.046412 | 1.819 |
| w26 | 16 | 0.060275 | 3.359 |
| w27 | 2 | 0.089888 | 2.808 |
| w28 | 29 | 0.151445 | 19.256 |
| w29 | 0 | None | 0.0 |
| w30 | 20 | 0.018017 | 4.144 |
| w31 | 7 | 0.059819 | 2.494 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 27 | -0.034575 | -5.107 |
| w27 | 1 | 0.12984 | 3.444 |
| w28 | 21 | 0.032373 | 3.974 |
| w29 | 0 | None | 0.0 |
| w30 | 16 | 0.007129 | 2.193 |
| w31 | 10 | 0.090376 | 5.018 |
| w32 | 1 | 0.157215 | 7.29 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 23 | 0.069898 | 7.503 |
| w21 | 1 | 0.006136 | 0.031 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 29 | -0.04314 | -5.639 |
| w27 | 1 | 0.012317 | -0.102 |
| w28 | 29 | 0.098079 | 13.665 |
| w29 | 1 | -0.004611 | -0.332 |
| w30 | 7 | -0.040821 | -1.577 |
| w31 | 8 | 0.0937 | 5.183 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | -0.013121 | -2.847 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 4 | 0.016374 | 0.307 |
| w26 | 24 | 0.064668 | 5.881 |
| w27 | 1 | 0.022859 | 0.086 |
| w28 | 27 | 0.140675 | 14.338 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | -0.489886 | -49.735 |
| w31 | 19 | -0.020658 | -2.872 |
| w32 | 12 | -0.077643 | -5.185 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 9 | -0.030825 | -1.126 |
| w8 | 0 | None | 0.0 |
| w9 | 19 | -0.028776 | -3.706 |
| w10 | 7 | -0.002869 | -2.933 |
| w11 | 8 | 0.064949 | 3.335 |
| w12 | 0 | None | 0.0 |
| w13 | 14 | 0.120901 | 6.575 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.013142 | -0.237 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | -0.024629 | -1.723 |
| w18 | 2 | 0.018306 | -0.197 |
| w19 | 0 | None | 0.0 |
| w20 | 31 | 0.21454 | 28.534 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 9 | 0.013824 | 1.097 |
| w24 | 4 | -0.095833 | -5.769 |
| w25 | 0 | None | 0.0 |
| w26 | 27 | 0.061273 | 6.482 |
| w27 | 0 | None | 0.0 |
| w28 | 21 | 0.03901 | 2.015 |
| w29 | 1 | 0.031273 | 0.825 |
| w30 | 19 | 0.002323 | -0.107 |
| w31 | 10 | 0.003427 | 0.421 |
| w32 | 0 | None | 0.0 |

