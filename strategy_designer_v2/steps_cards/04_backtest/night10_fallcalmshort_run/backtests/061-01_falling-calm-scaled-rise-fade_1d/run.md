# Backtest of 061-01_falling-calm-scaled-rise-fade_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/061-01_falling-calm-scaled-rise-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 2 | -0.175311 | -11.074 |
| w13 | 0 | None | 0.0 |
| w14 | 1 | 0.064773 | 2.769 |
| w15 | 1 | -0.010225 | -0.983 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.025573 | -1.497 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | -0.039679 | -1.005 |
| w21 | 0 | -0.007181 | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.053473 | 1.61 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.111447 | 7.369 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.023319 | 0.511 |
| w31 | 2 | 0.011425 | 0.34 |
| w32 | 1 | -0.03191 | -1.16 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.049298 | 1.51 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | 0.09397 | 2.664 |
| w29 | 2 | -0.008958 | -0.77 |
| w30 | 0 | None | 0.0 |
| w31 | 1 | 0.042047 | 1.661 |
| w32 | 2 | -0.121397 | -6.027 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 0 | None | 0.0 |
| w12 | 1 | 0.077902 | 2.941 |
| w13 | 1 | 0.016986 | 0.543 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.054704 | 1.408 |
| w19 | 2 | -0.087856 | -3.91 |
| w20 | 1 | 0.009394 | 0.263 |
| w21 | 1 | 0.114512 | 2.784 |
| w22 | 1 | -0.041797 | -0.943 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 1 | -0.084127 | -4.122 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.030073 | 1.318 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | 0.021651 | 0.764 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 2 | -0.07988 | -2.512 |
| w32 | 1 | 0.06469 | 2.088 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.018011 | -0.885 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | 0.090639 | 2.67 |
| w29 | 1 | -0.039195 | -1.231 |
| w30 | 1 | -0.050722 | -1.506 |
| w31 | 0 | None | 0.0 |
| w32 | 2 | -0.145297 | -8.579 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 1 | 0.193235 | 5.423 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.093997 | 1.973 |
| w23 | 1 | 0.127405 | 5.707 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 2 | -0.046827 | -2.748 |
| w30 | 1 | -0.00344 | 0.088 |
| w31 | 2 | -0.198905 | -8.555 |
| w32 | 1 | -0.250635 | -13.037 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.052798 | -2.577 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 1 | -0.024417 | -0.586 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 1 | 0.007112 | 0.431 |
| w20 | 2 | -0.155421 | -5.638 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | 0.020152 | 0.434 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 1 | 0.12055 | 3.613 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.071845 | 2.234 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

