# Backtest of 086-01.c2_heavy-up-day-extends-rebound_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-01.c2_heavy-up-day-extends-rebound_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 3 | -0.036386 | 30.795 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | 0.036482 | 6.35 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.047865 | 6.35 |
| w19 | 2 | -0.067883 | -9.78 |
| w20 | 2 | -0.042291 | 7.023 |
| w21 | 1 | -0.065321 | -10.607 |
| w22 | 2 | 0.053829 | 26.035 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.080194 | 5.75 |
| w29 | 0 | None | 0.0 |
| w30 | 2 | 0.003651 | 10.548 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.056087 | -1.053 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 4 | 0.001253 | 24.846 |
| w8 | 1 | -0.067896 | -4.84 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 2 | 0.133113 | -20.84 |
| w13 | 2 | -0.018876 | 16.415 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.04041 | 19.755 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.001758 | -1.504 |
| w22 | 2 | -0.040678 | 20.841 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.015899 | -2.425 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.22568 | -21.39 |
| w29 | 0 | None | 0.0 |
| w30 | 2 | -0.065772 | -11.348 |
| w31 | 3 | -0.018024 | -1.587 |
| w32 | 0 | None | 0.0 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 2 | -0.02066 | -5.224 |
| w11 | 0 | None | 0.0 |
| w12 | 11 | 0.085921 | -37.24 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.072096 | -7.73 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.00402 | 12.857 |
| w18 | 0 | None | 0.0 |
| w19 | 4 | 0.148 | 29.321 |
| w20 | 4 | 0.035799 | -1.817 |
| w21 | 6 | -0.142306 | -31.307 |
| w22 | 4 | -0.010791 | -1.699 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | 0.067437 | -8.245 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.019301 | 12.058 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 2 | 0.071018 | 24.488 |
| w24 | 1 | 0.092144 | 4.734 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.037737 | 14.257 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 4 | 0.202289 | -5.738 |
| w32 | 2 | 0.052839 | 12.278 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | -0.038534 | 34.425 |
| w23 | 7 | -0.045908 | -38.163 |
| w24 | 6 | -0.05174 | 2.289 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.069626 | -26.432 |
| w27 | 5 | 0.073362 | -2.333 |
| w28 | 2 | 0.060002 | 0.963 |
| w29 | 2 | 0.035169 | 1.923 |
| w30 | 1 | -0.009908 | -0.564 |
| w31 | 1 | -0.106862 | -16.241 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 5 | 0.004559 | -0.886 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.006768 | 10.708 |
| w23 | 2 | -0.08223 | -0.93 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | -0.009642 | 0.813 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.040082 | 34.157 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | 0.042903 | 3.61 |
| w32 | 3 | 0.160326 | 22.346 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 2 | -0.06977 | -7.289 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | -0.086957 | -4.602 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.098531 | 1.459 |
| w25 | 4 | -0.02666 | 7.663 |
| w26 | 0 | None | 0.0 |
| w27 | 2 | 0.020531 | 0.841 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.042254 | -29.103 |
| w31 | 2 | -0.067867 | -5.356 |
| w32 | 6 | -0.026813 | -17.619 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 0 | None | 0.0 |
| w12 | 5 | -0.037636 | 5.248 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.061423 | 10.683 |
| w18 | 2 | 0.040801 | 1.378 |
| w19 | 2 | -0.003401 | -2.932 |
| w20 | 2 | -0.000926 | 1.927 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.101654 | 3.541 |
| w23 | 1 | None | -0.314 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

