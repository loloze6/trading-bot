# Backtest of 027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h

- Plan: `../../../../03_test_plan/night4_panic_run/plans/027-03_panic-rebound-in-downtrend.b2_panic-premium-over-three-days.b1_panic-dip-in-uptrend_4h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 4h bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 4 | -0.079696 | -12.898 |
| w4 | 2 | -0.000992 | 3.068 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 7 | 0.000157 | 7.646 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.011398 | 3.774 |
| w11 | 5 | 0.010804 | 30.91 |
| w12 | 4 | 0.034486 | -3.696 |
| w13 | 0 | None | 0.0 |
| w14 | 4 | 0.008485 | -1.582 |
| w15 | 14 | 0.037615 | 17.977 |
| w16 | 1 | None | -0.018 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.150629 | 17.928 |
| w20 | 1 | 0.14862 | 12.865 |
| w21 | 2 | -0.036917 | 3.077 |
| w22 | 2 | -0.044797 | 0.135 |
| w23 | 0 | None | 0.0 |
| w24 | 4 | -0.030932 | 3.595 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.091665 | -3.5 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 8 | -0.028829 | 1.652 |
| w9 | 2 | 0.01148 | 0.169 |
| w10 | 5 | 0.031033 | 8.011 |
| w11 | 11 | -0.010398 | 16.281 |
| w12 | 2 | 0.002667 | -1.891 |
| w13 | 0 | 0.078359 | 0.0 |
| w14 | 4 | -0.00629 | -4.769 |
| w15 | 8 | -0.004655 | 17.952 |
| w16 | 0 | None | 0.0 |
| w17 | 2 | 0.082867 | 11.501 |
| w18 | 3 | 0.107584 | -2.162 |
| w19 | 2 | 0.215815 | 22.728 |
| w20 | 4 | -0.029636 | 5.712 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.034239 | 3.173 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | -0.049252 | 6.006 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.043262 | 0.014 |
| w7 | 0 | None | 0.0 |
| w8 | 9 | 0.025081 | 4.369 |
| w9 | 0 | None | 0.0 |
| w10 | 5 | -0.003789 | 1.587 |
| w11 | 3 | 0.019742 | -2.391 |
| w12 | 4 | 0.003318 | -1.734 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 5 | -0.026333 | 6.784 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.103635 | 5.492 |
| w20 | 3 | 0.142483 | 7.489 |
| w21 | 2 | -0.010737 | -0.564 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.037988 | 1.417 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 3 | -0.017771 | -9.893 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 4 | -0.028056 | 2.541 |
| w9 | 0 | None | 0.0 |
| w10 | 3 | 0.045207 | 9.305 |
| w11 | 8 | 0.112102 | 15.182 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | 0.131382 | 0.0 |
| w14 | 2 | -0.03103 | -1.538 |
| w15 | 8 | -0.055319 | 13.522 |
| w16 | 5 | 0.035731 | -0.039 |
| w17 | 2 | 0.071831 | 3.822 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | 0.088914 | -0.298 |
| w20 | 2 | 0.029955 | 10.25 |
| w21 | 4 | -0.028636 | 13.298 |
| w22 | 2 | -0.068285 | 0.126 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 7 | 0.0123 | 24.841 |
| w4 | 1 | 0.055307 | 10.279 |
| w5 | 3 | 0.028306 | -1.759 |
| w6 | 2 | 0.038811 | -2.736 |
| w7 | 0 | None | 0.0 |
| w8 | 2 | -0.033806 | 4.657 |
| w9 | 4 | 0.037786 | -1.375 |
| w10 | 3 | 0.078275 | 4.208 |
| w11 | 10 | -0.011325 | 27.888 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | 0.01401 | -11.566 |
| w14 | 6 | 0.001611 | -5.063 |
| w15 | 7 | -0.025472 | -1.162 |
| w16 | 2 | 0.043546 | -7.376 |
| w17 | 5 | -0.022035 | 24.755 |
| w18 | 0 | None | 0.0 |
| w19 | 6 | 0.08842 | 18.443 |
| w20 | 2 | -0.05492 | 0.907 |
| w21 | 14 | 0.084563 | 38.373 |
| w22 | 4 | 0.152988 | 3.262 |
| w23 | 2 | 0.05196 | 5.427 |
| w24 | 0 | None | 0.0 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 4 | 0.06511 | 3.169 |
| w7 | 4 | 0.073209 | 2.154 |
| w8 | 13 | -0.008196 | 1.757 |
| w9 | 0 | None | 0.0 |
| w10 | 4 | 0.032735 | 8.259 |
| w11 | 11 | 0.154448 | 24.384 |
| w12 | 4 | 0.100297 | 2.377 |
| w13 | 3 | 0.048312 | 1.777 |
| w14 | 2 | 0.018503 | 3.807 |
| w15 | 4 | -0.004814 | 0.282 |
| w16 | 10 | -0.004475 | 3.862 |
| w17 | 0 | None | 0.0 |
| w18 | 3 | -0.058087 | -2.12 |
| w19 | 6 | 0.096658 | 22.167 |
| w20 | 2 | -0.031622 | 4.016 |
| w21 | 0 | None | 0.0 |
| w22 | 5 | 0.028542 | 2.056 |
| w23 | 0 | None | 0.0 |
| w24 | 10 | 0.169323 | 69.479 |

