# Backtest of 086-01_first-up-after-long-down-run_1d

- Plan: `../../../../03_test_plan/night10_riseagilong_run/plans/086-01_first-up-after-long-down-run_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: LTC, ETH, XMR, INJ, GRT, DOGE, XRP, TRX as LTCUSD, ETHUSD, XMRUSD, INJUSD, GRTUSD, DOGEUSD, XRPUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- LTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | 0.071124 | 0.0 |
| w3 | 2 | 0.143678 | 0.379 |
| w4 | 5 | -0.017041 | 13.066 |
| w5 | 16 | 0.037082 | -3.809 |
| w6 | 10 | 0.048631 | 47.49 |
| w7 | 10 | -0.039481 | -11.979 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 10 | -0.058617 | 15.832 |
| w11 | 6 | 0.1721 | 19.284 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.025837 | -8.005 |
| w14 | 3 | -0.105338 | 1.056 |
| w15 | 12 | -0.004505 | 59.871 |
| w16 | 18 | 0.056827 | 5.555 |
| w17 | 3 | -0.299064 | -28.644 |
| w18 | 7 | 0.024175 | -13.704 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.11497 | 3.705 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | -0.003222 | -2.399 |
| w24 | 0 | None | 0.0 |
| w25 | 7 | -0.036377 | 9.537 |
| w26 | 0 | None | 0.0 |
| w27 | 15 | 0.029667 | 49.274 |
| w28 | 12 | 0.164451 | -4.377 |
| w29 | 5 | -0.052382 | -12.92 |
| w30 | 2 | 0.029313 | 1.788 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- ETHUSD: 26 of 32 windows run. 6 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w7 | 10 | -0.14057 | -3.241 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 8 | -0.066247 | -20.665 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.03208 | -22.896 |
| w14 | 6 | -0.024466 | -4.671 |
| w15 | 7 | -0.154641 | 24.641 |
| w16 | 20 | 0.192835 | 85.337 |
| w17 | 9 | -0.181609 | -38.059 |
| w18 | 3 | 0.047056 | 3.234 |
| w19 | 0 | None | 0.0 |
| w20 | 4 | -0.013249 | -2.545 |
| w21 | 3 | -0.160457 | -7.555 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | -0.040511 | 0.973 |
| w25 | 13 | -0.076805 | -13.407 |
| w26 | 6 | 0.02323 | -1.614 |
| w27 | 11 | -0.061583 | -3.666 |
| w28 | 0 | None | 0.0 |
| w29 | 7 | -0.025909 | -2.514 |
| w30 | 2 | 0.005296 | -9.083 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | -0.075925 | -23.576 |
| w12 | 0 | None | 0.0 |
| w13 | 4 | -0.062253 | -16.297 |
| w14 | 0 | None | 0.0 |
| w15 | 11 | -0.140661 | 9.627 |
| w16 | 17 | -0.018203 | 30.25 |
| w17 | 2 | -0.039738 | -1.987 |
| w18 | 5 | -0.064521 | -8.688 |
| w19 | 4 | -0.015569 | 2.287 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | 0.016386 | 2.17 |
| w25 | 0 | None | 0.0 |
| w26 | 9 | -0.191458 | 1.13 |
| w27 | 4 | -0.107554 | -1.682 |
| w28 | 10 | 0.069933 | 9.82 |
| w29 | 7 | 0.108294 | -7.525 |
| w30 | 18 | 0.111801 | 32.643 |
| w31 | 6 | -0.185937 | -20.125 |
| w32 | 2 | 0.057193 | -13.777 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 10 | -0.054734 | -3.389 |
| w26 | 0 | None | 0.0 |
| w27 | 8 | 0.076377 | 6.461 |
| w28 | 2 | 0.098771 | 12.407 |
| w29 | 6 | 0.071916 | -0.462 |
| w30 | 2 | 0.042553 | 0.057 |
| w31 | 0 | None | 0.0 |
| w32 | 11 | 0.153349 | 11.382 |

- GRTUSD: 10 of 32 windows run. 22 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21, w22 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w23 | 0 | None | 0.0 |
| w24 | 11 | 0.055598 | 15.229 |
| w25 | 17 | -0.114079 | -10.853 |
| w26 | 1 | -0.130783 | -5.957 |
| w27 | 9 | 0.021759 | 11.27 |
| w28 | 4 | 0.158951 | 7.474 |
| w29 | 4 | -0.02118 | 0.586 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 0 | None | 0.0 |
| w21 | 7 | -0.043075 | -5.901 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.106915 | 0.407 |
| w25 | 13 | -0.101087 | -17.213 |
| w26 | 0 | None | 0.0 |
| w27 | 10 | -0.120196 | 21.055 |
| w28 | 0 | None | 0.0 |
| w29 | 13 | -0.01047 | -14.423 |
| w30 | 2 | 0.061419 | 2.964 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 1 | -0.008619 | 0.749 |
| w13 | 4 | -0.100686 | -14.846 |
| w14 | 4 | -0.037026 | 1.262 |
| w15 | 9 | -0.050775 | -10.311 |
| w16 | 8 | -0.130486 | 7.79 |
| w17 | 7 | -0.041391 | -6.884 |
| w18 | 2 | 0.083744 | 0.743 |
| w19 | 0 | None | 0.0 |
| w21 | 0 | 0.041183 | 0.0 |
| w22 | 0 | -0.039006 | 0.0 |
| w23 | 7 | -0.117659 | -6.51 |
| w24 | 6 | 0.031664 | -4.022 |
| w25 | 5 | -0.07863 | -17.059 |
| w26 | 3 | -0.025399 | 2.793 |
| w27 | 9 | 0.011588 | 45.448 |
| w28 | 5 | -0.119627 | -4.776 |
| w29 | 4 | 0.07118 | 5.899 |
| w30 | 0 | None | 0.0 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.145765 | -4.956 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.054228 | -23.425 |
| w23 | 4 | -0.307865 | -23.176 |
| w24 | 10 | 0.032449 | -2.672 |
| w25 | 0 | None | 0.0 |
| w26 | 5 | 0.046761 | 11.722 |
| w27 | 15 | 0.035125 | 11.043 |
| w28 | 8 | -0.107244 | -1.481 |
| w29 | 2 | -0.120371 | -6.478 |
| w30 | 2 | 0.010474 | 11.367 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

