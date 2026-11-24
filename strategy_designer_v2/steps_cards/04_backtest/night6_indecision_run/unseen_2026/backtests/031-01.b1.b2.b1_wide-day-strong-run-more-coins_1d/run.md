# Backtest of 031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d

- Plan: `../../../../../03_test_plan/night6_indecision_run/plans/031-01.b1.b2.b1_wide-day-strong-run-more-coins_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC, ADA, DOGE, LINK, TRX, UNI, AAVE, AVAX, SOL, INJ, NEAR, SUI, TAO, ONDO as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD, ADAUSD, DOGEUSD, LINKUSD, TRXUSD, UNIUSD, AAVEUSD, AVAXUSD, SOLUSD, INJUSD, NEARUSD, SUIUSD, TAOUSD, ONDOUSD; 1d bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.027272 | -7.676 |
| w2 | 33 | 0.154605 | 35.19 |
| w3 | 16 | -0.173229 | -12.527 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.081633 | -25.635 |
| w2 | 32 | 0.136435 | 42.694 |
| w3 | 14 | -0.123497 | -12.912 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 47 | -0.111344 | -26.299 |
| w2 | 26 | 0.119652 | 22.21 |
| w3 | 15 | 0.143909 | 21.743 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 36 | 0.089895 | 20.877 |
| w2 | 53 | -0.06784 | 2.475 |
| w3 | 27 | -0.012529 | -1.244 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | 0.012048 | -5.437 |
| w2 | 28 | 0.094429 | 26.96 |
| w3 | 16 | -0.156523 | -15.836 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 30 | -0.047274 | -10.602 |
| w2 | 43 | 0.119903 | 78.144 |
| w3 | 22 | -0.031527 | -1.385 |

- ADAUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 35 | -0.152 | -28.055 |
| w2 | 22 | 0.219181 | 45.124 |
| w3 | 13 | 0.064766 | 4.772 |

- DOGEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 43 | -0.075897 | -14.937 |
| w2 | 35 | 0.06818 | 4.793 |
| w3 | 13 | -0.016654 | -2.791 |

- LINKUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 39 | -0.156306 | -30.646 |
| w2 | 32 | 0.180674 | 78.87 |
| w3 | 20 | 0.013512 | -7.8 |

- TRXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 50 | -0.106651 | 6.679 |
| w2 | 56 | 0.066202 | 9.508 |
| w3 | 27 | -0.323817 | -16.97 |

- UNIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 26 | -0.18221 | -30.928 |
| w2 | 33 | 0.133592 | 67.205 |
| w3 | 18 | 0.199352 | 26.572 |

- AAVEUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 29 | -0.065826 | -11.887 |
| w2 | 34 | 0.101609 | 37.344 |
| w3 | 21 | 0.067356 | 5.808 |

- AVAXUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 34 | -0.128424 | -28.489 |
| w2 | 37 | -0.044381 | -3.707 |
| w3 | 12 | 0.13074 | 24.241 |

- SOLUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 38 | -0.07175 | -13.864 |
| w2 | 33 | 0.204074 | 71.488 |
| w3 | 12 | 0.045714 | -0.912 |

- INJUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 33 | -0.048155 | -12.481 |
| w2 | 41 | -0.017457 | 6.54 |
| w3 | 16 | 0.049186 | 19.798 |

- NEARUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 40 | -0.045747 | -14.784 |
| w2 | 30 | 0.052393 | 28.475 |
| w3 | 17 | 0.22636 | 75.764 |

- SUIUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.01043 | -9.212 |
| w2 | 34 | 0.171724 | 39.283 |
| w3 | 15 | 0.233451 | 36.73 |

- TAOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 21 | 0.189337 | 35.525 |
| w2 | 33 | 0.032793 | 23.352 |
| w3 | 10 | 0.105982 | 5.1 |

- ONDOUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 32 | -0.123729 | -29.41 |
| w2 | 31 | 0.06712 | 36.214 |
| w3 | 14 | 0.087889 | 12.644 |

