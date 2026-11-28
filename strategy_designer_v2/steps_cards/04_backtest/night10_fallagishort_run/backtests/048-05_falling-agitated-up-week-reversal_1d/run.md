# Backtest of 048-05_falling-agitated-up-week-reversal_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/048-05_falling-agitated-up-week-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 8 | 0.050173 | 2.197 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.037534 | 1.161 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | -0.01317 | 0.281 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 13 | 0.063871 | 6.232 |
| w21 | 9 | -0.020305 | 0.521 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | 0.071227 | 3.736 |
| w24 | 9 | -0.010363 | -1.577 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | -0.045464 | 3.305 |
| w27 | 0 | None | 0.0 |
| w28 | 5 | 0.099324 | 8.144 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.008577 | -1.03 |
| w31 | 5 | -0.049212 | -0.6 |
| w32 | 7 | -0.047037 | -1.728 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 30 | -0.012097 | -5.5 |
| w27 | 0 | None | 0.0 |
| w28 | 21 | 0.033036 | 6.065 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.146392 | 0.46 |
| w31 | 10 | -0.012743 | -0.902 |
| w32 | 7 | -0.003622 | -1.043 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 0 | -0.045014 | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 19 | 0.002185 | -4.077 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.035832 | 3.086 |
| w18 | 0 | None | 0.0 |
| w19 | 10 | -0.118135 | -3.839 |
| w20 | 17 | -0.001229 | -6.671 |
| w21 | 2 | -0.015975 | -1.628 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.058763 | -1.243 |
| w25 | 8 | -0.112141 | -3.279 |
| w26 | 4 | -0.064523 | -4.474 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 8 | -0.034529 | 4.776 |
| w30 | 5 | -0.095351 | -4.896 |
| w31 | 6 | 0.010573 | 1.139 |
| w32 | 7 | 0.105932 | 1.547 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | 0.078869 | 4.23 |
| w26 | 13 | 0.070414 | 4.061 |
| w27 | 0 | None | 0.0 |
| w28 | 14 | 0.086689 | 7.684 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | 0.215234 | 14.706 |
| w31 | 6 | 0.076809 | 3.877 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | -0.023211 | 0.0 |
| w26 | 29 | -0.061097 | -9.256 |
| w27 | 0 | None | 0.0 |
| w28 | 13 | 0.099697 | 10.542 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | 0.175241 | 10.915 |
| w31 | 4 | 0.039916 | 0.243 |
| w32 | 2 | -0.062532 | -3.525 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 10 | -0.007583 | -0.742 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 20 | -0.062994 | -5.512 |
| w27 | 0 | None | 0.0 |
| w28 | 18 | 0.011494 | 4.943 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.073506 | 0.037 |
| w31 | 5 | 0.121423 | 0.218 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | -0.017277 | -12.363 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 3 | 0.072428 | 1.711 |
| w26 | 15 | -0.05009 | -3.628 |
| w27 | 0 | None | 0.0 |
| w28 | 15 | 0.079057 | 4.35 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | -0.355666 | -23.964 |
| w31 | 20 | 0.080833 | 9.998 |
| w32 | 8 | -0.049143 | -1.213 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 2 | -0.051342 | -11.423 |
| w8 | 0 | None | 0.0 |
| w9 | 14 | -0.012681 | 1.79 |
| w10 | 6 | 0.061821 | -0.459 |
| w11 | 6 | -0.005676 | -0.034 |
| w12 | 0 | None | 0.0 |
| w13 | 9 | 0.052991 | 1.152 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | 0.024753 | -0.085 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | -0.016616 | 0.064 |
| w18 | 0 | 0.156228 | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 14 | 0.034851 | 4.306 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | 0.076287 | 3.998 |
| w24 | 1 | 0.035514 | -0.032 |
| w25 | 0 | None | 0.0 |
| w26 | 17 | -0.108051 | -7.411 |
| w27 | 0 | None | 0.0 |
| w28 | 11 | 0.011603 | 1.24 |
| w29 | 1 | 0.0463 | 1.424 |
| w30 | 8 | 0.086307 | 4.745 |
| w31 | 6 | -0.061117 | -0.582 |
| w32 | 0 | None | 0.0 |

