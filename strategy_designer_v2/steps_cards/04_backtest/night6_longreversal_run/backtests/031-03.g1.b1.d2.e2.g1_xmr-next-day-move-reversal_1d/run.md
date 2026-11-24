# Backtest of 031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d

- Plan: `../../../../03_test_plan/night6_longreversal_run/plans/031-03.g1.b1.d2.e2.g1_xmr-next-day-move-reversal_1d.md`
- Config: `config.json` (a copy of the plan's config)
- Data: XMR as XMRUSD; 1d bars; folds A, B, C, D
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- XMRUSD: 24 of 24 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 102 | 0.053719 | -1.126 |
| w2 | 102 | 0.111408 | 12.338 |
| w3 | 103 | 0.125506 | 2.573 |
| w4 | 103 | 0.142359 | 15.512 |
| w5 | 113 | -0.037508 | -33.611 |
| w6 | 110 | 0.130001 | 2.201 |
| w7 | 103 | 0.174697 | 21.707 |
| w8 | 103 | 0.18287 | 19.892 |
| w9 | 108 | 0.044691 | -9.217 |
| w10 | 109 | 0.313414 | 73.573 |
| w11 | 99 | 0.087174 | 17.502 |
| w12 | 101 | -0.00129 | -10.023 |
| w13 | 102 | 0.137845 | 25.46 |
| w14 | 104 | 0.137382 | 10.704 |
| w15 | 102 | -0.034386 | -14.026 |
| w16 | 102 | 0.119624 | 12.083 |
| w17 | 112 | 0.19848 | 35.608 |
| w18 | 98 | 0.209201 | 52.058 |
| w19 | 99 | 0.192803 | 33.271 |
| w20 | 103 | 0.225527 | 33.029 |
| w21 | 99 | 0.054005 | -5.053 |
| w22 | 98 | 0.059319 | 2.42 |
| w23 | 104 | -0.108021 | -35.786 |
| w24 | 93 | -0.054652 | -12.444 |

