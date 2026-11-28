# Backtest of 033-02.d1_high-close-fades-in-selloffs_1d

- Plan: `../../../../03_test_plan/night10_fallagishort_run/plans/033-02.d1_high-close-fades-in-selloffs_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, AVAX, XMR, INJ, GRT, DOGE, FIL, LTC as BCHUSD, AVAXUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, FILUSD, LTCUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 31 | -0.018126 | -7.918 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.016224 | -2.927 |
| w16 | 0 | None | 0.0 |
| w17 | 19 | 0.012162 | 0.324 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 66 | 0.031736 | 10.955 |
| w21 | 17 | -0.128466 | -11.208 |
| w22 | 0 | None | 0.0 |
| w23 | 6 | 0.032039 | 0.151 |
| w24 | 20 | -0.091508 | -12.658 |
| w25 | 0 | None | 0.0 |
| w26 | 42 | -0.087228 | -16.046 |
| w27 | 2 | -0.059323 | -1.233 |
| w28 | 27 | 0.111176 | 12.872 |
| w29 | 1 | -0.142667 | -2.524 |
| w30 | 13 | 0.041661 | 2.028 |
| w31 | 19 | -0.007649 | -0.775 |
| w32 | 22 | -0.039763 | 1.295 |

- AVAXUSD: 7 of 32 windows run. 25 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18, w19 (the coin's first 90 days); w20, w21, w22, w23, w24, w25 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w26 | 55 | -0.073513 | -12.251 |
| w27 | 2 | 0.038636 | 1.023 |
| w28 | 67 | 0.047212 | 15.922 |
| w29 | 1 | 0.040983 | 0.997 |
| w30 | 24 | -0.031229 | -0.333 |
| w31 | 26 | -0.052493 | -3.446 |
| w32 | 13 | -0.027827 | -2.234 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 7 | -0.00596 | -0.871 |
| w12 | 2 | 0.021599 | 1.166 |
| w13 | 38 | -0.003232 | -6.993 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 34 | 0.035048 | 0.695 |
| w18 | 0 | None | 0.0 |
| w19 | 25 | -0.071361 | -10.91 |
| w20 | 43 | -0.080165 | -13.892 |
| w21 | 5 | -0.005553 | -1.361 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.018714 | -4.362 |
| w25 | 41 | -0.118395 | -16.915 |
| w26 | 5 | -0.031999 | -3.404 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 12 | -0.136456 | -16.765 |
| w30 | 11 | -0.035971 | -8.935 |
| w31 | 27 | -0.012425 | -2.979 |
| w32 | 18 | 0.057129 | 0.917 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 18 | 0.047933 | 5.567 |
| w26 | 40 | -0.031254 | -7.068 |
| w27 | 5 | 0.102294 | 4.14 |
| w28 | 60 | 0.091914 | 21.029 |
| w29 | 0 | None | 0.0 |
| w30 | 46 | -0.035363 | 5.034 |
| w31 | 15 | 0.078544 | 6.168 |
| w32 | 0 | None | 0.0 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 2 | -0.02187 | -0.377 |
| w26 | 60 | -0.098098 | -14.925 |
| w27 | 2 | 0.112922 | 4.275 |
| w28 | 47 | 0.033572 | 11.488 |
| w29 | 0 | None | 0.0 |
| w30 | 37 | -0.176138 | -16.091 |
| w31 | 24 | 0.001153 | 1.327 |
| w32 | 2 | 0.036758 | 1.701 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 48 | -0.064111 | 0.172 |
| w21 | 1 | 0.006136 | 0.054 |
| w22 | 2 | -0.075409 | -1.147 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 72 | -0.09801 | -11.599 |
| w27 | 3 | -0.00842 | -2.12 |
| w28 | 74 | 0.012543 | 10.228 |
| w29 | 1 | -0.004611 | -0.362 |
| w30 | 23 | -0.027413 | 0.084 |
| w31 | 23 | 0.002735 | -1.779 |
| w32 | 0 | None | 0.0 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 4 | -0.037835 | -5.918 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 8 | 0.027225 | 1.655 |
| w26 | 60 | -0.042966 | -4.358 |
| w27 | 2 | 0.005232 | -0.355 |
| w28 | 49 | 0.038246 | 10.123 |
| w29 | 0 | None | 0.0 |
| w30 | 38 | -0.206845 | -39.577 |
| w31 | 51 | -0.026323 | -0.351 |
| w32 | 24 | -0.045443 | -4.853 |

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 18 | -0.145389 | -11.629 |
| w8 | 0 | None | 0.0 |
| w9 | 44 | -0.021421 | 0.806 |
| w10 | 17 | 0.030096 | -4.882 |
| w11 | 18 | 0.026632 | 1.029 |
| w12 | 0 | None | 0.0 |
| w13 | 32 | 0.068651 | 4.393 |
| w14 | 0 | None | 0.0 |
| w15 | 8 | 0.027167 | -0.919 |
| w16 | 0 | None | 0.0 |
| w17 | 36 | -0.048996 | -5.052 |
| w18 | 4 | 0.024725 | 1.549 |
| w19 | 0 | None | 0.0 |
| w20 | 58 | 0.035176 | 16.197 |
| w21 | 1 | -0.393083 | -4.923 |
| w22 | 2 | -0.045578 | -0.76 |
| w23 | 20 | -0.010439 | -0.685 |
| w24 | 5 | -0.142118 | -7.38 |
| w25 | 1 | 0.045338 | 2.489 |
| w26 | 50 | -0.061758 | -4.086 |
| w27 | 1 | -0.047127 | -0.95 |
| w28 | 37 | 0.030577 | 3.773 |
| w29 | 4 | 0.025688 | 0.813 |
| w30 | 42 | -0.057307 | -5.661 |
| w31 | 22 | -0.088656 | -4.666 |
| w32 | 0 | None | 0.0 |

