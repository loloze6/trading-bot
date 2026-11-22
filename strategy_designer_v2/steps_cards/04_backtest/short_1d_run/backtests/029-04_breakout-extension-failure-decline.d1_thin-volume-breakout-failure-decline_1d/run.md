# Backtest of 029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d

- Plan: `../../../../03_test_plan/short_1d_run/plans/029-04_breakout-extension-failure-decline.d1_thin-volume-breakout-failure-decline_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.064838 | -1.719 |
| w12 | 2 | -0.06323 | -10.237 |
| w13 | 2 | -0.028032 | -1.077 |
| w14 | 1 | 0.088321 | 6.864 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.215771 | -6.662 |
| w17 | 4 | -0.036484 | 2.913 |
| w18 | 2 | 0.053586 | -6.604 |
| w19 | 1 | 0.085721 | 19.945 |
| w20 | 4 | -0.083175 | -6.52 |
| w21 | 4 | 0.210532 | 11.144 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.025551 | 0.844 |
| w24 | 3 | -0.030926 | 5.367 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.042339 | 11.764 |
| w3 | 1 | 0.061645 | 11.329 |
| w4 | 2 | 0.036864 | -1.469 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.035888 | 9.763 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 5 | 0.148768 | 4.887 |
| w12 | 4 | -0.081021 | -8.245 |
| w13 | 3 | 0.097336 | -1.962 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | 0.035751 | 0.707 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | -0.163997 | -11.835 |
| w22 | 0 | None | 0.0 |
| w23 | 1 | 0.064451 | 13.239 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.038221 | -12.093 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.049744 | 10.05 |
| w4 | 0 | None | 0.0 |
| w5 | 1 | 0.062767 | 6.885 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.102892 | -1.468 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.0111 | 12.35 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.044852 | -2.701 |
| w17 | 0 | None | 0.0 |
| w18 | 5 | -0.050016 | 9.156 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.051599 | 6.138 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.002679 | -3.148 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.045525 | 2.985 |
| w4 | 2 | -0.056289 | -4.721 |
| w5 | 0 | None | 0.0 |
| w6 | 6 | -0.05456 | -1.246 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | 0.154269 | 12.202 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.030676 | -2.343 |
| w20 | 2 | -0.028961 | -2.738 |
| w21 | 5 | -0.131897 | -20.603 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.265133 | 25.574 |
| w24 | 1 | 0.092611 | -3.198 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
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
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.043823 | 7.767 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.038131 | 0.442 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | -0.082199 | -18.184 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 2 | -0.032531 | -10.183 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 3 | 0.098182 | 0.362 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | -0.034274 | -9.303 |
| w19 | 2 | -0.172678 | -9.517 |
| w20 | 4 | 0.042498 | -9.389 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.04172 | 5.607 |
| w23 | 3 | 0.059828 | 4.46 |
| w24 | 3 | 0.031324 | 2.663 |

