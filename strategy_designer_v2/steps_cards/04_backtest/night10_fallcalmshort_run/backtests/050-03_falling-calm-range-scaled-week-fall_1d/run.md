# Backtest of 050-03_falling-calm-range-scaled-week-fall_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/050-03_falling-calm-range-scaled-week-fall_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 30 | -0.004614 | -0.27 |
| w13 | 4 | -0.199442 | -1.98 |
| w14 | 6 | -0.019828 | -2.542 |
| w15 | 10 | -0.008295 | -3.368 |
| w16 | 0 | None | 0.0 |
| w17 | 12 | -0.0041 | -1.556 |
| w18 | 21 | -0.078231 | -9.858 |
| w19 | 29 | 0.098165 | 19.872 |
| w21 | 0 | 0.024926 | 0.0 |
| w22 | 0 | 0.004044 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 8 | 0.01469 | -3.293 |
| w25 | 18 | -0.098117 | -14.013 |
| w26 | 21 | 0.013205 | 6.3 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.07296 | -0.516 |
| w29 | 4 | 0.001291 | -1.834 |
| w30 | 40 | -0.076916 | 10.877 |
| w31 | 27 | 0.21161 | 47.878 |
| w32 | 32 | -0.005917 | -19.315 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 10 | 0.00338 | -5.409 |
| w23 | 25 | 0.039317 | 9.918 |
| w24 | 28 | 0.106594 | -0.773 |
| w25 | 4 | -0.043299 | -2.005 |
| w26 | 16 | 0.008019 | 4.065 |
| w27 | 16 | 0.006649 | -7.263 |
| w28 | 12 | -0.054621 | -5.235 |
| w29 | 18 | -0.12955 | -17.449 |
| w30 | 17 | -0.015742 | -1.798 |
| w31 | 20 | 0.043849 | 11.698 |
| w32 | 45 | 0.027133 | 9.699 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 6 | 0.069705 | 4.626 |
| w12 | 34 | 0.010584 | 11.637 |
| w13 | 2 | -0.087438 | -1.411 |
| w14 | 3 | -0.263091 | -3.993 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.009036 | -1.153 |
| w18 | 22 | -0.038594 | -8.655 |
| w19 | 13 | -0.080777 | -7.49 |
| w20 | 4 | -0.080848 | -1.841 |
| w21 | 11 | 0.003067 | 0.127 |
| w22 | 7 | -0.235626 | -9.878 |
| w23 | 13 | -0.105765 | -0.615 |
| w24 | 9 | -0.096509 | -7.456 |
| w25 | 0 | None | 0.0 |
| w26 | 7 | -0.149907 | -7.313 |
| w27 | 6 | -0.052658 | -8.37 |
| w28 | 2 | -0.05728 | -2.823 |
| w29 | 11 | 0.075977 | 17.755 |
| w30 | 3 | 0.008415 | -0.152 |
| w31 | 18 | -0.031796 | -1.341 |
| w32 | 4 | -0.070004 | -3.059 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 4 | -0.087283 | -8.26 |
| w26 | 15 | 0.139757 | 13.557 |
| w27 | 4 | -0.016674 | -7.431 |
| w28 | 14 | -0.117454 | -7.534 |
| w29 | 5 | -0.027446 | -1.977 |
| w30 | 17 | 0.051972 | 16.856 |
| w31 | 27 | 0.0626 | 18.112 |
| w32 | 14 | -0.080896 | -16.247 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 5 | 0.033204 | 0.437 |
| w23 | 28 | 0.050089 | 14.821 |
| w24 | 26 | 0.016679 | -13.212 |
| w25 | 0 | None | 0.0 |
| w26 | 21 | 0.038487 | 18.267 |
| w27 | 9 | -0.066356 | -11.71 |
| w28 | 16 | -0.073952 | -5.953 |
| w29 | 15 | -0.139251 | -18.227 |
| w30 | 14 | 0.023164 | 14.08 |
| w31 | 16 | 0.132899 | 28.45 |
| w32 | 31 | -0.125224 | -31.432 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 12 | 0.056373 | 10.766 |
| w21 | 22 | -0.031339 | -10.527 |
| w22 | 17 | -0.131417 | -14.879 |
| w23 | 10 | -0.020309 | -0.924 |
| w24 | 12 | 0.035063 | -2.32 |
| w25 | 6 | -0.010644 | -3.613 |
| w26 | 7 | 0.020112 | 0.058 |
| w27 | 7 | -0.01569 | -5.021 |
| w28 | 3 | 0.098579 | 5.273 |
| w29 | 10 | -0.090009 | -6.491 |
| w30 | 34 | -0.094489 | -1.711 |
| w31 | 31 | -0.007506 | -1.464 |
| w32 | 39 | -0.121207 | -34.705 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.014971 | -1.126 |
| w2 | 2 | 0.030635 | 0.161 |
| w3 | 6 | -0.026887 | -3.928 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 10 | 0.021709 | -1.692 |
| w8 | 26 | -0.040742 | -1.108 |
| w9 | 8 | 0.167525 | 40.216 |
| w10 | 8 | 0.006928 | -0.585 |
| w11 | 0 | None | 0.0 |
| w12 | 25 | -0.270578 | -43.791 |
| w13 | 3 | -0.099265 | -4.898 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.034784 | 5.477 |
| w17 | 0 | None | 0.0 |
| w18 | 13 | -0.060784 | -10.193 |
| w19 | 24 | -0.002042 | 6.108 |
| w20 | 15 | 0.114979 | 20.717 |
| w21 | 21 | 0.143186 | -2.523 |
| w22 | 2 | 0.015406 | -0.487 |
| w23 | 10 | 0.00021 | -0.822 |
| w24 | 9 | -0.036708 | -5.147 |
| w25 | 0 | None | 0.0 |
| w26 | 4 | -0.077852 | 0.748 |
| w27 | 0 | None | 0.0 |
| w28 | 2 | -0.022724 | -4.229 |
| w29 | 0 | None | 0.0 |
| w30 | 2 | 0.071195 | 1.842 |
| w31 | 2 | -0.02031 | -1.712 |
| w32 | 7 | -0.099974 | -2.101 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 26 | -0.179563 | -21.218 |
| w22 | 5 | -0.069304 | -5.856 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 27 | -0.043396 | -2.82 |
| w31 | 0 | None | 0.0 |
| w32 | 0 | None | 0.0 |

