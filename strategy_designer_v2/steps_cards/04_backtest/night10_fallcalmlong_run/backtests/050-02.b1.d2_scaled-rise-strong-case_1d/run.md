# Backtest of 050-02.b1.d2_scaled-rise-strong-case_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/050-02.b1.d2_scaled-rise-strong-case_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 11 | 0.040656 | 30.337 |
| w14 | 3 | -0.060163 | -2.1 |
| w15 | 6 | 0.011766 | 4.182 |
| w16 | 0 | None | 0.0 |
| w17 | 8 | 0.047324 | 15.533 |
| w18 | 9 | -0.063752 | -7.406 |
| w19 | 15 | 0.000606 | -1.045 |
| w20 | 2 | 0.025454 | -1.251 |
| w21 | 2 | -0.099484 | -5.267 |
| w22 | 3 | -0.015776 | 4.117 |
| w23 | 4 | -0.008175 | 9.608 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | -0.066081 | -10.407 |
| w27 | 8 | -0.081978 | -8.267 |
| w28 | 6 | 0.281589 | 20.462 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.133372 | -2.322 |
| w31 | 13 | -0.062887 | -3.735 |
| w32 | 3 | 0.049317 | 1.543 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 13 | 0.128085 | 24.224 |
| w8 | 17 | -0.017721 | -9.942 |
| w9 | 5 | -0.005217 | -0.465 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.048698 | -0.771 |
| w12 | 14 | 0.121779 | 15.303 |
| w13 | 12 | -0.016982 | 13.03 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.067374 | -3.814 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.042074 | 3.584 |
| w18 | 0 | None | 0.0 |
| w19 | 13 | 0.048125 | -1.896 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.019931 | 9.393 |
| w22 | 2 | -0.015467 | 0.918 |
| w23 | 3 | -0.077045 | -9.684 |
| w24 | 5 | 0.029225 | 1.379 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 3 | 0.022947 | 0.389 |
| w28 | 5 | -0.211331 | -14.65 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.030237 | -3.418 |
| w31 | 11 | 0.044852 | 5.858 |
| w32 | 15 | -0.036165 | -2.006 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 8 | 0.08859 | -0.015 |
| w11 | 1 | -0.017439 | 0.076 |
| w12 | 15 | -0.028848 | -9.681 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.013878 | -1.177 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.09485 | 20.415 |
| w18 | 0 | -0.016409 | 0.0 |
| w19 | 11 | 0.062468 | 11.943 |
| w20 | 13 | 0.010514 | -0.244 |
| w21 | 9 | -0.055284 | -5.356 |
| w22 | 14 | -0.007522 | 0.626 |
| w23 | 6 | -0.078985 | -14.596 |
| w24 | 17 | 0.020681 | 1.649 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | 0.055369 | 13.901 |
| w27 | 5 | 0.211412 | 24.389 |
| w28 | 2 | 0.180561 | 1.338 |
| w29 | 4 | -0.119934 | -13.819 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 8 | 0.036861 | 3.579 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 10 | 0.209577 | 19.07 |
| w24 | 5 | 0.083823 | 8.459 |
| w25 | 8 | 0.056003 | 5.902 |
| w26 | 7 | 0.089895 | 17.531 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 4.437 |
| w30 | 8 | 0.083223 | 1.538 |
| w31 | 12 | 0.065231 | -4.005 |
| w32 | 7 | 0.005373 | 3.118 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.014869 | 7.385 |
| w23 | 18 | -0.003431 | -12.573 |
| w24 | 12 | -0.121414 | -13.247 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | -0.077863 | -10.367 |
| w27 | 6 | -0.019787 | 1.02 |
| w28 | 8 | 0.041181 | 2.975 |
| w29 | 9 | 0.020136 | 2.383 |
| w30 | 5 | -0.014921 | -8.082 |
| w31 | 8 | -0.002551 | -2.33 |
| w32 | 8 | -0.069817 | -10.283 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | -0.045206 | -4.41 |
| w21 | 7 | -0.039661 | 7.487 |
| w22 | 23 | 0.178431 | 44.217 |
| w23 | 10 | -0.05642 | -11.087 |
| w24 | 10 | -0.0832 | -6.487 |
| w25 | 8 | -0.001494 | 1.106 |
| w26 | 1 | -0.079041 | -0.397 |
| w27 | 6 | -0.065763 | 1.401 |
| w28 | 2 | -0.04484 | -3.473 |
| w29 | 3 | 0.074275 | 10.184 |
| w30 | 5 | -0.052977 | -7.258 |
| w31 | 16 | 0.035914 | -0.683 |
| w32 | 11 | 0.07949 | 29.124 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 10 | -0.004054 | -1.739 |
| w21 | 0 | -0.045033 | 0.0 |
| w22 | 8 | 0.076293 | 0.803 |
| w23 | 10 | 0.068321 | 0.885 |
| w24 | 4 | -0.036834 | 0.754 |
| w25 | 10 | 0.002512 | -2.183 |
| w26 | 23 | 0.066516 | -9.181 |
| w27 | 7 | -0.040784 | -3.308 |
| w28 | 0 | None | 0.0 |
| w29 | 12 | 0.287329 | 31.091 |
| w30 | 15 | -0.153738 | -22.956 |
| w31 | 11 | 0.014899 | 13.042 |
| w32 | 10 | -0.012618 | -7.066 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 0 | 0.024847 | 0.0 |
| w12 | 18 | -0.014385 | -5.95 |
| w13 | 4 | 0.101635 | 19.294 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.040201 | 10.258 |
| w18 | 5 | 0.003991 | 2.159 |
| w19 | 10 | -0.115011 | -11.222 |
| w20 | 14 | -0.036849 | 3.521 |
| w21 | 4 | -0.071678 | -0.423 |
| w22 | 9 | 0.090918 | 4.344 |
| w23 | 1 | -0.169013 | -0.225 |
| w24 | 3 | 0.056548 | -0.061 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.085349 | -0.457 |
| w27 | 0 | None | 0.0 |
| w28 | 3 | 0.034389 | 13.042 |
| w29 | 0 | -0.007473 | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 5 | -0.015589 | -2.888 |
| w32 | 6 | 0.024279 | 5.639 |

