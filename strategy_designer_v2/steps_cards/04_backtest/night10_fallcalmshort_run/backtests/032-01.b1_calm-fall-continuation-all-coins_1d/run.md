# Backtest of 032-01.b1_calm-fall-continuation-all-coins_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/032-01.b1_calm-fall-continuation-all-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 23 | 0.041943 | 14.18 |
| w13 | 1 | -0.122307 | -7.578 |
| w14 | 5 | -0.120335 | -20.439 |
| w15 | 2 | -0.04049 | -0.435 |
| w16 | 0 | None | 0.0 |
| w17 | 6 | 0.033923 | 2.196 |
| w18 | 7 | -0.031096 | -2.556 |
| w19 | 24 | 0.028452 | 10.285 |
| w21 | 0 | 0.013938 | 0.0 |
| w22 | 0 | -0.008989 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | -0.090336 | -0.207 |
| w25 | 13 | -0.07876 | -14.041 |
| w26 | 12 | 0.130213 | 17.992 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.069772 | -2.076 |
| w29 | 0 | -0.020124 | 0.0 |
| w30 | 30 | -0.069239 | 2.261 |
| w31 | 12 | 0.252073 | 30.848 |
| w32 | 27 | -0.017534 | -14.291 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | -0.076279 | -9.112 |
| w23 | 28 | -0.118866 | -10.049 |
| w24 | 21 | 0.107448 | -9.8 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.070138 | -7.169 |
| w27 | 13 | -0.016391 | -6.241 |
| w28 | 15 | -0.12361 | -7.5 |
| w29 | 11 | -0.11423 | -12.953 |
| w30 | 7 | -0.022246 | 0.101 |
| w31 | 10 | 0.043822 | 8.416 |
| w32 | 27 | 0.03071 | 19.505 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | 0.035732 | 1.313 |
| w12 | 38 | -0.07809 | -0.07 |
| w13 | 2 | -0.127735 | -10.357 |
| w14 | 0 | -0.308113 | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.045516 | -0.445 |
| w18 | 17 | -0.011598 | 0.883 |
| w19 | 7 | -0.15163 | -2.812 |
| w20 | 0 | None | 0.0 |
| w21 | 14 | -0.085177 | -9.157 |
| w22 | 8 | -0.270639 | -10.033 |
| w23 | 8 | -0.105396 | -15.02 |
| w24 | 2 | -0.01857 | -2.248 |
| w25 | 0 | None | 0.0 |
| w26 | 6 | -0.070971 | -5.341 |
| w27 | 4 | -0.128104 | -6.864 |
| w28 | 2 | -0.123728 | -5.111 |
| w29 | 5 | 0.07215 | 11.523 |
| w30 | 0 | None | 0.0 |
| w31 | 3 | -0.031869 | -0.701 |
| w32 | 4 | -0.008883 | -0.802 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 0 | -0.084944 | 0.0 |
| w26 | 9 | -0.001498 | -1.652 |
| w27 | 3 | -0.098556 | -4.587 |
| w28 | 10 | -0.106303 | -4.112 |
| w29 | 2 | -0.169279 | -4.764 |
| w30 | 17 | 0.129703 | 21.592 |
| w31 | 28 | -0.109025 | -10.405 |
| w32 | 7 | -0.051616 | -9.827 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 8 | -0.057888 | -11.49 |
| w23 | 29 | -0.13662 | -7.535 |
| w24 | 14 | 0.037416 | -11.094 |
| w25 | 0 | None | 0.0 |
| w26 | 14 | 0.022787 | 8.241 |
| w27 | 12 | -0.05346 | -7.356 |
| w28 | 13 | -0.097809 | -7.509 |
| w29 | 13 | -0.067615 | -7.244 |
| w30 | 16 | 0.021886 | 8.614 |
| w31 | 8 | 0.095908 | 11.585 |
| w32 | 21 | -0.14637 | -16.636 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 10 | -0.002908 | -0.712 |
| w21 | 18 | -0.056523 | -13.397 |
| w22 | 14 | -0.184034 | -21.601 |
| w23 | 18 | -0.07926 | -8.736 |
| w24 | 12 | -0.00655 | -3.15 |
| w25 | 3 | 0.028003 | 0.068 |
| w26 | 8 | 0.086836 | 13.509 |
| w27 | 6 | -0.066937 | -4.911 |
| w28 | 2 | 0.118025 | 16.051 |
| w29 | 7 | -0.119507 | -9.814 |
| w30 | 20 | -0.010258 | 4.956 |
| w31 | 23 | -0.051473 | -3.453 |
| w32 | 16 | -0.069212 | -2.227 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 2 | 0.030635 | 0.39 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 10 | -0.020705 | -1.831 |
| w8 | 16 | -0.015662 | 3.239 |
| w9 | 10 | 0.138701 | 40.658 |
| w10 | 2 | 0.045313 | 0.6 |
| w11 | 0 | None | 0.0 |
| w12 | 21 | -0.118423 | -15.076 |
| w13 | 2 | -0.097335 | -2.79 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.034784 | 0.122 |
| w17 | 0 | None | 0.0 |
| w18 | 8 | -0.011603 | -0.982 |
| w19 | 19 | -0.000116 | 2.296 |
| w20 | 2 | 0.19165 | 14.994 |
| w21 | 9 | 0.044141 | 4.786 |
| w22 | 2 | -0.001441 | -0.301 |
| w23 | 11 | -0.086531 | -10.034 |
| w24 | 1 | 0.100244 | 3.579 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | -0.083692 | -7.744 |
| w27 | 0 | None | 0.0 |
| w28 | 1 | -0.022724 | -1.4 |
| w29 | 0 | None | 0.0 |
| w30 | 3 | 0.204714 | 15.517 |
| w31 | 2 | -0.049863 | -0.859 |
| w32 | 2 | -0.135032 | -1.346 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 24 | -0.130467 | -18.823 |
| w22 | 1 | -0.113012 | -1.451 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 28 | 0.108615 | 23.494 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | -0.046079 | 0.0 |

