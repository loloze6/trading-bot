# Backtest of 032-01.b1.b1.e1_large-weekly-fall-continues_1d

- Plan: `../../../../03_test_plan/night7c_chopreversal_run/plans/032-01.b1.b1.e1_large-weekly-fall-continues_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 5 | -0.107983 | -9.663 |
| w2 | 8 | -0.013036 | 10.827 |
| w3 | 2 | -0.339915 | -5.836 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | 0.009676 | 2.516 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | -0.222148 | -7.876 |
| w8 | 0 | None | 0.0 |
| w9 | 7 | -0.029286 | -6.823 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | 0.082767 | -2.484 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.195881 | -7.668 |
| w14 | 7 | 0.160658 | 38.812 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.264057 | -9.752 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | 0.287022 | 5.416 |
| w19 | 0 | None | 0.0 |
| w20 | 6 | -0.01618 | -14.161 |
| w21 | 0 | None | 0.0 |
| w22 | 4 | -0.165642 | -12.298 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | 0.00736 | 0.662 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 6 | -0.040458 | -7.816 |
| w2 | 8 | -0.011319 | 10.441 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | -0.011797 | 0.181 |
| w6 | 0 | None | 0.0 |
| w7 | 6 | -0.054889 | -3.862 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | -0.157086 | -11.07 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 5 | -0.03502 | 0.728 |
| w14 | 9 | 0.136964 | 33.289 |
| w15 | 2 | -0.121535 | -3.285 |
| w16 | 2 | -0.310162 | -5.361 |
| w17 | 2 | -0.078449 | -2.121 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.299119 | -5.711 |
| w20 | 6 | -0.08405 | -8.187 |
| w21 | 0 | None | 0.0 |
| w22 | 6 | -0.349842 | -9.913 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.122795 | -10.189 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | -0.01048 | -1.666 |
| w2 | 4 | -0.10176 | -10.563 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.013796 | -2.414 |
| w5 | 3 | -0.021642 | -0.051 |
| w6 | 0 | None | 0.0 |
| w7 | 6 | -0.06104 | 0.773 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | -0.092753 | -7.912 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 3 | -0.030922 | -1.152 |
| w14 | 4 | 0.024262 | 21.339 |
| w15 | 2 | -0.039939 | -2.622 |
| w16 | 4 | -0.314345 | -4.397 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 5 | -0.240339 | -18.442 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 2 | -0.056841 | -15.017 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.023258 | -12.199 |
| w2 | 3 | 0.010964 | -5.469 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 4 | -0.230519 | 2.107 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | -0.136744 | -3.067 |
| w8 | 0 | None | 0.0 |
| w9 | 5 | -0.066688 | -7.709 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 3 | 0.026057 | 38.595 |
| w15 | 0 | None | 0.0 |
| w16 | 2 | -0.216863 | -6.781 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 2 | -0.130744 | 1.972 |
| w20 | 0 | None | 0.0 |
| w21 | 9 | 0.013557 | -14.943 |
| w22 | 0 | None | 0.0 |
| w23 | 3 | -0.220685 | -16.351 |
| w24 | 0 | None | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 4 | -0.123282 | -9.569 |
| w2 | 0 | -0.201049 | 0.0 |
| w3 | 2 | -0.346715 | -6.353 |
| w4 | 0 | None | 0.0 |
| w5 | 3 | -0.028404 | -1.272 |
| w6 | 0 | None | 0.0 |
| w7 | 3 | 0.041148 | -8.503 |
| w8 | 0 | None | 0.0 |
| w9 | 6 | -0.095852 | -8.939 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 2 | 0.06579 | 0.293 |
| w15 | 2 | -0.099365 | -2.233 |
| w16 | 2 | -0.274054 | -6.046 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 2 | 0.034997 | 0.274 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 3 | -0.12977 | 1.921 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 3 | 0.059885 | 5.101 |
| w2 | 2 | -0.108404 | -4.3 |
| w3 | 2 | -0.295707 | -10.244 |
| w4 | 2 | 0.142428 | 0.279 |
| w5 | 5 | -0.082941 | -5.348 |
| w6 | 2 | -0.048649 | -1.765 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 6 | -0.118638 | -3.665 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 5 | 0.073892 | 3.214 |
| w15 | 2 | -0.169025 | -1.994 |
| w16 | 2 | 0.004308 | -5.381 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 3 | -0.012842 | -0.568 |
| w20 | 1 | None | -0.037 |
| w21 | 2 | 0.00249 | 1.54 |
| w22 | 4 | -0.057085 | -7.029 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

