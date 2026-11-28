# Backtest of 050-02.b1.d1_large-scaled-rise-longer-hold_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d1_large-scaled-rise-longer-hold_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 6 | 0.040656 | 60.989 |
| w14 | 3 | -0.060163 | -3.696 |
| w15 | 6 | 0.011766 | 5.553 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.047324 | 13.966 |
| w18 | 8 | -0.063752 | 2.239 |
| w19 | 16 | 0.000606 | -11.304 |
| w20 | 3 | 0.025454 | 21.87 |
| w21 | 2 | -0.099484 | -10.622 |
| w22 | 3 | -0.015776 | 23.916 |
| w23 | 6 | -0.008175 | 86.368 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.066081 | -14.582 |
| w27 | 8 | -0.081978 | -6.495 |
| w28 | 6 | 0.281589 | -4.601 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.133372 | 2.505 |
| w31 | 8 | -0.062887 | -7.843 |
| w32 | 3 | 0.049317 | -3.194 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 8 | 0.128085 | 36.231 |
| w8 | 13 | -0.017721 | -17.756 |
| w9 | 5 | -0.005217 | -6.483 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.048698 | -2.842 |
| w12 | 11 | 0.121779 | -16.654 |
| w13 | 4 | -0.016982 | 28.178 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.067374 | 6.594 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.042074 | 17.695 |
| w18 | 0 | None | 0.0 |
| w19 | 12 | 0.048125 | -20.963 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.019931 | 18.129 |
| w22 | 2 | -0.015467 | 20.647 |
| w23 | 3 | -0.077045 | -9.684 |
| w24 | 4 | 0.029225 | -5.509 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | 0.022947 | -5.77 |
| w28 | 3 | -0.211331 | -18.714 |
| w29 | 0 | None | 0.0 |
| w30 | 11 | 0.030237 | -10.276 |
| w31 | 10 | 0.044852 | 6.887 |
| w32 | 10 | -0.036165 | 10.127 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 5 | 0.08859 | -7.987 |
| w11 | 2 | -0.017439 | -1.687 |
| w12 | 14 | -0.028848 | -39.419 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.013878 | 9.932 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.09485 | 21.543 |
| w18 | 0 | -0.016409 | 0.0 |
| w19 | 10 | 0.062468 | 36.712 |
| w20 | 7 | 0.010514 | 6.804 |
| w21 | 4 | -0.055284 | -1.299 |
| w22 | 11 | -0.007522 | -3.813 |
| w23 | 5 | -0.078985 | -24.457 |
| w24 | 11 | 0.020681 | 3.411 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.055369 | 20.013 |
| w27 | 5 | 0.211412 | 29.48 |
| w28 | 2 | 0.180561 | 1.338 |
| w29 | 3 | -0.119934 | 15.502 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | 0.036861 | 3.376 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 9 | 0.209577 | 23.819 |
| w24 | 4 | 0.083823 | 26.059 |
| w25 | 8 | 0.056003 | 34.155 |
| w26 | 7 | 0.089895 | 12.224 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 4.004 |
| w30 | 7 | 0.083223 | -10.87 |
| w31 | 12 | 0.065231 | -13.657 |
| w32 | 5 | 0.005373 | 7.982 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | 0.014869 | 26.247 |
| w23 | 10 | -0.003431 | -17.477 |
| w24 | 10 | -0.121414 | -18.368 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.077863 | -18.345 |
| w27 | 8 | -0.019787 | -2.839 |
| w28 | 3 | 0.041181 | 5.41 |
| w29 | 7 | 0.020136 | 18.36 |
| w30 | 4 | -0.014921 | -10.961 |
| w31 | 8 | -0.002551 | -3.056 |
| w32 | 9 | -0.069817 | -10.091 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 6 | -0.045206 | 3.285 |
| w21 | 9 | -0.039661 | 78.928 |
| w22 | 11 | 0.178431 | 13.499 |
| w23 | 9 | -0.05642 | 5.781 |
| w24 | 11 | -0.0832 | -14.028 |
| w25 | 7 | -0.001494 | 5.59 |
| w26 | 1 | -0.079041 | -2.352 |
| w27 | 6 | -0.065763 | -0.928 |
| w28 | 2 | -0.04484 | -6.966 |
| w29 | 4 | 0.074275 | 40.181 |
| w30 | 5 | -0.052977 | -11.311 |
| w31 | 15 | 0.035914 | -1.022 |
| w32 | 10 | 0.07949 | 22.725 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 11 | -0.004054 | -2.322 |
| w21 | 0 | -0.045033 | 0.0 |
| w22 | 8 | 0.076293 | -6.558 |
| w23 | 10 | 0.068321 | -2.489 |
| w24 | 5 | -0.036834 | -1.345 |
| w25 | 8 | 0.002512 | 34.257 |
| w26 | 15 | 0.066516 | -7.282 |
| w27 | 6 | -0.040784 | 2.152 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.287329 | 42.721 |
| w30 | 13 | -0.153738 | -50.024 |
| w31 | 11 | 0.014899 | -1.519 |
| w32 | 7 | -0.012618 | -15.891 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 0 | 0.024847 | 0.0 |
| w12 | 9 | -0.014385 | 3.834 |
| w13 | 4 | 0.101635 | 15.375 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.040201 | 20.695 |
| w18 | 5 | 0.003991 | 0.302 |
| w19 | 7 | -0.115011 | -25.599 |
| w20 | 3 | -0.036849 | 11.116 |
| w21 | 4 | -0.071678 | -0.1 |
| w22 | 7 | 0.090918 | 6.906 |
| w23 | 1 | -0.169013 | -0.225 |
| w24 | 3 | 0.056548 | 0.172 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.085349 | 12.648 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | 0.034389 | 47.376 |
| w29 | 0 | -0.007473 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.015589 | -4.898 |
| w32 | 3 | 0.024279 | 8.011 |

