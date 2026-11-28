# Backtest of 047-02_falling-agitated-scaled-rise-fade_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/047-02_falling-agitated-scaled-rise-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 15 | 0.11172 | -1.644 |
| w14 | 0 | None | 0.0 |
| w15 | 6 | 0.000421 | -2.03 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | -0.047119 | -1.216 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 32 | 0.032339 | -2.892 |
| w21 | 11 | -0.077516 | 3.679 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.099632 | -4.748 |
| w24 | 11 | -0.098288 | -11.612 |
| w25 | 0 | None | 0.0 |
| w26 | 19 | -0.009807 | -14.944 |
| w27 | 0 | None | 0.0 |
| w28 | 15 | 0.053619 | 6.587 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | 0.114784 | -7.704 |
| w31 | 6 | 0.006793 | 1.318 |
| w32 | 14 | -0.003757 | 1.277 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 29 | -0.024017 | -12.584 |
| w27 | 1 | 0.053125 | 0.102 |
| w28 | 40 | 0.165971 | 17.704 |
| w29 | 1 | 0.040983 | 2.731 |
| w30 | 14 | -0.021417 | 1.037 |
| w31 | 9 | 0.017323 | 10.429 |
| w32 | 7 | 0.050251 | -7.621 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 5 | -0.012313 | -2.144 |
| w12 | 1 | 0.08913 | 0.412 |
| w13 | 23 | 0.056536 | -9.176 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 15 | 0.012725 | 2.616 |
| w18 | 0 | None | 0.0 |
| w19 | 11 | -0.015374 | -18.391 |
| w20 | 25 | -0.112841 | -14.779 |
| w21 | 1 | 0.001283 | -1.294 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.101638 | -6.29 |
| w25 | 21 | -0.024087 | -3.193 |
| w26 | 4 | 0.028056 | -2.829 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.219773 | -9.153 |
| w30 | 7 | -0.025351 | -7.839 |
| w31 | 15 | -0.051426 | -0.803 |
| w32 | 8 | 0.093006 | 1.552 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 7 | 0.046412 | 1.015 |
| w26 | 21 | 0.060275 | -7.066 |
| w27 | 2 | 0.089888 | 3.726 |
| w28 | 32 | 0.151445 | 22.056 |
| w29 | 0 | None | 0.0 |
| w30 | 21 | 0.018017 | 20.763 |
| w31 | 8 | 0.059819 | 13.291 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 32 | -0.034575 | 2.259 |
| w27 | 1 | 0.12984 | 3.857 |
| w28 | 23 | 0.032373 | 16.481 |
| w29 | 0 | None | 0.0 |
| w30 | 17 | 0.007129 | 2.491 |
| w31 | 9 | 0.090376 | 11.411 |
| w32 | 2 | 0.157215 | -3.525 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 25 | 0.069898 | -6.045 |
| w21 | 2 | 0.006136 | -3.015 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 32 | -0.04314 | -1.483 |
| w27 | 2 | 0.012317 | 0.567 |
| w28 | 33 | 0.098079 | 13.961 |
| w29 | 2 | -0.004611 | 3.011 |
| w30 | 11 | -0.040821 | 1.441 |
| w31 | 11 | 0.0937 | 13.657 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.013121 | -15.516 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 5 | 0.016374 | 1.123 |
| w26 | 24 | 0.064668 | 1.861 |
| w27 | 1 | 0.022859 | 0.153 |
| w28 | 27 | 0.140675 | 19.271 |
| w29 | 0 | None | 0.0 |
| w30 | 18 | -0.489886 | -34.556 |
| w31 | 24 | -0.020658 | 23.349 |
| w32 | 15 | -0.077643 | -3.605 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 7 | -0.030825 | -11.999 |
| w8 | 0 | None | 0.0 |
| w9 | 19 | -0.028776 | -3.811 |
| w10 | 10 | -0.002869 | -1.942 |
| w11 | 7 | 0.064949 | 12.934 |
| w12 | 0 | None | 0.0 |
| w13 | 14 | 0.120901 | 4.676 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.013142 | 0.548 |
| w16 | 0 | None | 0.0 |
| w17 | 16 | -0.024629 | 0.264 |
| w18 | 2 | 0.018306 | 1.177 |
| w19 | 0 | None | 0.0 |
| w20 | 30 | 0.21454 | 9.325 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 11 | 0.013824 | 7.212 |
| w24 | 4 | -0.095833 | -10.019 |
| w25 | 0 | None | 0.0 |
| w26 | 29 | 0.061273 | -9.517 |
| w27 | 0 | None | 0.0 |
| w28 | 24 | 0.03901 | -7.639 |
| w29 | 1 | 0.031273 | 4.086 |
| w30 | 22 | 0.002323 | 1.832 |
| w31 | 13 | 0.003427 | 12.343 |
| w32 | 0 | None | 0.0 |

