# Backtest of 003-04_high-volume-down-move-continues_1h

- Plan: `../../../03_test_plan/plans/003-04_high-volume-down-move-continues_1h.md`
- Config: `config.json` (a copy of the plan's config)
- Data: BTC/USDT as BTCUSD; 1h bars; fold A
- Venue: Kraken spot prices as a proxy for Kraken futures; funding not modelled
- Engine: strategy-research/tools/run_protocol.py around trading-bot's run_backtest, unchanged; warm-up loaded before each window

- BTCUSD: 6 of 6 windows run.

| window | trades | forecast vs next return (all bars) | net return % |
|---|---|---|---|
| w1 | 471 | -0.003204 | -53.33 |
| w2 | 469 | 0.004449 | -45.034 |
| w3 | 466 | -0.008386 | -55.409 |
| w4 | 431 | -0.01132 | -60.319 |
| w5 | 442 | -0.023656 | -58.523 |
| w6 | 450 | -0.023792 | -62.238 |

