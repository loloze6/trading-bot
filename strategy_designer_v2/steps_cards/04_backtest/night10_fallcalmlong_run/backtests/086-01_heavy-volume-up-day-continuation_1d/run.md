# Backtest of 086-01_heavy-volume-up-day-continuation_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-01_heavy-volume-up-day-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 3 | -0.022213 | 15.915 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | 0.034205 | -2.548 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.023932 | -5.016 |
| w18 | 5 | -0.024636 | 0.289 |
| w19 | 4 | -0.002077 | 13.416 |
| w20 | 3 | -0.024878 | -5.372 |
| w21 | 3 | -0.087327 | -6.56 |
| w22 | 2 | 0.053829 | 3.51 |
| w23 | 3 | 0.019796 | -0.784 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | 0.034465 | 0.029 |
| w27 | 2 | -0.038407 | 2.065 |
| w28 | 10 | -0.066714 | 37.808 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | -0.072999 | -4.164 |
| w31 | 4 | 0.029393 | -6.559 |
| w32 | 4 | -0.050305 | -34.109 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 11 | -0.031786 | -10.757 |
| w8 | 4 | -0.056507 | -10.776 |
| w9 | 1 | -0.043021 | -26.75 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.029789 | 2.25 |
| w12 | 4 | 0.044129 | 10.594 |
| w13 | 2 | -0.018876 | -1.386 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.047612 | 11.286 |
| w16 | 0 | None | 0.0 |
| w17 | 4 | 0.037657 | 17.148 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.116034 | 20.964 |
| w20 | 0 | None | 0.0 |
| w21 | 1 | 0.001758 | -0.952 |
| w22 | 2 | -0.040243 | 4.839 |
| w23 | 3 | 0.067071 | 2.12 |
| w24 | 1 | 0.018339 | 0.394 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.22568 | -15.608 |
| w29 | 0 | None | 0.0 |
| w30 | 4 | -0.043825 | -8.425 |
| w31 | 3 | -0.018597 | -1.189 |
| w32 | 2 | -0.003704 | -2.198 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 6 | 0.004771 | 6.458 |
| w11 | 3 | -0.099144 | -22.411 |
| w12 | 14 | 0.052299 | 8.886 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.019886 | -12.338 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.00402 | 6.438 |
| w18 | 0 | None | 0.0 |
| w19 | 8 | 0.197374 | 14.133 |
| w20 | 8 | 0.072674 | 1.6 |
| w21 | 10 | -0.039719 | -17.124 |
| w22 | 8 | -0.047492 | 17.827 |
| w23 | 4 | 0.095282 | 8.046 |
| w24 | 6 | 0.13707 | 7.712 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.019301 | 2.488 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.092763 | 18.555 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 6 | -0.065155 | -20.47 |
| w24 | 2 | 0.090792 | 24.251 |
| w25 | 4 | 0.032941 | 1.644 |
| w26 | 4 | 0.046135 | 15.458 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.079421 | 7.963 |
| w29 | 0 | None | 0.0 |
| w30 | 6 | 0.08682 | -7.209 |
| w31 | 8 | 0.050923 | -18.856 |
| w32 | 5 | -0.039971 | 27.617 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | -0.038534 | 8.554 |
| w23 | 10 | -0.067814 | -31.032 |
| w24 | 7 | -0.060431 | -9.453 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.03358 | -15.466 |
| w27 | 6 | 0.073747 | 0.488 |
| w28 | 6 | -0.039352 | -15.206 |
| w29 | 4 | 0.108177 | 8.662 |
| w30 | 1 | -0.009908 | -0.358 |
| w31 | 1 | -0.106862 | -6.571 |
| w32 | 5 | 0.055164 | -0.975 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 7 | -0.005287 | -3.384 |
| w21 | 2 | -0.02521 | 24.683 |
| w22 | 6 | -0.059178 | 13.396 |
| w23 | 5 | -0.133912 | -25.007 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | -0.009642 | 5.753 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.071679 | 17.514 |
| w30 | 2 | 0.00344 | -2.943 |
| w31 | 7 | 0.122135 | 5.1 |
| w32 | 7 | 0.159306 | 33.554 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 8 | 0.130764 | 20.247 |
| w21 | 3 | -0.013 | -0.887 |
| w22 | 8 | -0.023608 | -7.511 |
| w23 | 7 | 0.061558 | -2.33 |
| w24 | 5 | -0.045904 | -7.192 |
| w25 | 4 | -0.02666 | 8.231 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | 0.033651 | 11.602 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.008518 | 2.547 |
| w30 | 10 | -0.028256 | -15.497 |
| w31 | 6 | 0.13823 | 28.911 |
| w32 | 7 | -0.01795 | -16.708 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 2 | -0.011217 | 1.988 |
| w12 | 8 | 0.038898 | 12.671 |
| w13 | 2 | -0.016986 | 18.482 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 3 | 0.056217 | 6.522 |
| w18 | 4 | 0.135238 | 3.958 |
| w19 | 1 | -0.003401 | -6.861 |
| w20 | 3 | 0.067634 | -2.062 |
| w21 | 3 | -0.022738 | -3.27 |
| w22 | 3 | 0.10009 | 15.848 |
| w23 | 1 | None | -0.314 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | -0.056131 | 5.272 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.084701 | -14.911 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | -0.055025 | -5.548 |
| w32 | 0 | None | 0.0 |

