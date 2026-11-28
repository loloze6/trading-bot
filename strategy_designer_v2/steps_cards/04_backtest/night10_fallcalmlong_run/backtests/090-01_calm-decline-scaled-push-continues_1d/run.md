# Backtest of 090-01_calm-decline-scaled-push-continues_1d

- Plan: `../../../../03_test_plan/night10_fallcalmlong_run/plans/090-01_calm-decline-scaled-push-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BCH, ETH, ZEC, AAVE, FIL, DOGE, ALGO, XMR as BCHUSD, ETHUSD, ZECUSD, AAVEUSD, FILUSD, DOGEUSD, ALGOUSD, XMRUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BCHUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's first 90 days); w7, w8, w9, w10, w11, w12 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w13 | 11 | 0.008466 | 8.524 |
| w14 | 5 | -0.07531 | 1.473 |
| w15 | 6 | 0.036832 | 6.529 |
| w16 | 0 | None | 0.0 |
| w17 | 9 | 0.062489 | 19.819 |
| w18 | 13 | 0.017631 | -2.784 |
| w19 | 25 | 0.029659 | -10.927 |
| w20 | 6 | 0.097911 | 11.678 |
| w21 | 6 | -0.031982 | 0.909 |
| w22 | 6 | -0.008299 | 5.748 |
| w23 | 6 | -0.005225 | 85.198 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.006261 | -9.242 |
| w27 | 11 | -0.038158 | -8.539 |
| w28 | 10 | 0.129588 | 16.805 |
| w29 | 0 | None | 0.0 |
| w30 | 7 | -0.027693 | 1.623 |
| w31 | 17 | -0.080488 | -6.185 |
| w32 | 4 | -0.033754 | -0.451 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 14 | 0.113243 | 21.324 |
| w8 | 27 | -0.039255 | -17.115 |
| w9 | 6 | 0.018271 | -4.443 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.08076 | -3.84 |
| w12 | 20 | 0.000853 | 1.776 |
| w13 | 8 | 0.00965 | 14.265 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.031396 | 0.322 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.04263 | 12.083 |
| w18 | 0 | None | 0.0 |
| w19 | 22 | -0.004396 | -5.491 |
| w20 | 0 | None | 0.0 |
| w21 | 12 | 0.087497 | 12.509 |
| w22 | 5 | -0.004594 | 5.47 |
| w23 | 5 | -0.013058 | 2.366 |
| w24 | 8 | 0.048176 | -5.124 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 1 | -0.058874 | -6.321 |
| w28 | 5 | -0.18217 | -17.622 |
| w29 | 0 | None | 0.0 |
| w30 | 13 | -0.072793 | -7.212 |
| w31 | 15 | -0.012181 | 3.17 |
| w32 | 12 | 0.004498 | 3.251 |

- ZECUSD: 23 of 32 windows run. 9 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w10 | 9 | -0.008225 | 1.745 |
| w11 | 2 | -0.08138 | -6.963 |
| w12 | 21 | 0.001102 | -7.627 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 7 | -0.054709 | -10.323 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | 0.095069 | 24.335 |
| w18 | 2 | 0.085576 | 4.991 |
| w19 | 16 | 0.064554 | 14.451 |
| w20 | 11 | 0.085696 | 4.64 |
| w21 | 16 | -0.070819 | -12.085 |
| w22 | 18 | 0.056861 | 9.399 |
| w23 | 12 | -0.087504 | -13.82 |
| w24 | 11 | -0.044226 | -0.968 |
| w25 | 0 | None | 0.0 |
| w26 | 11 | 0.100411 | 15.055 |
| w27 | 3 | 0.109118 | 16.628 |
| w28 | 0 | None | 0.0 |
| w29 | 4 | -0.038291 | 1.466 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 6 | 0.057735 | 7.99 |

- AAVEUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 17 | 0.198451 | 12.231 |
| w24 | 11 | 0.088388 | 14.498 |
| w25 | 6 | 0.054348 | 15.818 |
| w26 | 10 | 0.1784 | 15.044 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 5 | -0.102016 | -4.049 |
| w31 | 15 | 0.071158 | -8.915 |
| w32 | 9 | 0.044206 | 10.504 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 9 | 0.012229 | 8.936 |
| w23 | 28 | 0.017174 | -10.637 |
| w24 | 14 | -0.114242 | -12.908 |
| w25 | 0 | None | 0.0 |
| w26 | 12 | -0.000731 | -3.57 |
| w27 | 9 | 0.000184 | 3.693 |
| w28 | 11 | 0.084308 | 1.218 |
| w29 | 6 | 0.051131 | 8.057 |
| w30 | 6 | -0.059052 | -3.513 |
| w31 | 9 | -0.091893 | -8.079 |
| w32 | 7 | -0.038224 | -6.549 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 14 | 0.030112 | 0.211 |
| w21 | 9 | -0.02285 | 9.131 |
| w22 | 20 | 0.094024 | 22.204 |
| w23 | 12 | -0.017893 | -8.608 |
| w24 | 10 | -0.056935 | -5.349 |
| w25 | 6 | -0.003686 | 7.31 |
| w26 | 2 | -0.088922 | -0.32 |
| w27 | 8 | -0.026966 | 4.191 |
| w28 | 1 | -0.044736 | -2.385 |
| w29 | 5 | 0.069218 | 9.458 |
| w30 | 11 | -0.068875 | -17.569 |
| w31 | 15 | 0.029449 | -8.049 |
| w32 | 19 | 0.020656 | 16.355 |

- ALGOUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 15 | 0.013277 | 0.815 |
| w21 | 2 | 0.032079 | 0.165 |
| w22 | 13 | 0.101461 | -0.139 |
| w23 | 12 | 0.038497 | -10.053 |
| w24 | 9 | -0.050136 | -1.117 |
| w25 | 7 | 0.019589 | 8.825 |
| w26 | 14 | -0.029688 | 1.419 |
| w27 | 7 | -0.008104 | -3.603 |
| w28 | 0 | None | 0.0 |
| w29 | 9 | 0.262939 | 61.335 |
| w30 | 20 | -0.056934 | -30.235 |
| w31 | 15 | 0.077974 | 23.699 |
| w32 | 17 | 0.068961 | -4.51 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 3 | -0.097895 | -6.847 |
| w12 | 27 | -0.006031 | -5.884 |
| w13 | 7 | 0.108976 | 20.569 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 7 | 0.058597 | 15.432 |
| w18 | 9 | 0.087465 | 5.101 |
| w19 | 8 | -0.059098 | -18.478 |
| w20 | 14 | 0.000402 | 4.085 |
| w21 | 4 | -0.010551 | -4.323 |
| w22 | 9 | 0.105285 | 2.639 |
| w23 | 4 | -0.043107 | 13.611 |
| w24 | 5 | 0.037956 | -0.011 |
| w25 | 0 | None | 0.0 |
| w26 | 3 | -0.096267 | -1.057 |
| w27 | 2 | 0.094179 | 1.806 |
| w28 | 1 | 0.168803 | 6.716 |
| w29 | 1 | -0.020527 | -0.909 |
| w30 | 0 | None | 0.0 |
| w31 | 11 | -0.086626 | -3.545 |
| w32 | 5 | 0.026741 | 4.757 |

