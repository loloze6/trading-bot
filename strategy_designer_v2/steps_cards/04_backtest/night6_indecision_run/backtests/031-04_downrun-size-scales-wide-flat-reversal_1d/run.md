# Backtest of 031-04_downrun-size-scales-wide-flat-reversal_1d

- Plan: `../../../../03_test_plan/night6_indecision_run/plans/031-04_downrun-size-scales-wide-flat-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | 0.02591 | 4.823 |
| w2 | 1 | 0.034257 | 6.249 |
| w3 | 3 | -0.06805 | -1.287 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 4 | 0.060592 | 2.645 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | 0.006238 | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 0 | None | 0.0 |
| w12 | 0 | None | 0.0 |
| w13 | 1 | -0.073653 | -1.876 |
| w14 | 3 | -0.012843 | -40.702 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 4 | -0.081704 | -26.057 |
| w19 | 2 | 0.044147 | 0.167 |
| w20 | 2 | 0.091873 | 3.209 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | 0.071918 | 13.61 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

- ETHUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.160539 | 4.673 |
| w2 | 0 | None | 0.0 |
| w3 | 2 | 0.020018 | -1.113 |
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
| w14 | 1 | -0.043021 | -26.75 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 1 | -0.121666 | -16.763 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 1 | -0.102067 | -7.325 |
| w23 | 2 | 0.009714 | 0.391 |
| w24 | 0 | None | 0.0 |

- LTCUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 2 | 0.113973 | 3.951 |
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
| w12 | 0 | 0.036268 | 0.0 |
| w13 | 2 | 0.037257 | -2.916 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 0 | None | 0.0 |
| w21 | 0 | None | 0.0 |
| w22 | 3 | -0.088418 | 7.004 |
| w23 | 2 | 0.14942 | 3.144 |
| w24 | 0 | None | 0.0 |

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 1 | -0.090207 | -5.544 |
| w2 | 2 | 0.078999 | 18.886 |
| w3 | 0 | None | 0.0 |
| w4 | 2 | -0.173873 | 2.605 |
| w5 | 0 | None | 0.0 |
| w6 | 0 | None | 0.0 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 2 | 0.046884 | 1.93 |
| w10 | 0 | None | 0.0 |
| w11 | 1 | -0.13189 | -0.352 |
| w12 | 0 | None | 0.0 |
| w13 | 2 | -0.016578 | -4.114 |
| w14 | 0 | None | 0.0 |
| w15 | 0 | None | 0.0 |
| w16 | 0 | 0.016794 | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 2 | 0.100691 | 1.996 |
| w19 | 0 | None | 0.0 |
| w20 | 2 | 0.062264 | 0.204 |
| w21 | 0 | None | 0.0 |
| w22 | 0 | None | 0.0 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | 0.14188 | 0.0 |

- XRPUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | -0.033626 | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 1 | -0.240153 | -3.569 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 3 | -0.011138 | 5.363 |
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
| w22 | 4 | -0.082039 | -0.633 |
| w23 | 0 | None | 0.0 |
| w24 | 1 | 0.175322 | -2.886 |

- ZECUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 0 | None | 0.0 |
| w2 | 0 | None | 0.0 |
| w3 | 0 | None | 0.0 |
| w4 | 0 | None | 0.0 |
| w5 | 0 | None | 0.0 |
| w6 | 2 | -0.132509 | -13.14 |
| w7 | 0 | None | 0.0 |
| w8 | 0 | None | 0.0 |
| w9 | 0 | None | 0.0 |
| w10 | 0 | None | 0.0 |
| w11 | 2 | -0.147189 | 3.548 |
| w12 | 0 | None | 0.0 |
| w13 | 0 | None | 0.0 |
| w14 | 0 | None | 0.0 |
| w15 | 1 | -0.109154 | -2.368 |
| w16 | 0 | None | 0.0 |
| w17 | 0 | None | 0.0 |
| w18 | 0 | None | 0.0 |
| w19 | 0 | None | 0.0 |
| w20 | 1 | 0.191849 | 32.553 |
| w21 | 0 | None | 0.0 |
| w22 | 2 | 0.182682 | 2.852 |
| w23 | 0 | None | 0.0 |
| w24 | 0 | None | 0.0 |

