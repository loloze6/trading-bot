# Backtest of 089-02_calm-decline-up-down-volume-ratio_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/089-02_calm-decline-up-down-volume-ratio_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 4 | 0.072361 | 26.805 |
| w14 | 8 | 0.036114 | 6.976 |
| w15 | 3 | -0.017044 | 0.69 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.065035 | 5.604 |
| w18 | 3 | 0.095399 | -0.314 |
| w19 | 15 | 0.000349 | 0.613 |
| w20 | 2 | 0.004268 | -1.639 |
| w21 | 6 | -0.094097 | -10.002 |
| w22 | 4 | 0.071921 | 0.765 |
| w23 | 0 | -0.007886 | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | 0.028841 | 0.888 |
| w27 | 10 | -0.08293 | -7.492 |
| w28 | 7 | -0.087835 | -7.126 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | 0.033257 | 0.227 |
| w31 | 17 | -0.019093 | -7.904 |
| w32 | 19 | -0.106669 | -24.086 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 3 | -0.118133 | -6.492 |
| w8 | 17 | -0.151516 | -26.488 |
| w9 | 12 | 0.061215 | -9.318 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.133108 | -2.399 |
| w12 | 19 | -0.052346 | -10.362 |
| w13 | 4 | -0.010376 | -0.736 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.01782 | -0.016 |
| w19 | 14 | 0.149197 | -3.425 |
| w20 | 0 | None | 0.0 |
| w21 | 5 | -0.005801 | -1.994 |
| w22 | 3 | 0.017569 | 2.042 |
| w23 | 4 | 0.124746 | 2.153 |
| w24 | 14 | 0.004573 | 3.428 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 7 | -0.127787 | -7.743 |
| w28 | 3 | 0.05295 | 3.159 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 16 | 0.077162 | 9.861 |
| w32 | 1 | -0.073149 | -0.214 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 22 | -0.083067 | -1.384 |
| w11 | 13 | -0.114211 | -14.04 |
| w12 | 18 | -0.226792 | -31.317 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.081071 | -1.349 |
| w15 | 14 | 0.02465 | 3.494 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 25 | -0.061953 | -12.026 |
| w20 | 3 | 0.084705 | 2.686 |
| w21 | 17 | 0.021796 | -1.687 |
| w22 | 15 | 0.066937 | 11.693 |
| w23 | 7 | 0.034091 | -10.625 |
| w24 | 18 | 0.036298 | 10.288 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | 0.053753 | 16.977 |
| w27 | 7 | 0.085737 | 7.901 |
| w28 | 2 | 0.180561 | 2.463 |
| w29 | 2 | -0.067749 | -0.269 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 16 | 0.014776 | 1.506 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 16 | -0.113063 | -24.35 |
| w24 | 10 | 0.08945 | 15.337 |
| w25 | 6 | 0.063479 | 11.894 |
| w26 | 11 | -0.040805 | -3.649 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.377523 | 6.671 |
| w30 | 2 | 0.014677 | 3.296 |
| w31 | 25 | 0.044841 | -14.469 |
| w32 | 16 | 0.05778 | 16.58 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.089701 | 10.472 |
| w23 | 9 | 0.066484 | 0.089 |
| w24 | 0 | -0.00454 | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 21 | 0.051178 | -4.638 |
| w27 | 8 | 0.044977 | 7.01 |
| w28 | 9 | 0.091522 | 5.689 |
| w29 | 2 | 0.03708 | 0.355 |
| w30 | 4 | -0.005856 | -8.958 |
| w31 | 8 | -0.041001 | -3.35 |
| w32 | 13 | -0.057825 | -9.462 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 13 | -0.026406 | -6.376 |
| w21 | 4 | 0.014178 | -1.185 |
| w22 | 2 | 0.040317 | 0.042 |
| w23 | 6 | -0.111883 | -6.691 |
| w24 | 10 | -0.055313 | -2.796 |
| w25 | 6 | 0.027915 | 29.479 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | 0.059718 | 2.275 |
| w28 | 2 | -0.037553 | -6.561 |
| w29 | 9 | 0.092662 | 5.11 |
| w30 | 16 | -0.062974 | -9.059 |
| w31 | 21 | 0.069238 | 4.504 |
| w32 | 29 | 0.07993 | 27.531 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 17 | 0.10327 | 2.56 |
| w21 | 8 | -0.008453 | -2.04 |
| w22 | 17 | 0.108327 | -6.07 |
| w23 | 18 | -0.096133 | -25.961 |
| w24 | 6 | -0.056327 | -1.504 |
| w25 | 2 | -0.036063 | 0.528 |
| w26 | 10 | -0.039913 | -2.548 |
| w27 | 11 | 0.01372 | 12.816 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.240271 | 8.943 |
| w30 | 19 | -0.086899 | -17.446 |
| w31 | 21 | 0.093886 | 30.736 |
| w32 | 24 | 0.068289 | 7.942 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 1 | -0.085801 | -3.532 |
| w12 | 28 | 0.003533 | -23.158 |
| w13 | 4 | 0.13789 | 7.454 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | -0.015927 | 0.0 |
| w18 | 14 | 0.109649 | 11.355 |
| w19 | 7 | -0.022179 | -6.137 |
| w20 | 6 | 0.014488 | 1.175 |
| w21 | 3 | 0.064888 | -0.138 |
| w22 | 8 | 0.130392 | 6.193 |
| w23 | 4 | -0.027737 | 0.024 |
| w24 | 5 | 0.053962 | 0.288 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.118978 | 18.376 |
| w29 | 1 | -0.076474 | -4.51 |
| w30 | 0 | None | 0.0 |
| w31 | 12 | 0.009573 | -0.657 |
| w32 | 1 | 0.02138 | 0.537 |

