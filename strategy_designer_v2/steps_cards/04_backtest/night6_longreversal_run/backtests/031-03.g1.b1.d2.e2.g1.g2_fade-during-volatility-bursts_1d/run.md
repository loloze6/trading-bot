# Backtest of 031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1.g2_fade-during-volatility-bursts_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 100 | 0.074929 | 6.543 |
| w2 | 101 | 0.135479 | 24.997 |
| w3 | 101 | 0.108515 | 1.617 |
| w4 | 103 | 0.088704 | -1.217 |
| w5 | 109 | -0.056665 | -34.195 |
| w6 | 111 | 0.043825 | -20.641 |
| w7 | 108 | 0.182063 | 41.875 |
| w8 | 98 | 0.152663 | 13.414 |
| w9 | 102 | 0.047228 | -4.651 |
| w10 | 112 | 0.252849 | 54.527 |
| w11 | 99 | 0.149328 | 27.534 |
| w12 | 100 | 0.025007 | -5.667 |
| w13 | 101 | 0.137323 | 30.435 |
| w14 | 103 | 0.167171 | 41.926 |
| w15 | 95 | -0.022946 | -19.137 |
| w16 | 101 | 0.146468 | 22.505 |
| w17 | 111 | 0.189966 | 35.388 |
| w18 | 102 | 0.136895 | 32.027 |
| w19 | 92 | 0.156005 | 36.109 |
| w20 | 95 | 0.220647 | 35.031 |
| w21 | 93 | 0.046717 | -17.895 |
| w22 | 91 | 0.041849 | -5.538 |
| w23 | 102 | -0.103068 | -43.804 |
| w24 | 94 | -0.032966 | -18.006 |

