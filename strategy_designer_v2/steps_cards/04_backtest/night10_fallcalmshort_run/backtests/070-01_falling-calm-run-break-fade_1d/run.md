# Backtest of 070-01_falling-calm-run-break-fade_1d

- Plan: `../../../../03_test_plan/night10_fallcalmshort_run/plans/070-01_falling-calm-run-break-fade_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XRP, DOT, XMR, INJ, FIL, DOGE, BTC, TRX as XRPUSD, DOTUSD, XMRUSD, INJUSD, FILUSD, DOGEUSD, BTCUSD, TRXUSD; 1d bars; windows research_2016, data use 2
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XRPUSD: 20 of 32 windows run. 12 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5 (the coin's first 90 days); w6, w7, w8, w9, w10, w11 (the coin's history is shorter than the plan's warm-up: 790 days asked); w20 (a hole of 2 days).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w12 | 6 | 0.04547 | 3.637 |
| w13 | 1 | 0.052938 | 1.414 |
| w14 | 0 | None | 0.0 |
| w15 | 3 | -0.009405 | -2.14 |
| w16 | 0 | None | 0.0 |
| w17 | 5 | 0.065837 | 2.643 |
| w18 | 5 | -0.034579 | -1.328 |
| w19 | 6 | 0.058034 | 5.249 |
| w21 | 0 | 0.012023 | 0.0 |
| w22 | 0 | 0.038604 | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 5 | -0.027312 | -2.478 |
| w25 | 5 | 0.089976 | 7.284 |
| w26 | 5 | 0.094707 | 6.943 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 1 | 0.010489 | 0.029 |
| w30 | 11 | -0.065703 | -4.183 |
| w31 | 7 | 0.017233 | 1.876 |
| w32 | 7 | -0.008209 | -2.28 |

- DOTUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15 (the coin's first 90 days); w16, w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 1 | 0.026313 | 0.361 |
| w23 | 7 | -0.027719 | -2.86 |
| w24 | 9 | -0.019927 | -14.23 |
| w25 | 1 | -0.030942 | -0.743 |
| w26 | 4 | 0.047963 | 1.979 |
| w27 | 4 | -0.047591 | -6.319 |
| w28 | 1 | 0.09397 | 4.169 |
| w29 | 6 | -0.052973 | -5.527 |
| w30 | 3 | -0.118753 | -7.294 |
| w31 | 4 | 0.056695 | 3.339 |
| w32 | 14 | 0.126489 | 12.241 |

- XMRUSD: 22 of 32 windows run. 10 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4 (the coin's first 90 days); w5, w6, w7, w8, w9, w10 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w11 | 4 | 0.011648 | -0.059 |
| w12 | 14 | -0.050663 | -3.013 |
| w13 | 1 | 0.017783 | 0.265 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 1 | -0.007367 | -0.213 |
| w18 | 4 | -0.033248 | -1.943 |
| w19 | 3 | 0.060113 | 3.143 |
| w20 | 2 | 0.080295 | 3.356 |
| w21 | 4 | -0.040195 | -2.468 |
| w22 | 2 | -0.262823 | -10.801 |
| w23 | 2 | -0.093079 | -3.664 |
| w24 | 2 | -0.020094 | -1.66 |
| w25 | 0 | None | 0.0 |
| w26 | 2 | 0.057396 | 1.115 |
| w27 | 2 | 0.01407 | 0.154 |
| w28 | 0 | None | 0.0 |
| w29 | 1 | -0.000209 | -0.198 |
| w30 | 0 | None | 0.0 |
| w31 | 7 | -0.005044 | -0.761 |
| w32 | 0 | None | 0.0 |

- INJUSD: 8 of 32 windows run. 24 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16, w17, w18 (the coin's first 90 days); w19, w20, w21, w22, w23, w24 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w25 | 1 | -0.059501 | -2.758 |
| w26 | 4 | -0.037245 | -2.898 |
| w27 | 2 | -0.090381 | -3.448 |
| w28 | 3 | -0.10365 | -4.458 |
| w29 | 2 | -0.101387 | -3.493 |
| w30 | 5 | 0.089635 | 7.375 |
| w31 | 13 | -0.09173 | -7.837 |
| w32 | 3 | -0.149037 | -16.973 |

- FILUSD: 11 of 32 windows run. 21 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14, w15, w16 (the coin's first 90 days); w17, w18, w19, w20, w21 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w22 | 2 | 0.035521 | 0.547 |
| w23 | 9 | -0.023579 | -2.012 |
| w24 | 6 | 0.030484 | -3.249 |
| w25 | 0 | None | 0.0 |
| w26 | 8 | -0.018455 | -1.559 |
| w27 | 3 | 0.054928 | 3.253 |
| w28 | 4 | -0.090625 | -5.669 |
| w29 | 5 | -0.056546 | -3.596 |
| w30 | 5 | -0.010747 | -0.962 |
| w31 | 5 | -0.06331 | -4.758 |
| w32 | 6 | -0.057265 | -3.947 |

- DOGEUSD: 13 of 32 windows run. 19 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13 (the coin's first 90 days); w14, w15, w16, w17, w18, w19 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w20 | 4 | -0.250671 | -11.738 |
| w21 | 7 | -0.010661 | -4.405 |
| w22 | 2 | -0.123263 | -7.359 |
| w23 | 4 | 0.131872 | 8.816 |
| w24 | 8 | -0.005969 | -3.081 |
| w25 | 3 | -0.000149 | -1.219 |
| w26 | 2 | 0.035651 | 1.281 |
| w27 | 2 | -0.049071 | -2.922 |
| w28 | 2 | 0.003693 | 0.391 |
| w29 | 3 | -0.017555 | -1.13 |
| w30 | 11 | 0.008304 | 2.874 |
| w31 | 7 | -0.021781 | -1.192 |
| w32 | 12 | -0.102871 | -9.369 |

- BTCUSD: 32 of 32 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | -0.194109 | -2.609 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 5 | 0.121941 | 6.092 |
| w8 | 7 | 0.074217 | 4.939 |
| w9 | 5 | 0.162454 | 22.286 |
| w10 | 1 | 0.034372 | 0.721 |
| w11 | 0 | None | 0.0 |
| w12 | 8 | 0.000997 | 0.771 |
| w13 | 1 | 0.059636 | 1.714 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.021691 | -1.431 |
| w19 | 4 | -0.086762 | -6.53 |
| w20 | 4 | 0.060904 | 4.425 |
| w21 | 10 | -0.041969 | -2.439 |
| w22 | 1 | 0.006236 | -0.155 |
| w23 | 3 | 0.017132 | 0.636 |
| w24 | 3 | 0.023101 | -0.737 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 1 | 0.014226 | 0.278 |
| w31 | 1 | -0.014952 | -0.853 |
| w32 | 4 | -0.08231 | -3.603 |

- TRXUSD: 12 of 32 windows run. 20 left out by the data use (common/data_use.md, section 3): w1, w2, w3, w4, w5, w6, w7, w8, w9, w10, w11, w12, w13, w14 (the coin's first 90 days); w15, w16, w17, w18, w19, w20 (the coin's history is shorter than the plan's warm-up: 790 days asked).

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w21 | 8 | 0.0161 | -0.447 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |
| w25 | 0 | None | 0.0 |
| w26 | 0 | None | 0.0 |
| w27 | 0 | None | 0.0 |
| w28 | 0 | None | 0.0 |
| w29 | 0 | None | 0.0 |
| w30 | 10 | 0.00403 | -0.697 |
| w31 | 0 | None | 0.0 |
| w32 | 1 | -0.017096 | -0.419 |

