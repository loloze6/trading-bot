# Backtest of 017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h

- Plan: `../../../../../03_test_plan/step7ab_b_run/plans/017-05_settlement-move-reverses-after.d3_midnight-settlement-daily-reversal_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC, ETH, LTC, XMR, XRP, ZEC as BTCUSD, ETHUSD, LTCUSD, XMRUSD, XRPUSD, ZECUSD; 1h bars; windows unseen_2026
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: trading-bot/backtest/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 199 | 0.021465 | -25.035 |
| w2 | 203 | 0.002368 | -10.91 |
| w3 | 128 | -0.020173 | -6.928 |

- ETHUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 202 | 0.029045 | -17.545 |
| w2 | 203 | 0.006949 | -23.347 |
| w3 | 126 | -5.4e-05 | 15.118 |

- LTCUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 214 | 0.001009 | -30.228 |
| w2 | 224 | 0.031233 | -6.587 |
| w3 | 139 | 0.000284 | -7.53 |

- XMRUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 215 | 0.012497 | -8.972 |
| w2 | 208 | -0.005626 | 3.762 |
| w3 | 145 | -0.026387 | -8.471 |

- XRPUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 199 | 0.002433 | -38.685 |
| w2 | 215 | -0.001191 | -25.201 |
| w3 | 127 | -0.015869 | -14.069 |

- ZECUSD: 3 of 3 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 197 | 0.007968 | 7.838 |
| w2 | 196 | 0.007315 | -14.104 |
| w3 | 137 | 0.008553 | 5.273 |

