# Backtest of 029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d

- Plan: `../../../../03_test_plan/short_1d_run/plans/029-03_close-below-breakout-bar-low.d1_failed-breakout-after-small-run-up_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.07908 | 3.94 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 3 | 0.017585 | -3.65 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | -0.012877 | -3.215 |
| w11 | 0 | None | 0.0 |
| w12 | 4 | 0.011844 | 5.651 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.005631 | 27.605 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | -0.121328 | -17.775 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 3 | 0.122934 | 5.717 |
| w22 | 0 | None | 0.0 |
| w23 | 5 | -0.033859 | 8.627 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 1 | 0.014216 | 12.62 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | 0.039 | -2.109 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | 0.033355 | 2.71 |
| w7 | 1 | 0.002392 | 6.673 |
| w8 | 1 | 0.032204 | 2.619 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.108069 | -6.194 |
| w14 | 0 | None | 0.0 |
| w15 | 2 | -0.10247 | -0.328 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 2 | 0.027158 | 2.736 |
| w24 | 2 | -0.054394 | 6.665 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 3 | -0.037487 | 21.255 |
| w6 | 0 | None | 0.0 |
| w7 | 1 | 0.059218 | 10.032 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | -0.079634 | -1.128 |
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
| w23 | 2 | -0.018127 | -5.327 |
| w24 | 2 | -0.136571 | 0.786 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 1 | 0.078595 | 6.236 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | 0.018341 | 9.458 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | 0.026113 | -0.342 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 3 | -0.059275 | -6.98 |
| w12 | 2 | -0.109209 | -6.483 |
| w13 | 1 | 0.07639 | 5.415 |
| w14 | 1 | 0.070943 | 6.411 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 4 | -0.176414 | -21.395 |
| w22 | 2 | 0.114247 | -1.609 |
| w23 | 2 | -0.018522 | 2.746 |
| w24 | 2 | -0.032921 | -0.914 |

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
| w12 | 4 | -0.006559 | 11.455 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | -0.092256 | -9.319 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

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
| w11 | 1 | 0.050267 | 10.545 |
| w12 | 4 | 0.011998 | 5.733 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 1 | 0.026106 | 2.568 |
| w17 | 2 | 0.01341 | -5.276 |
| w18 | 2 | -0.060296 | 3.084 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | -0.072256 | 9.958 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

