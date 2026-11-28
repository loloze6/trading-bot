# Backtest of 086-02.c2_quiet-three-day-rise-continuation_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/086-02.c2_quiet-three-day-rise-continuation_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 4 | 0.017009 | 0.972 |
| w14 | 4 | -0.072416 | 2.553 |
| w15 | 6 | 0.049681 | 4.772 |
| w16 | 0 | None | 0.0 |
| w17 | 11 | 0.012165 | 6.628 |
| w18 | 9 | -0.030861 | -5.371 |
| w19 | 25 | -0.00424 | -6.292 |
| w20 | 3 | 0.120997 | 4.516 |
| w21 | 6 | 0.035105 | 1.399 |
| w22 | 6 | 0.066507 | 6.15 |
| w23 | 5 | -0.028556 | 17.41 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | 0.071174 | -8.789 |
| w27 | 8 | 0.038041 | -5.068 |
| w28 | 8 | -0.110326 | -14.373 |
| w29 | 0 | None | 0.0 |
| w30 | 8 | 0.084944 | 9.562 |
| w31 | 14 | -0.05925 | -11.316 |
| w32 | 9 | -0.053606 | -8.762 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 12 | 0.04982 | 23.453 |
| w8 | 18 | 0.051338 | -16.49 |
| w9 | 10 | 0.00691 | -11.673 |
| w10 | 0 | None | 0.0 |
| w11 | 4 | -0.152215 | -4.998 |
| w12 | 15 | 0.138499 | 10.189 |
| w13 | 2 | 0.024035 | 0.925 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.090209 | 3.675 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.018846 | 5.063 |
| w18 | 0 | None | 0.0 |
| w19 | 15 | 0.075784 | -14.331 |
| w20 | 0 | None | 0.0 |
| w21 | 16 | 0.030424 | 6.744 |
| w22 | 3 | 0.059251 | 2.257 |
| w23 | 6 | 0.105144 | 15.113 |
| w24 | 9 | -0.028862 | -5.687 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 4 | -0.074686 | -7.361 |
| w28 | 5 | -0.015609 | -11.277 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.083247 | 1.769 |
| w31 | 5 | 0.117837 | 5.45 |
| w32 | 13 | 0.049689 | -10.612 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 8 | -0.14693 | -9.265 |
| w11 | 4 | -0.035716 | -3.055 |
| w12 | 14 | -0.049791 | -7.869 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 4 | -0.021579 | -2.69 |
| w16 | 0 | None | 0.0 |
| w17 | 13 | 0.098269 | 12.171 |
| w18 | 5 | 0.107496 | 11.492 |
| w19 | 15 | 0.081215 | 5.907 |
| w20 | 7 | 0.15476 | 15.659 |
| w21 | 14 | 0.021022 | -8.81 |
| w22 | 7 | -0.041489 | 7.463 |
| w23 | 8 | -0.07353 | -21.469 |
| w24 | 12 | -0.04229 | 5.713 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | 0.041846 | 9.623 |
| w27 | 4 | 0.09524 | 14.399 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | -0.040204 | -4.887 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 5 | -0.055875 | 1.911 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 9 | -0.025467 | -0.693 |
| w24 | 1 | -0.01524 | -2.824 |
| w25 | 2 | -0.024843 | 0.481 |
| w26 | 3 | -0.110781 | -5.122 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | -0.241607 | 0.0 |
| w29 | 2 | 0.377523 | 4.805 |
| w30 | 10 | 0.050777 | -12.779 |
| w31 | 14 | 0.001048 | 3.988 |
| w32 | 6 | -0.006692 | -2.679 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 6 | 0.089083 | 14.796 |
| w23 | 16 | 0.151298 | 15.53 |
| w24 | 14 | -0.08401 | -9.102 |
| w25 | 0 | None | 0.0 |
| w26 | 16 | -0.032324 | -14.272 |
| w27 | 6 | -0.067886 | -0.654 |
| w28 | 8 | 0.013187 | -13.828 |
| w29 | 10 | -0.005215 | 9.61 |
| w30 | 7 | -0.004773 | -14.225 |
| w31 | 13 | -0.031541 | -10.534 |
| w32 | 15 | -0.038918 | 52.503 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | 0.081491 | 7.465 |
| w21 | 15 | -0.043035 | 15.187 |
| w22 | 11 | 0.093179 | 32.864 |
| w23 | 10 | -0.06793 | 0.172 |
| w24 | 12 | -0.121774 | -11.305 |
| w25 | 5 | -0.004645 | 2.235 |
| w26 | 7 | -0.123104 | -17.567 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | 0.269677 | 10.017 |
| w30 | 9 | -0.000922 | -9.386 |
| w31 | 11 | -0.066102 | -2.641 |
| w32 | 13 | 0.080652 | 46.515 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 9 | 0.016076 | -5.967 |
| w21 | 4 | -0.024418 | 9.228 |
| w22 | 4 | 0.004328 | 2.509 |
| w23 | 29 | -0.01077 | -33.097 |
| w24 | 10 | -0.09085 | -15.612 |
| w25 | 5 | 0.07542 | 8.496 |
| w26 | 18 | -0.017633 | -8.744 |
| w27 | 5 | -0.094638 | 0.475 |
| w28 | 0 | None | 0.0 |
| w29 | 5 | 0.098728 | 29.139 |
| w30 | 17 | -0.075007 | -18.174 |
| w31 | 17 | 0.013914 | 2.517 |
| w32 | 19 | 0.078745 | 25.274 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 3 | -0.098122 | -4.46 |
| w12 | 18 | -0.000484 | -9.582 |
| w13 | 3 | 0.004452 | 0.685 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.040329 | 0.928 |
| w18 | 10 | 0.125759 | 0.314 |
| w19 | 5 | 0.234698 | 7.232 |
| w20 | 9 | -0.005622 | 3.35 |
| w21 | 5 | -0.008823 | -2.725 |
| w22 | 6 | 0.04762 | 3.823 |
| w23 | 4 | 0.100285 | 17.023 |
| w24 | 7 | -0.103769 | 4.166 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.061665 | 2.489 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | 0.168803 | 3.916 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 6 | -0.071503 | -0.81 |
| w32 | 5 | 0.009952 | 4.809 |

